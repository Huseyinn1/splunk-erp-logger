import os
import yaml
from typing import Dict, Any
from dotenv import load_dotenv


class Config:
    """Yapılandırma yöneticisi - .env ve config.yaml dosyalarını birleştirir"""
    
    def __init__(self, config_path: str = "app/config/config.yaml"):
        self.config_path = config_path
        self._load_env()
        self._load_config()
        self._merge_env_with_config()
    
    def _load_env(self):
        """Environment değişkenlerini yükler"""
        # .env dosyasını yükle
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
        else:
            # .env dosyası yoksa, environment değişkenlerini kullan
            pass
    
    def _load_config(self):
        """config.yaml dosyasını yükler"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            self.config = {}
    
    def _merge_env_with_config(self):
        """Environment değişkenlerini config ile birleştirir"""
        # IFS ayarları
        if 'ifs' in self.config:
            self.config['ifs']['api_base_url'] = os.getenv('IFS_API_BASE_URL', self.config['ifs'].get('api_base_url', ''))
            self.config['ifs']['username'] = os.getenv('IFS_USERNAME', self.config['ifs'].get('username', ''))
            self.config['ifs']['password'] = os.getenv('IFS_PASSWORD', self.config['ifs'].get('password', ''))
        
        # Infor ayarları
        if 'infor' in self.config:
            self.config['infor']['api_base_url'] = os.getenv('INFOR_API_BASE_URL', self.config['infor'].get('api_base_url', ''))
            self.config['infor']['username'] = os.getenv('INFOR_USERNAME', self.config['infor'].get('username', ''))
            self.config['infor']['password'] = os.getenv('INFOR_PASSWORD', self.config['infor'].get('password', ''))
        
        # Splunk ayarları
        if 'splunk' in self.config:
            self.config['splunk']['hec_url'] = os.getenv('SPLUNK_HEC_URL', self.config['splunk'].get('hec_url', ''))
            self.config['splunk']['hec_token'] = os.getenv('SPLUNK_HEC_TOKEN', self.config['splunk'].get('hec_token', ''))
            self.config['splunk']['username'] = os.getenv('SPLUNK_USERNAME', self.config['splunk'].get('username', ''))
            self.config['splunk']['password'] = os.getenv('SPLUNK_PASSWORD', self.config['splunk'].get('password', ''))
        
        # Genel ayarlar
        if 'log_collector' in self.config:
            self.config['log_collector']['log_level'] = os.getenv('LOG_LEVEL', self.config['log_collector'].get('log_level', 'INFO'))
            self.config['log_collector']['interval_minutes'] = int(os.getenv('LOG_INTERVAL_MINUTES', self.config['log_collector'].get('interval_minutes', 5)))
            self.config['log_collector']['use_mock_data'] = os.getenv('USE_MOCK_DATA', 'true').lower() == 'true'
    
    def get(self, key: str, default: Any = None) -> Any:
        """Config değerini döndürür"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_config(self) -> Dict[str, Any]:
        """Tüm config'i döndürür"""
        return self.config
    
    def is_env_configured(self) -> bool:
        """Environment değişkenlerinin yapılandırılıp yapılandırılmadığını kontrol eder"""
        env_vars = [
            'IFS_API_BASE_URL', 'IFS_USERNAME', 'IFS_PASSWORD',
            'INFOR_API_BASE_URL', 'INFOR_USERNAME', 'INFOR_PASSWORD',
            'SPLUNK_HEC_URL', 'SPLUNK_HEC_TOKEN'
        ]
        
        configured_vars = [var for var in env_vars if os.getenv(var)]
        return len(configured_vars) > 0 