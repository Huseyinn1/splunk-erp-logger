import json
import logging
import os
from datetime import datetime
from typing import List, Dict, Any
import requests
from requests.auth import HTTPBasicAuth


class IFSClient:
    """IFS Applications API Client"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.base_url = config.get('api_base_url', '')
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.timeout = config.get('timeout_seconds', 30)
        self.use_mock_data = config.get('use_mock_data', True)
        self.mock_data_path = config.get('mock_data_path', 'app/mock_data')
        
        self.logger = logging.getLogger(__name__)
        
    def get_system_logs(self, last_check_time: str = None) -> List[Dict[str, Any]]:
        """Sistem loglarını çeker"""
        if self.use_mock_data:
            return self._get_mock_system_logs()
        
        try:
            endpoint = f"{self.base_url}{self.config['system_logs']['endpoint']}"
            params = {}
            
            if last_check_time:
                params['since'] = last_check_time
                
            response = requests.get(
                endpoint,
                auth=HTTPBasicAuth(self.username, self.password),
                params=params,
                timeout=self.timeout,
                verify=False  # Geliştirme ortamı için
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"IFS system logs API error: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error fetching IFS system logs: {str(e)}")
            return []
    
    def get_audit_logs(self, last_check_time: str = None) -> List[Dict[str, Any]]:
        """Audit loglarını çeker"""
        if self.use_mock_data:
            return self._get_mock_audit_logs()
        
        try:
            endpoint = f"{self.base_url}{self.config['audit_logs']['endpoint']}"
            params = {}
            
            if last_check_time:
                params['since'] = last_check_time
                
            response = requests.get(
                endpoint,
                auth=HTTPBasicAuth(self.username, self.password),
                params=params,
                timeout=self.timeout,
                verify=False  # Geliştirme ortamı için
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"IFS audit logs API error: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error fetching IFS audit logs: {str(e)}")
            return []
    
    def get_user_activity_logs(self, last_check_time: str = None) -> List[Dict[str, Any]]:
        """Kullanıcı etkinliği loglarını çeker"""
        if self.use_mock_data:
            return self._get_mock_user_activity_logs()
        
        try:
            endpoint = f"{self.base_url}{self.config['user_activity_logs']['endpoint']}"
            params = {}
            
            if last_check_time:
                params['since'] = last_check_time
                
            response = requests.get(
                endpoint,
                auth=HTTPBasicAuth(self.username, self.password),
                params=params,
                timeout=self.timeout,
                verify=False  # Geliştirme ortamı için
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                self.logger.error(f"IFS user activity logs API error: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error fetching IFS user activity logs: {str(e)}")
            return []
    
    def _get_mock_system_logs(self) -> List[Dict[str, Any]]:
        """Mock sistem loglarını okur"""
        try:
            mock_file = os.path.join(self.mock_data_path, 'ifs_system_logs.json')
            with open(mock_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # Timestamp'i güncelle
            current_time = datetime.utcnow().isoformat() + 'Z'
            for log in logs:
                log['timestamp'] = current_time
                
            return logs
            
        except Exception as e:
            self.logger.error(f"Error reading mock IFS system logs: {str(e)}")
            return []
    
    def _get_mock_audit_logs(self) -> List[Dict[str, Any]]:
        """Mock audit loglarını okur"""
        try:
            mock_file = os.path.join(self.mock_data_path, 'ifs_audit_logs.json')
            with open(mock_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # Timestamp'i güncelle
            current_time = datetime.utcnow().isoformat() + 'Z'
            for log in logs:
                log['timestamp'] = current_time
                
            return logs
            
        except Exception as e:
            self.logger.error(f"Error reading mock IFS audit logs: {str(e)}")
            return []
    
    def _get_mock_user_activity_logs(self) -> List[Dict[str, Any]]:
        """Mock kullanıcı etkinliği loglarını okur"""
        try:
            mock_file = os.path.join(self.mock_data_path, 'ifs_user_activity_logs.json')
            with open(mock_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            # Timestamp'i güncelle
            current_time = datetime.utcnow().isoformat() + 'Z'
            for log in logs:
                log['timestamp'] = current_time
                
            return logs
            
        except Exception as e:
            self.logger.error(f"Error reading mock IFS user activity logs: {str(e)}")
            return []
