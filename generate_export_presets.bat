@echo off
setlocal enabledelayedexpansion

set "BASE=%~dp0"
set "PROJECT=%1"

if "%PROJECT%"=="" (
    echo [ INFO ] No project specified. Exiting.
    exit /b 1
)

set "TEMPLATE_FILE=%BASE%\templates\export_presets.cfg"
set "DEST_FILE=%PROJECT%\export_presets.cfg"

if not exist "%TEMPLATE_FILE%" (
    echo [ INFO ] Template export_presets.cfg not found in %BASE%\templates
    exit /b 1
)

xcopy /Y "%TEMPLATE_FILE%" "%DEST_FILE%" 
echo [ INFO ] export_presets.cfg copied to %PROJECT%
