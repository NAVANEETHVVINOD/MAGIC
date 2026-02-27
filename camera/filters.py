import cv2
import numpy as np
import random

def apply_filter(frame, filter_name):
    if filter_name == "NONE":
        # Basic enhancement
        alpha = 1.1 # Contrast control
        beta = 10   # Brightness control
        return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
        
    elif filter_name == "NOIR":
        # Dark dramatic B&W
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Increase contrast heavily
        gray = cv2.convertScaleAbs(gray, alpha=1.3, beta=-30)
        # Convert back to BGR so it matches other filters' shape
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
    elif filter_name == "NEON":
        # Stranger Things glow (Red/blue tint)
        # Map colors towards red/blue
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Shift hue slightly towards red/magenta for red glow
        # OpenCV hue is 0-179. Red is around 0 or 170-179.
        s = cv2.add(s, 20) # increase saturation
        v = cv2.add(v, 10) # increase value
        
        enhanced_hsv = cv2.merge([h, s, v])
        bgr = cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2BGR)
        
        # Add a red-tint overlay
        overlay = np.full(frame.shape, (20, 10, 60), dtype=np.uint8) # BGR: slight red tint + blue
        result = cv2.addWeighted(bgr, 0.8, overlay, 0.2, 0)
        return result
        
    elif filter_name == "GLITCH":
        # Upside Down distortion
        # Shift channels and add noise
        h, w, c = frame.shape
        glitch_frame = frame.copy()
        
        # Random channel shift
        shift = random.randint(-15, 15)
        if shift > 0:
            glitch_frame[:, shift:, 0] = frame[:, :-shift, 0] # Shift Blue
            glitch_frame[:, :-shift, 2] = frame[:, shift:, 2] # Shift Red
        else:
            shift = abs(shift)
            glitch_frame[:, :-shift, 0] = frame[:, shift:, 0]
            glitch_frame[:, shift:, 2] = frame[:, :-shift, 2]
            
        # Add scanlines
        for i in range(0, h, 4):
            glitch_frame[i:i+1, :] = cv2.add(glitch_frame[i:i+1, :], np.array([-20, -20, -20], dtype=np.int16).clip(0,255))
            
        return glitch_frame
        
    elif filter_name == "RETRO":
        # 80s film look (Warm, faded, slightly grainy)
        # Decrease contrast, add warmth
        faded = cv2.convertScaleAbs(frame, alpha=0.9, beta=20)
        
        # Warm tint (more red/green, less blue)
        b, g, r = cv2.split(faded)
        b = cv2.subtract(b, 20)
        r = cv2.add(r, 20)
        g = cv2.add(g, 10)
        warm = cv2.merge([b, g, r])
        
        # Add grain
        noise = np.random.randint(-15, 15, warm.shape, dtype='int16')
        retro = np.clip(warm.astype('int16') + noise, 0, 255).astype('uint8')
        
        return retro
        
    elif filter_name == "DREAMY":
        # Soft eerie glow
        # Gaussian blur + blend with original for bloom effect
        blur = cv2.GaussianBlur(frame, (15, 15), 0)
        # Lighten the image slightly
        bright = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)
        # Screen blend or add weighted
        dreamy = cv2.addWeighted(bright, 0.6, blur, 0.5, 0)
        
        return dreamy
        
    return frame

