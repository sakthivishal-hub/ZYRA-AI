import re
from modules.app_controller import AppController
from modules.file_manager import FileManager
from modules.web_search import WebSearch

class CommandParser:
    def __init__(self):
        self.app_controller = AppController()
        self.file_manager = FileManager()
        self.web_search = WebSearch()
        
        # Command patterns
        self.patterns = {
            'open_app': r'open\s+(.+)',
            'close_app': r'close\s+(.+)',
            'search_web': r'search\s+(?:for\s+)?(.+)',
            'find_file': r'find\s+(?:file\s+)?(.+)',
            'create_file': r'create\s+(?:file\s+)?(.+)',
            'delete_file': r'delete\s+(?:file\s+)?(.+)',
        }
    
    def parse(self, command):
        """Parse command and execute action"""
        command = command.lower().strip()
        
        # Check each pattern
        for action, pattern in self.patterns.items():
            match = re.search(pattern, command)
            if match:
                param = match.group(1).strip()
                return self.execute_action(action, param)
        
        return None  # No command matched, treat as regular chat
    
    def execute_action(self, action, param):
        """Execute the parsed action"""
        try:
            if action == 'open_app':
                result = self.app_controller.open_app(param)
                return {"success": True, "message": result}
            
            elif action == 'close_app':
                result = self.app_controller.close_app(param)
                return {"success": True, "message": result}
            
            elif action == 'search_web':
                results = self.web_search.search(param)
                return {"success": True, "message": f"Found results for '{param}'", "data": results}
            
            elif action == 'find_file':
                files = self.file_manager.find_file(param)
                return {"success": True, "message": f"Found {len(files)} file(s)", "data": files}
            
            elif action == 'create_file':
                result = self.file_manager.create_file(param)
                return {"success": True, "message": result}
            
            elif action == 'delete_file':
                result = self.file_manager.delete_file(param)
                return {"success": True, "message": result}
        #python inforgraphic
        except Exception as e:
            return {"success": False, "message": f"Error: {str(e)}"}
