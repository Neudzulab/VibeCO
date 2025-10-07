# VibeCO
Vibe Coding Orchestrator

Nasıl kullanacağız (özet)

GitHub’ta yeni public repo aç → bu ZIP’i yükle veya localde açıp push et.

python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

make test ile temel testleri çalıştır.

Planı ilerletmek için:

python scripts/next.py --dry-run (gösterim)

python scripts/next.py --lock (adımı üzerine al, çakışma kilidi koy)

Çalış bittiğinde PR → review → make ci geçince merge.

Agent önerileri için GitHub Issues → Agent Proposal (RFC) şablonunu kullan.

Şablonun çekirdeği

PLAN.md: “Tek gerçeklik.” Adımlar [ ] / [x] ile işaretlenir, STEP-00X ID’leri ve owner/depends_on alanları var.

scripts/next.py: İlk tamamlanmamış adımı işaretler; --lock/--unlock ile çakışmayı önler.

.github/workflows/ci.yml: PR ve push’ta lint+test koşar.

agents/ ve roles/: Lead, Researcher, Coder, Reviewer, QA rollerinin alanları; agent_config.yaml orkestrasyon ipuçları.

ISSUE_TEMPLATE/: Task ve Agent Proposal (RFC) şablonları.

CODEOWNERS: İnceleme akışını rollerle bağlar.

tests/ + src/: En basit örnek ve test—CI hattı hemen yeşersin.

“Next” akışı (hafif sihir)

Next → PLAN.md’deki ilk [ ] adımı [x] yapar (isteğe göre lock bırakır).

Bu repo, planın yapıcısı: Planı yazıyor, ilerletiyor, kilitliyor, testlerle doğruluyor.

Agent’lar yalnızca kendi lock’ladıkları adımları alır; kilit kalkmadan yeni adım yok → çatışma yok.

Codex/Agent entegrasyonu

Codex benzeri bir orkestratör bu repodaki PLAN.md’yi “truth source” olarak okuyabilir; agents/agent_config.yaml içindeki:

strategy: fifo (ya da priority’e evrilebilir),

conflict_avoidance: file_lock,

next_command: python scripts/next.py
alanlarıyla tetikleyici komut netleştirilmiştir.

Agent, bir adımı üstlenirken ilgili Task issue’sunu bu STEP-ID ile açar, kabul kriterlerini ve test stratejisini doldurur.

Disiplin (kısa ilkeler)

PR’lar: 1 Reviewer + 1 QA onayı şart (CONTRIBUTING.md).

Her adım “tanımlı test” içerir; CI geçmeyen birleşmez.

README rozetleriyle ilerleme görünür; plan değişiklikleri PR ile akar.

Bundan sonra?

İstersen birlikte:

PLAN.md’yi senin projene göre detaylandıralım (gereksinimler, POC hedefleri, kabul kriterleri).

GitHub Actions’a otomatik “progress badge” güncellemesi ekleyelim.

“priority lanes” ve “blocked-by” etiketleriyle depends_on’u Issue otomasyonuna bağlayalım.
