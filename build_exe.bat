@echo off
echo Installing PyInstaller...
python -m pip install pyinstaller

echo.
echo Building Appnort executable...
echo This may take a minute.
python -m PyInstaller --noconfirm --onedir --windowed --name "Appnort" --add-data "appnort;appnort" --icon="appnort.png" entry_point.py

echo.
echo Build complete!
echo The executable is located in: dist\Appnort\Appnort.exe
echo.
echo To create the installer:
echo 1. Install Inno Setup Compiler (https://jrsoftware.org/isdl.php)
echo 2. Open 'appnort_setup.iss'
echo 3. Click 'Compile'
pause
