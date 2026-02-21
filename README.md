# VibeCO
VibeCO, endpoint doğrulama raporundan sağlık skoru üreten küçük bir Python aracıdır.

## Çalıştırma
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m vibeco.health_score tests/fixtures/sample_report.json
```

Komut çıktısı: `total=<n> failures=<n> health_score=<0-100>`
