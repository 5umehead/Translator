# VerbalScript: Voice Translator Tool 

## Overview

**VerbalScript** is a Python-based desktop application that provides real-time voice and text translation. Built using **Tkinter**, it allows users to input text manually or via voice, translate it into multiple languages, and even listen to both the original and translated text using text-to-speech.

---

## Features

*  **Voice Input** – Speak directly into your microphone and convert speech to text.
*  **Multi-language Translation** – Supports a wide range of languages with auto-detection.
*  **Text-to-Speech (TTS)** – Listen to both input and translated text.
*  **Clipboard Copy** – Easily copy translated text.
*  **Language Swap** – Quickly switch source and destination languages.
*  **Clear Interface** – Reset input and output fields instantly.
*  **Modern UI** – Clean, blue-themed graphical interface.

---

## Technologies Used

* **Python 3**
* **Tkinter** – GUI framework
* **deep-translator** – Translation API wrapper
* **gTTS (Google Text-to-Speech)** – Speech synthesis
* **SpeechRecognition** – Voice input processing
* **PyAudio** – Microphone access
* **pyperclip** – Clipboard functionality
* **threading** – Background processing

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/verbalscript.git
cd verbalscript
```

### 2. Install Dependencies

```bash
pip install tkinter deep-translator pyperclip gTTS SpeechRecognition pyaudio
```

>  Note: Installing **PyAudio** may require additional setup depending on your OS.

---

## How to Run

```bash
python your_script_name.py
```

---

## Usage Guide

### Text Translation

1. Enter text in the **Original Text** box.
2. Select source and target languages.
3. Click **Translate**.

### Voice Input

1. Click **Start Voice Input**.
2. Speak clearly into your microphone.
3. Click again to stop recording.

### Text-to-Speech

* Click **Speak** to hear input text.
* Click **Speak Translation** to hear translated text.

### Other Actions

* **Copy** – Copies translated text to clipboard.
* **Clear** – Clears both text fields.
* **Swap** – Switches source and target languages.

---

## Supported Languages

The app supports a wide variety of languages including:

* English, Hindi, Marathi, Spanish, French, German, Chinese, Arabic, and many more.
* Includes **Auto-detect** for automatic source language detection.

---

## Known Limitations

* Requires internet connection for translation and speech services.
* Voice recognition accuracy depends on microphone quality and background noise.
* Text-to-speech playback command is OS-dependent:

  * Windows: `start`
  * Linux: `mpg123`
  * macOS: `afplay`

---

## Future Improvements

* Offline translation support
* Better language detection accuracy
* Save translation history
* UI enhancements and themes
* Packaging as a standalone executable

---

## License

This project is open-source and available under the MIT License.

---

## Author

Developed as a voice-enabled translation tool using Python.

---

## Contributing

Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

## Acknowledgements

* Google Translate API (via deep-translator)
* Google Text-to-Speech
* Open-source Python libraries

---
