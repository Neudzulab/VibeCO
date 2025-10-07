# aurora-agent

[![CI](https://github.com/VibeCO/aurora-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/VibeCO/aurora-agent/actions/workflows/ci.yml)

Aurora Agent, uzman rollü otomasyon kadrosu ve Kanban akışını birlikte yöneten bir referans projedir. Bu depo, ekip yapılandırması, süreç otomasyonu ve CI hazır bir başlangıç sağlar.

## Hızlı Başlangıç
1. Depoyu klonlayın ve bağımlılıkları yükleyin:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Test ve lint adımlarını çalıştırın:
   ```bash
   make ci
   ```

## Kadro Nasıl Oluşturulur?
Proje gereksinimlerine göre önerilen kadroyu ve CODEOWNERS dosyasını üretmek için:
```bash
python scripts/staff.py
python scripts/gen_codeowners.py
```

## Kanban Nasıl Kullanılır?
Sütun yapısı, WIP limitleri ve kart şablonuna `docs/KANBAN.md` dosyasından erişebilirsiniz.

## Plan Akışı
`PLAN.md`, rollerle eşleştirilmiş adımları içerir. `python scripts/next.py` komutuyla sıradaki adımı tamamlama veya kilitleme işlemlerini yönetebilirsiniz.

## Katkı
- Katkıda bulunmadan önce `CONTRIBUTING.md` ve `CODE_OF_CONDUCT.md` belgelerini inceleyin.
- Görev, hata ve öneri için `.github/ISSUE_TEMPLATE` altındaki şablonları kullanın.
