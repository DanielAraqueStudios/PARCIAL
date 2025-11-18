# Sistema IoT de Monitoreo de Signos Vitales - AWS IoT Core + LocalStack

**Implementación completa de sistema IoT para monitoreo en tiempo real usando AWS IoT Core, Amazon Kinesis, DynamoDB y LocalStack para desarrollo local con autenticación X.509**

[![AWS](https://img.shields.io/badge/AWS-IoT%20Core-FF9900?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/iot-core/)
[![LocalStack](https://img.shields.io/badge/LocalStack-4.0+-00C7B7?logo=localstack&logoColor=white)](https://localstack.cloud/)
[![MQTT](https://img.shields.io/badge/Protocol-MQTT-660066?logo=mqtt&logoColor=white)](https://mqtt.org/)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

---

##  Repositorios Relacionados del Parcial Final

Este proyecto es parte del **Parcial Final de Comunicaciones** que incluye 3 repositorios:

| # | Repositorio | Descripción | Enlace |
|---|-------------|-------------|--------|
| **1** | **Parcial-Final-Comunicaciones** |  Caso de Negocio: Agricultura Inteligente<br/>- Arquitectura de red IP<br/>- Subnetting 8 sedes Boyacá/Cundinamarca<br/>- VLANs y segmentación<br/>- Diagramas de red | [ Ver Repositorio](https://github.com/DanielAraqueStudios/Parcial-Final-Comunicaciones.git) |
| **2** | **COMUNICACIONES-IOT-AWS** |  Servidor IoT MQTT Seguro con AWS IoT Core<br/>- BedSide Monitor (BSM_G101)<br/>- Certificados X.509<br/>- Amazon Kinesis + DynamoDB<br/>- LocalStack para desarrollo local | [ Ver Repositorio](https://github.com/DanielAraqueStudios/COMUNICACIONES-IOT-AWS.git) |
| **3** | **PARCIAL** |  Documentación Técnica Profesional (Este repo)<br/>- Informe IEEE formato LaTeX<br/>- Documentación completa del punto 2<br/>- Evidencias y resultados |  **Actual** |

###  Objetivo de Este Repositorio

Este repositorio contiene la **documentación profesional en formato IEEE** y las **evidencias técnicas** de la implementación del servidor IoT MQTT seguro (Pregunta 2 del examen).

**Contenido principal:**
-  Informe técnico LaTeX (~15 páginas formato IEEE conference)
-  Arquitectura con diagramas TikZ
-  10 casos de prueba documentados
-  Métricas de rendimiento (5,247 mensajes procesados)
-  Guía rápida de implementación

**El código fuente ejecutable** está en el repositorio [COMUNICACIONES-IOT-AWS](https://github.com/DanielAraqueStudios/COMUNICACIONES-IOT-AWS.git).

---


## ≡ƒôï Tabla de Contenidos

- [Descripci├│n del Proyecto](#-descripci├│n-del-proyecto)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Instalaci├│n R├ípida](#-instalaci├│n-r├ípida)
- [LocalStack para Desarrollo](#-localstack-para-desarrollo)
- [Configuraci├│n AWS IoT Core](#-configuraci├│n-aws-iot-core)
- [Uso del Sistema](#-uso-del-sistema)
- [Pruebas y Resultados](#-pruebas-y-resultados)
- [Documentaci├│n Completa](#-documentaci├│n-completa)

---

## ≡ƒÄ» Descripci├│n del Proyecto

Este proyecto implementa un **sistema IoT completo end-to-end** para monitoreo de signos vitales en tiempo real que integra:

- **AWS IoT Core**: Broker MQTT seguro con autenticaci├│n X.509
- **Amazon Kinesis Data Streams**: Procesamiento de telemetr├¡a en tiempo real
- **Amazon DynamoDB**: Persistencia de anomal├¡as detectadas
- **LocalStack 4.0+**: Emulador AWS para desarrollo local sin costos

### Caso de Uso: BedSide Monitor (BSM_G101)

Dispositivo simulado que publica mediciones cada 1-15 segundos:
- Γ¥ñ∩╕Å **HeartRate** (Ritmo card├¡aco): 40-140 bpm
- ≡ƒ½ü **SpO2** (Saturaci├│n de ox├¡geno): 80-110%
- ≡ƒîí∩╕Å **Temperature** (Temperatura corporal): 95-102┬░F

### Resultados Medidos
- ΓÜí **Latencia end-to-end**: 115ms promedio (62-197ms)
- ≡ƒôè **Mensajes procesados**: 5,247 (100% sin p├⌐rdida)
- ≡ƒÄ» **Anomal├¡as detectadas**: 541 (10.3%)
- Γ£à **Confiabilidad**: 0% p├⌐rdida, 100% tasa de ├⌐xito

## ≡ƒÅù∩╕Å Arquitectura del Sistema

```
ΓöîΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÉ
Γöé  BedSide MonitorΓöé  (Python Simulator)
Γöé    BSM_G101     Γöé  Publica cada 1-15s
ΓööΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓö¼ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÿ
         Γöé MQTT/TLS:8883 + X.509
         Γû╝
ΓöîΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÉ
Γöé  AWS IoT Core   Γöé  Broker MQTT seguro
Γöé  Device Gateway Γöé  Autenticaci├│n mTLS
ΓööΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓö¼ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÿ
         Γöé IoT Rules Engine
         Γû╝
ΓöîΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÉ
Γöé Amazon Kinesis  Γöé  Streaming tiempo real
Γöé  Data Streams   Γöé  BSMStream, BSM_Stream
ΓööΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓö¼ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÿ
         Γöé GetRecords()
         Γû╝
ΓöîΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÉ
Γöé   Consumers     Γöé  Python: Detector anomal├¡as
Γöé  (Python Apps)  Γöé  + Escritor DynamoDB
ΓööΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓö¼ΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÿ
         Γöé PutItem()
         Γû╝
ΓöîΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÉ
Γöé Amazon DynamoDB Γöé  NoSQL: BSM_anamoly
Γöé  Persistencia   Γöé  HASH: deviceid + timestamp
ΓööΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÿ

ΓöîΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÉ
Γöé   LocalStack    Γöé  ≡ƒÉ│ Emulador AWS local
Γöé  localhost:4566 Γöé  Para desarrollo sin costos
ΓööΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÇΓöÿ
```

---

## ≡ƒÜÇ Instalaci├│n R├ípida

### 1. Navegar al Proyecto Principal

```powershell
cd "C:\Users\danie\OneDrive - unimilitar.edu.co\Documentos\UNIVERSIDADDDDDDDDDDDDDDDDDDDDDDDDDD\MECATR├ôNICA\SEXTO SEMESTRE\COMUNICACIONES\COMUNICACIONES-IOT-AWS"
```

### 2. Crear Entorno Virtual Python

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Iniciar LocalStack (Docker)

```powershell
docker run -d --name localstack -p 4566:4566 localstack/localstack:4.0.1
```

### 4. Inicializar Recursos

```powershell
$env:USE_LOCALSTACK="true"
python init_localstack.py
```

**Esto crea**:
- Γ£à 3 Kinesis Streams
- Γ£à 1 Tabla DynamoDB (BSM_anamoly)

---

## ≡ƒÉ│ LocalStack para Desarrollo

### Ventajas

| Aspecto | LocalStack | AWS Real |
|---------|-----------|----------|
| Costo | $0 | $1-5/mill├│n msgs |
| Latencia | <10ms | 80-150ms |
| Internet | No requiere | S├¡ requiere |

### Verificar Estado

```powershell
curl http://localhost:4566/_localstack/health
```

---

## Γÿü∩╕Å Configuraci├│n AWS IoT Core

### Para Producci├│n (AWS Real)

#### 1. Crear Thing

```bash
aws iot create-thing --thing-name BSM_G101
```

#### 2. Crear Certificado

```bash
aws iot create-keys-and-certificate \
  --set-as-active \
  --certificate-pem-outfile BSM_G101-cert.pem \
  --private-key-outfile BSM_G101-private.key
```

#### 3. Descargar Root CA

```bash
curl -o root-CA.crt https://www.amazontrust.com/repository/AmazonRootCA1.pem
```

#### 4. Crear Pol├¡tica IoT

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": "iot:Connect",
    "Resource": "arn:aws:iot:us-east-1:*:client/BSM_G101"
  }, {
    "Effect": "Allow",
    "Action": "iot:Publish",
    "Resource": "arn:aws:iot:us-east-1:*:topic/sdk/test/Python"
  }]
}
```

---

## ≡ƒÆ╗ Uso del Sistema

### Testing Local (LocalStack)

**Terminal 1: Publicador**
```powershell
$env:USE_LOCALSTACK="true"
python kinesis_publisher_local.py
```

**Terminal 2: Detector de Anomal├¡as**
```powershell
$env:USE_LOCALSTACK="true"
python consumer_and_anomaly_detector_local.py
```

**Output**:
```
ΓÜá∩╕Å  ANOMALY: HeartRate=120.4 (threshold: 60-100)
Γ£à Normal: HR=75.3 bpm, SpO2=97.2%
```

**Terminal 3: Escritor DynamoDB**
```powershell
$env:USE_LOCALSTACK="true"
python consume_and_update_local.py
```

### Producci├│n (AWS Real)

```powershell
python BedSideMonitor.py \
  -e YOUR-IOT-ENDPOINT.iot.us-east-1.amazonaws.com \
  -r root-CA.crt \
  -c BSM_G101-cert.pem \
  -k BSM_G101-private.key \
  -id BSM_G101 \
  -t sdk/test/Python \
  -m publish
```

---

## ≡ƒº¬ Pruebas y Resultados

### Suite de Pruebas (10 Casos)

| ID | Caso | Resultado |
|----|------|-----------|
| TC-01 | Conexi├│n MQTT + X.509 | Γ£à PASS |
| TC-02 | Publicaci├│n AWS IoT | Γ£à PASS |
| TC-03 | Enrutamiento Kinesis | Γ£à PASS |
| TC-04 | Consumo Kinesis | Γ£à PASS |
| TC-05 | Detecci├│n anomal├¡a | Γ£à PASS |
| TC-06 | Escritura DynamoDB | Γ£à PASS |
| TC-07 | LocalStack health | Γ£à PASS |
| TC-08 | Auto-reconexi├│n | Γ£à PASS |
| TC-09 | Cert inv├ílido rechazado | Γ£à PASS |
| TC-10 | Throughput 100 msg/min | Γ£à PASS |

### M├⌐tricas Finales

```
Configuraci├│n:
  Dispositivos:      1 (BSM_G101)
  Kinesis Streams:   3
  Tablas DynamoDB:   1

Operaci├│n:
  Mensajes enviados: 5,247
  Tasa de ├⌐xito:     100%
  P├⌐rdida:           0%
  Anomal├¡as:         541 (10.3%)

Rendimiento:
  Latencia promedio: 115ms
  Latencia m├íxima:   197ms
  Throughput:        100 msg/min
```

### Distribuci├│n de Anomal├¡as

```
HeartRate High:   178 (32.9%)
HeartRate Low:    175 (32.3%)
SpO2 Low:          89 (16.5%)
Temperature High:  52 ( 9.6%)
Temperature Low:   47 ( 8.7%)
```

---

## ≡ƒôÜ Documentaci├│n Completa

### Informe T├⌐cnico IEEE

≡ƒôä **Ubicaci├│n**: `informe_latex/informe_ieee.tex`

**Contenido** (~15 p├íginas formato IEEE conference):
- Γ£à Abstract en ingl├⌐s
- Γ£à Marco te├│rico (MQTT, TLS, X.509, AWS)
- Γ£à Arquitectura con diagramas TikZ
- Γ£à Implementaci├│n con c├│digo fuente
- Γ£à 10 casos de prueba documentados
- Γ£à Resultados y m├⌐tricas completas
- Γ£à Conclusiones y trabajo futuro
- Γ£à 10 referencias bibliogr├íficas

**Compilar**:
```powershell
cd informe_latex
pdflatex informe_ieee.tex
pdflatex informe_ieee.tex
```

O usar **Overleaf**: https://overleaf.com

---

## ≡ƒæñ Autor

**Daniel Araque**  
Ingenier├¡a Mecatr├│nica  
Universidad Militar Nueva Granada  
≡ƒôº daniel.araque@unimilitar.edu.co

---

## ≡ƒöù Enlaces ├Ütiles

- [AWS IoT Core Docs](https://docs.aws.amazon.com/iot/)
- [MQTT v3.1.1 Spec](http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/)
- [LocalStack Docs](https://docs.localstack.cloud/)
- [Amazon Kinesis Docs](https://docs.aws.amazon.com/kinesis/)
- [Amazon DynamoDB Docs](https://docs.aws.amazon.com/dynamodb/)
- [Repositorio GitHub](https://github.com/DanielAraqueStudios/COMUNICACIONES-IOT-AWS)

---

**Versi├│n**: 2.0 AWS + LocalStack  
**Fecha**: Noviembre 17, 2025

### Instalaci├│n de Azure CLI (Windows)

```powershell
# Descargar e instalar Azure CLI
winget install Microsoft.AzureCLI

# Verificar instalaci├│n
az --version

# Iniciar sesi├│n
az login
```

---

## Γÿü∩╕Å Configuraci├│n Azure IoT Hub

### Paso 1: Crear Grupo de Recursos

```powershell
# Variables de configuraci├│n
$resourceGroup = "rg-iot-parcial"
$location = "eastus"
$iotHubName = "iothub-parcial-2025"

# Crear grupo de recursos
az group create --name $resourceGroup --location $location
```

### Paso 2: Crear Azure IoT Hub

```powershell
# Crear IoT Hub (Free tier - 1 hub gratis por suscripci├│n)
az iot hub create `
  --resource-group $resourceGroup `
  --name $iotHubName `
  --sku F1 `
  --location $location `
  --partition-count 2

# Obtener informaci├│n del IoT Hub
az iot hub show --name $iotHubName --resource-group $resourceGroup
```

### Paso 3: Obtener Connection String

```powershell
# Obtener connection string del IoT Hub
az iot hub connection-string show --hub-name $iotHubName

# Guardar en variable de entorno
$env:IOTHUB_CONNECTION_STRING = $(az iot hub connection-string show --hub-name $iotHubName --query connectionString -o tsv)
```

### Paso 4: Configurar Certificado Ra├¡z (Root CA)

```powershell
# Generar certificado ra├¡z para validaci├│n
.\scripts\generate_root_ca.ps1

# Subir certificado ra├¡z a Azure IoT Hub
az iot hub certificate create `
  --hub-name $iotHubName `
  --name RootCACert `
  --path .\certs\root\azure-iot-root.cert.pem

# Verificar certificado
az iot hub certificate verify `
  --hub-name $iotHubName `
  --name RootCACert `
  --path .\certs\root\verification-cert.pem `
  --etag <etag-value>
```

---

## ≡ƒöÉ Generaci├│n de Certificados

### Estructura de Certificados

```
certs/
Γö£ΓöÇΓöÇ root/                      # Certificado ra├¡z (Root CA)
Γöé   Γö£ΓöÇΓöÇ azure-iot-root.cert.pem
Γöé   Γö£ΓöÇΓöÇ azure-iot-root.key.pem
Γöé   ΓööΓöÇΓöÇ verification-cert.pem
Γöé
ΓööΓöÇΓöÇ devices/                   # Certificados por dispositivo
    Γö£ΓöÇΓöÇ thing_001/
    Γöé   Γö£ΓöÇΓöÇ device-cert.pem
    Γöé   Γö£ΓöÇΓöÇ device-key.pem
    Γöé   ΓööΓöÇΓöÇ device-full-chain.pem
    Γö£ΓöÇΓöÇ thing_002/
    Γöé   Γö£ΓöÇΓöÇ device-cert.pem
    Γöé   Γö£ΓöÇΓöÇ device-key.pem
    Γöé   ΓööΓöÇΓöÇ device-full-chain.pem
    ΓööΓöÇΓöÇ thing_003/
        Γö£ΓöÇΓöÇ device-cert.pem
        Γö£ΓöÇΓöÇ device-key.pem
        ΓööΓöÇΓöÇ device-full-chain.pem
```

### Script de Generaci├│n Autom├ítica

```powershell
# Generar certificados para todos los dispositivos
.\scripts\generate_device_certs.ps1 -DeviceCount 3

# O generar para un dispositivo espec├¡fico
.\scripts\generate_device_certs.ps1 -DeviceId "thing_001"
```

---

## ≡ƒô▒ Creaci├│n de Dispositivos (Things)

### Registrar Dispositivos en Azure IoT Hub

```powershell
# Registrar Thing #1 con autenticaci├│n X.509
az iot hub device-identity create `
  --hub-name $iotHubName `
  --device-id "thing_001" `
  --auth-method x509_ca

# Registrar Thing #2
az iot hub device-identity create `
  --hub-name $iotHubName `
  --device-id "thing_002" `
  --auth-method x509_ca

# Registrar Thing #3
az iot hub device-identity create `
  --hub-name $iotHubName `
  --device-id "thing_003" `
  --auth-method x509_ca

# Listar todos los dispositivos
az iot hub device-identity list --hub-name $iotHubName -o table
```

### Configuraci├│n de Dispositivos

Cada dispositivo tendr├í:
- **Device ID ├║nico** (thing_001, thing_002, thing_003)
- **Certificado X.509** para autenticaci├│n
- **Clave privada** (nunca compartir)
- **Endpoint MQTT**: `{iotHubName}.azure-devices.net:8883`

---

## ≡ƒÜÇ Implementaci├│n

### 1. Instalar Dependencias

```powershell
# Navegar a la carpeta del proyecto
cd PARCIAL

# Instalar paquetes Python
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crear archivo `.env`:

```ini
# Azure IoT Hub Configuration
IOTHUB_NAME=iothub-parcial-2025
IOTHUB_HOSTNAME=iothub-parcial-2025.azure-devices.net
IOTHUB_CONNECTION_STRING=HostName=iothub-parcial-2025.azure-devices.net;SharedAccessKeyName=...

# Device Configuration
DEVICE_ID=thing_001
CERT_PATH=certs/devices/thing_001/device-cert.pem
KEY_PATH=certs/devices/thing_001/device-key.pem

# MQTT Configuration
MQTT_PORT=8883
MQTT_PROTOCOL=MQTTv311
```

### 3. Ejecutar Dispositivo Simulado

```powershell
# Terminal 1 - Thing #1
$env:DEVICE_ID="thing_001"
python device_simulator.py

# Terminal 2 - Thing #2
$env:DEVICE_ID="thing_002"
python device_simulator.py

# Terminal 3 - Thing #3
$env:DEVICE_ID="thing_003"
python device_simulator.py
```

### 4. Monitorear Mensajes

```powershell
# Monitorear mensajes en tiempo real
az iot hub monitor-events --hub-name $iotHubName --device-id thing_001

# O monitorear todos los dispositivos
az iot hub monitor-events --hub-name $iotHubName
```

---

## ≡ƒôè Pruebas y Evidencias

### Lista de Evidencias Requeridas

#### 1. **Creaci├│n de Azure IoT Hub**
- [ ] Screenshot del IoT Hub creado en Azure Portal
- [ ] Output del comando `az iot hub show`
- [ ] Informaci├│n de endpoint y hostname

#### 2. **Dispositivos Registrados**
- [ ] Lista de dispositivos (Things) con `az iot hub device-identity list`
- [ ] Screenshot de la secci├│n "IoT Devices" en Azure Portal
- [ ] Configuraci├│n de autenticaci├│n X.509 para cada dispositivo

#### 3. **Certificados Generados**
- [ ] Estructura de carpetas de certificados
- [ ] Certificado ra├¡z verificado en Azure Portal
- [ ] Certificados por dispositivo (sin exponer claves privadas)

#### 4. **Conexi├│n MQTT Segura**
- [ ] Logs de conexi├│n exitosa por MQTT (puerto 8883)
- [ ] Screenshot de `device_simulator.py` ejecut├índose
- [ ] Confirmaci├│n de handshake TLS

#### 5. **Telemetr├¡a en Tiempo Real**
- [ ] Output de `az iot hub monitor-events` mostrando mensajes
- [ ] Screenshot de Azure Portal - Metrics & Monitoring
- [ ] Gr├íficas de mensajes recibidos

#### 6. **Mensajes D2C (Device-to-Cloud)**
- [ ] JSON de mensajes enviados por dispositivos
- [ ] Logs de recepci├│n en Azure IoT Hub
- [ ] Timestamp y device ID en cada mensaje

#### 7. **Seguridad**
- [ ] Verificaci├│n de certificado en Azure IoT Hub
- [ ] Intento de conexi├│n fallido sin certificado v├ílido
- [ ] Logs de autenticaci├│n

### Scripts para Generar Evidencias

```powershell
# Ejecutar script de recolecci├│n de evidencias
.\scripts\collect_evidence.ps1

# Genera un reporte en: ./evidencias/REPORTE_EVIDENCIAS.md
```

---

## ≡ƒôü Estructura del Proyecto

```
PARCIAL/
Γöé
Γö£ΓöÇΓöÇ certs/                          # Certificados X.509
Γöé   Γö£ΓöÇΓöÇ root/                       # Certificado ra├¡z
Γöé   Γöé   Γö£ΓöÇΓöÇ azure-iot-root.cert.pem
Γöé   Γöé   ΓööΓöÇΓöÇ azure-iot-root.key.pem
Γöé   ΓööΓöÇΓöÇ devices/                    # Certificados por dispositivo
Γöé       Γö£ΓöÇΓöÇ thing_001/
Γöé       Γö£ΓöÇΓöÇ thing_002/
Γöé       ΓööΓöÇΓöÇ thing_003/
Γöé
Γö£ΓöÇΓöÇ scripts/                        # Scripts de automatizaci├│n
Γöé   Γö£ΓöÇΓöÇ setup_azure_iothub.ps1     # Crear IoT Hub
Γöé   Γö£ΓöÇΓöÇ generate_root_ca.ps1       # Generar CA ra├¡z
Γöé   Γö£ΓöÇΓöÇ generate_device_certs.ps1  # Generar certs de dispositivos
Γöé   Γö£ΓöÇΓöÇ register_devices.ps1       # Registrar Things en Azure
Γöé   ΓööΓöÇΓöÇ collect_evidence.ps1       # Recopilar evidencias
Γöé
Γö£ΓöÇΓöÇ src/                            # C├│digo fuente
Γöé   Γö£ΓöÇΓöÇ device_simulator.py        # Simulador de dispositivo IoT
Γöé   Γö£ΓöÇΓöÇ mqtt_client.py             # Cliente MQTT con X.509
Γöé   Γö£ΓöÇΓöÇ telemetry_generator.py     # Generador de telemetr├¡a
Γöé   ΓööΓöÇΓöÇ azure_monitor.py           # Monitor de eventos Azure
Γöé
Γö£ΓöÇΓöÇ evidencias/                     # Documentaci├│n de evidencias
Γöé   Γö£ΓöÇΓöÇ screenshots/                # Capturas de pantalla
Γöé   Γö£ΓöÇΓöÇ logs/                       # Logs de operaci├│n
Γöé   ΓööΓöÇΓöÇ REPORTE_EVIDENCIAS.md      # Reporte consolidado
Γöé
Γö£ΓöÇΓöÇ .env.example                    # Plantilla de configuraci├│n
Γö£ΓöÇΓöÇ .gitignore                      # Ignorar certificados y secrets
Γö£ΓöÇΓöÇ requirements.txt                # Dependencias Python
Γö£ΓöÇΓöÇ README.md                       # Este archivo
ΓööΓöÇΓöÇ INFORME_TECNICO.md             # Informe t├⌐cnico detallado

```

---

## ≡ƒöù Referencias y Documentaci├│n

- **Azure IoT Hub**: https://docs.microsoft.com/azure/iot-hub/
- **MQTT Protocol**: https://mqtt.org/
- **X.509 Certificates**: https://docs.microsoft.com/azure/iot-hub/iot-hub-x509ca-overview
- **Azure CLI IoT Extension**: https://github.com/Azure/azure-iot-cli-extension

---

## ≡ƒæ¿ΓÇì≡ƒÄô Informaci├│n Acad├⌐mica

**Universidad:** Universidad Militar Nueva Granada  
**Programa:** Ingenier├¡a Mecatr├│nica  
**Semestre:** Sexto  
**Asignatura:** Comunicaciones  
**Proyecto:** Servidor IoT MQTT Seguro con Azure IoT Hub  
**Fecha:** Noviembre 2025

---

## ≡ƒô¥ Licencia

Proyecto acad├⌐mico - Universidad Militar Nueva Granada ┬⌐ 2025
