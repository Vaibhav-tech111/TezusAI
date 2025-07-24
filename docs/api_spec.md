# 🔧 Tezus API Specification

## 🧠 Brain Layer

### `POST /parse_intent`
- **Input:** `{ "text": "open calculator" }`
- **Output:** `{ "intent": "open_app", "entities": ["calculator"], "confidence": 0.95 }`

### `POST /generate_plan`
- **Input:** `{ "intent": "...", "entities": [...] }`
- **Output:** `[ { "plugin": "app_controller", "action": "open", "params": {...} } ]`

---

## ⚙️ Executor Layer

### `POST /run_task`
- **Input:** `task_plan[]`
- **Output:** `fused_result`

### `GET /task_history`
- **Output:** `[ { timestamp, intent, plugin, action, result } ]`

---

## 🔌 Plugin Interfaces

### `GET /system_info`
- **Output:** `{ cpu, ram, disk, network }`

### `POST /speak`
- **Input:** `{ "text": "Hello Anand!" }`
- **Output:** `status: success`

---

## 🗃️ Database Access

### `GET /user_profile`
- **Output:** `{ "name": "Anand", "preferences": {...} }`

### `POST /update_permission`
- **Input:** `{ "plugin_action": "system_control.shutdown", "decision": "allow" }`
