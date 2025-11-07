@echo off
echo ========================================
echo  RENDER FIX - Push Updated Requirements
echo ========================================
echo.

cd /d Z:\VESIRE_35

echo Step 1: Adding updated files...
git add Backend/requirements.txt PYTHON_VERSION_FIX.md RENDER_FIX_GUIDE.md render.yaml

echo.
echo Step 2: Committing changes...
git commit -m "fix: update Pillow 10.3.0 and force Python 3.11 compatibility"

echo.
echo Step 3: Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo  Push Complete!
echo ========================================
echo.
echo IMPORTANT: Now do this in Render Dashboard:
echo.
echo 1. Go to: https://dashboard.render.com
echo 2. Click your service: agriscan-backend
echo 3. Click Settings (left sidebar)
echo 4. Find "Python Version" dropdown
echo 5. Select "3.11.6" (NOT 3.13!)
echo 6. Click "Save Changes"
echo.
echo Then watch the build logs for:
echo "==> Using Python version 3.11.6"
echo.
pause
