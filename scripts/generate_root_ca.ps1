# PowerShell Script: Generate Root CA Certificate
# Creates a self-signed root CA for device certificate signing

param(
    [string]$OutputDir = "certs\root",
    [int]$ValidityDays = 3650  # 10 years
)

Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Root CA Certificate Generator" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check for OpenSSL
Write-Host "🔍 Checking for OpenSSL..." -ForegroundColor Yellow
$opensslPath = $null

# Try common locations
$locations = @(
    "C:\Program Files\OpenSSL-Win64\bin\openssl.exe",
    "C:\Program Files (x86)\OpenSSL-Win32\bin\openssl.exe",
    "C:\OpenSSL-Win64\bin\openssl.exe",
    "openssl.exe"  # In PATH
)

foreach ($loc in $locations) {
    if (Test-Path $loc -ErrorAction SilentlyContinue) {
        $opensslPath = $loc
        break
    } elseif ($loc -eq "openssl.exe") {
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
    Write-Host "❌ OpenSSL not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install OpenSSL from:" -ForegroundColor Yellow
    Write-Host "  https://slproweb.com/products/Win32OpenSSL.html" -ForegroundColor White
    Write-Host ""
    exit 1
}

Write-Host "✅ OpenSSL found: $opensslPath" -ForegroundColor Green

# Create output directory
$rootDir = Join-Path $PSScriptRoot ".." $OutputDir
if (-not (Test-Path $rootDir)) {
    New-Item -ItemType Directory -Path $rootDir -Force | Out-Null
    Write-Host "📁 Created directory: $rootDir" -ForegroundColor Green
}

# Certificate paths
$rootKeyPath = Join-Path $rootDir "azure-iot-root.key.pem"
$rootCertPath = Join-Path $rootDir "azure-iot-root.cert.pem"
$configPath = Join-Path $rootDir "openssl_root_ca.cnf"

# Create OpenSSL config
Write-Host ""
Write-Host "📝 Creating OpenSSL configuration..." -ForegroundColor Yellow

$opensslConfig = @"
[ req ]
default_bits        = 4096
distinguished_name  = req_distinguished_name
string_mask         = utf8only
default_md          = sha256
x509_extensions     = v3_ca

[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
countryName_default             = CO
stateOrProvinceName             = State or Province Name
stateOrProvinceName_default     = Bogota
localityName                    = Locality Name
localityName_default            = Bogota
organizationName                = Organization Name
organizationName_default        = Universidad Militar Nueva Granada
organizationalUnitName          = Organizational Unit Name
organizationalUnitName_default  = Mecatronica IoT Lab
commonName                      = Common Name
commonName_default              = Azure IoT Root CA
emailAddress                    = Email Address
emailAddress_default            = iot@unimilitar.edu.co

[ v3_ca ]
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign
"@

$opensslConfig | Set-Content $configPath -Encoding UTF8
Write-Host "✅ Configuration created" -ForegroundColor Green

# Generate Root CA private key
Write-Host ""
Write-Host "🔐 Generating Root CA private key (4096-bit RSA)..." -ForegroundColor Yellow
& $opensslPath genrsa -out $rootKeyPath 4096 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to generate private key" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Private key generated: $rootKeyPath" -ForegroundColor Green

# Generate Root CA certificate
Write-Host ""
Write-Host "📜 Generating Root CA certificate..." -ForegroundColor Yellow
& $opensslPath req -new -x509 `
    -key $rootKeyPath `
    -out $rootCertPath `
    -days $ValidityDays `
    -config $configPath `
    -subj "/C=CO/ST=Bogota/L=Bogota/O=Universidad Militar Nueva Granada/OU=Mecatronica IoT Lab/CN=Azure IoT Root CA/emailAddress=iot@unimilitar.edu.co" 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to generate certificate" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Root CA certificate generated: $rootCertPath" -ForegroundColor Green

# Display certificate info
Write-Host ""
Write-Host "📋 Certificate Information:" -ForegroundColor Cyan
& $opensslPath x509 -in $rootCertPath -noout -subject -issuer -dates

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  ✅ Root CA Generation Complete!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Files created:" -ForegroundColor Cyan
Write-Host "  Private Key: $rootKeyPath" -ForegroundColor White
Write-Host "  Certificate: $rootCertPath" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  IMPORTANT: Keep the private key secure!" -ForegroundColor Yellow
Write-Host "   Never commit it to version control" -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 Next Step:" -ForegroundColor Cyan
Write-Host "  Upload $rootCertPath to Azure IoT Hub" -ForegroundColor White
Write-Host "  Portal → IoT Hub → Certificates → Add" -ForegroundColor White
Write-Host ""
