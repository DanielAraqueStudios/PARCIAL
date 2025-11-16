# PowerShell Script: Setup Azure IoT Hub
# Creates IoT Hub, resource group, and configures basic settings

param(
    [string]$ResourceGroup = "rg-iot-parcial",
    [string]$Location = "eastus",
    [string]$IoTHubName = "iothub-parcial-2025",
    [string]$Sku = "F1"  # Free tier
)

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Azure IoT Hub Setup Script" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
Write-Host "🔍 Checking Azure CLI installation..." -ForegroundColor Yellow
try {
    $azVersion = az --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Azure CLI not found. Please install from: https://aka.ms/installazurecliwindows" -ForegroundColor Red
    exit 1
}

# Login to Azure
Write-Host ""
Write-Host "🔐 Logging in to Azure..." -ForegroundColor Yellow
az login --use-device-code

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Azure login failed" -ForegroundColor Red
    exit 1
}

# Show current subscription
Write-Host ""
Write-Host "📋 Current Azure Subscription:" -ForegroundColor Cyan
az account show --query "{Name:name, SubscriptionId:id}" -o table

# Create Resource Group
Write-Host ""
Write-Host "📦 Creating Resource Group: $ResourceGroup" -ForegroundColor Yellow
az group create --name $ResourceGroup --location $Location

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create resource group" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Resource group created" -ForegroundColor Green

# Create IoT Hub
Write-Host ""
Write-Host "🏗️  Creating IoT Hub: $IoTHubName (Sku: $Sku)" -ForegroundColor Yellow
Write-Host "⏳ This may take 2-3 minutes..." -ForegroundColor Yellow

az iot hub create `
    --resource-group $ResourceGroup `
    --name $IoTHubName `
    --sku $Sku `
    --location $Location `
    --partition-count 2

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create IoT Hub" -ForegroundColor Red
    Write-Host "💡 Note: Free tier (F1) allows only 1 IoT Hub per subscription" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ IoT Hub created successfully" -ForegroundColor Green

# Get IoT Hub details
Write-Host ""
Write-Host "📊 IoT Hub Details:" -ForegroundColor Cyan
az iot hub show --name $IoTHubName --resource-group $ResourceGroup --query "{Name:name, Location:location, State:state, Hostname:properties.hostName}" -o table

# Get connection string
Write-Host ""
Write-Host "🔑 Retrieving Connection String..." -ForegroundColor Yellow
$connectionString = az iot hub connection-string show --hub-name $IoTHubName --query connectionString -o tsv

if ($connectionString) {
    Write-Host "✅ Connection string retrieved" -ForegroundColor Green
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  IMPORTANT: Save this connection string!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "Connection String:" -ForegroundColor Yellow
    Write-Host $connectionString -ForegroundColor White
    Write-Host ""
    
    # Save to .env file
    $envPath = Join-Path $PSScriptRoot ".." ".env"
    $envContent = Get-Content "$envPath.example" -Raw
    $envContent = $envContent -replace 'IOTHUB_NAME=.*', "IOTHUB_NAME=$IoTHubName"
    $envContent = $envContent -replace 'IOTHUB_HOSTNAME=.*', "IOTHUB_HOSTNAME=$IoTHubName.azure-devices.net"
    $envContent = $envContent -replace 'IOTHUB_CONNECTION_STRING=.*', "IOTHUB_CONNECTION_STRING=$connectionString"
    $envContent | Set-Content $envPath
    
    Write-Host "💾 Connection string saved to .env file" -ForegroundColor Green
}

# Get endpoint information
Write-Host ""
Write-Host "🔗 MQTT Endpoint Information:" -ForegroundColor Cyan
Write-Host "  Hostname: $IoTHubName.azure-devices.net" -ForegroundColor White
Write-Host "  Port: 8883 (MQTT over TLS)" -ForegroundColor White
Write-Host "  Protocol: MQTTv3.1.1" -ForegroundColor White

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✅ Azure IoT Hub Setup Complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Run: .\scripts\generate_root_ca.ps1" -ForegroundColor White
Write-Host "  2. Run: .\scripts\generate_device_certs.ps1 -DeviceCount 3" -ForegroundColor White
Write-Host "  3. Run: .\scripts\register_devices.ps1" -ForegroundColor White
Write-Host ""
