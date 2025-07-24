# 📐 Tezus Architecture Overview

Tezus is a modular, voice-enabled AI assistant designed for ethical control, dynamic interaction, and scalable intelligence. It blends technical precision with artistic expression through an aura-based interface and multi-model fusion.

---

## 🧱 Core Layers

| Layer             | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `brain/`          | Intent parsing, planning, memory, and fusion logic  
| `executor/`       | Task execution, queue management, permission control  
| `connectors/`     | External APIs (AI models, web search, social media, device control)  
| `plugins/`        | Modular capabilities (voice, image, system, app, file, location, etc.)  
| `database/`       | SQLite-based memory, logs, permissions, and usage tracking  
| `web/`            | Animated aura-style interface with dynamic feedback  

---

## 🧠 Brain Layer

- `brain.py`: Central controller for memory, tools, planning, and fusion  
- `parser.py`: Regex-based intent and entity extraction  
- `planner.py`: Converts intent into executable roadmap  
- `fusion.py`: Combines multi-model responses into one coherent output  

---

## ⚙️ Execution Layer

- `executor.py`: Runs roadmap steps using plugins  
- `queue_manager.py`: Background task queue with priority  
- `permission_manager.py`: Ethical control for sensitive actions  

---

## 🔌 Connectors

- `ai_models.py`: Unified interface for ChatGPT, Gemini, Claude, etc.  
- `web_search.py`: DuckDuckGo-based search with result parsing  
- `social_media.py`: Fetches posts/comments from Twitter, Reddit, YouTube  
- `device_control.py`: OS-level control for WiFi, Bluetooth, volume  

---

## 🧩 Plugins

- `stt_tts.py`: Voice input/output using `speech_recognition` and `pyttsx3`  
- `image_generator.py`: DALL·E-based image generation  
- `system_control.py`: Shutdown, restart, lock screen  
- `app_controller.py`: Open/close apps across OSes  
- `network_controller.py`: Toggle WiFi/Bluetooth  
- `file_editor.py`: Read/write/replace text files  
- `system_info.py`: CPU, RAM, disk, network stats via `psutil`  
- `location_manager.py`: IP-based geolocation + reverse geocoding  
- `input_controller.py`: Gamepad/joystick input via `inputs`  

---

## 🗃️ Database

- `Tezus.db`: SQLite file storing memory, logs, permissions  
- `schema.py`: Table definitions for user profile, task history, plugin usage  
- `manager.py`: Interface for reading/writing to the DB  

---

## 🌈 Web Interface

- `index.html`: Aura-style animated layout  
- `style.css`: Glowing core, rotating rays, waveform, spark  
- `script.js`: Dynamic text and interaction feedback  
- `assets/spark.png`: Visual spark element for animation  

---

## 🔮 Future Directions

- Emotion-aware voice and visuals  
- Plugin chaining and self-optimization  
- Local model support via Ollama  
- Biometric permission verification  
- Cloud sync and multi-device memory
