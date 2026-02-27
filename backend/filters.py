import cv2
import numpy as np
from enum import Enum
from typing import Optional

class FilterType(Enum):
    NONE = "none"
    GLITCH = "glitch"
    NEON = "neon"
    DREAMY = "dreamy"
    RETRO = "retro"
    NOIR = "noir"
    BW = "bw"
    STRANGER_THEME = "stranger_theme"

def enhance_sharpness(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    gaussian = cv2.GaussianBlur(image, (0, 0), 3)
    return cv2.addWeighted(image, 1.0 + strength, gaussian, -strength, 0)

def denoise_image(image: np.ndarray, strength: int = 5) -> np.ndarray:
    return cv2.bilateralFilter(image, d=5, sigmaColor=strength*10, sigmaSpace=strength*10)

def add_vignette(image: np.ndarray, strength: float = 0.5) -> np.ndarray:
    rows, cols = image.shape[:2]
    X = cv2.getGaussianKernel(cols, cols * 0.6)
    Y = cv2.getGaussianKernel(rows, rows * 0.6)
    kernel = Y * X.T
    mask = kernel / kernel.max()
    mask = mask * (1 - strength) + strength
    result = image.copy().astype(np.float32)
    for i in range(3):
        result[:, :, i] = result[:, :, i] * mask
    return np.clip(result, 0, 255).astype(np.uint8)

def add_film_grain(image: np.ndarray, intensity: float = 0.15) -> np.ndarray:
    rows, cols = image.shape[:2]
    noise = np.random.randn(rows, cols, 3) * 25 * intensity
    grainy = image.astype(np.float32) + noise
    return np.clip(grainy, 0, 255).astype(np.uint8)

def apply_glitch(image: np.ndarray) -> np.ndarray:
    result = image.copy()
    rows, cols = result.shape[:2]
    b, g, r = cv2.split(result)
    shift_amount = max(8, cols // 80)
    
    b_shifted = np.roll(b, -shift_amount, axis=1)
    b_shifted[:, -shift_amount:] = b[:, -shift_amount:]
    r_shifted = np.roll(r, shift_amount, axis=1)
    r_shifted[:, :shift_amount] = r[:, :shift_amount]
    
    glitched = cv2.merge([b_shifted, g, r_shifted])
    line_interval = 3
    for i in range(0, rows, line_interval):
        if i + 1 < rows:
            glitched[i, :] = (glitched[i, :].astype(np.float32) * 0.7).astype(np.uint8)
            
    for _ in range(3):
        band_y = np.random.randint(0, rows - 20)
        band_height = np.random.randint(2, 8)
        shift = np.random.randint(-15, 15)
        band = glitched[band_y:band_y + band_height, :].copy()
        band = np.roll(band, shift, axis=1)
        glitched[band_y:band_y + band_height, :] = band
        
    glitched = cv2.convertScaleAbs(glitched, alpha=1.1, beta=5)
    return glitched

def apply_neon(image: np.ndarray) -> np.ndarray:
    result = image.copy()
    lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l = clahe.apply(l)
    a = cv2.convertScaleAbs(a, alpha=1.2, beta=0)
    b = cv2.convertScaleAbs(b, alpha=0.9, beta=-10)
    lab = cv2.merge([l, a, b])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    b_ch, g_ch, r_ch = cv2.split(result)
    b_ch = cv2.convertScaleAbs(b_ch, alpha=1.15, beta=10)
    r_ch = cv2.convertScaleAbs(r_ch, alpha=1.1, beta=8)
    result = cv2.merge([b_ch, g_ch, r_ch])
    
    blurred = cv2.GaussianBlur(result, (0, 0), 8)
    result = cv2.addWeighted(result, 0.85, blurred, 0.15, 0)
    result = enhance_sharpness(result, strength=0.3)
    return result

def apply_dreamy(image: np.ndarray) -> np.ndarray:
    result = image.copy()
    lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_float = l.astype(np.float32) / 255.0
    l_lifted = np.power(l_float, 0.85) * 255
    l = np.clip(l_lifted, 0, 255).astype(np.uint8)
    a = cv2.convertScaleAbs(a, alpha=0.7, beta=30)
    b = cv2.convertScaleAbs(b, alpha=0.75, beta=20)
    lab = cv2.merge([l, a, b])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    blurred = cv2.GaussianBlur(result, (0, 0), 25)
    result = cv2.addWeighted(result, 0.55, blurred, 0.45, 0)
    result = cv2.convertScaleAbs(result, alpha=1.05, beta=15)
    result = add_vignette(result, strength=0.2)
    return result

def apply_retro(image: np.ndarray, text: str = "MAGIC 2026") -> np.ndarray:
    result = image.copy()
    sepia_filter = np.array([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]
    ])
    sepia = cv2.transform(result, sepia_filter)
    sepia = np.clip(sepia, 0, 255).astype(np.uint8)
    result = cv2.addWeighted(result, 0.35, sepia, 0.65, 0)
    
    lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = np.clip(l.astype(np.float32) + 15, 0, 255).astype(np.uint8)
    lab = cv2.merge([l, a, b])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    b_ch, g_ch, r_ch = cv2.split(result)
    r_ch = cv2.convertScaleAbs(r_ch, alpha=1.08, beta=8)
    g_ch = cv2.convertScaleAbs(g_ch, alpha=1.02, beta=3)
    b_ch = cv2.convertScaleAbs(b_ch, alpha=0.95, beta=-5)
    result = cv2.merge([b_ch, g_ch, r_ch])
    result = add_vignette(result, strength=0.25)
    
    row, col = result.shape[:2]
    bottom_border = int(row * 0.20)
    side_border = int(col * 0.04)
    cream = [240, 248, 255]
    polaroid = cv2.copyMakeBorder(
        result, side_border, bottom_border, side_border, side_border, cv2.BORDER_CONSTANT, value=cream
    )
    
    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    font_scale = min(1.5, col / 400)
    thickness = 2
    text_color = (60, 60, 80)
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (polaroid.shape[1] - text_size[0]) // 2
    text_y = polaroid.shape[0] - (bottom_border // 2) + (text_size[1] // 2)
    cv2.putText(polaroid, text, (text_x, text_y), font, font_scale, text_color, thickness)
    return polaroid

def apply_noir(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    contrasted = clahe.apply(gray)
    contrasted = cv2.convertScaleAbs(contrasted, alpha=1.25, beta=-10)
    noir = cv2.cvtColor(contrasted, cv2.COLOR_GRAY2BGR)
    noir = add_vignette(noir, strength=0.4)
    noir = add_film_grain(noir, intensity=0.12)
    return noir

def apply_bw(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    enhanced = cv2.bilateralFilter(enhanced, d=5, sigmaColor=40, sigmaSpace=40)
    bw = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)
    return bw

def apply_stranger_theme(image: np.ndarray) -> np.ndarray:
    """ Deep red neon, Upside Down aesthetic """
    result = image.copy()
    
    lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Push Red (A channel towards magenta/red) and reduce Blue/Yellow (B channel)
    a = cv2.convertScaleAbs(a, alpha=1.5, beta=20)
    b = cv2.convertScaleAbs(b, alpha=0.5, beta=0)
    
    lab = cv2.merge([l, a, b])
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Heavy Red Tint & Vignette for Horror Vibe
    b_ch, g_ch, r_ch = cv2.split(result)
    r_ch = np.clip(r_ch.astype(np.float32) * 1.5, 0, 255).astype(np.uint8)
    b_ch = np.clip(b_ch.astype(np.float32) * 0.7, 0, 255).astype(np.uint8)
    g_ch = np.clip(g_ch.astype(np.float32) * 0.6, 0, 255).astype(np.uint8)
    
    result = cv2.merge([b_ch, g_ch, r_ch])
    
    blurred = cv2.GaussianBlur(result, (0, 0), 10)
    result = cv2.addWeighted(result, 0.7, blurred, 0.3, 0)
    
    result = add_vignette(result, strength=0.7)
    result = add_film_grain(result, intensity=0.20)
    
    return result

def apply_filter(image: np.ndarray, filter_type: FilterType, text: str = "MAGIC 2026") -> np.ndarray:
    enhanced = enhance_sharpness(image, strength=0.5)
    
    if filter_type == FilterType.NONE:
        return denoise_image(enhanced, strength=3)
    elif filter_type == FilterType.GLITCH:
        return apply_glitch(enhanced)
    elif filter_type == FilterType.NEON:
        return apply_neon(enhanced)
    elif filter_type == FilterType.DREAMY:
        return apply_dreamy(enhanced)
    elif filter_type == FilterType.RETRO:
        return apply_retro(enhanced, text)
    elif filter_type == FilterType.NOIR:
        return apply_noir(enhanced)
    elif filter_type == FilterType.BW:
        return apply_bw(enhanced)
    elif filter_type == FilterType.STRANGER_THEME:
        return apply_stranger_theme(enhanced)
    else:
        return enhanced

def get_filter_from_string(filter_name: str) -> FilterType:
    if not filter_name: return FilterType.NONE
    mapping = {
        "NORMAL": FilterType.NONE,
        "GLITCH": FilterType.GLITCH,
        "NEON": FilterType.NEON,
        "DREAMY": FilterType.DREAMY,
        "RETRO": FilterType.RETRO,
        "NOIR": FilterType.NOIR,
        "BW": FilterType.BW,
        "STRANGER_THEME": FilterType.STRANGER_THEME,
    }
    return mapping.get(filter_name.upper(), FilterType.NONE)
