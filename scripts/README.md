# Scripts - Dev Tools

This folder contains helper `.bat` scripts for quickly starting/stopping your MCP development server.

---

## 🟢 `start_server.bat`

Runs the server with:

```bat
poetry run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Recommended entry point for development.

---

## 🔴 `stop_server.bat`

For future use or extension. Could be extended to kill `uvicorn` processes.

---

## 🔄 `restart_server.bat`

Shortcut to run `stop_server.bat` followed by `start_server.bat`.

---

## ✅ Setup Tips

* All scripts assume your working directory is the root of the repo
* Poetry environment must be installed (`poetry install`)
* Server auto-authenticates via MSAL device code flow
