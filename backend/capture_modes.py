import cv2
import numpy as np
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from filters import FilterType, apply_filter

class CaptureMode(Enum):
    SINGLE = "single"
    BURST = "burst"
    GIF = "gif"

@dataclass
class CaptureResult:
    mode: CaptureMode
    images: List[np.ndarray]
    timestamps: List[float]
    base_timestamp: int
    gif_bytes: Optional[bytes] = None
    collage_image: Optional[np.ndarray] = None

class CaptureManager:
    BURST_COUNT = 4
    BURST_INTERVAL_MS = 500
    GIF_FRAME_COUNT = 8
    GIF_INTERVAL_MS = 200

    def capture_single(self, frame: np.ndarray, filter_type: FilterType) -> CaptureResult:
        timestamp = time.time()
        filtered = apply_filter(frame, filter_type, text="MAGIC 2026")
        return CaptureResult(
            mode=CaptureMode.SINGLE,
            images=[filtered],
            timestamps=[timestamp],
            base_timestamp=int(timestamp)
        )

    def capture_burst(self, cap: cv2.VideoCapture, filter_type: FilterType) -> CaptureResult:
        images = []
        timestamps = []
        base_timestamp = int(time.time())
        
        for i in range(self.BURST_COUNT):
            if i > 0:
                self._countdown(cap, seconds=3)
            
            # Flush a couple frames to ensure we don't get a frozen frame from the countdown
            for _ in range(3):
                cap.read()
            
            ret, frame = cap.read()
            if not ret: continue
            
            frame = cv2.flip(frame, 1)
            timestamp = time.time()
            filtered = apply_filter(frame, filter_type, text="MAGIC 2026")
            images.append(filtered)
            timestamps.append(timestamp)
            
            # Flash effect
            self._flash(cap)
            
        collage = self._create_collage(images) if len(images) == self.BURST_COUNT else (images[0] if images else None)
        return CaptureResult(
            mode=CaptureMode.BURST,
            images=images,
            timestamps=timestamps,
            base_timestamp=base_timestamp,
            collage_image=collage
        )

    def capture_gif(self, cap: cv2.VideoCapture, filter_type: FilterType, duration_per_frame: float = 0.2) -> CaptureResult:
        images = []
        timestamps = []
        base_timestamp = int(time.time())
        rgb_images = []
        
        for i in range(self.GIF_FRAME_COUNT):
            ret, frame = cap.read()
            if not ret: continue
            
            frame = cv2.flip(frame, 1)
            timestamp = time.time()
            
            filtered = apply_filter(frame, filter_type, text="MAGIC 2026")
            images.append(filtered)
            timestamps.append(timestamp)
            
            rgb_frame = cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB)
            rgb_images.append(rgb_frame)
            
            # Preview delay while capturing
            if i < self.GIF_FRAME_COUNT - 1:
                wait_start = time.time()
                while (time.time() - wait_start) < (self.GIF_INTERVAL_MS / 1000.0):
                    cap.read()  # keep reading to clear buffer
        
        # Create GIF in memory
        import io
        import imageio
        gif_bytes = None
        if rgb_images:
            with io.BytesIO() as buf:
                imageio.mimsave(buf, rgb_images, format='GIF', duration=duration_per_frame, loop=0)
                gif_bytes = buf.getvalue()
                
        return CaptureResult(
            mode=CaptureMode.GIF,
            images=images,
            timestamps=timestamps,
            base_timestamp=base_timestamp,
            gif_bytes=gif_bytes
        )

    def _create_collage(self, images: List[np.ndarray]) -> np.ndarray:
        if len(images) != 4:
             return images[0] if images else None
             
        target_h = min(img.shape[0] for img in images)
        target_w = min(img.shape[1] for img in images)
        resized = [cv2.resize(img, (target_w, target_h)) for img in images]
        top_row = np.hstack([resized[0], resized[1]])
        bottom_row = np.hstack([resized[2], resized[3]])
        return np.vstack([top_row, bottom_row])

    def _countdown(self, cap: cv2.VideoCapture, seconds: int):
        for i in range(seconds, 0, -1):
            start = time.time()
            while time.time() - start < 1.0:
                ret, frame = cap.read()
                if ret:
                    frame = cv2.flip(frame, 1)
                    display = frame.copy()
                    text = str(i)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 6
                    thickness = 15
                    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
                    text_x = (display.shape[1] - text_size[0]) // 2
                    text_y = (display.shape[0] + text_size[1]) // 2
                    
                    # Red shadow
                    cv2.putText(display, text, (text_x+5, text_y+5), font, font_scale, (0, 0, 150), thickness)
                    # White text
                    cv2.putText(display, text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)
                    
                    cv2.imshow("MAGIC Photo Booth", display)
                    cv2.waitKey(1)
                    
    def _flash(self, cap: cv2.VideoCapture):
        ret, frame = cap.read()
        if ret:
            flash = np.ones_like(frame) * 255
            cv2.imshow("MAGIC Photo Booth", flash)
            cv2.waitKey(50)
