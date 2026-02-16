@echo off
setlocal enabledelayedexpansion

set "BASE=%~dp0"
set "ADB=%BASE%build-tools\platform-tools\adb.exe"

if not exist "%ADB%" (
    echo [ INFO ] ADB not found at "%ADB%"
    exit /b 1
)

"%ADB%" start-server

for /f "skip=1 tokens=1,2" %%A in ('"%ADB% devices"') do (
    if "%%B"=="device" (
        set "DEVICE_FOUND=1"
        set "DEVICE_ID=%%A"
    )
)

if defined DEVICE_FOUND (
    echo [ INFO ] Meta Quest 3 detected: %DEVICE_ID%
) else (
    echo [ INFO ] No devices detected. Please connect your Quest 3 via USB and enable developer mode.
    exit /b 1
)
