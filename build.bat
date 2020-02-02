
cmd /k "venv\Scripts\activate & pyinstaller main.spec & powershell Compress-Archive -Force dist\main dist\main.zip"

