# Backend Render Deployment Fix Guide

## Problem
The backend is failing to deploy on Render with the error:
```
ModuleNotFoundError: No module named 'services'
```

## Root Cause
The `render.yaml` has `rootDir: Backend` but the start command runs from within that directory, so the imports can't find the modules.

## Solution Applied

### 1. Updated `app.py` imports
Added sys.path manipulation to ensure imports work:

```python
from pathlib import Path
import sys

# Add api directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import services
from services.model_service import model_service
from services.db_service import db_service
from services.rag_service import rag_service
from config import config
```

### 2. Updated `render.yaml`
Changed from:
```yaml
rootDir: Backend/api
```

To:
```yaml
rootDir: Backend
startCommand: cd api && gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --worker-class sync app:app
```

This ensures:
- Build runs from `Backend/` directory (where `requirements.txt` is)
- Start command changes into `api/` subdirectory before running gunicorn
- Imports work because we added the current directory to sys.path

## Files Modified
1. `Z:\VESIRE_35\render.yaml` - Updated rootDir and startCommand
2. `Z:\VESIRE_35\Backend\Procfile` - Updated with cd command
3. `Z:\VESIRE_35\Backend\api\app.py` - Added sys.path manipulation

## Testing Locally
```powershell
cd Z:\VESIRE_35\Backend\api
python -c "import sys; from pathlib import Path; sys.path.insert(0, str(Path.cwd())); from services.model_service import model_service; print('✅ Imports work!')"
```

## Next Steps for Deployment
1. Commit and push these changes to your repository
2. Render will automatically redeploy
3. The import error should be resolved

## Alternative Solutions (if above doesn't work)

### Option A: Create `__init__.py` in Backend directory
```python
# Backend/__init__.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'api'))
```

### Option B: Use relative imports in app.py
```python
from .services.model_service import model_service
from .services.db_service import db_service
from .services.rag_service import rag_service
from .config import config
```

But then start command needs to be:
```bash
python -m api.app
```

## Verification
Once deployed, check:
1. Health endpoint: `https://vesire-35.onrender.com/api/health`
2. Should return `{"status": "healthy"}`
