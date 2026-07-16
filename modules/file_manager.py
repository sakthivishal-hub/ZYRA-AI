import os
import shutil
from pathlib import Path
from datetime import datetime

class FileManager:
    def __init__(self):
        self.search_paths = [
            str(Path.home() / "Documents"),
            str(Path.home() / "Downloads"),
            str(Path.home() / "Desktop"),
        ]
    
    def find_file(self, filename, search_in=None):
        """Find files by name"""
        if search_in is None:
            search_in = self.search_paths
        
        found_files = []
        
        for search_path in search_in:
            if not os.path.exists(search_path):
                continue
            
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if filename.lower() in file.lower():
                        full_path = os.path.join(root, file)
                        found_files.append({
                            'name': file,
                            'path': full_path,
                            'size': os.path.getsize(full_path),
                            'modified': datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
                        })
                
                # Limit search depth to avoid taking too long
                if len(found_files) >= 50:
                    break
        
        return found_files
    
    def create_file(self, filepath, content=""):
        """Create a new file"""
        try:
            # Expand user path (~)
            filepath = os.path.expanduser(filepath)
            
            # Create directory if doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            return f"✅ Created file: {filepath}"
        
        except Exception as e:
            return f"❌ Error creating file: {str(e)}"
    
    def delete_file(self, filepath):
        """Delete a file"""
        try:
            filepath = os.path.expanduser(filepath)
            
            if os.path.isfile(filepath):
                os.remove(filepath)
                return f"✅ Deleted file: {filepath}"
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)
                return f"✅ Deleted directory: {filepath}"
            else:
                return f"⚠️ File not found: {filepath}"
        
        except Exception as e:
            return f"❌ Error deleting file: {str(e)}"
    
    def read_file(self, filepath):
        """Read file contents"""
        try:
            filepath = os.path.expanduser(filepath)
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            return content
        
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"
    
    def get_file_info(self, filepath):
        """Get file information"""
        try:
            filepath = os.path.expanduser(filepath)
            stat = os.stat(filepath)
            
            return {
                'name': os.path.basename(filepath),
                'path': filepath,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'is_file': os.path.isfile(filepath),
                'is_dir': os.path.isdir(filepath)
            }
        
        except Exception as e:
            return f"❌ Error getting file info: {str(e)}"