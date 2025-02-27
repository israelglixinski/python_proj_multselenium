cd client
rm -rf dist/exec
pyinstaller exec.py
xcopy "dist/webdrivers" "dist/exec/_internal/webdrivers" /E /I
copy "dist/configs.json" "dist/exec/_internal/configs.json"
cd..