from core.ai_brain import AIBrain
from core.voice_engine import VoiceEngine
from core.memory_manager import MemoryManager
from core.command_parser import CommandParser
from config import Config
import sys

class ZYRA:
    def __init__(self):
        print("🚀 Initializing ZYRA AI...")
        
        self.brain = AIBrain()
        self.voice = VoiceEngine()
        self.memory = MemoryManager()
        self.parser = CommandParser()
        
        print(f"✅ {Config.AI_NAME} is ready!")
        self.voice.speak(f"Hello {Config.USER_NAME}, {Config.AI_NAME} is online and ready to assist you.")
    
    def process_input(self, user_input):
        """Process user input (text or voice)"""
        
        # First, check if it's a command
        command_result = self.parser.parse(user_input)
        
        if command_result:
            # It's a command
            response = command_result.get('message', 'Command executed')
            print(f"\n{Config.AI_NAME}: {response}")
            self.voice.speak(response)
            return response
        else:
            # It's a regular chat
            response = self.brain.chat(user_input)
            print(f"\n{Config.AI_NAME}: {response}")
            self.voice.speak(response)
            return response
    
    def text_mode(self):
        """Run in text-only mode"""
        print(f"\n{'='*50}")
        print(f"  {Config.AI_NAME} AI - Text Mode")
        print(f"{'='*50}")
        print("Type 'exit' to quit, 'voice' to switch to voice mode\n")
        
        while True:
            try:
                user_input = input(f"{Config.USER_NAME}: ").strip()
                
                if user_input.lower() == 'exit':
                    self.voice.speak("Goodbye!")
                    break
                
                if user_input.lower() == 'voice':
                    self.voice_mode()
                    continue
                
                if user_input:
                    self.process_input(user_input)
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
    
    def voice_mode(self):
        """Run in voice mode"""
        print(f"\n{'='*50}")
        print(f"  {Config.AI_NAME} AI - Voice Mode")
        print(f"{'='*50}")
        print("Say 'exit' to quit, 'text mode' to switch to text\n")
        
        self.voice.speak("Voice mode activated. I'm listening.")
        
        while True:
            try:
                print(f"\n{Config.USER_NAME}: ", end="", flush=True)
                user_input = self.voice.listen()
                
                if user_input is None:
                    continue
                
                if 'exit' in user_input.lower():
                    self.voice.speak("Goodbye!")
                    break
                
                if 'text mode' in user_input.lower():
                    self.voice.speak("Switching to text mode")
                    self.text_mode()
                    continue
                
                self.process_input(user_input)
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
    
    def run(self):
        """Main run method"""
        print("\nSelect mode:")
        print("1. Text Mode")
        print("2. Voice Mode")
        
        choice = input("\nEnter choice (1/2): ").strip()
        
        if choice == '2':
            self.voice_mode()
        else:
            self.text_mode()

if __name__ == "__main__":
    zyra = ZYRA()
    zyra.run()