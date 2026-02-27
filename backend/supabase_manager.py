import os
import shutil
import threading
import traceback
from queue import Queue, Empty
from supabase import create_client, Client

class SupabaseManager:
    def __init__(self, url: str, key: str, upload_queue: Queue, shutdown_event: threading.Event, retry_dir: str = "storage/retry_queue"):
        self.supabase: Client = create_client(url, key)
        self.upload_queue = upload_queue
        self.shutdown_event = shutdown_event
        self.retry_dir = retry_dir
        self.bucket = "magic-photos"
        self.table = "photos"
        self.max_images = 600
        
        os.makedirs(self.retry_dir, exist_ok=True)
        
    def start_worker(self):
        worker = threading.Thread(target=self._worker_loop, daemon=True)
        worker.start()
        return worker
        
    def _worker_loop(self):
        # First try to upload any offline queued files
        self._process_retry_queue()
        
        while not self.shutdown_event.is_set():
            try:
                # Wait for items with timeout to allow checking shutdown_event
                job = self.upload_queue.get(timeout=1.0)
                file_path = job.get("file_path")
                
                if file_path and os.path.exists(file_path):
                    success = self._upload_file(file_path)
                    if not success:
                        self._move_to_retry(file_path)
                
                self.upload_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                print(f"[Supabase] Worker error: {e}")
                    
    def _upload_file(self, file_path: str) -> bool:
        try:
            filename = os.path.basename(file_path)
            
            # Upload to bucket
            with open(file_path, "rb") as f:
                res = self.supabase.storage.from_(self.bucket).upload(
                    path=filename,
                    file=f,
                    file_options={"content-type": "image/jpeg", "upsert": "true"}
                )
            
            # Get public URL
            public_url = self.supabase.storage.from_(self.bucket).get_public_url(filename)
            
            # Insert to DB
            self.supabase.table(self.table).insert({
                "filename": filename,
                "url": public_url
            }).execute()
            
            # Enforce limit
            self._enforce_limit()
            return True
            
        except Exception as e:
            print(f"[Supabase] Upload failed: {e}")
            return False
            
    def _process_retry_queue(self):
        try:
            for filename in os.listdir(self.retry_dir):
                file_path = os.path.join(self.retry_dir, filename)
                if os.path.isfile(file_path):
                    print(f"[Supabase] Retrying offline file: {filename}")
                    if self._upload_file(file_path):
                        os.remove(file_path) # cleanup after success
        except Exception as e:
            print(f"[Supabase] Retry queue error: {e}")
            
    def _move_to_retry(self, file_path):
        try:
            filename = os.path.basename(file_path)
            dest = os.path.join(self.retry_dir, filename)
            shutil.copy2(file_path, dest)
            print(f"[Supabase] Moved {filename} to offline retry queue.")
        except Exception as e:
            print(f"[Supabase] Failed to move offline: {e}")
            
    def _enforce_limit(self):
        try:
            # Check count
            count_res = self.supabase.table(self.table).select('id', count='exact').execute()
            total_count = count_res.count
            
            if total_count and total_count > self.max_images:
                excess = total_count - self.max_images
                
                # Get oldest
                oldest_res = self.supabase.table(self.table).select('id, filename').order('created_at', desc=False).limit(excess).execute()
                
                if oldest_res.data:
                    ids_to_delete = [item['id'] for item in oldest_res.data]
                    filenames_to_delete = [item['filename'] for item in oldest_res.data]
                    
                    # Delete from bucket
                    self.supabase.storage.from_(self.bucket).remove(filenames_to_delete)
                    
                    # Delete from DB
                    for row_id in ids_to_delete:
                        self.supabase.table(self.table).delete().eq('id', row_id).execute()
                        
                    print(f"[Supabase] Cleaned {excess} old images.")
        except Exception as e:
            print(f"[Supabase] Cleanup error: {e}")
