import logging
import os
import time
from datetime import datetime
from typing import Dict, Any
import schedule

from .config import Config
from .api_clients.ifs_client import IFSClient
from .api_clients.infor_client import InforClient
from .splunk_sender import SplunkSender
from .log_formatter import LogFormatter


class LogScheduler:
    """Log toplama işlemini zamanlayan sınıf"""
    
    def __init__(self, config_path: str = "app/config/config.yaml"):
        self.config_path = config_path
        self.config_manager = Config(config_path)
        self.config = self.config_manager.get_config()
        self.logger = self._setup_logging()
        
        # Bileşenleri başlat
        self.ifs_client = None
        self.infor_client = None
        self.splunk_sender = None
        self.log_formatter = LogFormatter()
        
        self._initialize_components()
    
    def _setup_logging(self) -> logging.Logger:
        """Logging ayarlarını yapar"""
        log_config = self.config.get('log_collector', {})
        log_file = log_config.get('log_file', 'app/logs/app.log')
        log_level = getattr(logging, log_config.get('log_level', 'INFO'))
        
        # Log dizinini oluştur
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        # Logger'ı yapılandır
        logger = logging.getLogger('log_collector')
        logger.setLevel(log_level)
        
        # Dosya handler'ı
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        
        # Console handler'ı
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Handler'ları ekle
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_components(self):
        """Bileşenleri başlatır"""
        try:
            # Environment yapılandırması kontrolü
            if self.config_manager.is_env_configured():
                self.logger.info("Environment variables detected - using .env configuration")
            else:
                self.logger.info("Using config.yaml configuration")
            
            # IFS Client
            if self.config.get('ifs', {}).get('enabled', False):
                ifs_config = self.config['ifs'].copy()
                ifs_config['use_mock_data'] = self.config['log_collector'].get('use_mock_data', True)
                ifs_config['mock_data_path'] = self.config['log_collector'].get('mock_data_path', 'app/mock_data')
                self.ifs_client = IFSClient(ifs_config)
                self.logger.info("IFS Client initialized")
            
            # Infor Client
            if self.config.get('infor', {}).get('enabled', False):
                infor_config = self.config['infor'].copy()
                infor_config['use_mock_data'] = self.config['log_collector'].get('use_mock_data', True)
                infor_config['mock_data_path'] = self.config['log_collector'].get('mock_data_path', 'app/mock_data')
                self.infor_client = InforClient(infor_config)
                self.logger.info("Infor Client initialized")
            
            # Splunk Sender
            if self.config.get('splunk', {}).get('enabled', False):
                self.splunk_sender = SplunkSender(self.config['splunk'])
                self.logger.info("Splunk Sender initialized")
            
        except Exception as e:
            self.logger.error(f"Error initializing components: {str(e)}")
    
    def collect_and_send_logs(self):
        """Logları toplar ve Splunk'a gönderir"""
        self.logger.info("Starting log collection cycle")
        
        try:
            all_logs = []
            
            # IFS loglarını topla
            if self.ifs_client:
                self.logger.info("Collecting IFS logs...")
                
                # Sistem logları
                ifs_system_logs = self.ifs_client.get_system_logs()
                if ifs_system_logs:
                    formatted_system_logs = self.log_formatter.format_logs_for_splunk(
                        ifs_system_logs, "IFS Applications"
                    )
                    all_logs.extend(formatted_system_logs)
                    self.logger.info(f"Collected {len(formatted_system_logs)} IFS system logs")
                
                # Audit logları
                ifs_audit_logs = self.ifs_client.get_audit_logs()
                if ifs_audit_logs:
                    formatted_audit_logs = self.log_formatter.format_logs_for_splunk(
                        ifs_audit_logs, "IFS Applications"
                    )
                    all_logs.extend(formatted_audit_logs)
                    self.logger.info(f"Collected {len(formatted_audit_logs)} IFS audit logs")
                
                # Kullanıcı etkinliği logları
                ifs_user_activity_logs = self.ifs_client.get_user_activity_logs()
                if ifs_user_activity_logs:
                    formatted_user_activity_logs = self.log_formatter.format_logs_for_splunk(
                        ifs_user_activity_logs, "IFS Applications"
                    )
                    all_logs.extend(formatted_user_activity_logs)
                    self.logger.info(f"Collected {len(formatted_user_activity_logs)} IFS user activity logs")
            
            # Infor loglarını topla
            if self.infor_client:
                self.logger.info("Collecting Infor logs...")
                
                # Sistem logları
                infor_system_logs = self.infor_client.get_system_logs()
                if infor_system_logs:
                    formatted_system_logs = self.log_formatter.format_logs_for_splunk(
                        infor_system_logs, "Infor CloudSuite"
                    )
                    all_logs.extend(formatted_system_logs)
                    self.logger.info(f"Collected {len(formatted_system_logs)} Infor system logs")
                
                # Audit logları
                infor_audit_logs = self.infor_client.get_audit_logs()
                if infor_audit_logs:
                    formatted_audit_logs = self.log_formatter.format_logs_for_splunk(
                        infor_audit_logs, "Infor CloudSuite"
                    )
                    all_logs.extend(formatted_audit_logs)
                    self.logger.info(f"Collected {len(formatted_audit_logs)} Infor audit logs")
                
                # Kullanıcı etkinliği logları
                infor_user_activity_logs = self.infor_client.get_user_activity_logs()
                if infor_user_activity_logs:
                    formatted_user_activity_logs = self.log_formatter.format_logs_for_splunk(
                        infor_user_activity_logs, "Infor CloudSuite"
                    )
                    all_logs.extend(formatted_user_activity_logs)
                    self.logger.info(f"Collected {len(formatted_user_activity_logs)} Infor user activity logs")
            
            # Splunk'a gönder
            if self.splunk_sender and all_logs:
                self.logger.info(f"Sending {len(all_logs)} logs to Splunk...")
                success = self.splunk_sender.send_logs(all_logs)
                
                if success:
                    self.logger.info("Successfully sent all logs to Splunk")
                else:
                    self.logger.error("Failed to send some logs to Splunk")
            elif not all_logs:
                self.logger.info("No logs to send")
            else:
                self.logger.warning("Splunk sender not configured")
                
        except Exception as e:
            self.logger.error(f"Error in log collection cycle: {str(e)}")
    
    def start(self):
        """Scheduler'ı başlatır"""
        try:
            interval_minutes = self.config['log_collector'].get('interval_minutes', 5)
            
            # İlk çalıştırma
            self.logger.info("Running initial log collection...")
            self.collect_and_send_logs()
            
            # Zamanlanmış çalıştırma
            schedule.every(interval_minutes).minutes.do(self.collect_and_send_logs)
            
            self.logger.info(f"Log scheduler started. Running every {interval_minutes} minutes.")
            
            # Sonsuz döngü
            while True:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("Log scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"Error in scheduler: {str(e)}")
    
    def test_connections(self):
        """Tüm bağlantıları test eder"""
        self.logger.info("Testing connections...")
        
        # Environment yapılandırması kontrolü
        if self.config_manager.is_env_configured():
            self.logger.info("✓ Environment variables configured")
        else:
            self.logger.warning("⚠ No environment variables found, using config.yaml")
        
        # Splunk bağlantı testi
        if self.splunk_sender:
            if self.splunk_sender.test_connection():
                self.logger.info("✓ Splunk connection test: SUCCESS")
            else:
                self.logger.error("✗ Splunk connection test: FAILED")
        
        # Mock veri testi
        if self.ifs_client:
            system_logs = self.ifs_client.get_system_logs()
            audit_logs = self.ifs_client.get_audit_logs()
            self.logger.info(f"✓ IFS mock data test: {len(system_logs)} system logs, {len(audit_logs)} audit logs")
        
        if self.infor_client:
            system_logs = self.infor_client.get_system_logs()
            audit_logs = self.infor_client.get_audit_logs()
            self.logger.info(f"✓ Infor mock data test: {len(system_logs)} system logs, {len(audit_logs)} audit logs")
