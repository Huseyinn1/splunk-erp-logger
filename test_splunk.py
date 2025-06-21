#!/usr/bin/env python3
"""
Splunk HEC Test Scripti
Bu script, Splunk HEC'ye test logları gönderir.
"""

import json
import requests
from datetime import datetime

# Splunk HEC ayarları
SPLUNK_CONFIG = {
    "hec_url": "https://127.0.0.1:8088/services/collector",
    "hec_token": "e403d02d-699c-4f62-8512-b369fbd825ea",
    "sourcetype": "erp_logs",
    "index": "main"
}

def send_test_logs():
    """Test logları gönderir"""
    
    # Test logları
    test_logs = [
        {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "source_system": "IFS Applications",
            "log_type": "system",
            "message": {
                "Content": "Test system log from IFS",
                "EntryType": "INFO",
                "description": "Bu bir test sistem logudur"
            }
        },
        {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "source_system": "IFS Applications", 
            "log_type": "audit",
            "message": {
                "event_type": "User_Login_Success",
                "user_id": "test_user",
                "description": "Test kullanıcı girişi"
            }
        },
        {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "source_system": "Infor CloudSuite",
            "log_type": "system", 
            "message": {
                "api_suite": "TestAPI",
                "endpoint": "/test/endpoint",
                "response_code": 200,
                "description": "Test API çağrısı"
            }
        },
        {
            "timestamp": datetime.utcnow().isoformat() + 'Z',
            "source_system": "Infor CloudSuite",
            "log_type": "audit",
            "message": {
                "message_type": 1,
                "user_name": "test_user",
                "description": "Test audit log"
            }
        }
    ]
    
    headers = {
        "Authorization": f"Splunk {SPLUNK_CONFIG['hec_token']}",
        "Content-Type": "application/json"
    }
    
    success_count = 0
    
    for i, log in enumerate(test_logs):
        event = {
            "sourcetype": SPLUNK_CONFIG['sourcetype'],
            "index": SPLUNK_CONFIG['index'],
            "event": log
        }
        
        try:
            response = requests.post(
                SPLUNK_CONFIG['hec_url'],
                headers=headers,
                data=json.dumps(event),
                verify=False,
                timeout=30
            )
            
            if response.status_code == 200:
                success_count += 1
                print(f"✓ Test log {i+1} başarıyla gönderildi")
            else:
                print(f"✗ Test log {i+1} gönderilemedi: {response.status_code}")
                
        except Exception as e:
            print(f"✗ Test log {i+1} hatası: {str(e)}")
    
    print(f"\nToplam {success_count}/{len(test_logs)} test logu başarıyla gönderildi")
    
    if success_count == len(test_logs):
        print("\n🎉 Tüm testler başarılı! Splunk'ta logları kontrol edin:")
        print("Splunk Search: sourcetype=\"erp_logs\"")
        print("Splunk Search: source_system=\"IFS Applications\"")
        print("Splunk Search: source_system=\"Infor CloudSuite\"")

if __name__ == "__main__":
    print("Splunk HEC Test Scripti")
    print("=" * 30)
    send_test_logs() 