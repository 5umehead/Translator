import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyperclip
from gtts import gTTS
import os
import threading
import speech_recognition as sr
import pyaudio


class VoiceTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("VerbalScript:Translating tool")
        self.root.geometry("1000x650")

        # Color scheme
        self.dark_blue = "#001a33"
        self.medium_blue = "#003366"
        self.light_blue = "#0077b3"
        self.text_bg = "#e6f2ff"
        self.button_blue = "#005c99"
        self.highlight_blue = "#0088cc"
        self.auto_detect_color = "#ff9900"

        self.root.configure(bg=self.dark_blue)

        # Initialize audio components
        self.audio = pyaudio.PyAudio()
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False

        # Languages with their codes (including 'Auto-detect')
        self.languages = {
            'Auto-detect': 'auto',
            'Afrikaans': 'af', 'Albanian': 'sq', 'Amharic': 'am', 'Arabic': 'ar',
            'Armenian': 'hy', 'Azerbaijani': 'az', 'Basque': 'eu', 'Belarusian': 'be',
            'Bengali': 'bn', 'Bosnian': 'bs', 'Bulgarian': 'bg', 'Burmese': 'my',
            'Catalan': 'ca', 'Cebuano': 'ceb', 'Chinese (Simplified)': 'zh-CN',
            'Chinese (Traditional)': 'zh-TW', 'Corsican': 'co', 'Croatian': 'hr',
            'Czech': 'cs', 'Danish': 'da', 'Dutch': 'nl', 'English': 'en',
            'Esperanto': 'eo', 'Estonian': 'et', 'Finnish': 'fi', 'French': 'fr',
            'Frisian': 'fy', 'Galician': 'gl', 'Georgian': 'ka', 'German': 'de',
            'Greek': 'el', 'Gujarati': 'gu', 'Haitian Creole': 'ht', 'Hausa': 'ha',
            'Hawaiian': 'haw', 'Hebrew': 'he', 'Hindi': 'hi', 'Hmong': 'hmn',
            'Hungarian': 'hu', 'Icelandic': 'is', 'Igbo': 'ig', 'Indonesian': 'id',
            'Irish': 'ga', 'Italian': 'it', 'Japanese': 'ja', 'Javanese': 'jv',
            'Kannada': 'kn', 'Kazakh': 'kk', 'Khmer': 'km', 'Kinyarwanda': 'rw',
            'Korean': 'ko', 'Kurdish': 'ku', 'Kyrgyz': 'ky', 'Lao': 'lo',
            'Latin': 'la', 'Latvian': 'lv', 'Lithuanian': 'lt', 'Luxembourgish': 'lb',
            'Macedonian': 'mk', 'Malagasy': 'mg', 'Malay': 'ms', 'Malayalam': 'ml',
            'Maltese': 'mt', 'Maori': 'mi', 'Marathi': 'mr', 'Mongolian': 'mn',
            'Nepali': 'ne', 'Norwegian': 'no', 'Nyanja': 'ny', 'Odia': 'or',
            'Pashto': 'ps', 'Persian': 'fa', 'Polish': 'pl', 'Portuguese': 'pt',
            'Punjabi': 'pa', 'Romanian': 'ro', 'Russian': 'ru', 'Samoan': 'sm',
            'Scots Gaelic': 'gd', 'Serbian': 'sr', 'Sesotho': 'st', 'Shona': 'sn',
            'Sindhi': 'sd', 'Sinhala': 'si', 'Slovak': 'sk', 'Slovenian': 'sl',
            'Somali': 'so', 'Spanish': 'es', 'Sundanese': 'su', 'Swahili': 'sw',
            'Swedish': 'sv', 'Tagalog': 'tl', 'Tajik': 'tg', 'Tamil': 'ta',
            'Tatar': 'tt', 'Telugu': 'te', 'Thai': 'th', 'Turkish': 'tr',
            'Turkmen': 'tk', 'Ukrainian': 'uk', 'Urdu': 'ur', 'Uyghur': 'ug',
            'Uzbek': 'uz', 'Vietnamese': 'vi', 'Welsh': 'cy', 'Xhosa': 'xh',
            'Yiddish': 'yi', 'Yoruba': 'yo', 'Zulu': 'zu'
        }

        self.setup_ui()

    def setup_ui(self):
        # Font styles
        title_font = ("Helvetica", 24, "bold")
        button_font = ("Helvetica", 10, "bold")
        text_font = ("Segoe UI", 11)
        status_font = ("Helvetica", 9)

        # Main container
        main_frame = tk.Frame(self.root, bg=self.dark_blue)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Frame
        header_frame = tk.Frame(main_frame, bg=self.medium_blue)
        header_frame.pack(fill="x", pady=(0, 20))

        tk.Label(
            header_frame,
            text="VerbalScript: Translation tool",
            font=title_font,
            fg="white",
            bg=self.medium_blue,
            pady=15
        ).pack()

        # Status label
        self.status_label = tk.Label(
            header_frame,
            text="Ready (Auto-detect enabled)",
            font=status_font,
            fg="#b3d9ff",
            bg=self.medium_blue
        )
        self.status_label.pack(pady=(0, 10))

        # Text areas frame
        text_frame = tk.Frame(main_frame, bg=self.dark_blue)
        text_frame.pack(fill="both", expand=True)

        # Input area
        input_frame = tk.LabelFrame(
            text_frame,
            text=" Original Text ",
            font=button_font,
            bg=self.medium_blue,
            fg="white",
            bd=2,
            relief="groove"
        )
        input_frame.pack(side="left", fill="both", expand=True, padx=10)

        self.input_text = tk.Text(
            input_frame,
            height=12,
            width=40,
            font=text_font,
            wrap="word",
            padx=10,
            pady=10,
            bg=self.text_bg,
            fg="#003366",
            relief="flat",
            insertbackground="#003366"
        )
        self.input_text.pack(fill="both", expand=True)

        # Input buttons frame
        input_btn_frame = tk.Frame(input_frame, bg=self.medium_blue)
        input_btn_frame.pack(fill="x", pady=5)

        # Voice input button
        self.voice_btn = tk.Button(
            input_btn_frame,
            text="🎤 Start Voice Input",
            command=self.toggle_listening,
            font=button_font,
            bg=self.light_blue,
            fg="white",
            activebackground=self.highlight_blue,
            relief="flat"
        )
        self.voice_btn.pack(side="left", padx=5)

        # Input TTS button
        input_tts_btn = tk.Button(
            input_btn_frame,
            text="🔊 Speak",
            command=lambda: self.text_to_speech(self.input_text.get("1.0", "end-1c"), self.src_lang.get()),
            font=button_font,
            bg=self.light_blue,
            fg="white",
            activebackground=self.highlight_blue,
            relief="flat"
        )
        input_tts_btn.pack(side="right", padx=5)

        # Output area
        output_frame = tk.LabelFrame(
            text_frame,
            text=" Translation ",
            font=button_font,
            bg=self.medium_blue,
            fg="white",
            bd=2,
            relief="groove"
        )
        output_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.output_text = tk.Text(
            output_frame,
            height=12,
            width=40,
            font=text_font,
            wrap="word",
            state="disabled",
            padx=10,
            pady=10,
            bg=self.text_bg,
            fg="#003366",
            relief="flat"
        )
        self.output_text.pack(fill="both", expand=True)

        # Output TTS button
        output_tts_btn = tk.Button(
            output_frame,
            text="🔊 Speak Translation",
            command=lambda: self.text_to_speech(self.output_text.get("1.0", "end-1c"), self.dest_lang.get()),
            font=button_font,
            bg=self.light_blue,
            fg="white",
            activebackground=self.highlight_blue,
            relief="flat"
        )
        output_tts_btn.pack(pady=5)

        # Control frame
        control_frame = tk.Frame(main_frame, bg=self.dark_blue)
        control_frame.pack(fill="x", pady=10)

        # Language selection
        tk.Label(
            control_frame,
            text="From:",
            font=button_font,
            fg="white",
            bg=self.dark_blue
        ).grid(row=0, column=0, padx=5, sticky="e")

        self.src_lang = ttk.Combobox(
            control_frame,
            values=list(self.languages.keys()),
            font=text_font,
            state="readonly",
            width=15
        )
        self.src_lang.current(0)  # Default to Auto-detect
        self.src_lang.grid(row=0, column=1, padx=5)

        # Swap button
        swap_btn = tk.Button(
            control_frame,
            text="⇄ Swap",
            command=self.swap_languages,
            font=button_font,
            bg=self.button_blue,
            fg="white",
            activebackground=self.highlight_blue,
            relief="raised",
            padx=10,
            pady=3
        )
        swap_btn.grid(row=0, column=2, padx=10)

        tk.Label(
            control_frame,
            text="To:",
            font=button_font,
            fg="white",
            bg=self.dark_blue
        ).grid(row=0, column=3, padx=5, sticky="e")

        self.dest_lang = ttk.Combobox(
            control_frame,
            values=list(self.languages.keys())[1:],  # Exclude Auto-detect
            font=text_font,
            state="readonly",
            width=15
        )
        self.dest_lang.current(1)  # Default to English
        self.dest_lang.grid(row=0, column=4, padx=5)

        # Action buttons
        btn_frame = tk.Frame(main_frame, bg=self.dark_blue)
        btn_frame.pack(fill="x", pady=10)

        buttons = [
            ("Translate", "#0066cc", self.translate_text),
            ("Copy", "#1a8cff", self.copy_text),
            ("Clear", "#004d99", self.clear_text)
        ]

        for i, (text, color, cmd) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=text,
                font=button_font,
                bg=color,
                fg="white",
                activebackground=self.highlight_blue,
                relief="raised",
                padx=15,
                pady=5,
                command=cmd
            )
            btn.grid(row=0, column=i, padx=10)

    def toggle_listening(self):
        """Toggle voice input on/off"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        """Start voice input"""
        try:
            self.is_listening = True
            self.voice_btn.config(text="🎤 Listening...", bg="#e74c3c")
            self.status_label.config(text="Listening... Speak now")
            self.input_text.insert("end", "\n[Listening...]")

            # Start listening in a separate thread
            threading.Thread(target=self.listen_input, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Microphone error: {str(e)}")
            self.stop_listening()

    def stop_listening(self):
        """Stop voice input"""
        self.is_listening = False
        self.voice_btn.config(text="🎤 Start Voice Input", bg=self.light_blue)
        self.status_label.config(text="Ready", fg="#b3d9ff")
        # Remove the listening indicator
        self.input_text.delete("end-1c linestart", "end")

    def listen_input(self):
        """Capture voice input from microphone"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                while self.is_listening:
                    try:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        text = self.recognizer.recognize_google(audio)

                        # Update UI in main thread
                        self.root.after(0, self.update_input_text, text)

                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        self.root.after(0, lambda: self.status_label.config(text="Could not understand audio"))
                    except Exception as e:
                        self.root.after(0, lambda: self.status_label.config(text=f"Error: {str(e)}"))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Microphone error: {str(e)}"))
        finally:
            self.root.after(0, self.stop_listening)

    def update_input_text(self, text):
        """Update input text with recognized speech"""
        self.input_text.delete("end-1c linestart", "end")  # Remove listening indicator
        self.input_text.insert("end", f" {text}")
        self.status_label.config(text="Voice input received", fg="#b3d9ff")

    def text_to_speech(self, text, lang_name):
        """Convert text to speech"""
        if not text.strip():
            messagebox.showwarning("Warning", "No text to speak")
            return

        def speak():
            try:
                lang_code = self.languages.get(lang_name, 'en')
                tts = gTTS(text=text, lang=lang_code)
                tts.save("speech.mp3")
                os.system("start speech.mp3")  # Windows
                # For Linux: os.system("mpg123 speech.mp3")
                # For Mac: os.system("afplay speech.mp3")
            except Exception as e:
                messagebox.showerror("Error", f"Text-to-speech failed: {str(e)}")

        threading.Thread(target=speak, daemon=True).start()
        self.status_label.config(text="Speaking...", fg="#b3d9ff")

    def translate_text(self):
        """Handle translation with auto-detection"""
        try:
            text = self.input_text.get("1.0", "end-1c").strip()
            if not text:
                messagebox.showwarning("Warning", "Please enter text to translate")
                return

            src = self.languages[self.src_lang.get()]
            dest = self.languages[self.dest_lang.get()]

            self.status_label.config(text="Translating...", fg="orange")
            self.root.update()

            # Use auto-detection if selected
            if src == 'auto':
                translated = GoogleTranslator(source='auto', target=dest).translate(text)
                # Try to detect the language (first 100 chars for efficiency)
                try:
                    detected_lang = GoogleTranslator(source='auto', target='en').translate(text[:100])
                    detected_lang_name = [k for k, v in self.languages.items() if v == detected_lang][0]
                    self.status_label.config(text=f"Detected: {detected_lang_name}", fg=self.auto_detect_color)
                except:
                    self.status_label.config(text="Translation complete (auto-detected)", fg=self.auto_detect_color)
            else:
                translated = GoogleTranslator(source=src, target=dest).translate(text)
                self.status_label.config(text="Translation complete", fg="#b3d9ff")

            self.output_text.config(state="normal")
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", translated)
            self.output_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", f"Translation failed: {str(e)}")
            self.status_label.config(text="Translation failed", fg="red")

    def swap_languages(self):
        """Swap source and destination languages"""
        current_src = self.src_lang.current()
        current_dest = self.dest_lang.current()

        # Don't swap if source is Auto-detect
        if current_src != 0:
            self.src_lang.current(current_dest + 1)  # +1 to skip Auto-detect
            self.dest_lang.current(current_src - 1 if current_src > 0 else 0)

            if self.output_text.get("1.0", "end-1c"):
                input_content = self.input_text.get("1.0", "end-1c")
                output_content = self.output_text.get("1.0", "end-1c")

                self.input_text.delete("1.0", "end")
                self.input_text.insert("1.0", output_content)

                self.output_text.config(state="normal")
                self.output_text.delete("1.0", "end")
                self.output_text.insert("1.0", input_content)
                self.output_text.config(state="disabled")

    def copy_text(self):
        """Copy translation to clipboard"""
        translated = self.output_text.get("1.0", "end-1c")
        if translated.strip():
            pyperclip.copy(translated)
            messagebox.showinfo("Success", "Translation copied to clipboard!")
            self.status_label.config(text="Text copied to clipboard", fg="#b3d9ff")
        else:
            messagebox.showwarning("Warning", "No translation to copy")

    def clear_text(self):
        """Clear all text fields"""
        self.input_text.delete("1.0", "end")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")
        self.status_label.config(text="Ready", fg="#b3d9ff")

    def __del__(self):
        """Clean up audio resources"""
        if hasattr(self, 'audio'):
            self.audio.terminate()


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTranslator(root)
    root.mainloop()