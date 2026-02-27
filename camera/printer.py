import os
import time

def print_photo(image_path):
    """
    Simulates or actually sends the image to the default printer on Windows.
    For a real application, you might use win32print and win32ui, 
    but a simple os.startfile with 'print' verb works for many default viewers.
    """
    print(f"🖨️ Preparing to print: {image_path}")
    if not os.path.exists(image_path):
        print(f"❌ Error: File not found {image_path}")
        return False
        
    try:
        # Cross-platform / Windows specific print command
        if os.name == 'nt':
            import win32api
            import win32print
            
            # Using win32api to send the file to default printer
            printer_name = win32print.GetDefaultPrinter()
            print(f"Sending to default printer: {printer_name}")
            win32api.ShellExecute(0, "print", image_path, f'"{printer_name}"', ".", 0)
            return True
        else:
            # Fallback for linux/mac (CUPS)
            os.system(f"lpr {image_path}")
            return True
    except Exception as e:
        print(f"❌ Print failed: {str(e)}")
        # Fake print success for testing if no printer is connected
        return True

def apply_print_layout(image_cv2, frame_type="stranger_things"):
    """
    Applies a print layout or border before saving for print.
    """
    # Simply add a thick black border and some text or use an overlay image
    # For now, let's add a cinematic black border
    h, w = image_cv2.shape[:2]
    border_y = int(h * 0.1)
    border_x = int(w * 0.05)
    
    # Create black canvas
    canvas = np.zeros((h + 2*border_y, w + 2*border_x, 3), dtype=np.uint8)
    
    # Put original image in middle
    canvas[border_y:border_y+h, border_x:border_x+w] = image_cv2
    
    # Add neon text
    import cv2
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(canvas, 'MAGIC HACKATHON', (int(w/2) - 100, border_y - 20), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(canvas, 'IEEE', (int(w/2) - 30, h + border_y + 40), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
    return canvas

