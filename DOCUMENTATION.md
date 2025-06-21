# ERP Log Collector - Kullanım Kılavuzu

## 🎯 Proje Özeti

Bu proje, **Infor CloudSuite** ve **IFS Applications** ERP sistemlerinden log verilerini toplayan ve **Splunk**'a gönderen Python tabanlı bir uygulamadır.

## ✅ Tamamlanan Özellikler

### 1. Mock Veri Yapısı
- **IFS Applications** sistem ve audit logları
- **Infor CloudSuite** sistem ve audit logları
- Gerçekçi log formatları ve örnek veriler

### 2. Modüler Yapı (Logex Mantığına Benzer)
```
app/src/
├── api_clients/          # API istemcileri
│   ├── ifs_client.py     # IFS API client
│   └── infor_client.py   # Infor API client
├── config.py             # Yapılandırma yöneticisi
├── log_formatter.py      # Log formatlama
├── scheduler.py          # Zamanlayıcı
└── splunk_sender.py      # Splunk HEC gönderici
```

### 3. Güvenli Yapılandırma (.env Desteği)
- Hassas bilgiler .env dosyasında
- Environment variables desteği
- Güvenli token yönetimi

### 4. Yapılandırılabilir Parametreler
- Log toplama aralığı (varsayılan: 5 dakika)
- API URL'leri ve kimlik bilgileri
- Splunk HEC ayarları
- Mock veri kullanımı

### 5. Splunk HEC Entegrasyonu
- HTTP Event Collector desteği
- Token tabanlı kimlik doğrulama
- JSON formatında log gönderimi

## 🚀 Kurulum ve Çalıştırma

### 1. Sanal Ortam Aktifleştirme
```bash
env\Scripts\activate
```

### 2. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 3. Environment Variables Yapılandırması

#### .env Dosyası Oluşturma
Proje kök dizininde `.env` dosyası oluşturun:

```bash
# ERP Log Collector Environment Variables
# Bu dosya hassas bilgileri içerir, git'e commit etmeyin!

# IFS Applications Credentials
IFS_API_BASE_URL=https://ifs.example.com/api
IFS_USERNAME=ifs_user
IFS_PASSWORD=ifs_password

# Infor CloudSuite Credentials
INFOR_API_BASE_URL=https://infor.example.com/api
INFOR_USERNAME=infor_user
INFOR_PASSWORD=infor_password

# Splunk HEC Configuration
SPLUNK_HEC_URL=https://127.0.0.1:8088/services/collector
SPLUNK_HEC_TOKEN=your-hec-token-here
SPLUNK_USERNAME=admin
SPLUNK_PASSWORD=your-splunk-password

# Application Settings
LOG_LEVEL=INFO
LOG_INTERVAL_MINUTES=5
USE_MOCK_DATA=true
```

#### Environment Variables Önceliği
1. `.env` dosyası (en yüksek öncelik)
2. `config.yaml` dosyası (varsayılan değerler)

### 4. Test Modu
```bash
python main.py --test
```

### 5. Tek Seferlik Çalıştırma
```bash
python main.py --once
```

### 6. Zamanlanmış Çalıştırma
```bash
python main.py
```

## 📊 Log Yapısı

Her log kaydı şu alanları içerir:

```json
{
  "timestamp": "2024-06-21T14:00:00Z",
  "source_system": "IFS Applications",
  "log_type": "system",
  "message": {
    "Content": "Log mesajı",
    "EntryType": "ERROR",
    "description": "Açıklama"
  }
}
```

## 🔧 Yapılandırma

### Environment Variables (.env)

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `IFS_API_BASE_URL` | IFS API URL'i | `https://ifs.example.com/api` |
| `IFS_USERNAME` | IFS kullanıcı adı | `ifs_user` |
| `IFS_PASSWORD` | IFS şifresi | `ifs_password` |
| `INFOR_API_BASE_URL` | Infor API URL'i | `https://infor.example.com/api` |
| `INFOR_USERNAME` | Infor kullanıcı adı | `infor_user` |
| `INFOR_PASSWORD` | Infor şifresi | `infor_password` |
| `SPLUNK_HEC_URL` | Splunk HEC URL'i | `https://127.0.0.1:8088/services/collector` |
| `SPLUNK_HEC_TOKEN` | Splunk HEC token'ı | `your-hec-token` |
| `LOG_LEVEL` | Log seviyesi | `INFO` |
| `LOG_INTERVAL_MINUTES` | Log toplama aralığı | `5` |
| `USE_MOCK_DATA` | Mock veri kullanımı | `true` |

### config.yaml (Varsayılan Değerler)

```yaml
log_collector:
  interval_minutes: 5
  use_mock_data: true

splunk:
  sourcetype: "erp_logs"
  index: "main"
  verify_ssl: false
```

## 📈 Splunk'ta Görüntüleme

### Temel Sorgular
```spl
# Tüm ERP logları
sourcetype="erp_logs"

# IFS sistem logları
sourcetype="erp_logs" source_system="IFS Applications" log_type="system"

# Infor audit logları
sourcetype="erp_logs" source_system="Infor CloudSuite" log_type="audit"

# Hata logları
sourcetype="erp_logs" message.EntryType="ERROR"
```

### Dashboard Önerileri
1. **Sistem Durumu Dashboard'u**
   - Log sayıları (sistem/audit)
   - Hata oranları
   - Kaynak sistem dağılımı

2. **Güvenlik Dashboard'u**
   - Kullanıcı giriş logları
   - Audit trail olayları
   - Şüpheli aktiviteler

## 🔄 Gerçek API'ye Geçiş

### 1. Environment Variables Güncelleme
```bash
# .env dosyasında
USE_MOCK_DATA=false
IFS_API_BASE_URL=https://gercek-ifs-sunucu.com/api
IFS_USERNAME=gercek_kullanici
IFS_PASSWORD=gercek_sifre
```

### 2. API Endpoint'leri
- IFS: `/system/logs`, `/audit/logs`
- Infor: `/system/logs`, `/audit/logs`

## 🔒 Güvenlik

### .env Dosyası Güvenliği
- `.env` dosyası `.gitignore`'da yer alır
- Git'e commit edilmez
- Hassas bilgileri içerir

### Production Ortamı
- SSL sertifikalarını etkinleştirin
- Güçlü şifreler kullanın
- Network güvenliğini sağlayın

## 📝 Test Sonuçları

### Başarılı Testler
- ✅ Environment variables yükleme
- ✅ Mock veri okuma
- ✅ Log formatlama
- ✅ Splunk HEC bağlantısı
- ✅ Log gönderimi (12 log başarıyla gönderildi)
- ✅ Zamanlanmış çalışma (5 dakika aralıkla)

### Test Komutları
```bash
# Bağlantı testi
python main.py --test

# Tek seferlik test
python main.py --once

# Splunk test scripti
python test_splunk.py
```

## 🎯 Sonraki Adımlar

### 1. Gerçek API Entegrasyonu
- IFS ve Infor API endpoint'lerini doğrulama
- Kimlik doğrulama yöntemlerini test etme
- Rate limiting ve pagination ekleme

### 2. Kullanıcı Activity Logları
- Kullanıcı etkinlik loglarını ekleme
- Session tracking
- User behavior analytics

### 3. Gelişmiş Özellikler
- Log filtreleme ve dönüştürme
- Alerting ve notification
- Performance monitoring
- Data retention policies

## 📞 Destek

Sorularınız için proje sahibi ile iletişime geçebilirsiniz.

---

**Not:** Bu uygulama Logex mantığına benzer sade ve modüler yapıda geliştirilmiştir. 