# Know-How Defteri Stratejisi

## 1. Amaç
- Teknik ve operasyonel bilgiyi kurumsal hafızaya dönüştürmek.
- Yeni üyelerin hızla uyumlanmasını kolaylaştırmak.
- Yeniden kullanılabilir çözümlerle orkestralar arası öğrenme akışını artırmak.

## 2. Kapsam
| Orkestra | Öncelik | Know-How Odağı |
| --- | --- | --- |
| Feedback Orkestrası | Yüksek | Test sonuçları, öneri skor kartları, metrik panolar |
| Core Product Orkestrası | Yüksek | Kod standartları, mimari karar kayıtları |
| Growth Orkestrası | Orta | Deney setup rehberleri, kanal optimizasyonu |
| Operasyon Orkestrası | Orta | SOP'lar, otomasyon script'leri |
| Destek Orkestrası | Orta | Makro template'leri, vaka eskalasyon kılavuzları |

## 3. Uygulama Döngüsü
1. **Kayıt**
   - Yeni teknik çözüm veya süreç iyileştirmesi 48 saat içinde kaydedilir.
   - Şablon alanları: Başlık, tarih, sorumlu kişi, bağlam (story/epic ID), çözüm adımları, test sonuçları, yeniden kullanılabilirlik seviyesi.
2. **Doğrulama**
   - Konu uzmanı ve orkestra şefi 72 saat içinde "Onaylandı / Geliştirme Gerekiyor" statüsü verir.
   - Gerektiğinde ek deney veya ölçüm planlanır ve kayıt güncellenir.
3. **Sınıflandırma ve Paylaşım**
   - Taxonomy: Alan (ürün, veri, altyapı, operasyon), etki (performans, kalite, maliyet), anahtar kelimeler.
   - Haftalık "bilgi keşif" oturumu: Yeni kayıtlar paylaşılır, orkestralar arası transfer planlanır.

## 4. Ölçümleme
- Diğer orkestralar tarafından yeniden kullanılan kayıt sayısı.
- 90 günden eski kayıtlar için otomatik "gözden geçir" görevi tamamlama oranı.
- Know-how kayıtlarının projelerdeki hızlanmaya etkisini ölçmek için sprint başına tasarruf edilen saat sayısı.

## 5. Entegrasyon Bağlantıları
- Entegrasyon yol haritasındaki bilgi yönetimi alanı ile çift yönlü ilişkilendirilmiş veritabanı yapılandırılır.
- Issue tracker ve test panoları ile API entegrasyonları kurularak kayıtlar otomatik olarak güncellenir.
- Slack entegrasyonu üzerinden yeni veya güncellenen know-how kayıtları #orchestra-learning kanalına bildirilir.

## 6. Eğitim ve Onboarding
- İlk hafta: Know-how defteri hızlı başlangıç rehberi.
- İlk ay: Mentor eşliğinde bir know-how kaydı oluşturma görevi.
- Sürekli: Çeyreklik paylaşım günlerinde en etkili üç know-how kaydının sunulması.

## 7. Sürekli İyileştirme
- Çeyreklik "bilgi ekosistemi" retrosu ile defterin etkinliği değerlendirilir.
- NLP ve arama analitiği ile kayıtların bulunabilirliği ölçülür, düşük performanslı etiketler güncellenir.
- Yeni teknolojiler, ritüeller ve metrikler düzenli olarak deftere eklenir; kullanılmayan şablonlar emekliye ayrılır.
