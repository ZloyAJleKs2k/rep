@echo off
cls

:: --- ПРОВЕРКА ПРАВ АДМИНИСТРАТОРА ---
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ?? Требуются права администратора...
    echo Запуск от имени администратора...
    echo.
    powershell -Command "Start-Process cmd -ArgumentList '/c %~f0' -Verb RunAs"
    exit /b
)

:: --- УСТАНОВКА ПУТИ К СКРИПТУ И СОХРАНЕНИЯ ---
set "SCRIPT_DIR=%~dp0"
set "DOWNLOAD_PATH=%SCRIPT_DIR%Скачанные_серии"
mkdir "%DOWNLOAD_PATH%" 2>nul

:: --- ВСТРОЕННЫЙ PowerShell-скрипт (в виде строки) ---
set "PS_SCRIPT="
set "PS_SCRIPT=%PS_SCRIPT%$downloadPath = '%DOWNLOAD_PATH%'; $total = 24;"
set "PS_SCRIPT=%PS_SCRIPT%$ProgressPreference = 'SilentlyContinue';"  :: Отключает прогресс-бар и его запросы
set "PS_SCRIPT=%PS_SCRIPT%$seriesList = @("
set "PS_SCRIPT=%PS_SCRIPT%[PSCustomObject]@{ Url = 'https://jointinum.cloud.solodcdn.com/useruploads/a36475db-2974-4416-a242-ea3e98d3582b/5ef7a24da98896132a41e56b0e22fd82:2026042301/480.mp4'; Filename = '17 серия.mp4' },"
set "PS_SCRIPT=%PS_SCRIPT%[PSCustomObject]@{ Url = 'https://aurum.cloud.solodcdn.com/useruploads/3343f5e2-89aa-435d-bd47-4e61841d9993/75a7a003cad1cae8486881343e19917d:2026042301/480.mp4'; Filename = '19 серия.mp4' },"
set "PS_SCRIPT=%PS_SCRIPT%[PSCustomObject]@{ Url = 'https://secret.cloud.solodcdn.com/useruploads/8257f0b7-fadf-4afc-906f-9e32eae7fdf5/5d86b45502185e16de82e587b2d0b040:2026042301/480.mp4'; Filename = '21 серия.mp4' },"
set "PS_SCRIPT=%PS_SCRIPT%[PSCustomObject]@{ Url = 'https://plumbum.cloud.solodcdn.com/useruploads/dd21aca1-8d3b-48df-9314-55a3fff647d9/f94ce219b887f23fac0b5f7809d14a35:2026042301/480.mp4'; Filename = '22 серия.mp4' },"
set "PS_SCRIPT=%PS_SCRIPT%[PSCustomObject]@{ Url = 'https://glory.cloud.solodcdn.com/useruploads/8df9d4e0-6ea6-4097-a378-fb77b60685ee/4de74b48dcaff4899acca3397b9d45a6:2026042301/480.mp4'; Filename = '23 серия.mp4' },"
set "PS_SCRIPT=%PS_SCRIPT%[PSCustomObject]@{ Url = 'https://fractal.cloud.solodcdn.com/useruploads/c506e379-9e58-41ec-b825-a8e280aa8612/120d04242071ea6de5dc2566f0ba8a64:2026042301/480.mp4'; Filename = '24 серия.mp4' }"
set "PS_SCRIPT=%PS_SCRIPT%);"
set "PS_SCRIPT=%PS_SCRIPT%Write-Host '?? Скачивание 1 сезона ?Я в тебе не сомневаюсь? (OVA: Blackbird Sound, 480p)' -ForegroundColor Cyan;"
set "PS_SCRIPT=%PS_SCRIPT%Write-Host '?? Сохранение в: %DOWNLOAD_PATH%' -ForegroundColor Yellow;"
set "PS_SCRIPT=%PS_SCRIPT%$i = 0;"
set "PS_SCRIPT=%PS_SCRIPT%foreach ($series in $seriesList) {"
set "PS_SCRIPT=%PS_SCRIPT%    $i++;"
set "PS_SCRIPT=%PS_SCRIPT%    $url = $series.Url;"
set "PS_SCRIPT=%PS_SCRIPT%    $filename = $series.Filename;"
set "PS_SCRIPT=%PS_SCRIPT%    $filepath = Join-Path $downloadPath $filename;"
set "PS_SCRIPT=%PS_SCRIPT%    Write-Host ('?? Скачано: {0} из {1}...' -f $i, $total) -ForegroundColor Yellow -NoNewLine;"
set "PS_SCRIPT=%PS_SCRIPT%    try {"
set "PS_SCRIPT=%PS_SCRIPT%        Invoke-WebRequest -Uri $url -OutFile $filepath -TimeoutSec 60 -UseBasicParsing -ErrorAction Stop;"
set "PS_SCRIPT=%PS_SCRIPT%        Write-Host ' ?' -ForegroundColor Green;"
set "PS_SCRIPT=%PS_SCRIPT%    } catch {"
set "PS_SCRIPT=%PS_SCRIPT%        Write-Host ' ?' -ForegroundColor Red;"
set "PS_SCRIPT=%PS_SCRIPT%        Write-Host ('   Ошибка: $($_.Exception.Message)' -replace '.*?: ', '') -ForegroundColor DarkRed;"
set "PS_SCRIPT=%PS_SCRIPT%    }"
set "PS_SCRIPT=%PS_SCRIPT%};"
set "PS_SCRIPT=%PS_SCRIPT%Write-Host '`n?? Все 24 серии успешно скачаны!' -ForegroundColor Green;"
set "PS_SCRIPT=%PS_SCRIPT%Write-Host '?? Озвучка: Blackbird Sound | Качество: 480p' -ForegroundColor Magenta;"

:: --- ЗАПУСК PowerShell С ПЕРЕДАЧЕЙ СКРИПТА КАК СТРОКИ ---
powershell -ExecutionPolicy Bypass -Command "& { %PS_SCRIPT% }"

:: --- Не ставим pause ? скрипт завершается автоматически после загрузки ---