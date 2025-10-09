# Ekip Kültürü Günlüğü ve Know-How Defteri Stratejisi

## 1. Amaç
- Tüm orkestralarda öğrenme döngülerini görünür, ölçülebilir ve tekrar kullanılabilir hale getirmek.
- Ekip kültürünü ritüeller, değerler ve davranışsal sinyaller üzerinden sürekli olarak güncellemek.
- Teknik ve operasyonel know-how'ı kurumsal hafızaya dönüştürmek; yeni üyelerin hızla uyumlanmasını sağlamak.

## 2. Kapsam
| Orkestra | Öncelik | Kültür Odağı | Know-How Odağı |
| --- | --- | --- | --- |
| Feedback Orkestra | Yüksek | Paydaş senkronizasyon ritüelleri, karar şeffaflığı | Test sonuçları, öneri skor kartları, metrik panolar |
| Core Product Orkestrası | Yüksek | Sprint retro içgörüleri, müşteri empatisi | Kod standartları, mimari karar kayıtları |
| Growth Orkestrası | Orta | Deney kültürü, hızlı iterasyon prensipleri | Deney setup rehberleri, kanal optimizasyonu |
| Operasyon Orkestrası | Orta | Vardiya ritüelleri, kriz senaryosu tatbikatları | SOP'lar, otomasyon script'leri |
| Destek Orkestrası | Orta | Empati ve çözüm ritüelleri | Makro template'leri, vaka eskalasyon kılavuzları |

## 3. Ekip Kültürü Günlüğü Uygulaması
1. **Ritüel Tasarımı**
   - Her orkestrada sprint kapanışının bir parçası olarak 30 dakikalık "Kültür Retrosu" oturumu.
   - Oturum çıktıları: "En iyi çalıştığımız an", "Zorlandığımız alan", "Bir dahaki sprintte deneyelim" başlıkları.
2. **Format**
   - Şablon: Tarih, sprint adı, katılımcılar, anlatı bölümü (maks. 500 kelime), davranışsal sinyal etiketleri (#güven, #şeffaflık, #odak vb.).
   - Depolama: Paylaşılan bilgi yönetim aracı (Notion/Confluence) + aylık PDF arşivi.
3. **Sahiplik**
   - Orkestra şefi: Moderasyon ve yayın.
   - İnsan ve Kültür temsilcisi: Etiketlerin standardizasyonu ve ekipler arası karşılaştırma.
4. **Metrikler**
   - Katılım oranı (%), "eyleme dönen içgörü" sayısı, ekip NPS korelasyonu.
   - Çeyreklik trend analizi: Davranışsal sinyallerdeki değişim (ör. #şeffaflık etiketli notların % değişimi).

## 4. Know-How Defteri Uygulaması
1. **Kayıt Döngüsü**
   - Yeni bir teknik çözüm, süreç iyileştirmesi veya öğrenme her doğduğunda 48 saat içinde kayıt.
   - Şablon: Başlık, tarih, sorumlu kişi, bağlam (story/epic ID), çözüm adımları, test sonuçları, yeniden kullanılabilirlik seviyesi.
2. **Doğrulama**
   - Konu uzmanı + orkestra şefi 72 saat içinde inceleyip "Onaylandı / Geliştirme Gerekiyor" statüsü verir.
   - Gerektiğinde ek deney veya ölçüm planlanır ve kayıt güncellenir.
3. **Sınıflandırma ve Arama**
   - Taxonomy: Alan (ürün, veri, altyapı, operasyon), etki alanı (performans, kalite, maliyet), anahtar kelimeler.
   - Haftalık "bilgi keşif" oturumu: Yeni kayıtlar paylaşılır, farklı orkestralara aktarım planlanır.
4. **Ölçüm**
   - Kullanım oranı: Diğer orkestralar tarafından yeniden kullanılan kayıt sayısı.
   - Güncel kalma: 90 günü geçen kayıtlar için otomatik "gözden geçir" görevi.

## 5. Entegrasyon ve Otomasyon
- **Tek Kaynak**: Kültür günlüğü ve know-how defteri tek bir bilgi yönetimi alanında, ilişkilendirilmiş veritabanlarıyla tutulur.
- **API/Entegrasyonlar**: Issue tracker (Jira), test sonuç panoları ve metrik sistemleriyle çift yönlü link.
- **Bildirimler**: Slack entegrasyonu ile yeni kayıt ve güncellemelerde #orchestra-learning kanalına otomatik duyuru.
- **Analitik**: Aylık veri çekimi ile kültür-davranış metrikleri ile KPI performans korelasyonu.

## 6. Eğitim ve Onboarding
- İlk hafta: Yeni üyeler için kültür günlüğü "highlight" turu + know-how defteri hızlı başlangıç rehberi.
- İlk ay: Mentor eşliğinde bir know-how kaydı oluşturma görevi.
- Sürekli: Çeyreklik bilgi paylaşım günü; en etkili 3 kültür içgörüsü ve 3 know-how kaydı sunumu.

## 7. Yarım Kalan Proje Devir Planı
### 7.1. İlk 10 Günlük İnceleme
| Gün | Aktivite | Çıktı |
| --- | --- | --- |
| 1-2 | Mevcut durum brifingi, paydaş haritalaması | Paydaş listesi, iletişim planı |
| 3-4 | Kod tabanı ve mimari keşif | Sistem diyagramı, kritik bağımlılıklar |
| 5-6 | Süreç ve ritim analizi (ritüeller, karar mekanizmaları) | Ritim değerlendirme notu |
| 7 | Kültür günlüğü & know-how defteri taraması | Önceki öğrenim listesi |
| 8-9 | Açık backlog ve hedef incelemesi | Önceliklendirilmiş hedef tablosu |
| 10 | Risk ve fırsat değerlendirmesi | Risk matrisi, hızlandırma önerileri |

### 7.2. Strateji ve Yol Haritası Geliştirme
1. **Değerlendirme Raporu**
   - Mevcut kodlama dilinin avantaj/dezavantaj analizi (performans, ekip yetkinliği, ekosistem desteği).
   - Alternatif dil veya teknolojiye geçiş maliyet modeli (kısa, orta, uzun vade senaryoları).
   - Teknik borç ve tamamlanması gereken kritik modüller.
2. **Karar Noktaları**
   - Devam: Avantaj skorunun (performans + ekip yetkinliği + entegrasyon kolaylığı) ≥ 7/10 olduğu durumda mevcut dilde kal.
   - Geçiş: Avantaj skoru düşükse, geçiş maliyeti ≤ 1.5× tahmini MVP tamamlama maliyeti ise refactor/yeniden yazım planı.
   - Yeniden Kurulum: Teknik borç/ölçeklenebilirlik riski kritikse (SEV-1) ve geçiş maliyeti < 2×, yeni mimari kurulum kararı.
3. **Yol Haritası**
   - `Sprint 1`: Güvenlik açıkları ve kritik hataların kapatılması.
   - `Sprint 2`: Temel mimari düzeltmeler + otomasyon pipeline'larının ayağa kaldırılması.
   - `Sprint 3`: Eksik modüllerin tamamlanması + entegre testler.
   - `Sprint 4`: Performans optimizasyonu + kullanıcı kabul testleri.
   - Her sprintte kültür günlüğü ve know-how kayıtlarıyla öğrenimlerin belgelenmesi.

### 7.3. Yönetim ve İletişim Ritüelleri
- Haftalık durum toplantısı: Risk, ilerleme, karar ihtiyaçları.
- İki haftada bir strateji revizyonu: Alternatif dil değerlendirmesi ve maliyet modeli güncellemesi.
- Aylık paydaş demosu: Orkestra vizyonu, hedeflere ilerleme, öğrenim paylaşımları.
- Kültür günlüğü özel bölümü: "Devir sonrası öğrendiklerimiz".

## 8. Başarı Ölçütleri
| Alan | Metrik | Hedef |
| --- | --- | --- |
| Kültür Günlüğü | Katılım oranı | ≥ %85 |
| Kültür Günlüğü | Eyleme dönen içgörü sayısı | Sprint başına ≥ 2 |
| Know-How Defteri | Yeni kayıt sayısı | Haftalık ≥ 3 |
| Know-How Defteri | Yeniden kullanım oranı | ≥ %30 |
| Proje Devir | Kritik risklerin kapanma süresi | ≤ 2 sprint |
| Proje Devir | MVP tamamlanma sapması | ≤ %10 |

## 9. Sürekli İyileştirme
- Çeyreklik "bilgi ekosistemi" retrosu: Kültür ve know-how kayıtlarının etkinliği değerlendirilir.
- Otomatik analiz: NLP ile kültür günlüklerinden duygu analizi çıkarımı, trend raporları.
- Dış benchmark: Yılda bir benzer ölçekli ekiplerle kıyaslama çalışması.
- Güncellenen standartlar: Yeni teknolojiler, ritüeller ve metrikler deftere eklenir; kullanılmayan şablonlar emekli edilir.

---
Bu strateji, orkestralar arası öğrenme akışını hızlandırarak yarım kalan projelerin hedefe yeniden hizalanmasını ve kurumsal hafızanın güçlenmesini sağlar.
