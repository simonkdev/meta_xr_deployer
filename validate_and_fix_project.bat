@echo off
setlocal enabledelayedexpansion

set "BASE=%~dp0"
set "PROJECT=%BASE%projects\%1"
set "PROJECT_ADDONS=%PROJECT%\addons"
set "SOURCE_ADDONS=%BASE%addons"

if not exist "%PROJECT%" (
    echo [ INFO ] Project "%1" not found
    exit /b 1
)

if not exist "%PROJECT_ADDONS%\openxr" (
    xcopy /E /I /Y "%SOURCE_ADDONS%\openxr" "%PROJECT_ADDONS%\openxr" >nul
    echo [ INFO ] OpenXR addon installed
) else (
    echo [ INFO ] OpenXR addon already present
)

if not exist "%PROJECT_ADDONS%\godot-xr-tools" (
    xcopy /E /I /Y "%SOURCE_ADDONS%\godot-xr-tools" "%PROJECT_ADDONS%\godot-xr-tools" >nul
    echo [ INFO ] Godot XR Tools addon installed
) else (
    echo [ INFO ] Godot XR Tools addon already present
)

if not exist "%PROJECT%\icon.png" (
    copy "%BASE%assets\icon.png" "%PROJECT%\icon.png" >nul
    echo [ INFO ] Default icon added
) else (
    echo [ INFO ] Icon already present
)

call "%BASE%generate_export_presets.bat" "%PROJECT%"

if exist "%BASE%projects\temp_project\export_presets.cfg" (
    move /Y "%BASE%projects\temp_project\export_presets.cfg" "%PROJECT%\export_presets.cfg" >nul
    echo [ INFO ] export_presets.cfg moved to project
)

echo [ INFO ] Project validation complete
