import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import threading
import pyttsx3
import pyperclip
import urllib.parse
import re

class LanguageTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌍 Advanced Language Translator - CodeAlpha")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
        except:
            self.tts_engine = None
            print("Text-to-speech not available")
        
        # Language codes mapping for MyMemory API
        self.languages = {
            'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
            'Italian': 'it', 'Portuguese': 'pt', 'Russian': 'ru', 'Chinese': 'zh',
            'Japanese': 'ja', 'Korean': 'ko', 'Arabic': 'ar', 'Hindi': 'hi',
            'Dutch': 'nl', 'Swedish': 'sv', 'Norwegian': 'no', 'Turkish': 'tr',
            'Polish': 'pl', 'Greek': 'el', 'Hebrew': 'he', 'Thai': 'th',
            'Vietnamese': 'vi', 'Czech': 'cs', 'Hungarian': 'hu', 'Finnish': 'fi',
            'Danish': 'da', 'Bulgarian': 'bg', 'Croatian': 'hr', 'Slovak': 'sk'
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🌍 Advanced Language Translator",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Language selection frame
        lang_frame = tk.Frame(main_frame, bg='#2c3e50')
        lang_frame.pack(fill='x', pady=10)
        
        # Source language
        tk.Label(lang_frame, text="From:", font=('Arial', 12, 'bold'), 
                bg='#2c3e50', fg='#ecf0f1').grid(row=0, column=0, padx=5)
        
        self.source_lang = ttk.Combobox(
            lang_frame, 
            values=list(self.languages.keys()),
            state='readonly',
            width=15,
            font=('Arial', 10)
        )
        self.source_lang.set('English')
        self.source_lang.grid(row=0, column=1, padx=10)
        
        # Swap button
        swap_btn = tk.Button(
            lang_frame,
            text="⇄",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.swap_languages,
            width=3
        )
        swap_btn.grid(row=0, column=2, padx=10)
        
        # Target language
        tk.Label(lang_frame, text="To:", font=('Arial', 12, 'bold'), 
                bg='#2c3e50', fg='#ecf0f1').grid(row=0, column=3, padx=5)
        
        self.target_lang = ttk.Combobox(
            lang_frame, 
            values=list(self.languages.keys()),
            state='readonly',
            width=15,
            font=('Arial', 10)
        )
        self.target_lang.set('Spanish')
        self.target_lang.grid(row=0, column=4, padx=10)
        
        # Input text area
        input_frame = tk.Frame(main_frame, bg='#2c3e50')
        input_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(input_frame, text="Enter text to translate:", 
                font=('Arial', 12, 'bold'), bg='#2c3e50', fg='#ecf0f1').pack(anchor='w')
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=8,
            width=80,
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            wrap=tk.WORD
        )
        self.input_text.pack(fill='both', expand=True, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg='#2c3e50')
        btn_frame.pack(fill='x', pady=10)
        
        # Translate button
        translate_btn = tk.Button(
            btn_frame,
            text="🔄 Translate",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.translate_text,
            padx=20,
            pady=5
        )
        translate_btn.pack(side='left', padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear",
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            command=self.clear_text,
            padx=20,
            pady=5
        )
        clear_btn.pack(side='left', padx=5)
        
        # Detect language button
        detect_btn = tk.Button(
            btn_frame,
            text="🔍 Auto-Detect",
            font=('Arial', 12, 'bold'),
            bg='#f39c12',
            fg='white',
            command=self.detect_language,
            padx=20,
            pady=5
        )
        detect_btn.pack(side='left', padx=5)
        
        # Output text area
        output_frame = tk.Frame(main_frame, bg='#2c3e50')
        output_frame.pack(fill='both', expand=True, pady=10)
        
        output_label_frame = tk.Frame(output_frame, bg='#2c3e50')
        output_label_frame.pack(fill='x')
        
        tk.Label(output_label_frame, text="Translation:", 
                font=('Arial', 12, 'bold'), bg='#2c3e50', fg='#ecf0f1').pack(side='left')
        
        # Copy button
        copy_btn = tk.Button(
            output_label_frame,
            text="📋 Copy",
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            command=self.copy_translation,
            padx=10
        )
        copy_btn.pack(side='right')
        
        # Speak button
        speak_btn = tk.Button(
            output_label_frame,
            text="🔊 Speak",
            font=('Arial', 10),
            bg='#34495e',
            fg='white',
            command=self.speak_translation,
            padx=10
        )
        speak_btn.pack(side='right', padx=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            width=80,
            font=('Arial', 11),
            bg='#d5dbdb',
            fg='#2c3e50',
            wrap=tk.WORD,
            state='disabled'
        )
        self.output_text.pack(fill='both', expand=True, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to translate")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor='w',
            bg='#34495e',
            fg='white',
            font=('Arial', 10)
        )
        status_bar.pack(side='bottom', fill='x')
        
    def translate_with_mymemory(self, text, source_lang, target_lang):
        """Translate using MyMemory API (free, no API key required)"""
        try:
            # Encode text for URL
            encoded_text = urllib.parse.quote(text)
            
            # MyMemory API endpoint
            url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair={source_lang}|{target_lang}"
            
            # Make request
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data['responseStatus'] == 200:
                return data['responseData']['translatedText']
            else:
                return None
                
        except Exception as e:
            print(f"MyMemory translation error: {e}")
            return None
            
    def translate_with_libre(self, text, source_lang, target_lang):
        """Translate using LibreTranslate API (fallback)"""
        try:
            # LibreTranslate public instance
            url = "https://libretranslate.de/translate"
            
            data = {
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text'
            }
            
            response = requests.post(url, data=data, timeout=10)
            result = response.json()
            
            if 'translatedText' in result:
                return result['translatedText']
            else:
                return None
                
        except Exception as e:
            print(f"LibreTranslate error: {e}")
            return None
    
    def simple_translate(self, text, source_lang, target_lang):
        """Simple dictionary-based translation for common phrases"""
        translations = {
            'en': {
                'hello': {'es': 'hola', 'fr': 'bonjour', 'de': 'hallo', 'it': 'ciao'},
                'goodbye': {'es': 'adiós', 'fr': 'au revoir', 'de': 'auf wiedersehen', 'it': 'ciao'},
                'thank you': {'es': 'gracias', 'fr': 'merci', 'de': 'danke', 'it': 'grazie'},
                'please': {'es': 'por favor', 'fr': 's\'il vous plaît', 'de': 'bitte', 'it': 'per favore'},
                'yes': {'es': 'sí', 'fr': 'oui', 'de': 'ja', 'it': 'sì'},
                'no': {'es': 'no', 'fr': 'non', 'de': 'nein', 'it': 'no'},
                'how are you': {'es': '¿cómo estás?', 'fr': 'comment allez-vous?', 'de': 'wie geht es dir?', 'it': 'come stai?'},
                'good morning': {'es': 'buenos días', 'fr': 'bonjour', 'de': 'guten morgen', 'it': 'buongiorno'},
                'good evening': {'es': 'buenas tardes', 'fr': 'bonsoir', 'de': 'guten abend', 'it': 'buonasera'},
                'i love you': {'es': 'te amo', 'fr': 'je t\'aime', 'de': 'ich liebe dich', 'it': 'ti amo'}
            }
        }
        
        text_lower = text.lower().strip()
        if source_lang in translations and text_lower in translations[source_lang]:
            if target_lang in translations[source_lang][text_lower]:
                return translations[source_lang][text_lower][target_lang]
        
        return None
        
    def translate_text(self):
        input_text = self.input_text.get('1.0', tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("Warning", "Please enter text to translate!")
            return
            
        # Start translation in a separate thread
        threading.Thread(target=self._perform_translation, args=(input_text,), daemon=True).start()
        
    def _perform_translation(self, text):
        try:
            self.status_var.set("Translating...")
            self.root.config(cursor="wait")
            
            source_code = self.languages[self.source_lang.get()]
            target_code = self.languages[self.target_lang.get()]
            
            translation = None
            
            # Try simple translation first for common phrases
            translation = self.simple_translate(text, source_code, target_code)
            
            if not translation:
                # Try MyMemory API
                translation = self.translate_with_mymemory(text, source_code, target_code)
            
            if not translation:
                # Try LibreTranslate as fallback
                translation = self.translate_with_libre(text, source_code, target_code)
            
            if not translation:
                # If all else fails, provide a message
                translation = f"Translation not available. Original text: {text}"
            
            # Update UI in main thread
            self.root.after(0, self._update_translation_result, translation, source_code)
            
        except Exception as e:
            self.root.after(0, self._show_error, f"Translation failed: {str(e)}")
        finally:
            self.root.after(0, lambda: self.root.config(cursor=""))
            
    def _update_translation_result(self, translation, detected_lang):
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', translation)
        self.output_text.config(state='disabled')
        
        # Update status
        lang_name = next((k for k, v in self.languages.items() if v == detected_lang), detected_lang)
        self.status_var.set(f"Translation completed! Source language: {lang_name}")
        
    def _show_error(self, error_msg):
        messagebox.showerror("Error", error_msg)
        self.status_var.set("Translation failed")
        
    def swap_languages(self):
        source = self.source_lang.get()
        target = self.target_lang.get()
        self.source_lang.set(target)
        self.target_lang.set(source)
        
    def clear_text(self):
        self.input_text.delete('1.0', tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state='disabled')
        self.status_var.set("Ready to translate")
        
    def detect_language(self):
        input_text = self.input_text.get('1.0', tk.END).strip()
        if not input_text:
            messagebox.showwarning("Warning", "Please enter text to detect language!")
            return
            
        # Simple language detection based on common words/patterns
        detection_patterns = {
            'Spanish': ['el', 'la', 'es', 'en', 'de', 'que', 'y', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'una', 'está', 'hola', 'gracias', 'adiós'],
            'French': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'bonjour', 'merci', 'au revoir'],
            'German': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf', 'für', 'ist', 'im', 'dem', 'nicht', 'ein', 'eine', 'als', 'hallo', 'danke'],
            'Italian': ['di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra', 'il', 'lo', 'la', 'i', 'gli', 'le', 'un', 'uno', 'una', 'ciao', 'grazie', 'prego']
        }
        
        text_lower = input_text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        scores = {}
        for lang, patterns in detection_patterns.items():
            score = sum(1 for word in words if word in patterns)
            if score > 0:
                scores[lang] = score / len(words)
        
        if scores:
            detected_lang = max(scores, key=scores.get)
            confidence = scores[detected_lang]
            self.source_lang.set(detected_lang)
            self.status_var.set(f"Detected language: {detected_lang} (Confidence: {confidence:.2f})")
        else:
            self.status_var.set("Could not detect language - assuming English")
            self.source_lang.set('English')
            
    def copy_translation(self):
        translation = self.output_text.get('1.0', tk.END).strip()
        if translation:
            try:
                pyperclip.copy(translation)
                self.status_var.set("Translation copied to clipboard!")
            except:
                # Fallback if pyperclip doesn't work
                self.root.clipboard_clear()
                self.root.clipboard_append(translation)
                self.status_var.set("Translation copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No translation to copy!")
            
    def speak_translation(self):
        translation = self.output_text.get('1.0', tk.END).strip()
        if translation:
            if self.tts_engine:
                threading.Thread(target=self._speak_text, args=(translation,), daemon=True).start()
            else:
                messagebox.showinfo("Info", "Text-to-speech not available on this system")
        else:
            messagebox.showwarning("Warning", "No translation to speak!")
            
    def _speak_text(self, text):
        try:
            if self.tts_engine:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Text-to-speech failed: {str(e)}"))
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LanguageTranslator()
    app.run()
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json
import threading
import pyttsx3
import pyperclip
import urllib.parse
import re

class LanguageTranslator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🌍 Advanced Language Translator - CodeAlpha")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Initialize text-to-speech
        try:
            self.tts_engine = pyttsx3.init()
        except:
            self.tts_engine = None
            print("Text-to-speech not available")
        
        # Language codes mapping for MyMemory API
        self.languages = {
            'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de',
            'Italian': 'it', 'Portuguese': 'pt', 'Russian': 'ru', 'Chinese': 'zh',
            'Japanese': 'ja', 'Korean': 'ko', 'Arabic': 'ar', 'Hindi': 'hi',
            'Dutch': 'nl', 'Swedish': 'sv', 'Norwegian': 'no', 'Turkish': 'tr',
            'Polish': 'pl', 'Greek': 'el', 'Hebrew': 'he', 'Thai': 'th',
            'Vietnamese': 'vi', 'Czech': 'cs', 'Hungarian': 'hu', 'Finnish': 'fi',
            'Danish': 'da', 'Bulgarian': 'bg', 'Croatian': 'hr', 'Slovak': 'sk'
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🌍 Advanced Language Translator",
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Language selection frame
        lang_frame = tk.Frame(main_frame, bg='#2c3e50')
        lang_frame.pack(fill='x', pady=10)
        
        # Source language
        tk.Label(lang_frame, text="From:", font=('Arial', 12, 'bold'), 
                bg='#2c3e50', fg='#ecf0f1').grid(row=0, column=0, padx=5)
        
        self.source_lang = ttk.Combobox(
            lang_frame, 
            values=list(self.languages.keys()),
            state='readonly',
            width=15,
            font=('Arial', 10)
        )
        self.source_lang.set('English')
        self.source_lang.grid(row=0, column=1, padx=10)
        
        # Swap button
        swap_btn = tk.Button(
            lang_frame,
            text="⇄",
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.swap_languages,
            width=3
        )
        swap_btn.grid(row=0, column=2, padx=10)
        
        # Target language
        tk.Label(lang_frame, text="To:", font=('Arial', 12, 'bold'), 
                bg='#2c3e50', fg='#ecf0f1').grid(row=0, column=3, padx=5)
        
        self.target_lang = ttk.Combobox(
            lang_frame, 
            values=list(self.languages.keys()),
            state='readonly',
            width=15,
            font=('Arial', 10)
        )
        self.target_lang.set('Spanish')
        self.target_lang.grid(row=0, column=4, padx=10)
        
        # Input text area
        input_frame = tk.Frame(main_frame, bg='#2c3e50')
        input_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(input_frame, text="Enter text to translate:", 
                font=('Arial', 12, 'bold'), bg='#2c3e50', fg='#ecf0f1').pack(anchor='w')
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame,
            height=8,
            width=80,
            font=('Arial', 11),
            bg='#ecf0f1',
            fg='#2c3e50',
            wrap=tk.WORD
        )
        self.input_text.pack(fill='both', expand=True, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg='#2c3e50')
        btn_frame.pack(fill='x', pady=10)
        
        # Translate button
        translate_btn = tk.Button(
            btn_frame,
            text="🔄 Translate",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.translate_text,
            padx=20,
            pady=5
        )
        translate_btn.pack(side='left', padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear",
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            command=self.clear_text,
            padx=20,
            pady=5
        )
        clear_btn.pack(side='left', padx=5)
        
        # Detect language button
        detect_btn = tk.Button(
            btn_frame,
            text="🔍 Auto-Detect",
            font=('Arial', 12, 'bold'),
            bg='#f39c12',
            fg='white',
            command=self.detect_language,
            padx=20,
            pady=5
        )
        detect_btn.pack(side='left', padx=5)
        
        # Output text area
        output_frame = tk.Frame(main_frame, bg='#2c3e50')
        output_frame.pack(fill='both', expand=True, pady=10)
        
        output_label_frame = tk.Frame(output_frame, bg='#2c3e50')
        output_label_frame.pack(fill='x')
        
        tk.Label(output_label_frame, text="Translation:", 
                font=('Arial', 12, 'bold'), bg='#2c3e50', fg='#ecf0f1').pack(side='left')
        
        # Copy button
        copy_btn = tk.Button(
            output_label_frame,
            text="📋 Copy",
            font=('Arial', 10),
            bg='#9b59b6',
            fg='white',
            command=self.copy_translation,
            padx=10
        )
        copy_btn.pack(side='right')
        
        # Speak button
        speak_btn = tk.Button(
            output_label_frame,
            text="🔊 Speak",
            font=('Arial', 10),
            bg='#34495e',
            fg='white',
            command=self.speak_translation,
            padx=10
        )
        speak_btn.pack(side='right', padx=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            width=80,
            font=('Arial', 11),
            bg='#d5dbdb',
            fg='#2c3e50',
            wrap=tk.WORD,
            state='disabled'
        )
        self.output_text.pack(fill='both', expand=True, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to translate")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor='w',
            bg='#34495e',
            fg='white',
            font=('Arial', 10)
        )
        status_bar.pack(side='bottom', fill='x')
        
    def translate_with_mymemory(self, text, source_lang, target_lang):
        """Translate using MyMemory API (free, no API key required)"""
        try:
            # Encode text for URL
            encoded_text = urllib.parse.quote(text)
            
            # MyMemory API endpoint
            url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair={source_lang}|{target_lang}"
            
            # Make request
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data['responseStatus'] == 200:
                return data['responseData']['translatedText']
            else:
                return None
                
        except Exception as e:
            print(f"MyMemory translation error: {e}")
            return None
            
    def translate_with_libre(self, text, source_lang, target_lang):
        """Translate using LibreTranslate API (fallback)"""
        try:
            # LibreTranslate public instance
            url = "https://libretranslate.de/translate"
            
            data = {
                'q': text,
                'source': source_lang,
                'target': target_lang,
                'format': 'text'
            }
            
            response = requests.post(url, data=data, timeout=10)
            result = response.json()
            
            if 'translatedText' in result:
                return result['translatedText']
            else:
                return None
                
        except Exception as e:
            print(f"LibreTranslate error: {e}")
            return None
    
    def simple_translate(self, text, source_lang, target_lang):
        """Simple dictionary-based translation for common phrases"""
        translations = {
            'en': {
                'hello': {'es': 'hola', 'fr': 'bonjour', 'de': 'hallo', 'it': 'ciao'},
                'goodbye': {'es': 'adiós', 'fr': 'au revoir', 'de': 'auf wiedersehen', 'it': 'ciao'},
                'thank you': {'es': 'gracias', 'fr': 'merci', 'de': 'danke', 'it': 'grazie'},
                'please': {'es': 'por favor', 'fr': 's\'il vous plaît', 'de': 'bitte', 'it': 'per favore'},
                'yes': {'es': 'sí', 'fr': 'oui', 'de': 'ja', 'it': 'sì'},
                'no': {'es': 'no', 'fr': 'non', 'de': 'nein', 'it': 'no'},
                'how are you': {'es': '¿cómo estás?', 'fr': 'comment allez-vous?', 'de': 'wie geht es dir?', 'it': 'come stai?'},
                'good morning': {'es': 'buenos días', 'fr': 'bonjour', 'de': 'guten morgen', 'it': 'buongiorno'},
                'good evening': {'es': 'buenas tardes', 'fr': 'bonsoir', 'de': 'guten abend', 'it': 'buonasera'},
                'i love you': {'es': 'te amo', 'fr': 'je t\'aime', 'de': 'ich liebe dich', 'it': 'ti amo'}
            }
        }
        
        text_lower = text.lower().strip()
        if source_lang in translations and text_lower in translations[source_lang]:
            if target_lang in translations[source_lang][text_lower]:
                return translations[source_lang][text_lower][target_lang]
        
        return None
        
    def translate_text(self):
        input_text = self.input_text.get('1.0', tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("Warning", "Please enter text to translate!")
            return
            
        # Start translation in a separate thread
        threading.Thread(target=self._perform_translation, args=(input_text,), daemon=True).start()
        
    def _perform_translation(self, text):
        try:
            self.status_var.set("Translating...")
            self.root.config(cursor="wait")
            
            source_code = self.languages[self.source_lang.get()]
            target_code = self.languages[self.target_lang.get()]
            
            translation = None
            
            # Try simple translation first for common phrases
            translation = self.simple_translate(text, source_code, target_code)
            
            if not translation:
                # Try MyMemory API
                translation = self.translate_with_mymemory(text, source_code, target_code)
            
            if not translation:
                # Try LibreTranslate as fallback
                translation = self.translate_with_libre(text, source_code, target_code)
            
            if not translation:
                # If all else fails, provide a message
                translation = f"Translation not available. Original text: {text}"
            
            # Update UI in main thread
            self.root.after(0, self._update_translation_result, translation, source_code)
            
        except Exception as e:
            self.root.after(0, self._show_error, f"Translation failed: {str(e)}")
        finally:
            self.root.after(0, lambda: self.root.config(cursor=""))
            
    def _update_translation_result(self, translation, detected_lang):
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', translation)
        self.output_text.config(state='disabled')
        
        # Update status
        lang_name = next((k for k, v in self.languages.items() if v == detected_lang), detected_lang)
        self.status_var.set(f"Translation completed! Source language: {lang_name}")
        
    def _show_error(self, error_msg):
        messagebox.showerror("Error", error_msg)
        self.status_var.set("Translation failed")
        
    def swap_languages(self):
        source = self.source_lang.get()
        target = self.target_lang.get()
        self.source_lang.set(target)
        self.target_lang.set(source)
        
    def clear_text(self):
        self.input_text.delete('1.0', tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state='disabled')
        self.status_var.set("Ready to translate")
        
    def detect_language(self):
        input_text = self.input_text.get('1.0', tk.END).strip()
        if not input_text:
            messagebox.showwarning("Warning", "Please enter text to detect language!")
            return
            
        # Simple language detection based on common words/patterns
        detection_patterns = {
            'Spanish': ['el', 'la', 'es', 'en', 'de', 'que', 'y', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'una', 'está', 'hola', 'gracias', 'adiós'],
            'French': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'bonjour', 'merci', 'au revoir'],
            'German': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich', 'des', 'auf', 'für', 'ist', 'im', 'dem', 'nicht', 'ein', 'eine', 'als', 'hallo', 'danke'],
            'Italian': ['di', 'a', 'da', 'in', 'con', 'su', 'per', 'tra', 'fra', 'il', 'lo', 'la', 'i', 'gli', 'le', 'un', 'uno', 'una', 'ciao', 'grazie', 'prego']
        }
        
        text_lower = input_text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        scores = {}
        for lang, patterns in detection_patterns.items():
            score = sum(1 for word in words if word in patterns)
            if score > 0:
                scores[lang] = score / len(words)
        
        if scores:
            detected_lang = max(scores, key=scores.get)
            confidence = scores[detected_lang]
            self.source_lang.set(detected_lang)
            self.status_var.set(f"Detected language: {detected_lang} (Confidence: {confidence:.2f})")
        else:
            self.status_var.set("Could not detect language - assuming English")
            self.source_lang.set('English')
            
    def copy_translation(self):
        translation = self.output_text.get('1.0', tk.END).strip()
        if translation:
            try:
                pyperclip.copy(translation)
                self.status_var.set("Translation copied to clipboard!")
            except:
                # Fallback if pyperclip doesn't work
                self.root.clipboard_clear()
                self.root.clipboard_append(translation)
                self.status_var.set("Translation copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No translation to copy!")
            
    def speak_translation(self):
        translation = self.output_text.get('1.0', tk.END).strip()
        if translation:
            if self.tts_engine:
                threading.Thread(target=self._speak_text, args=(translation,), daemon=True).start()
            else:
                messagebox.showinfo("Info", "Text-to-speech not available on this system")
        else:
            messagebox.showwarning("Warning", "No translation to speak!")
            
    def _speak_text(self, text):
        try:
            if self.tts_engine:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Text-to-speech failed: {str(e)}"))
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = LanguageTranslator()
    app.run()
