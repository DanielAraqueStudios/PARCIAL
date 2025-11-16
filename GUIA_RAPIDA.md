# Guía Rápida: Implementación de Servidor IoT MQTT en Azure

## 🚀 Inicio Rápido (Quick Start)

### Requisitos Previos
```powershell
# 1. Verificar instalaciones
az --version          # Azure CLI
python --version      # Python 3.7+
openssl version       # OpenSSL
```

### Instalación de Dependencias
```powershell
# Clonar/navegar al proyecto
cd PARCIAL

# Instalar paquetes Python
pip install -r requirements.txt

# Instalar Azure IoT extension
az extension add --name azure-iot
```

---

## 📋 Pasos de Implementación

### Paso 1: Crear Azure IoT Hub (5 minutos)
```powershell
# Ejecutar script de setup
.\scripts\setup_azure_iothub.ps1

# Resultado: IoT Hub creado, connection string guardado en .env
```

**Evidencia necesaria:**
- Screenshot del Azure Portal mostrando IoT Hub creado
- Screenshot del output del script

---

### Paso 2: Generar Certificado Root CA (2 minutos)
```powershell
# Generar certificado raíz
.\scripts\generate_root_ca.ps1

# Ubicación: certs/root/azure-iot-root.cert.pem
```

**Importante:** 
- Subir certificado raíz a Azure Portal
- Portal → IoT Hub → Certificates → Add → Cargar `azure-iot-root.cert.pem`
- Verificar certificado (seguir wizard de verificación en portal)

**Evidencia necesaria:**
- Screenshot de certificado verificado en Azure Portal

---

### Paso 3: Generar Certificados de Dispositivos (3 minutos)
```powershell
# Generar certificados para 3 dispositivos
.\scripts\generate_device_certs.ps1 -DeviceCount 3

# Resultado: 
#   certs/devices/thing_001/
#   certs/devices/thing_002/
#   certs/devices/thing_003/
```

**Evidencia necesaria:**
- Screenshot de estructura de carpetas `certs/`

---

### Paso 4: Registrar Dispositivos en IoT Hub (2 minutos)
```powershell
# Registrar todos los dispositivos
.\scripts\register_devices.ps1

# Verificar registro
az iot hub device-identity list --hub-name iothub-parcial-2025 -o table
```

**Evidencia necesaria:**
- Screenshot del output mostrando devices registrados
- Screenshot de Azure Portal → IoT Hub → IoT devices

---

### Paso 5: Ejecutar Simulador de Dispositivo (DEMO)
```powershell
# Terminal 1 - Thing #1
$env:DEVICE_ID="thing_001"
python device_simulator.py

# Terminal 2 - Thing #2 (opcional)
$env:DEVICE_ID="thing_002"
python device_simulator.py

# Terminal 3 - Thing #3 (opcional)
$env:DEVICE_ID="thing_003"
python device_simulator.py
```

**Output esperado:**
```
╔════════════════════════════════════════════════╗
║   Azure IoT Device Simulator - MQTT + X.509    ║
╚════════════════════════════════════════════════╝
📱 Device ID: thing_001
🔗 IoT Hub: iothub-parcial-2025.azure-devices.net
🔐 Certificate: device-cert.pem

🔌 Connecting to Azure IoT Hub...
✅ Connected successfully via MQTT (port 8883)
🔒 TLS/SSL Handshake completed

🚀 Starting telemetry transmission (every 5s)
Press Ctrl+C to stop
────────────────────────────────────────────────────────────

✅ [12:30:45] Message #1
   HR: 75.3 bpm | SpO2: 97.2% | Temp: 36.5°C

✅ [12:30:50] Message #2
   HR: 78.1 bpm | SpO2: 96.8% | Temp: 36.6°C
```

**Evidencia necesaria:**
- Screenshot de terminal(es) con simulador ejecutándose
- Screenshot mostrando conexión exitosa y mensajes siendo enviados

---

### Paso 6: Monitorear Mensajes en Tiempo Real (DEMO)
```powershell
# Terminal separado - Monitorear eventos
az iot hub monitor-events --hub-name iothub-parcial-2025

# O monitorear un dispositivo específico
az iot hub monitor-events --hub-name iothub-parcial-2025 --device-id thing_001
```

**Output esperado:**
```json
{
    "event": {
        "origin": "thing_001",
        "payload": {
            "deviceId": "thing_001",
            "timestamp": "2025-11-16T12:30:45Z",
            "messageId": 1,
            "heartRate": 75.3,
            "spo2": 97.2,
            "temperature": 36.5,
            "status": "online"
        },
        "properties": {
            "application": {
                "deviceType": "bedside_monitor",
                "priority": "normal"
            }
        }
    }
}
```

**Evidencia necesaria:**
- Screenshot completo del monitor mostrando múltiples mensajes
- Capturar al menos 3-5 mensajes para demostrar flujo continuo

---

### Paso 7: Recopilar Evidencias para Informe (5 minutos)
```powershell
# Ejecutar script de recopilación
.\scripts\collect_evidence.ps1

# Resultado: 
#   evidencias/logs/ (7 archivos .txt con información técnica)
#   evidencias/REPORTE_EVIDENCIAS.md (reporte consolidado)
```

**Capturar screenshots manualmente:**
1. Azure Portal - IoT Hub Overview
2. Azure Portal - Lista de dispositivos
3. Azure Portal - Detalles de un dispositivo
4. Azure Portal - Métricas/Monitoring
5. Terminal con device_simulator.py corriendo
6. Terminal con az iot hub monitor-events
7. Explorador de archivos mostrando estructura de certificados

**Guardar screenshots en:** `evidencias/screenshots/`

---

## 🎯 Checklist de Entrega

### Archivos Generados
- [ ] `.env` con configuración completa
- [ ] `certs/root/` con certificado Root CA
- [ ] `certs/devices/thing_00X/` con certificados por dispositivo
- [ ] `evidencias/logs/` con 7 archivos técnicos
- [ ] `evidencias/screenshots/` con 7 screenshots
- [ ] `evidencias/REPORTE_EVIDENCIAS.md` completo

### Evidencias Visuales
- [ ] Screenshot: Azure IoT Hub creado
- [ ] Screenshot: Certificado Root CA verificado
- [ ] Screenshot: Lista de dispositivos registrados
- [ ] Screenshot: Simulador ejecutándose
- [ ] Screenshot: Monitoreo de eventos en tiempo real
- [ ] Screenshot: Métricas en Azure Portal
- [ ] Screenshot: Estructura de certificados

### Demostración Funcional
- [ ] Al menos 1 dispositivo conectado y transmitiendo
- [ ] Mensajes D2C recibidos en Azure IoT Hub
- [ ] Logs mostrando conexión MQTT exitosa (puerto 8883)
- [ ] Autenticación X.509 funcionando

---

## 🔧 Troubleshooting Común

### Error: "IoT Hub already exists"
```powershell
# Si ya tienes un IoT Hub F1 (free tier), usar uno existente
# Editar .env con el nombre de tu IoT Hub existente
```

### Error: "Certificate verification failed"
```powershell
# Regenerar certificado y verificar en portal
.\scripts\generate_root_ca.ps1
# Subir nuevamente a Azure Portal y completar verificación
```

### Error: "Connection refused"
```powershell
# Verificar que el dispositivo está registrado
az iot hub device-identity show --hub-name <hub-name> --device-id thing_001

# Verificar paths de certificados en .env
```

### Error: "openssl not found"
```powershell
# Instalar OpenSSL desde: https://slproweb.com/products/Win32OpenSSL.html
# Descargar: Win64 OpenSSL v3.x.x MSI
```

---

## 📚 Comandos Útiles

### Azure IoT Hub
```powershell
# Ver información del IoT Hub
az iot hub show --name <hub-name>

# Listar dispositivos
az iot hub device-identity list --hub-name <hub-name> -o table

# Ver métricas
az monitor metrics list --resource <resource-id> --metric "telemetry.ingress.allProtocol"

# Eliminar dispositivo
az iot hub device-identity delete --hub-name <hub-name> --device-id <device-id>
```

### Certificados
```powershell
# Ver información de certificado
openssl x509 -in certs/devices/thing_001/device-cert.pem -text -noout

# Verificar cadena de certificados
openssl verify -CAfile certs/root/azure-iot-root.cert.pem certs/devices/thing_001/device-cert.pem
```

### Python
```powershell
# Ejecutar con device ID específico
$env:DEVICE_ID="thing_002"; python device_simulator.py

# Ejecutar con intervalo personalizado
$env:TELEMETRY_INTERVAL="10"; python device_simulator.py

# Deshabilitar anomalías simuladas
$env:ENABLE_ANOMALIES="false"; python device_simulator.py
```

---

## 📞 Recursos de Ayuda

- **Azure IoT Hub Docs:** https://docs.microsoft.com/azure/iot-hub/
- **MQTT Protocol:** https://mqtt.org/
- **X.509 Certificates:** https://docs.microsoft.com/azure/iot-hub/iot-hub-x509ca-overview
- **Azure CLI Reference:** https://docs.microsoft.com/cli/azure/iot

---

## ⏱️ Tiempo Estimado Total

| Paso | Tiempo | Acumulado |
|------|--------|-----------|
| Setup Azure IoT Hub | 5 min | 5 min |
| Generar Root CA | 2 min | 7 min |
| Generar certs dispositivos | 3 min | 10 min |
| Registrar dispositivos | 2 min | 12 min |
| Ejecutar simulador | 2 min | 14 min |
| Monitorear eventos | 3 min | 17 min |
| Recopilar evidencias | 5 min | 22 min |
| Capturar screenshots | 10 min | 32 min |
| **TOTAL** | | **~30 min** |

---

**¡Éxito en tu proyecto! 🚀**
