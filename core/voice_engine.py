import speech_recognition as sr
import pyttsx3
import threading
from config import Config

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Text-to-Speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', Config.VOICE_RATE)
        self.tts_engine.setProperty('volume', Config.VOICE_VOLUME)
        
        # Set voice (0 = male, 1 = female usually)
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)  # Female voice
        
        self.is_listening = False
    
    def speak(self, text):
        """Convert text to speech"""
        if not Config.VOICE_ENABLED:
            return
        
        def _speak():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"Speech error: {e}")
        
        # Run in separate thread to avoid blocking
        thread = threading.Thread(target=_speak)
        thread.start()
    
    def listen(self, timeout=5):
        """Listen to microphone and convert to text"""
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                print("🔄 Processing...")
                # Convert speech to text
                text = self.recognizer.recognize_google(audio)
                print(f"📝 You said: {text}")
                return text
                
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def continuous_listen(self, callback):
        """Continuously listen for commands"""
        self.is_listening = True
        
        def _listen_loop():
            while self.is_listening:
                text = self.listen()
                if text:
                    callback(text)
        
        thread = threading.Thread(target=_listen_loop, daemon=True)
        thread.start()
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False