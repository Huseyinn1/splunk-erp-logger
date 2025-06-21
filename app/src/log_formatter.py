import logging
from datetime import datetime
from typing import List, Dict, Any


class LogFormatter:
    """Log formatlama ve işleme sınıfı"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def format_logs_for_splunk(self, logs: List[Dict[str, Any]], source_system: str) -> List[Dict[str, Any]]:
        """Logları Splunk için formatlar"""
        formatted_logs = []
        
        for log in logs:
            try:
                formatted_log = self._format_single_log(log, source_system)
                if formatted_log:
                    formatted_logs.append(formatted_log)
            except Exception as e:
                self.logger.error(f"Error formatting log: {str(e)}")
                continue
        
        return formatted_logs
    
    def _format_single_log(self, log: Dict[str, Any], source_system: str) -> Dict[str, Any]:
        """Tek bir logu formatlar"""
        try:
            # Temel alanları kontrol et
            if not isinstance(log, dict):
                self.logger.warning(f"Invalid log format: {log}")
                return None
            
            # Timestamp kontrolü
            timestamp = log.get('timestamp')
            if not timestamp:
                timestamp = datetime.utcnow().isoformat() + 'Z'
            
            # Log türü kontrolü
            log_type = log.get('log_type', 'unknown')
            
            # Mesaj alanı kontrolü
            message = log.get('message', {})
            if not message:
                message = log
            
            # Splunk için standart format
            formatted_log = {
                "timestamp": timestamp,
                "source_system": source_system,
                "log_type": log_type,
                "message": message,
                "raw_log": log  # Orijinal log verisi
            }
            
            return formatted_log
            
        except Exception as e:
            self.logger.error(f"Error formatting single log: {str(e)}")
            return None
    
    def validate_log_structure(self, log: Dict[str, Any]) -> bool:
        """Log yapısını doğrular"""
        required_fields = ['timestamp', 'source_system', 'log_type', 'message']
        
        for field in required_fields:
            if field not in log:
                self.logger.warning(f"Missing required field: {field}")
                return False
        
        return True
    
    def add_metadata(self, log: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Log'a metadata ekler"""
        log_copy = log.copy()
        log_copy['metadata'] = metadata
        return log_copy
    
    def filter_logs_by_type(self, logs: List[Dict[str, Any]], log_type: str) -> List[Dict[str, Any]]:
        """Logları türüne göre filtreler"""
        return [log for log in logs if log.get('log_type') == log_type]
    
    def filter_logs_by_timestamp(self, logs: List[Dict[str, Any]], start_time: str, end_time: str = None) -> List[Dict[str, Any]]:
        """Logları timestamp'e göre filtreler"""
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            
            if end_time:
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            else:
                end_dt = datetime.utcnow()
            
            filtered_logs = []
            for log in logs:
                try:
                    log_timestamp = log.get('timestamp')
                    if log_timestamp:
                        log_dt = datetime.fromisoformat(log_timestamp.replace('Z', '+00:00'))
                        if start_dt <= log_dt <= end_dt:
                            filtered_logs.append(log)
                except Exception as e:
                    self.logger.warning(f"Error parsing log timestamp: {str(e)}")
                    continue
            
            return filtered_logs
            
        except Exception as e:
            self.logger.error(f"Error filtering logs by timestamp: {str(e)}")
            return logs
