# Servidor IoT MQTT Seguro - Azure IoT Hub

**Implementación de servidor IoT con protocolo MQTT seguro usando Azure IoT Hub para dispositivos IoT con autenticación mediante certificados X.509**

[![Azure](https://img.shields.io/badge/Azure-IoT%20Hub-0078D4?logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/services/iot-hub/)
[![MQTT](https://img.shields.io/badge/Protocol-MQTT-660066?logo=mqtt&logoColor=white)](https://mqtt.org/)
[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?logo=python&logoColor=white)](https://www.python.org/)

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Configuración Azure IoT Hub](#-configuración-azure-iot-hub)
- [Generación de Certificados](#-generación-de-certificados)
- [Creación de Dispositivos (Things)](#-creación-de-dispositivos-things)
- [Implementación](#-implementación)
- [Pruebas y Evidencias](#-pruebas-y-evidencias)
- [Estructura del Proyecto](#-estructura-del-proyecto)

---

## 🎯 Descripción del Proyecto

Este proyecto implementa un **servidor IoT seguro** accesible desde internet que permite la integración de múltiples dispositivos IoT usando el protocolo **MQTT con autenticación basada en certificados X.509**.

### Objetivos
✅ Desplegar un servicio IoT en la nube (Azure IoT Hub)  
✅ Configurar acceso seguro mediante MQTT  
✅ Crear múltiples "Things" (dispositivos) con certificados únicos  
✅ Implementar comunicación bidireccional segura  
✅ Generar evidencias de operación del servicio  

### Características
- 🔒 **Autenticación segura** con certificados X.509
- 🌐 **Acceso desde internet** mediante Azure IoT Hub
- 📡 **Protocolo MQTT** (Puerto 8883 - TLS)
- 🔑 **Certificados únicos** por dispositivo
- 📊 **Monitoreo en tiempo real** de telemetría
- ☁️ **Escalable** y tolerante a fallos

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    Azure Cloud                               │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Azure IoT Hub                             │    │
│  │  - MQTT Endpoint (port 8883)                       │    │
│  │  - Device Registry                                  │    │
│  │  - X.509 Certificate Authentication                │    │
│  │  - Message Routing                                  │    │
│  └─────────────┬──────────────────────────────────────┘    │
│                │                                             │
│                ├─────────────────┬───────────────────┐      │
│                ▼                 ▼                   ▼      │
│       ┌────────────────┐ ┌────────────────┐ ┌──────────┐  │
│       │ Azure Monitor  │ │ Event Hubs     │ │ Storage  │  │
│       │ (Metrics/Logs) │ │ (Streaming)    │ │ Account  │  │
│       └────────────────┘ └────────────────┘ └──────────┘  │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │ MQTT over TLS (8883)
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  Device #1    │  │  Device #2    │  │  Device #3    │
│  (Thing_001)  │  │  (Thing_002)  │  │  (Thing_003)  │
│               │  │               │  │               │
│  - Cert X.509 │  │  - Cert X.509 │  │  - Cert X.509 │
│  - Priv Key   │  │  - Priv Key   │  │  - Priv Key   │
│  - Telemetry  │  │  - Telemetry  │  │  - Telemetry  │
└───────────────┘  └───────────────┘  └───────────────┘
```

---

## 🔧 Requisitos Previos

### Cuenta Azure
- Cuenta Azure activa (cuenta educativa disponible)
- Acceso al portal: https://portal.azure.com
- Suscripción con créditos disponibles

### Software Local
- **Python 3.7+**
- **Azure CLI** - https://docs.microsoft.com/cli/azure/install-azure-cli
- **OpenSSL** - Para generación de certificados
- **Git** - Para control de versiones

### Instalación de Azure CLI (Windows)

```powershell
# Descargar e instalar Azure CLI
winget install Microsoft.AzureCLI

# Verificar instalación
az --version

# Iniciar sesión
az login
```

---

## ☁️ Configuración Azure IoT Hub

### Paso 1: Crear Grupo de Recursos

```powershell
# Variables de configuración
$resourceGroup = "rg-iot-parcial"
$location = "eastus"
$iotHubName = "iothub-parcial-2025"

# Crear grupo de recursos
az group create --name $resourceGroup --location $location
```

### Paso 2: Crear Azure IoT Hub

```powershell
# Crear IoT Hub (Free tier - 1 hub gratis por suscripción)
az iot hub create `
  --resource-group $resourceGroup `
  --name $iotHubName `
  --sku F1 `
  --location $location `
  --partition-count 2

# Obtener información del IoT Hub
az iot hub show --name $iotHubName --resource-group $resourceGroup
```

### Paso 3: Obtener Connection String

```powershell
# Obtener connection string del IoT Hub
az iot hub connection-string show --hub-name $iotHubName

# Guardar en variable de entorno
$env:IOTHUB_CONNECTION_STRING = $(az iot hub connection-string show --hub-name $iotHubName --query connectionString -o tsv)
```

### Paso 4: Configurar Certificado Raíz (Root CA)

```powershell
# Generar certificado raíz para validación
.\scripts\generate_root_ca.ps1

# Subir certificado raíz a Azure IoT Hub
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

## 🔐 Generación de Certificados

### Estructura de Certificados

```
certs/
├── root/                      # Certificado raíz (Root CA)
│   ├── azure-iot-root.cert.pem
│   ├── azure-iot-root.key.pem
│   └── verification-cert.pem
│
└── devices/                   # Certificados por dispositivo
    ├── thing_001/
    │   ├── device-cert.pem
    │   ├── device-key.pem
    │   └── device-full-chain.pem
    ├── thing_002/
    │   ├── device-cert.pem
    │   ├── device-key.pem
    │   └── device-full-chain.pem
    └── thing_003/
        ├── device-cert.pem
        ├── device-key.pem
        └── device-full-chain.pem
```

### Script de Generación Automática

```powershell
# Generar certificados para todos los dispositivos
.\scripts\generate_device_certs.ps1 -DeviceCount 3

# O generar para un dispositivo específico
.\scripts\generate_device_certs.ps1 -DeviceId "thing_001"
```

---

## 📱 Creación de Dispositivos (Things)

### Registrar Dispositivos en Azure IoT Hub

```powershell
# Registrar Thing #1 con autenticación X.509
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

### Configuración de Dispositivos

Cada dispositivo tendrá:
- **Device ID único** (thing_001, thing_002, thing_003)
- **Certificado X.509** para autenticación
- **Clave privada** (nunca compartir)
- **Endpoint MQTT**: `{iotHubName}.azure-devices.net:8883`

---

## 🚀 Implementación

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

## 📊 Pruebas y Evidencias

### Lista de Evidencias Requeridas

#### 1. **Creación de Azure IoT Hub**
- [ ] Screenshot del IoT Hub creado en Azure Portal
- [ ] Output del comando `az iot hub show`
- [ ] Información de endpoint y hostname

#### 2. **Dispositivos Registrados**
- [ ] Lista de dispositivos (Things) con `az iot hub device-identity list`
- [ ] Screenshot de la sección "IoT Devices" en Azure Portal
- [ ] Configuración de autenticación X.509 para cada dispositivo

#### 3. **Certificados Generados**
- [ ] Estructura de carpetas de certificados
- [ ] Certificado raíz verificado en Azure Portal
- [ ] Certificados por dispositivo (sin exponer claves privadas)

#### 4. **Conexión MQTT Segura**
- [ ] Logs de conexión exitosa por MQTT (puerto 8883)
- [ ] Screenshot de `device_simulator.py` ejecutándose
- [ ] Confirmación de handshake TLS

#### 5. **Telemetría en Tiempo Real**
- [ ] Output de `az iot hub monitor-events` mostrando mensajes
- [ ] Screenshot de Azure Portal - Metrics & Monitoring
- [ ] Gráficas de mensajes recibidos

#### 6. **Mensajes D2C (Device-to-Cloud)**
- [ ] JSON de mensajes enviados por dispositivos
- [ ] Logs de recepción en Azure IoT Hub
- [ ] Timestamp y device ID en cada mensaje

#### 7. **Seguridad**
- [ ] Verificación de certificado en Azure IoT Hub
- [ ] Intento de conexión fallido sin certificado válido
- [ ] Logs de autenticación

### Scripts para Generar Evidencias

```powershell
# Ejecutar script de recolección de evidencias
.\scripts\collect_evidence.ps1

# Genera un reporte en: ./evidencias/REPORTE_EVIDENCIAS.md
```

---

## 📁 Estructura del Proyecto

```
PARCIAL/
│
├── certs/                          # Certificados X.509
│   ├── root/                       # Certificado raíz
│   │   ├── azure-iot-root.cert.pem
│   │   └── azure-iot-root.key.pem
│   └── devices/                    # Certificados por dispositivo
│       ├── thing_001/
│       ├── thing_002/
│       └── thing_003/
│
├── scripts/                        # Scripts de automatización
│   ├── setup_azure_iothub.ps1     # Crear IoT Hub
│   ├── generate_root_ca.ps1       # Generar CA raíz
│   ├── generate_device_certs.ps1  # Generar certs de dispositivos
│   ├── register_devices.ps1       # Registrar Things en Azure
│   └── collect_evidence.ps1       # Recopilar evidencias
│
├── src/                            # Código fuente
│   ├── device_simulator.py        # Simulador de dispositivo IoT
│   ├── mqtt_client.py             # Cliente MQTT con X.509
│   ├── telemetry_generator.py     # Generador de telemetría
│   └── azure_monitor.py           # Monitor de eventos Azure
│
├── evidencias/                     # Documentación de evidencias
│   ├── screenshots/                # Capturas de pantalla
│   ├── logs/                       # Logs de operación
│   └── REPORTE_EVIDENCIAS.md      # Reporte consolidado
│
├── .env.example                    # Plantilla de configuración
├── .gitignore                      # Ignorar certificados y secrets
├── requirements.txt                # Dependencias Python
├── README.md                       # Este archivo
└── INFORME_TECNICO.md             # Informe técnico detallado

```

---

## 🔗 Referencias y Documentación

- **Azure IoT Hub**: https://docs.microsoft.com/azure/iot-hub/
- **MQTT Protocol**: https://mqtt.org/
- **X.509 Certificates**: https://docs.microsoft.com/azure/iot-hub/iot-hub-x509ca-overview
- **Azure CLI IoT Extension**: https://github.com/Azure/azure-iot-cli-extension

---

## 👨‍🎓 Información Académica

**Universidad:** Universidad Militar Nueva Granada  
**Programa:** Ingeniería Mecatrónica  
**Semestre:** Sexto  
**Asignatura:** Comunicaciones  
**Proyecto:** Servidor IoT MQTT Seguro con Azure IoT Hub  
**Fecha:** Noviembre 2025

---

## 📝 Licencia

Proyecto académico - Universidad Militar Nueva Granada © 2025
