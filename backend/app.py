import os
import sys
import time
import argparse
import threading
import traceback
import datetime
from queue import Queue, Full
from flask import Flask, request, jsonify

import cv2
from gesture import GestureRecognizer
from capture_modes import CaptureManager, CaptureMode
from filters import FilterType, get_filter_from_string
from supabase_manager import SupabaseManager
from printer import PrinterWorker

# Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--event-mode", action="store_true", help="Enable event mode (auto-restart, less logging)")
args = parser.parse_args()
EVENT_MODE = args.event_mode

# Global State
shutdown_event = threading.Event()
state_lock = threading.Lock()
current_mode = CaptureMode.SINGLE
current_filter = FilterType.STRANGER_THEME

ALLOWED_FILTERS = [f.name for f in FilterType]
ALLOWED_MODES = [m.value.upper() for m in CaptureMode]

# Queues
upload_queue = Queue()
print_queue = Queue()
capture_queue = Queue(maxsize=5)

# Flask App
app = Flask(__name__)

# Load Env
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", ".env"))
SUPABASE_URL = os.environ.get("VITE_SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("VITE_SUPABASE_ANON_KEY", "")

# Initialize Workers
supabase_worker = SupabaseManager(SUPABASE_URL, SUPABASE_KEY, upload_queue, shutdown_event)
printer_worker = PrinterWorker(print_queue, shutdown_event)

# API Endpoints
@app.route("/health", methods=["GET"])
def health():
    with state_lock:
        return jsonify({
            "status": "ok",
            "mode": current_mode.value,
            "filter": current_filter.name,
            "event_mode": EVENT_MODE
        })

@app.route("/set_filter", methods=["POST"])
def set_filter():
    global current_filter
    data = request.json or {}
    filter_name = data.get("filter", "").upper()
    if filter_name in ALLOWED_FILTERS:
        if EVENT_MODE:
            return jsonify({"error": "Event Mode locked settings"}), 403
        with state_lock:
            current_filter = get_filter_from_string(filter_name)
        return jsonify({"success": True, "filter": current_filter.name}), 200
    return jsonify({"error": "Invalid filter"}), 400

@app.route("/set_mode", methods=["POST"])
def set_mode():
    global current_mode
    data = request.json or {}
    mode_name = data.get("mode", "").upper()
    if mode_name in ALLOWED_MODES:
        if EVENT_MODE:
            return jsonify({"error": "Event Mode locked settings"}), 403
        with state_lock:
            current_mode = CaptureMode(mode_name.lower())
        return jsonify({"success": True, "mode": current_mode.value}), 200
    return jsonify({"error": "Invalid mode"}), 400

@app.route("/print", methods=["POST"])
def print_image():
    data = request.json or {}
    image_url = data.get("imageUrl")
    if not image_url:
        return jsonify({"error": "Missing imageUrl"}), 400

    def fetch_and_print():
        try:
            import urllib.request
            temp_dir = os.path.join("storage", "temp")
            os.makedirs(temp_dir, exist_ok=True)
            filename = image_url.split("/")[-1].split("?")[0]
            local_path = os.path.join(temp_dir, filename)
            urllib.request.urlretrieve(image_url, local_path)
            print_queue.put({"file_path": local_path})
        except Exception as e:
            if not EVENT_MODE: print(f"Fetch failed: {e}")

    threading.Thread(target=fetch_and_print, daemon=True).start()
    return jsonify({"success": True}), 200

# Camera Loop
def _save_and_dispatch(res):
    date_str = datetime.datetime.now().strftime("%Y_%m_%d")
    backup_dir = os.path.join("storage", "local_backup", date_str)
    os.makedirs(backup_dir, exist_ok=True)
    
    file_path = None
    if res.mode == CaptureMode.SINGLE:
        filename = f"magic_{res.base_timestamp}.jpg"
        file_path = os.path.join(backup_dir, filename)
        cv2.imwrite(file_path, res.images[0])
    elif res.mode == CaptureMode.BURST:
        filename = f"magic_burst_{res.base_timestamp}.jpg"
        file_path = os.path.join(backup_dir, filename)
        if res.collage_image is not None:
            cv2.imwrite(file_path, res.collage_image)
        else: return
    elif res.mode == CaptureMode.GIF:
        filename = f"magic_anim_{res.base_timestamp}.gif"
        file_path = os.path.join(backup_dir, filename)
        if res.gif_bytes is not None:
            with open(file_path, "wb") as f:
                f.write(res.gif_bytes)
        else: return
            
    if file_path:
        upload_queue.put({"file_path": file_path})
        print_queue.put({"file_path": file_path})

def run_camera():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened(): cap = cv2.VideoCapture(0)
    
    cv2.namedWindow("MAGIC Photo Booth", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("MAGIC Photo Booth", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    recognizer = GestureRecognizer()
    capture_manager = CaptureManager()
    
    last_capture_time = 0
    COOLDOWN = 6.0
    
    while not shutdown_event.is_set():
        ret, frame = cap.read()
        if not ret: continue
        
        display_frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        
        results, gesture = recognizer.process_frame(rgb_frame)
        
        with state_lock:
            act_filter = current_filter
            act_mode = current_mode
            
        cv2.putText(display_frame, f"MODE: {act_mode.value.upper()} | FILTER: {act_filter.name}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(display_frame, "THUMBS UP TO CAPTURE", (20, display_frame.shape[0] - 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        
        cv2.imshow("MAGIC Photo Booth", display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'): # ESC
            shutdown_event.set()
            break
            
        if gesture == "THUMBS_UP" and (time.time() - last_capture_time) > COOLDOWN:
            try:
                capture_queue.put_nowait(True) # Memory bound check
            except Full:
                if not EVENT_MODE: print("Capture queue full. Ignored.")
                continue
                
            last_capture_time = time.time()
            
            # Execute capture sequence
            if act_mode == CaptureMode.BURST:
                res = capture_manager.capture_burst(cap, act_filter)
            elif act_mode == CaptureMode.GIF:
                res = capture_manager.capture_gif(cap, act_filter)
            else:
                ret, snap = cap.read()
                if ret:
                    snap = cv2.flip(snap, 1)
                    res = capture_manager.capture_single(snap, act_filter)
                    
            if 'res' in locals() and res:
                _save_and_dispatch(res)
            
            # Clear token
            try: capture_queue.get_nowait(); capture_queue.task_done()
            except: pass
            
    cap.release()
    cv2.destroyAllWindows()

def camera_watchdog():
    while not shutdown_event.is_set():
        try:
            run_camera()
        except Exception as e:
            if not EVENT_MODE: print(f"Camera crashed: {e}"); traceback.print_exc()
            time.sleep(2)
            if not EVENT_MODE: print("Restarting camera...")
            continue
        break # Exit normally if broke out correctly

if __name__ == "__main__":
    try:
        if SUPABASE_URL and SUPABASE_KEY:
            supabase_worker.start_worker()
        else:
            print("Warning: Missing Supabase credentials. Cloud sync disabled.")
            
        printer_worker.start_worker()
        
        cam_thread = threading.Thread(target=camera_watchdog, daemon=True)
        cam_thread.start()
        
        app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        shutdown_event.set()
        # Non-blocking wait / timeout could be added, but simple join is ok for workers
        # upload_queue.join()
        # print_queue.join()
