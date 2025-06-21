#!/usr/bin/env python3
"""
ERP Log Collector - Infor CloudSuite ve IFS Applications log toplama sistemi

Bu uygulama, ERP sistemlerinden log verilerini toplar ve Splunk'a gönderir.
"""

import sys
import argparse
import logging
from pathlib import Path

# Proje kök dizinini Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent))

from app.src.scheduler import LogScheduler


def main():
    """Ana uygulama fonksiyonu"""
    parser = argparse.ArgumentParser(
        description="ERP Log Collector - Infor CloudSuite ve IFS Applications log toplama sistemi"
    )
    
    parser.add_argument(
        "--config",
        default="app/config/config.yaml",
        help="Yapılandırma dosyası yolu (varsayılan: app/config/config.yaml)"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Bağlantıları test et ve çık"
    )
    
    parser.add_argument(
        "--once",
        action="store_true",
        help="Tek seferlik log toplama yap ve çık"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        help="Log toplama aralığı (dakika)"
    )
    
    args = parser.parse_args()
    
    try:
        # Scheduler'ı başlat
        scheduler = LogScheduler(args.config)
        
        # Test modu
        if args.test:
            print("Bağlantı testleri başlatılıyor...")
            scheduler.test_connections()
            return
        
        # Tek seferlik çalıştırma
        if args.once:
            print("Tek seferlik log toplama başlatılıyor...")
            scheduler.collect_and_send_logs()
            return
        
        # Aralık değiştirme
        if args.interval:
            scheduler.config['log_collector']['interval_minutes'] = args.interval
            print(f"Log toplama aralığı {args.interval} dakika olarak ayarlandı")
        
        # Normal çalıştırma
        print("ERP Log Collector başlatılıyor...")
        print("Çıkmak için Ctrl+C tuşlayın")
        scheduler.start()
        
    except KeyboardInterrupt:
        print("\nUygulama kullanıcı tarafından durduruldu")
    except Exception as e:
        print(f"Hata: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
