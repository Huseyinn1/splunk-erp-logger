import json
import logging
from typing import List, Dict, Any
import requests
from requests.auth import HTTPBasicAuth


class SplunkSender:
    """Splunk HTTP Event Collector (HEC) Sender"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.hec_url = config.get('hec_url', '')
        self.hec_token = config.get('hec_token', '')
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.sourcetype = config.get('sourcetype', 'erp_logs')
        self.index = config.get('index', 'main')
        self.timeout = config.get('timeout_seconds', 30)
        self.verify_ssl = config.get('verify_ssl', False)
        
        self.logger = logging.getLogger(__name__)
        
    def send_logs(self, logs: List[Dict[str, Any]]) -> bool:
        """Logları Splunk HEC'ye gönderir"""
        if not logs:
            self.logger.info("No logs to send")
            return True
            
        try:
            # Her log için Splunk formatında event oluştur
            events = []
            for log in logs:
                event = {
                    "sourcetype": self.sourcetype,
                    "index": self.index,
                    "event": log
                }
                events.append(event)
            
            # Authorization header'ı oluştur
            headers = {
                "Authorization": f"Splunk {self.hec_token}",
                "Content-Type": "application/json"
            }
            
            # Her event'i ayrı ayrı gönder (Splunk HEC formatı)
            success_count = 0
            for event in events:
                try:
                    response = requests.post(
                        self.hec_url,
                        headers=headers,
                        data=json.dumps(event),
                        timeout=self.timeout,
                        verify=self.verify_ssl
                    )
                    
                    if response.status_code == 200:
                        success_count += 1
                        self.logger.debug(f"Successfully sent log to Splunk: {event['event'].get('timestamp', 'N/A')}")
                    else:
                        self.logger.error(f"Splunk HEC error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    self.logger.error(f"Error sending individual log to Splunk: {str(e)}")
            
            self.logger.info(f"Sent {success_count}/{len(events)} logs to Splunk successfully")
            return success_count == len(events)
            
        except Exception as e:
            self.logger.error(f"Error sending logs to Splunk: {str(e)}")
            return False
    
    def send_single_log(self, log: Dict[str, Any]) -> bool:
        """Tek bir logu Splunk HEC'ye gönderir"""
        return self.send_logs([log])
    
    def test_connection(self) -> bool:
        """Splunk HEC bağlantısını test eder"""
        try:
            test_event = {
                "sourcetype": self.sourcetype,
                "index": self.index,
                "event": {
                    "timestamp": "2024-06-21T00:00:00Z",
                    "source_system": "test",
                    "log_type": "test",
                    "message": "Connection test event"
                }
            }
            
            headers = {
                "Authorization": f"Splunk {self.hec_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.hec_url,
                headers=headers,
                data=json.dumps(test_event),
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            
            if response.status_code == 200:
                self.logger.info("Splunk HEC connection test successful")
                return True
            else:
                self.logger.error(f"Splunk HEC connection test failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Splunk HEC connection test error: {str(e)}")
            return False
