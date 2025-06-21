# ERP Log Collector

Infor CloudSuite ve IFS Applications ERP sistemlerinden **sistem logları** ve **audit logları** toplayan ve Splunk'a gönderen Python uygulaması.

**Not:** Bu uygulama ERP sistemlerinden gelen logları toplar ve Splunk'a iletir. Uygulamanın kendi logları değil, ERP sistemlerinin logları gönderilir.

## Özellikler

- **IFS Applications** sistem ve audit loglarını toplama
- **Infor CloudSuite** sistem ve audit loglarını toplama
- **Splunk HEC** entegrasyonu
- **Zamanlanmış çalışma** (varsayılan: 5 dakika)
- **Mock veri desteği** (geliştirme/test için)
- **Modüler yapı** (Logex mantığına benzer)
- **Güvenli yapılandırma** (.env desteği)
- **Yapılandırılabilir parametreler**

## Hızlı Başlangıç

### Kurulum

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/Huseyinn1/splunk-erp-logger.git
cd splunk-erp-logger
```

2. **Sanal ortam oluşturun:**
```bash
python -m venv env
env\Scripts\activate  # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Environment variables yapılandırın:**
```bash
# .env.template dosyasını kopyalayın
copy .env.template .env

# .env dosyasını düzenleyin ve kendi bilgilerinizi girin
notepad .env  # Windows
# veya
nano .env     # Linux/Mac
```

**Önemli:** `.env.template` dosyası güvenli bir şekilde git'e eklenmiştir. Bu dosyayı kopyalayıp `.env` olarak adlandırarak kendi bilgilerinizi girebilirsiniz. `.env` dosyası `.gitignore`'da yer aldığı için git'e commit edilmez.

5. **Test edin:**
```bash
python main.py --test
```

### Kullanım

```bash
# Tek seferlik çalıştırma
python main.py --once

# Zamanlanmış çalışma (5 dakika aralıkla)
python main.py

# Özel aralık (1 dakika)
python main.py --interval 1
```

## Yapılandırma

### Environment Variables (.env)

Hassas bilgiler için `.env` dosyası kullanın:

```bash
# Splunk HEC
SPLUNK_HEC_URL=https://127.0.0.1:8088/services/collector
SPLUNK_HEC_TOKEN=your-hec-token

# IFS Applications
IFS_API_BASE_URL=https://ifs.example.com/api
IFS_USERNAME=ifs_user
IFS_PASSWORD=ifs_password

# Infor CloudSuite
INFOR_API_BASE_URL=https://infor.example.com/api
INFOR_USERNAME=infor_user
INFOR_PASSWORD=infor_password

# Application
LOG_INTERVAL_MINUTES=5
USE_MOCK_DATA=true
```

### config.yaml (Varsayılan Değerler)

```yaml
log_collector:
  interval_minutes: 5
  use_mock_data: true

splunk:
  sourcetype: "erp_logs"
  index: "main"
```

## Splunk Sorguları

```spl
# Tüm ERP logları
sourcetype="erp_logs"

# IFS sistem logları
sourcetype="erp_logs" source_system="IFS Applications"

# Hata logları
sourcetype="erp_logs" message.EntryType="ERROR"
```

## Proje Yapısı

```
splunk-erp-logger/
├── app/
│   ├── config/config.yaml     # Yapılandırma
│   ├── logs/                  # Uygulama logları (otomatik oluşur)
│   ├── mock_data/             # Mock veriler
│   └── src/                   # Kaynak kodlar
├── .env                       # Environment variables (git'e commit edilmez)
├── .env.template              # Environment variables şablonu
├── main.py                    # Ana uygulama
├── test_splunk.py            # Test scripti
├── README.md                 # Bu dosya
└── DOCUMENTATION.md          # Detaylı dokümantasyon
```

**Not:** `app/logs/` klasörü ve `app.log` dosyası uygulama çalıştırıldığında otomatik olarak oluşturulur.

## Detaylı Bilgi

Kapsamlı kullanım kılavuzu ve teknik detaylar için [DOCUMENTATION.md](DOCUMENTATION.md) dosyasını inceleyin.

## Test Sonuçları

- ✅ Environment variables yükleme
- ✅ Mock veri okuma
- ✅ Log formatlama  
- ✅ Splunk HEC bağlantısı
- ✅ Zamanlanmış çalışma (5 dakika aralıkla)
- ✅ 12 log başarıyla gönderildi
- ✅ Uygulama logları başarıyla Splunk'a iletildi
- ✅ Zamanlama mekanizması 1 dakika aralıklarla çalışıyor
- ✅ IFS ve Infor logları düzenli olarak toplanıyor
- ✅ Splunk HEC entegrasyonu sorunsuz çalışıyor

## Güvenlik

- `.env` dosyası `.gitignore`'da yer alır
- `.env.template` dosyası güvenli şekilde git'e eklenmiştir
- Hassas bilgiler git'e commit edilmez
- Production ortamında SSL sertifikalarını etkinleştirin

## Lisans

Bu proje açık kaynak olarak geliştirilmiştir.