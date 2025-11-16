# PowerShell Script: Register Devices in Azure IoT Hub
# Registers IoT devices with X.509 authentication

param(
    [string]$IoTHubName = "",
    [string]$DeviceDir = "certs\devices"
)

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Azure IoT Device Registration" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Get IoT Hub name from .env if not provided
if ($IoTHubName -eq "") {
    $envPath = Join-Path $PSScriptRoot ".." ".env"
    if (Test-Path $envPath) {
        $envContent = Get-Content $envPath
        $hubLine = $envContent | Where-Object { $_ -match '^IOTHUB_NAME=' }
        if ($hubLine) {
            $IoTHubName = ($hubLine -split '=')[1].Trim()
        }
    }
}

if ($IoTHubName -eq "") {
    Write-Host "❌ IoT Hub name not found" -ForegroundColor Red
    Write-Host "Specify with: -IoTHubName <name>" -ForegroundColor Yellow
    exit 1
}

Write-Host "🏢 IoT Hub: $IoTHubName" -ForegroundColor Cyan
Write-Host ""

# Check Azure CLI
try {
    $null = az --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Azure CLI not found"
    }
} catch {
    Write-Host "❌ Azure CLI not installed" -ForegroundColor Red
    exit 1
}

# Check IoT extension
Write-Host "🔍 Checking Azure IoT extension..." -ForegroundColor Yellow
$extensions = az extension list --query "[?name=='azure-iot'].name" -o tsv 2>$null
if (-not $extensions) {
    Write-Host "📦 Installing azure-iot extension..." -ForegroundColor Yellow
    az extension add --name azure-iot
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install extension" -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ Azure IoT extension ready" -ForegroundColor Green

# Find all device directories
$deviceBaseDir = Join-Path $PSScriptRoot ".." $DeviceDir
if (-not (Test-Path $deviceBaseDir)) {
    Write-Host "❌ Device certificates directory not found: $deviceBaseDir" -ForegroundColor Red
    Write-Host "Run generate_device_certs.ps1 first" -ForegroundColor Yellow
    exit 1
}

$deviceDirs = Get-ChildItem $deviceBaseDir -Directory

if ($deviceDirs.Count -eq 0) {
    Write-Host "❌ No device certificates found" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📱 Found $($deviceDirs.Count) device(s)" -ForegroundColor Cyan
Write-Host ""

# Register each device
$successCount = 0
$failCount = 0

foreach ($dir in $deviceDirs) {
    $deviceId = $dir.Name
    
    Write-Host "🔧 Registering device: $deviceId" -ForegroundColor Yellow
    
    # Check if device already exists
    $existing = az iot hub device-identity show `
        --hub-name $IoTHubName `
        --device-id $deviceId 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ⚠️  Device already registered, skipping..." -ForegroundColor Yellow
        $successCount++
        continue
    }
    
    # Register device with X.509 CA authentication
    az iot hub device-identity create `
        --hub-name $IoTHubName `
        --device-id $deviceId `
        --auth-method x509_ca 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Device registered successfully" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "  ❌ Failed to register device" -ForegroundColor Red
        $failCount++
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  Registration Complete" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Results:" -ForegroundColor Cyan
Write-Host "  ✅ Successful: $successCount" -ForegroundColor Green
if ($failCount -gt 0) {
    Write-Host "  ❌ Failed: $failCount" -ForegroundColor Red
}
Write-Host ""

# List all devices
Write-Host "📋 Registered Devices:" -ForegroundColor Cyan
az iot hub device-identity list --hub-name $IoTHubName -o table

Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Update .env file with device IDs" -ForegroundColor White
Write-Host "  2. Run: python device_simulator.py" -ForegroundColor White
Write-Host "  3. Monitor: az iot hub monitor-events --hub-name $IoTHubName" -ForegroundColor White
Write-Host ""
