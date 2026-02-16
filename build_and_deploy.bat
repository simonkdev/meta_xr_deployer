@echo on
setlocal enabledelayedexpansion
set "PROJECT=%~1"
set "BASE=%~dp0"
set "PROJECT_PATH=%BASE%projects\%PROJECT%"
set "GODOT=%BASE%godot-4.5.exe"
set "BUILD_PATH=%BASE%builds\%PROJECT%.apk"
set "TEMPLATES=%BASE%templates"
set "ADB=%BASE%build-tools\platform-tools\adb.exe"

echo [ INFO ] Setting up environment
call "%BASE%setup_environment.bat"
echo\ %ANDROID_SDK_ROOT%

echo [ INFO ] Validating and fixing project
call "%BASE%validate_and_fix_project.bat" "%PROJECT%"

echo [ INFO ] Building project
"%GODOT%" --headless --path "%PROJECT_PATH%" --export-debug "Quest3" "%BUILD_PATH%" --template-path "%TEMPLATES% --install-android-build-template"
echo [ INFO ] Build completed

echo [ INFO ] Setting up ADB
call "%BASE%setup_adb.bat"

echo [ INFO ] Deploying APK to Quest 3
"%ADB%" install -r "%BUILD_PATH%"
echo [ INFO ] Deployment completed
