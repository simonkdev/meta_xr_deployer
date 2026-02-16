@echo on
setlocal enabledelayedexpansion

set "BASE=%~dp0"
set "GODOT=%BASE%godot-4.5.exe"
set "TEMPLATES=%BASE%templates"
set "BUILD_TOOLS=%BASE%build-tools"
set "SDK=%BUILD_TOOLS%\android-sdk"
set "NDK=%BUILD_TOOLS%\android-ndk"
set "JDK=%BUILD_TOOLS%\jdk"
set "PLATFORM_TOOLS=%BUILD_TOOLS%\platform-tools"

if not exist "%TEMPLATES%" mkdir "%TEMPLATES%"
if not exist "%BUILD_TOOLS%" mkdir "%BUILD_TOOLS%"
if not exist "%BASE%projects" mkdir "%BASE%projects"
if not exist "%BASE%builds" mkdir "%BASE%builds"
echo [ INFO ] Directories ensured

set "MISSING=0"

if not exist "%GODOT%" (
    echo [ INFO ] Godot executable "%GODOT%" not found
    set MISSING=1
) else (
    echo [ INFO ] Godot executable found
)

if not exist "%TEMPLATES%" (
    echo [ INFO ] Export templates folder "%TEMPLATES%" not found
    set MISSING=1
) else (
    echo [ INFO ] Export templates folder found
)

if not exist "%SDK%" (
    echo [ INFO ] Android SDK folder "%SDK%" not found
    set MISSING=1
) else (
    echo [ INFO ] Android SDK folder found
)

if not exist "%NDK%" (
    echo [ INFO ] Android NDK folder "%NDK%" not found
    set MISSING=1
) else (
    echo [ INFO ] Android NDK folder found
)

if not exist "%JDK%" (
    echo [ INFO ] JDK folder "%JDK%" not found
    set MISSING=1
) else (
    echo [ INFO ] JDK folder found
)

if not exist "%PLATFORM_TOOLS%" (
    echo [ INFO ] Platform-tools folder "%PLATFORM_TOOLS%" not found
    set MISSING=1
) else (
    echo [ INFO ] Platform-tools folder found
)

::if %MISSING%==1 (
::    echo [ INFO ] One or more dependencies are missing. Please ensure all required files and folders exist.
::    exit /b 1
::)

:: Set environment variables for current session
:: set "ANDROID_SDK_ROOT=%SDK%"
set "ANDROID_NDK_ROOT=%NDK%"
set "JAVA_HOME=%JDK%"
set "PATH=%PATH%;%JDK%\bin;%PLATFORM_TOOLS%"
set "GODOT_EDITOR_SETTINGS=%BASE%editor_settings-4.5.tres"

:: Optionally, also set permanent environment variables if desired
:: setx ANDROID_SDK_ROOT "%SDK%"
:: setx ANDROID_NDK_ROOT "%NDK%"
:: setx JAVA_HOME "%JDK%"

echo [ INFO ] Environment variables set for current session
echo [ INFO ] ANDROID_SDK_ROOT=%ANDROID_SDK_ROOT%
echo [ INFO ] ANDROID_NDK_ROOT=%ANDROID_NDK_ROOT%
echo [ INFO ] JAVA_HOME=%JAVA_HOME%
echo [ INFO ] PATH updated
