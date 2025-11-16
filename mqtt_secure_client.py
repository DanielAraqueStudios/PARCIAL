#!/usr/bin/env python3
"""
Cliente IoT Simulado - MQTT Seguro con Certificados TLS/X.509
Simula un dispositivo IoT (Cosa/Thing) que se conecta a Azure IoT Hub

Autor: Universidad Militar Nueva Granada - Mecatrónica
Proyecto: Comunicaciones IoT Seguras
Fecha: Noviembre 2025
"""

import os
import sys
import json
import time
import random
import datetime
import ssl
import threading
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import paho.mqtt.client as mqtt
    from colorama import Fore, Style, init
    from dotenv import load_dotenv
    init(autoreset=True)
except ImportError as e:
    print(f"Error: Falta instalar dependencias. Ejecute: pip install -r requirements.txt")
    print(f"Detalle: {e}")
    sys.exit(1)

# Cargar variables de entorno
load_dotenv()


class SecureIoTClient:
    """
    Cliente IoT seguro con autenticación mediante certificados X.509
    y comunicación MQTT sobre TLS
    """
    
    def __init__(self, device_id: str, cert_path: str, key_path: str, 
                 hostname: str, port: int = 8883):
        """
        Inicializar cliente IoT seguro
        
        Args:
            device_id: Identificador único del dispositivo (Thing ID)
            cert_path: Ruta al certificado X.509 del dispositivo
            key_path: Ruta a la clave privada del dispositivo
            hostname: Hostname del servidor IoT (ej: iothub.azure-devices.net)
            port: Puerto MQTT sobre TLS (default: 8883)
        """
        self.device_id = device_id
        self.hostname = hostname
        self.port = port
        self.cert_path = Path(cert_path)
        self.key_path = Path(key_path)
        
        # Validar archivos de certificados
        if not self.cert_path.exists():
            raise FileNotFoundError(f"Certificado no encontrado: {self.cert_path}")
        if not self.key_path.exists():
            raise FileNotFoundError(f"Clave privada no encontrada: {self.key_path}")
        
        # Estado del cliente
        self.connected = False
        self.message_count = 0
        self.last_message_time = None
        
        # Cliente MQTT
        self.client = None
        self._setup_mqtt_client()
        
        # Estadísticas
        self.stats = {
            'messages_sent': 0,
            'messages_failed': 0,
            'connection_attempts': 0,
            'last_error': None
        }
        
        self._print_header()
    
    def _print_header(self):
        """Imprimir encabezado informativo"""
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║     Cliente IoT Seguro - MQTT sobre TLS con X.509         ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        print(f"📱 {Fore.YELLOW}Device ID:{Style.RESET_ALL}     {Fore.GREEN}{self.device_id}{Style.RESET_ALL}")
        print(f"🌐 {Fore.YELLOW}Servidor IoT:{Style.RESET_ALL}  {Fore.GREEN}{self.hostname}:{self.port}{Style.RESET_ALL}")
        print(f"🔐 {Fore.YELLOW}Certificado:{Style.RESET_ALL}   {Fore.CYAN}{self.cert_path.name}{Style.RESET_ALL}")
        print(f"🔑 {Fore.YELLOW}Clave privada:{Style.RESET_ALL} {Fore.CYAN}{self.key_path.name}{Style.RESET_ALL}")
        print(f"🔒 {Fore.YELLOW}Protocolo:{Style.RESET_ALL}     {Fore.GREEN}MQTT v3.1.1 sobre TLS 1.2+{Style.RESET_ALL}")
        print()
    
    def _setup_mqtt_client(self):
        """Configurar cliente MQTT con TLS y certificados X.509"""
        # Crear cliente MQTT con ID único
        client_id = self.device_id
        self.client = mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv311,
            transport="tcp"
        )
        
        # Configurar callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish
        self.client.on_message = self._on_message
        self.client.on_log = self._on_log
        
        # Configurar autenticación con certificados X.509
        self.client.tls_set(
            certfile=str(self.cert_path),
            keyfile=str(self.key_path),
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2,
            ciphers=None
        )
        
        # Deshabilitar verificación de hostname (Azure IoT Hub maneja esto)
        self.client.tls_insecure_set(False)
        
        # Username para Azure IoT Hub
        username = f"{self.hostname}/{self.device_id}/?api-version=2021-04-12"
        self.client.username_pw_set(username=username, password=None)
        
        print(f"{Fore.GREEN}✅ Cliente MQTT configurado con TLS 1.2+{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Autenticación X.509 habilitada{Style.RESET_ALL}")
        print()
    
    def _on_connect(self, client, userdata, flags, rc):
        """
        Callback ejecutado al conectarse al broker MQTT
        
        Args:
            rc: Código de resultado de conexión
                0: Conexión exitosa
                1-5: Errores de conexión
        """
        if rc == 0:
            self.connected = True
            print(f"{Fore.GREEN}✅ Conexión MQTT establecida exitosamente{Style.RESET_ALL}")
            print(f"{Fore.GREEN}🔒 Handshake TLS completado{Style.RESET_ALL}")
            print(f"{Fore.GREEN}🔐 Certificado X.509 validado{Style.RESET_ALL}")
            print()
            
            # Suscribirse a mensajes Cloud-to-Device
            c2d_topic = f"devices/{self.device_id}/messages/devicebound/#"
            self.client.subscribe(c2d_topic, qos=1)
            print(f"{Fore.CYAN}📥 Suscrito a mensajes C2D: {c2d_topic}{Style.RESET_ALL}")
            print()
        else:
            self.connected = False
            error_messages = {
                1: "Versión de protocolo incorrecta",
                2: "Identificador de cliente inválido",
                3: "Servidor no disponible",
                4: "Usuario/contraseña incorrectos",
                5: "No autorizado (certificado inválido)"
            }
            error_msg = error_messages.get(rc, f"Error desconocido (código {rc})")
            print(f"{Fore.RED}❌ Error de conexión: {error_msg}{Style.RESET_ALL}")
            self.stats['last_error'] = error_msg
            self.stats['connection_attempts'] += 1
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback ejecutado al desconectarse del broker"""
        self.connected = False
        if rc == 0:
            print(f"{Fore.YELLOW}🔌 Desconexión limpia del servidor{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}⚠️  Desconexión inesperada (código {rc}){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}🔄 Intentando reconexión...{Style.RESET_ALL}")
    
    def _on_publish(self, client, userdata, mid):
        """Callback ejecutado cuando se publica un mensaje"""
        self.stats['messages_sent'] += 1
    
    def _on_message(self, client, userdata, msg):
        """
        Callback ejecutado al recibir mensajes Cloud-to-Device
        
        Args:
            msg: Mensaje MQTT recibido
        """
        try:
            payload = msg.payload.decode('utf-8')
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            
            print(f"{Fore.MAGENTA}📩 [{timestamp}] Mensaje C2D recibido:{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   Topic: {msg.topic}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}   Payload: {payload}{Style.RESET_ALL}")
            print()
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error procesando mensaje C2D: {e}{Style.RESET_ALL}")
    
    def _on_log(self, client, userdata, level, buf):
        """Callback para logs de depuración (opcional)"""
        # Descomentar para debugging detallado
        # print(f"[MQTT LOG] {buf}")
        pass
    
    def connect(self, keepalive: int = 60) -> bool:
        """
        Conectar al servidor IoT mediante MQTT seguro
        
        Args:
            keepalive: Intervalo de keep-alive en segundos
            
        Returns:
            True si la conexión fue exitosa
        """
        try:
            print(f"{Fore.YELLOW}🔌 Conectando a {self.hostname}:{self.port}...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}⏳ Estableciendo conexión TLS...{Style.RESET_ALL}")
            
            self.stats['connection_attempts'] += 1
            self.client.connect(self.hostname, self.port, keepalive)
            
            # Iniciar loop en background
            self.client.loop_start()
            
            # Esperar conexión (máximo 10 segundos)
            timeout = 10
            elapsed = 0
            while not self.connected and elapsed < timeout:
                time.sleep(0.5)
                elapsed += 0.5
            
            if not self.connected:
                print(f"{Fore.RED}❌ Timeout: No se pudo conectar en {timeout}s{Style.RESET_ALL}")
                return False
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error al conectar: {e}{Style.RESET_ALL}")
            self.stats['last_error'] = str(e)
            return False
    
    def disconnect(self):
        """Desconectar del servidor IoT"""
        try:
            if self.connected:
                self.client.loop_stop()
                self.client.disconnect()
                print(f"{Fore.GREEN}✅ Desconectado del servidor IoT{Style.RESET_ALL}")
                self.print_stats()
        except Exception as e:
            print(f"{Fore.RED}❌ Error al desconectar: {e}{Style.RESET_ALL}")
    
    def send_telemetry(self, data: Dict[str, Any]) -> bool:
        """
        Enviar telemetría Device-to-Cloud
        
        Args:
            data: Diccionario con datos de telemetría
            
        Returns:
            True si el mensaje se envió exitosamente
        """
        if not self.connected:
            print(f"{Fore.RED}❌ No conectado - no se puede enviar mensaje{Style.RESET_ALL}")
            self.stats['messages_failed'] += 1
            return False
        
        try:
            # Topic para mensajes D2C en Azure IoT Hub
            topic = f"devices/{self.device_id}/messages/events/"
            
            # Agregar metadata
            message_data = {
                **data,
                'deviceId': self.device_id,
                'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
                'messageId': self.message_count
            }
            
            # Serializar a JSON
            payload = json.dumps(message_data)
            
            # Publicar con QoS 1 (at least once delivery)
            result = self.client.publish(
                topic=topic,
                payload=payload,
                qos=1,
                retain=False
            )
            
            # Verificar resultado
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                self.message_count += 1
                self.last_message_time = datetime.datetime.now()
                
                timestamp = self.last_message_time.strftime("%H:%M:%S")
                
                # Detectar alertas
                is_alert = self._is_alert(data)
                
                if is_alert:
                    print(f"{Fore.RED}⚠️  [{timestamp}] Mensaje #{self.message_count} (ALERTA){Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}✅ [{timestamp}] Mensaje #{self.message_count}{Style.RESET_ALL}")
                
                # Mostrar datos de forma compacta
                self._print_telemetry(data)
                
                return True
            else:
                print(f"{Fore.RED}❌ Error al publicar (rc={result.rc}){Style.RESET_ALL}")
                self.stats['messages_failed'] += 1
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error enviando telemetría: {e}{Style.RESET_ALL}")
            self.stats['messages_failed'] += 1
            return False
    
    def _is_alert(self, data: Dict[str, Any]) -> bool:
        """Detectar si los datos contienen valores anómalos"""
        alerts = []
        
        if 'heartRate' in data:
            hr = data['heartRate']
            if hr > 100 or hr < 60:
                alerts.append(f"HR:{hr}")
        
        if 'spo2' in data:
            spo2 = data['spo2']
            if spo2 < 90:
                alerts.append(f"SpO2:{spo2}")
        
        if 'temperature' in data:
            temp = data['temperature']
            if temp > 37.5 or temp < 36.0:
                alerts.append(f"Temp:{temp}")
        
        return len(alerts) > 0
    
    def _print_telemetry(self, data: Dict[str, Any]):
        """Imprimir datos de telemetría de forma legible"""
        values = []
        
        if 'heartRate' in data:
            hr = data['heartRate']
            color = Fore.RED if hr > 100 or hr < 60 else Fore.WHITE
            values.append(f"{color}HR: {hr} bpm{Style.RESET_ALL}")
        
        if 'spo2' in data:
            spo2 = data['spo2']
            color = Fore.RED if spo2 < 90 else Fore.WHITE
            values.append(f"{color}SpO2: {spo2}%{Style.RESET_ALL}")
        
        if 'temperature' in data:
            temp = data['temperature']
            color = Fore.RED if temp > 37.5 or temp < 36.0 else Fore.WHITE
            values.append(f"{color}Temp: {temp}°C{Style.RESET_ALL}")
        
        if values:
            print(f"   {' | '.join(values)}")
    
    def generate_vital_signs(self) -> Dict[str, float]:
        """
        Generar datos simulados de signos vitales
        
        Returns:
            Diccionario con signos vitales simulados
        """
        # Valores normales con distribución gaussiana
        heart_rate = random.gauss(75, 10)  # μ=75, σ=10
        spo2 = random.gauss(97, 2)         # μ=97, σ=2
        temperature = random.gauss(36.5, 0.5)  # μ=36.5, σ=0.5
        
        # Inyectar anomalías ocasionalmente (10% probabilidad)
        if random.random() < 0.1:
            anomaly_type = random.choice(['hr', 'spo2', 'temp'])
            if anomaly_type == 'hr':
                heart_rate = random.choice([
                    random.gauss(120, 5),  # Taquicardia
                    random.gauss(45, 5)    # Bradicardia
                ])
            elif anomaly_type == 'spo2':
                spo2 = random.gauss(88, 2)  # Hipoxemia
            elif anomaly_type == 'temp':
                temperature = random.gauss(38.5, 0.3)  # Fiebre
        
        # Limitar a rangos físicamente posibles
        return {
            'heartRate': round(max(40, min(200, heart_rate)), 1),
            'spo2': round(max(70, min(100, spo2)), 1),
            'temperature': round(max(35.0, min(42.0, temperature)), 2),
            'status': 'online'
        }
    
    def run_simulation(self, interval: int = 5, duration: Optional[int] = None):
        """
        Ejecutar simulación continua de telemetría
        
        Args:
            interval: Segundos entre mensajes
            duration: Duración total en segundos (None = infinito)
        """
        print(f"{Fore.CYAN}🚀 Iniciando simulación de telemetría{Style.RESET_ALL}")
        print(f"{Fore.CYAN}⏱️  Intervalo: {interval}s | Duración: {'∞' if duration is None else f'{duration}s'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Press Ctrl+C para detener{Style.RESET_ALL}")
        print("─" * 70)
        print()
        
        start_time = time.time()
        
        try:
            while True:
                # Verificar duración
                if duration and (time.time() - start_time) >= duration:
                    print()
                    print(f"{Fore.YELLOW}⏱️  Duración completada ({duration}s){Style.RESET_ALL}")
                    break
                
                # Generar y enviar telemetría
                telemetry = self.generate_vital_signs()
                self.send_telemetry(telemetry)
                
                # Esperar intervalo
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print()
            print(f"{Fore.YELLOW}🛑 Simulación detenida por usuario{Style.RESET_ALL}")
        except Exception as e:
            print()
            print(f"{Fore.RED}❌ Error en simulación: {e}{Style.RESET_ALL}")
    
    def print_stats(self):
        """Imprimir estadísticas de la sesión"""
        print()
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                  Estadísticas de Sesión                    ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print()
        print(f"📊 {Fore.YELLOW}Mensajes enviados:{Style.RESET_ALL}     {Fore.GREEN}{self.stats['messages_sent']}{Style.RESET_ALL}")
        print(f"❌ {Fore.YELLOW}Mensajes fallidos:{Style.RESET_ALL}     {Fore.RED}{self.stats['messages_failed']}{Style.RESET_ALL}")
        print(f"🔌 {Fore.YELLOW}Intentos de conexión:{Style.RESET_ALL} {self.stats['connection_attempts']}")
        
        if self.last_message_time:
            print(f"⏱️  {Fore.YELLOW}Último mensaje:{Style.RESET_ALL}        {self.last_message_time.strftime('%H:%M:%S')}")
        
        if self.stats['last_error']:
            print(f"⚠️  {Fore.YELLOW}Último error:{Style.RESET_ALL}          {Fore.RED}{self.stats['last_error']}{Style.RESET_ALL}")
        
        print()


def main():
    """Punto de entrada principal"""
    
    # Configuración desde variables de entorno
    device_id = os.getenv('DEVICE_ID', 'thing_001')
    hostname = os.getenv('IOTHUB_HOSTNAME')
    port = int(os.getenv('MQTT_PORT', 8883))
    
    # Paths de certificados
    base_dir = Path(__file__).parent
    cert_path = os.getenv('CERT_PATH', f'certs/devices/{device_id}/device-cert.pem')
    key_path = os.getenv('KEY_PATH', f'certs/devices/{device_id}/device-key.pem')
    
    cert_path = base_dir / cert_path
    key_path = base_dir / key_path
    
    # Validar configuración
    if not hostname:
        print(f"{Fore.RED}❌ Error: IOTHUB_HOSTNAME no configurado en .env{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ejemplo: IOTHUB_HOSTNAME=iothub-parcial-2025.azure-devices.net{Style.RESET_ALL}")
        sys.exit(1)
    
    try:
        # Crear cliente IoT seguro
        client = SecureIoTClient(
            device_id=device_id,
            cert_path=str(cert_path),
            key_path=str(key_path),
            hostname=hostname,
            port=port
        )
        
        # Conectar al servidor
        if client.connect():
            # Ejecutar simulación
            interval = int(os.getenv('TELEMETRY_INTERVAL', 5))
            client.run_simulation(interval=interval)
        else:
            print(f"{Fore.RED}❌ No se pudo establecer conexión. Verifique:{Style.RESET_ALL}")
            print(f"   • Servidor IoT Hub está accesible")
            print(f"   • Certificados son válidos")
            print(f"   • Dispositivo está registrado")
            print(f"   • Firewall permite puerto {port}")
            sys.exit(1)
        
    except FileNotFoundError as e:
        print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Genere certificados con: .\\scripts\\generate_device_certs.ps1{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}❌ Error fatal: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Desconectar limpiamente
        try:
            client.disconnect()
        except:
            pass


if __name__ == "__main__":
    main()
