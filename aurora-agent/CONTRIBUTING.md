# Katkı Rehberi

Aurora Agent'e katkıda bulunmak için aşağıdaki adımları izleyin.

1. **Klonla ve Hazırlık Yap**
   - `python -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`

2. **Kod Kalitesi**
   - Lint: `make lint`
   - Test: `make test`
   - CI eşleniği: `make ci`

3. **Plan ve Kanban**
   - `PLAN.md` üzerinden ilerlemeyi takip edin, `python scripts/next.py` ile sıradaki adımı tamamlayın.
   - Kanban politikaları için `docs/KANBAN.md` belgesine bakın.

4. **Pull Request**
   - PR açıklamalarında ilgili rolü ve kabul kriterlerini belirtin.
   - Gerekirse `python scripts/staff.py --codeowners` ile kadro ve CODEOWNERS dosyalarını güncelleyin.

5. **Davranış Kuralları**
   - Tüm katkılar `CODE_OF_CONDUCT.md` kapsamında değerlendirilir.
