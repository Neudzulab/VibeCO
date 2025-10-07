# Production plan (daily stabilisation)

This plan automates **daily health**, **log anomaly**, **SLO/budget**, and **tech radar** checks for the production environment.

## Daily flow (every day 06:00 TRT ~ 03:00 UTC)
- Health check → `configs/prod_targets.yaml`
- Log scan → `configs/log_rules.yaml`
- SLO / error budget → `docs/RUNBOOKS/SLO.md`
- Tech radar → `configs/tech_feeds.yaml`
- Report → `reports/daily/YYYY-MM-DD.md`
- When thresholds are exceeded, open an issue and optionally send a Slack notification

## Checklist
- [ ] Health endpoints defined with correct permissions
- [ ] Log sources identified / external systems integrated
- [ ] SLO metrics and targets documented
- [ ] Tech radar sources confirmed
- [ ] Notification channel (Slack/Email) configured
