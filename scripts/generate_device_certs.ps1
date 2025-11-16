# PowerShell Script: Generate Device Certificates
# Creates X.509 certificates for IoT devices signed by Root CA

param(
    [string]$DeviceId = "",
    [int]$DeviceCount = 0,
    [string]$RootCertDir = "certs\root",
    [string]$DeviceDir = "certs\devices",
    [int]$ValidityDays = 365
)

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Device Certificate Generator" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Validate parameters
if ($DeviceId -eq "" -and $DeviceCount -eq 0) {
    Write-Host "❌ Error: Specify either -DeviceId or -DeviceCount" -ForegroundColor Red
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host '  .\generate_device_certs.ps1 -DeviceId "thing_001"' -ForegroundColor White
    Write-Host "  .\generate_device_certs.ps1 -DeviceCount 3" -ForegroundColor White
    exit 1
}

# Check for OpenSSL
$opensslPath = $null
$locations = @(
    "C:\Program Files\OpenSSL-Win64\bin\openssl.exe",
    "C:\Program Files (x86)\OpenSSL-Win32\bin\openssl.exe",
    "openssl"
)

foreach ($loc in $locations) {
    if (Test-Path $loc -ErrorAction SilentlyContinue) {
        $opensslPath = $loc
        break
    } elseif ($loc -eq "openssl") {
        try {
            $null = & openssl version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $opensslPath = "openssl"
                break
            }
        } catch {}
    }
}

if (-not $opensslPath) {
    Write-Host "❌ OpenSSL not found! Install from: https://slproweb.com/products/Win32OpenSSL.html" -ForegroundColor Red
    exit 1
}

# Verify Root CA exists
$rootDir = Join-Path $PSScriptRoot ".." $RootCertDir
$rootKeyPath = Join-Path $rootDir "azure-iot-root.key.pem"
$rootCertPath = Join-Path $rootDir "azure-iot-root.cert.pem"

if (-not (Test-Path $rootKeyPath) -or -not (Test-Path $rootCertPath)) {
    Write-Host "❌ Root CA not found! Run generate_root_ca.ps1 first" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Root CA found" -ForegroundColor Green

# Create device directory
$deviceBaseDir = Join-Path $PSScriptRoot ".." $DeviceDir
if (-not (Test-Path $deviceBaseDir)) {
    New-Item -ItemType Directory -Path $deviceBaseDir -Force | Out-Null
}

# Function to generate certificate for a device
function Generate-DeviceCert {
    param([string]$DevId)
    
    Write-Host ""
    Write-Host "🔧 Generating certificate for: $DevId" -ForegroundColor Yellow
    
    # Create device directory
    $devDir = Join-Path $deviceBaseDir $DevId
    if (-not (Test-Path $devDir)) {
        New-Item -ItemType Directory -Path $devDir -Force | Out-Null
    }
    
    $devKeyPath = Join-Path $devDir "device-key.pem"
    $devCsrPath = Join-Path $devDir "device-csr.pem"
    $devCertPath = Join-Path $devDir "device-cert.pem"
    $devFullChainPath = Join-Path $devDir "device-full-chain.pem"
    $devConfigPath = Join-Path $devDir "openssl_device.cnf"
    
    # OpenSSL config for device
    $deviceConfig = @"
[ req ]
default_bits        = 2048
distinguished_name  = req_distinguished_name
string_mask         = utf8only
default_md          = sha256
req_extensions      = v3_req

[ req_distinguished_name ]
commonName          = $DevId

[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = $DevId
"@
    
    $deviceConfig | Set-Content $devConfigPath -Encoding UTF8
    
    # Generate device private key
    Write-Host "  🔐 Generating private key..." -ForegroundColor Gray
    & $opensslPath genrsa -out $devKeyPath 2048 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ Failed to generate key" -ForegroundColor Red
        return $false
    }
    
    # Generate CSR
    Write-Host "  📝 Creating certificate signing request..." -ForegroundColor Gray
    & $opensslPath req -new `
        -key $devKeyPath `
        -out $devCsrPath `
        -config $devConfigPath `
        -subj "/CN=$DevId" 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ Failed to generate CSR" -ForegroundColor Red
        return $false
    }
    
    # Sign with Root CA
    Write-Host "  ✍️  Signing with Root CA..." -ForegroundColor Gray
    & $opensslPath x509 -req `
        -in $devCsrPath `
        -CA $rootCertPath `
        -CAkey $rootKeyPath `
        -CAcreateserial `
        -out $devCertPath `
        -days $ValidityDays `
        -sha256 `
        -extensions v3_req `
        -extfile $devConfigPath 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ❌ Failed to sign certificate" -ForegroundColor Red
        return $false
    }
    
    # Create full chain (device cert + root cert)
    Write-Host "  🔗 Creating certificate chain..." -ForegroundColor Gray
    $deviceCertContent = Get-Content $devCertPath -Raw
    $rootCertContent = Get-Content $rootCertPath -Raw
    "$deviceCertContent`n$rootCertContent" | Set-Content $devFullChainPath -Encoding UTF8
    
    # Clean up CSR
    Remove-Item $devCsrPath -Force
    
    Write-Host "  ✅ Certificate generated for $DevId" -ForegroundColor Green
    Write-Host "     📁 $devDir" -ForegroundColor Gray
    
    return $true
}

# Generate certificates
if ($DeviceId -ne "") {
    # Single device
    $success = Generate-DeviceCert -DevId $DeviceId
    if (-not $success) { exit 1 }
} else {
    # Multiple devices
    Write-Host "Generating certificates for $DeviceCount devices..." -ForegroundColor Cyan
    for ($i = 1; $i -le $DeviceCount; $i++) {
        $devId = "thing_{0:D3}" -f $i
        $success = Generate-DeviceCert -DevId $devId
        if (-not $success) { exit 1 }
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✅ Device Certificates Generated!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Certificates location: $deviceBaseDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Next Step:" -ForegroundColor Cyan
Write-Host "  Run: .\scripts\register_devices.ps1" -ForegroundColor White
Write-Host ""
