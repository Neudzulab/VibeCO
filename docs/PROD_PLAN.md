# Prod Plan (Günlük Stabilizasyon)

Bu plan, prod ortamı için **günlük sağlık**, **log anomali**, **SLO/bütçe** ve **tech-radar** kontrollerini otomatik yürütür.

## Günlük Akış (her gün 06:00 TRT ~ 03:00 UTC)
- Health check → `configs/prod_targets.yaml`
- Log taraması → `configs/log_rules.yaml`
- SLO / Error-Budget → `docs/RUNBOOKS/SLO.md`
- Tech Radar → `configs/tech_feeds.yaml`
- Rapor → `reports/daily/YYYY-MM-DD.md`
- Eşik aşıldıysa Issue aç + (opsiyonel) Slack bildirimi

## Checklist
- [ ] Health end-point’ler tanımlı ve yetkiler hazır
- [ ] Log kaynakları belirlendi / dış sistem entegrasyonu
- [ ] SLO metrikleri ve hedefler tanımlı
- [ ] Tech-radar kaynakları net
- [ ] Bildirim kanalı (Slack/Email) ayarlı
