import os
import threading
from queue import Queue, Empty
import traceback

try:
    import win32print
    import win32ui
    from PIL import Image, ImageWin
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

class PrinterWorker:
    def __init__(self, print_queue: Queue, shutdown_event: threading.Event):
        self.print_queue = print_queue
        self.shutdown_event = shutdown_event
        
    def start_worker(self):
        worker = threading.Thread(target=self._worker_loop, daemon=True)
        worker.start()
        return worker
        
    def _worker_loop(self):
        while not self.shutdown_event.is_set():
            try:
                job = self.print_queue.get(timeout=1.0)
                file_path = job.get("file_path")
                
                if file_path and os.path.exists(file_path):
                    self._print_image(file_path)
                
                self.print_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                print(f"[Printer] Worker error: {e}")
                
    def _print_image(self, file_path: str):
        if not WIN32_AVAILABLE:
            print(f"[Printer] Simulated printing (win32print/PIL.ImageWin unavailable): {file_path}")
            return
            
        try:
            print(f"[Printer] Starting print job for {file_path}")
            printer_name = win32print.GetDefaultPrinter()
            img = Image.open(file_path)
            
            hDC = win32ui.CreateDC()
            hDC.CreatePrinterDC(printer_name)
            
            printable_area = hDC.GetDeviceCaps(8), hDC.GetDeviceCaps(10) # HORZRES, VERTRES
            
            hDC.StartDoc("MAGIC Photo Booth")
            hDC.StartPage()
            
            dib = ImageWin.Dib(img)
            
            ratio = min(printable_area[0] / img.width, printable_area[1] / img.height)
            scaled_width = int(img.width * ratio)
            scaled_height = int(img.height * ratio)
            
            x1 = int((printable_area[0] - scaled_width) / 2)
            y1 = int((printable_area[1] - scaled_height) / 2)
            x2 = x1 + scaled_width
            y2 = y1 + scaled_height
            
            dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))
            
            hDC.EndPage()
            hDC.EndDoc()
            hDC.DeleteDC()
            
            print(f"[Printer] Successfully sent to {printer_name}")
            
        except Exception as e:
            print(f"[Printer] Print failed: {e}")
