from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from flask_cors import CORS
import cv2
import threading
import time
import os

from filters import apply_filter
from capture_modes import init_storage, save_single_photo, create_gif
from printer import print_photo

app = Flask(__name__, static_folder='../website', static_url_path='')
CORS(app)

# Global variables
camera = None
current_filter = "NONE"
current_mode = "SINGLE" # SINGLE, BURST
is_capturing = False
storage_path = "E:\\magic_booth\\photos"

def init_camera():
    global camera, storage_path
    storage_path = init_storage("E:\\magic_booth\\photos")
    # Try multiple camera indices if 0 fails
    for i in range(2):
        camera = cv2.VideoCapture(i)
        if camera.isOpened():
            # Set to 720p
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            print(f"📸 Camera {i} initialized successfully.")
            return True
    print("❌ Camera initialization failed.")
    return False

def generate_frames():
    global camera, current_filter, is_capturing
    
    while True:
        if not camera or not camera.isOpened():
            time.sleep(1)
            continue
            
        success, frame = camera.read()
        if not success:
            continue
            
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Apply current filter
        processed_frame = apply_filter(frame, current_filter)
        
        # Encode as JPEG
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        # Yield the frame for mjpeg stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return app.send_static_file('index.html')
    
@app.route('/assets/<path:path>')
def send_assets(path):
    # Depending on where assets are relative to MAGIC, e.g. MAGIC/public for s3.gif
    return send_from_directory('../public', path)

@app.route('/photos/<path:path>')
def send_photos(path):
    return send_from_directory(storage_path, path)

@app.route('/api/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/set_filter', methods=['POST'])
def set_filter():
    global current_filter
    data = request.json
    current_filter = data.get('filter', 'NONE')
    print(f"🎨 Filter changed to: {current_filter}")
    return jsonify({"status": "success", "filter": current_filter})
    
@app.route('/api/set_mode', methods=['POST'])
def set_mode():
    global current_mode
    data = request.json
    current_mode = data.get('mode', 'SINGLE')
    print(f"⚙️ Mode changed to: {current_mode}")
    return jsonify({"status": "success", "mode": current_mode})

@app.route('/api/capture', methods=['POST'])
def capture():
    global camera, current_filter, current_mode, storage_path, is_capturing
    
    if is_capturing or not camera or not camera.isOpened():
        return jsonify({"status": "error", "message": "Camera busy or not ready."}), 400
        
    is_capturing = True
    images = []
    
    try:
        if current_mode == "SINGLE":
            # Clear buffer
            for _ in range(5):
                camera.read()
                
            success, frame = camera.read()
            if success:
                frame = cv2.flip(frame, 1)
                processed = apply_filter(frame, current_filter)
                filepath, filename = save_single_photo(processed, current_filter, storage_path)
                images.append(filename)
                
        elif current_mode == "BURST":
            # Take 3 photos
            frames_to_save = []
            for _ in range(3):
                success, frame = camera.read()
                if success:
                    frame = cv2.flip(frame, 1)
                    processed = apply_filter(frame, current_filter)
                    frames_to_save.append(processed)
                time.sleep(0.5) # Time between bursts
                
            for idx, processed in enumerate(frames_to_save):
                filepath, filename = save_single_photo(processed, f"{current_filter}_burst{idx}", storage_path)
                images.append(filename)
                
        elif current_mode == "GIF":
            # Take 10 frames fast
            frames_to_save = []
            for _ in range(10):
                success, frame = camera.read()
                if success:
                    frame = cv2.flip(frame, 1)
                    processed = apply_filter(frame, current_filter)
                    frames_to_save.append(processed)
                time.sleep(0.1)
                
            filepath, filename = create_gif(frames_to_save, current_filter, storage_path)
            if filename:
                images.append(filename)
            
    finally:
        is_capturing = False
        
    # Return latest captured photo paths
    return jsonify({
        "status": "success", 
        "images": images, 
        "folder": storage_path
    })

@app.route('/api/print', methods=['POST'])
def print_file():
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({"status": "error", "message": "No file specified"}), 400
        
    filepath = os.path.join(storage_path, filename)
    success = print_photo(filepath)
    
    if success:
        return jsonify({"status": "success", "message": "Sent to printer"})
    else:
        return jsonify({"status": "error", "message": "Failed to print"}), 500

if __name__ == '__main__':
    # Initialize camera before starting server
    threading.Thread(target=init_camera).start()
    
    print("🚀 Starting Magic Booth API Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)

