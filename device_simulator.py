#!/usr/bin/env python3
"""
Device Simulator for Azure IoT Hub
Simulates an IoT device sending telemetry data via MQTT with X.509 authentication
"""

import os
import sys
import json
import time
import random
import datetime
from pathlib import Path
from dotenv import load_dotenv

try:
    from azure.iot.device import IoTHubDeviceClient, Message
    from azure.iot.device import X509
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError as e:
    print(f"Error: Missing required package. Run: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)

# Load environment variables
load_dotenv()

class DeviceSimulator:
    """Simulates an IoT device with telemetry generation"""
    
    def __init__(self, device_id=None, cert_path=None, key_path=None):
        """
        Initialize device simulator
        
        Args:
            device_id: Device identifier (thing_001, thing_002, etc.)
            cert_path: Path to device certificate
            key_path: Path to device private key
        """
        self.device_id = device_id or os.getenv('DEVICE_ID', 'thing_001')
        self.hostname = os.getenv('IOTHUB_HOSTNAME')
        
        if not self.hostname:
            raise ValueError("IOTHUB_HOSTNAME not set in environment")
        
        # Certificate paths
        base_dir = Path(__file__).parent
        self.cert_path = cert_path or os.getenv('CERT_PATH', 
            f'certs/devices/{self.device_id}/device-cert.pem')
        self.key_path = key_path or os.getenv('KEY_PATH', 
            f'certs/devices/{self.device_id}/device-key.pem')
        
        # Make paths absolute
        self.cert_path = base_dir / self.cert_path
        self.key_path = base_dir / self.key_path
        
        # Verify certificate files exist
        if not self.cert_path.exists():
            raise FileNotFoundError(f"Certificate not found: {self.cert_path}")
        if not self.key_path.exists():
            raise FileNotFoundError(f"Private key not found: {self.key_path}")
        
        self.client = None
        self.message_count = 0
        
        print(f"{Fore.CYAN}╔════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║   Azure IoT Device Simulator - MQTT + X.509    ║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════╝{Style.RESET_ALL}")
        print(f"📱 Device ID: {Fore.GREEN}{self.device_id}{Style.RESET_ALL}")
        print(f"🔗 IoT Hub: {Fore.GREEN}{self.hostname}{Style.RESET_ALL}")
        print(f"🔐 Certificate: {Fore.YELLOW}{self.cert_path.name}{Style.RESET_ALL}")
        print()
    
    def connect(self):
        """Establish MQTT connection to Azure IoT Hub with X.509 authentication"""
        try:
            print(f"{Fore.YELLOW}🔌 Connecting to Azure IoT Hub...{Style.RESET_ALL}")
            
            # Create X.509 authentication object
            x509 = X509(
                cert_file=str(self.cert_path),
                key_file=str(self.key_path)
            )
            
            # Create IoT Hub client with X.509
            self.client = IoTHubDeviceClient.create_from_x509_certificate(
                hostname=self.hostname,
                device_id=self.device_id,
                x509=x509
            )
            
            # Connect to IoT Hub
            self.client.connect()
            
            print(f"{Fore.GREEN}✅ Connected successfully via MQTT (port 8883){Style.RESET_ALL}")
            print(f"{Fore.GREEN}🔒 TLS/SSL Handshake completed{Style.RESET_ALL}")
            print()
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Connection failed: {e}{Style.RESET_ALL}")
            return False
    
    def generate_telemetry(self):
        """
        Generate simulated telemetry data
        
        Returns:
            dict: Telemetry payload
        """
        # Simulate vital signs with occasional anomalies
        enable_anomalies = os.getenv('ENABLE_ANOMALIES', 'true').lower() == 'true'
        
        # Normal ranges
        heart_rate = random.gauss(75, 10)
        spo2 = random.gauss(97, 2)
        temperature = random.gauss(36.5, 0.5)
        
        # Inject anomalies (10% chance)
        if enable_anomalies and random.random() < 0.1:
            anomaly_type = random.choice(['heart_rate', 'spo2', 'temperature'])
            if anomaly_type == 'heart_rate':
                heart_rate = random.choice([random.gauss(120, 5), random.gauss(45, 5)])
            elif anomaly_type == 'spo2':
                spo2 = random.gauss(88, 2)
            elif anomaly_type == 'temperature':
                temperature = random.gauss(38.5, 0.3)
        
        telemetry = {
            'deviceId': self.device_id,
            'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
            'messageId': self.message_count,
            'heartRate': round(max(40, min(200, heart_rate)), 1),
            'spo2': round(max(70, min(100, spo2)), 1),
            'temperature': round(max(35, min(42, temperature)), 2),
            'status': 'online'
        }
        
        return telemetry
    
    def send_message(self, payload):
        """
        Send telemetry message to Azure IoT Hub
        
        Args:
            payload: Dictionary with telemetry data
        """
        try:
            # Create message
            message = Message(json.dumps(payload))
            
            # Add custom properties
            message.message_id = str(self.message_count)
            message.correlation_id = self.device_id
            message.content_encoding = "utf-8"
            message.content_type = "application/json"
            
            # Add custom application properties
            message.custom_properties["deviceType"] = "bedside_monitor"
            message.custom_properties["priority"] = "normal"
            
            # Check for anomalies and flag
            if (payload['heartRate'] > 100 or payload['heartRate'] < 60 or
                payload['spo2'] < 90 or payload['temperature'] > 37.5):
                message.custom_properties["alert"] = "true"
                message.custom_properties["priority"] = "high"
            
            # Send message
            self.client.send_message(message)
            self.message_count += 1
            
            # Display message
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            alert = message.custom_properties.get("alert") == "true"
            
            if alert:
                print(f"{Fore.RED}⚠️  [{timestamp}] Message #{self.message_count} (ALERT){Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}✅ [{timestamp}] Message #{self.message_count}{Style.RESET_ALL}")
            
            print(f"   HR: {payload['heartRate']} bpm | SpO2: {payload['spo2']}% | Temp: {payload['temperature']}°C")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to send message: {e}{Style.RESET_ALL}")
    
    def run(self, interval=None):
        """
        Run device simulator loop
        
        Args:
            interval: Seconds between messages (default from env or 5)
        """
        interval = interval or int(os.getenv('TELEMETRY_INTERVAL', 5))
        
        print(f"{Fore.CYAN}🚀 Starting telemetry transmission (every {interval}s){Style.RESET_ALL}")
        print(f"{Fore.CYAN}Press Ctrl+C to stop{Style.RESET_ALL}")
        print("─" * 60)
        print()
        
        try:
            while True:
                # Generate and send telemetry
                telemetry = self.generate_telemetry()
                self.send_message(telemetry)
                
                # Wait for next interval
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print()
            print(f"{Fore.YELLOW}🛑 Stopping device simulator...{Style.RESET_ALL}")
            self.disconnect()
        except Exception as e:
            print(f"{Fore.RED}❌ Error in main loop: {e}{Style.RESET_ALL}")
            self.disconnect()
    
    def disconnect(self):
        """Disconnect from Azure IoT Hub"""
        try:
            if self.client:
                self.client.disconnect()
                print(f"{Fore.GREEN}✅ Disconnected from Azure IoT Hub{Style.RESET_ALL}")
                print(f"📊 Total messages sent: {self.message_count}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error during disconnect: {e}{Style.RESET_ALL}")

def main():
    """Main entry point"""
    
    # Allow override via command line
    device_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        # Create and run simulator
        simulator = DeviceSimulator(device_id=device_id)
        
        if simulator.connect():
            simulator.run()
        else:
            print(f"{Fore.RED}Failed to establish connection. Exiting.{Style.RESET_ALL}")
            sys.exit(1)
            
    except Exception as e:
        print(f"{Fore.RED}❌ Fatal error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
