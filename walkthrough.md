# System Launch Walkthrough

## Overview
The "Fear & Greed Index" system for Casablanca Stock Exchange has been successfully launched.

## Steps Taken

### 1. Script Fixes
- **`start_system.sh`**: Updated the `PROJECT_DIR` variable to dynamically resolve the project path, fixing a hardcoded path issue that prevented the script from running in the current workspace.

### 2. Dependency Management
- **Python 3.13 Compatibility**: The system environment uses Python 3.13.2. Several dependencies in `backend/requirements.txt` were pinned to older versions incompatible with this new Python release.
- **Resolution**: Removed strict version pinning in `backend/requirements.txt` to allow `pip` to resolve compatible versions for all dependencies (including `pandas`, `numpy`, `spacy`, `pydantic`, etc.).
- **Installation**: Successfully created a virtual environment (`.venv`) and installed all backend dependencies.

### 3. System Launch
- Executed `./start_system.sh`.
- **Backend**: Started on `http://127.0.0.1:8000`.
- **Frontend**: Started on `http://localhost:3000`.

## Verification
- **Backend API**: Verified via `curl http://localhost:8000/api/v1/index/latest` -> Returns valid JSON with score.
- **Frontend Dashboard**: Verified via `curl -I http://localhost:3000` -> Returns HTTP 200 OK.

## How to Access
- **Dashboard**: [http://localhost:3000](http://localhost:3000)
- **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## How to Stop
To stop the system, run:
```bash
./stop_system.sh
```
Or press `Ctrl+C` in the terminal where the system is running (if attached).
