import cv2
import os
import time
from datetime import datetime
from PIL import Image

def init_storage(base_path="E:\\magic_booth\\photos"):
    if not os.path.exists(base_path):
        try:
            os.makedirs(base_path)
            print(f"📁 Created photo directory at {base_path}")
        except Exception as e:
            fallback = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'photos'))
            os.makedirs(fallback, exist_ok=True)
            print(f"⚠️ Could not create {base_path}. Using fallback: {fallback}")
            return fallback
    return base_path

def save_single_photo(frame, filter_name, storage_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"magic_{timestamp}_{filter_name}.jpg"
    filepath = os.path.join(storage_path, filename)
    
    cv2.imwrite(filepath, frame)
    print(f"📸 Saved photo: {filepath}")
    return filepath, filename

def create_gif(frames, filter_name, storage_path):
    if not frames:
        return None, None
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"magic_burst_{timestamp}_{filter_name}.gif"
    filepath = os.path.join(storage_path, filename)
    
    # Convert OpenCV BGR frames to PIL RGB Images
    pil_frames = [Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)) for f in frames]
    
    # Save as GIF
    pil_frames[0].save(
        filepath,
        save_all=True,
        append_images=pil_frames[1:],
        duration=200, # 200ms per frame
        loop=0
    )
    print(f"🎞️ Saved GIF: {filepath}")
    return filepath, filename
