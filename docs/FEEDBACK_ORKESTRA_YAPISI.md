# Feedback Orkestra Ekibi Yapısı

## 1. Amaç ve Kapsam
- Alfa, beta, lansman öncesi ve lansman sonrası dönemlerde proje kararlarını, müşteri deneyimini ve yatırımcı güvenini güçlendirecek geri bildirim döngüsü kurmak.
- Customer panel kullanıcıları, iç personel, yatırımcılar, partnerler, iş danışmanları ve pazarlama ekiplerinden gelen verileri bütüncül biçimde değerlendirmek.
- Her öneriyi somut kanıtlara dayandırarak ölçülebilir aksiyon planlarına çevirmek.

## 2. Paydaş Segmentleri ve Roller
| Segment | Rol | Eklenme Zamanı | Sorumluluklar |
| --- | --- | --- | --- |
| **Customer Panel Kullanıcıları** | Birincil dış kullanıcı sesi | Alfa hazırlık aşaması | Kullanıcı yolculuğu geri bildirimi, kullanım zorluklarının raporlanması, önerilerin önceliklendirilmesine katkı.
| **İç Personel (Staff)** | Operasyonel geri bildirim sağlayıcı | Proje başlangıcı | Ürün ve süreçlerin uygulanabilirliği, teknik/operasyonel risklerin paylaşılması, test planlarının yürütülmesi.
| **Partnerler** | Ekosistem uyum danışmanı | Alfa başlangıcı | Entegrasyon gereksinimleri, partner müşterilerinin beklentileri, ortak pazarlama fırsatları.
| **Yatırımcılar** | Stratejik denetçi ve vizyon sağlayıcı | Beta hazırlık aşaması | KPI hedeflerinin doğrulanması, risk yönetimi önerileri, ROI beklentilerinin iletişimi.
| **İş Danışmanları** | Süreç optimizasyonu uzmanı | Alfa süreci | Regülasyon uyumu, operasyonel verimlilik, ölçeklenebilirlik tavsiyeleri.
| **Pazarlama Ekibi** | Pazar sesi ve iletişim stratejisti | Beta başlangıcı | Mesaj testi, konumlandırma, lansman planlarının optimize edilmesi.

## 3. Aşamalara Göre Katılım ve Odak Alanları
1. **Proje Başlangıcı (T-16 hafta)**
   - Çekirdek ekip: Ürün lideri, operasyon lideri, teknik lider, veri analisti.
   - İç personel ve iş danışmanlarıyla “temel hipotez” atölyesi.
   - Çıktı: Öncelikli varsayımlar, MVP kapsamı, metrik çerçevesi.

2. **Alfa Öncesi (T-12 hafta)**
   - Customer panel adayları seçimi ve NDA süreçleri.
   - Partnerlerle entegrasyon ön çalışması.
   - Yatırımcı bilgilendirme notu: hedef metrikler ve riskler.

3. **Alfa Süreci (T-8 → T-4 hafta)**
   - Haftalık “Feedback Orkestra” toplantıları.
   - Kullanıcılar ve personel için görev bazlı testler (task-based testing, kullanım senaryoları).
   - Öneri skorlama matrisi (Etki, Uygulanabilirlik, Kanıt düzeyi).

4. **Beta Süreci (T-4 → T-1 hafta)**
   - Pazarlama mesaj testleri (A/B, konsept testleri).
   - Yatırımcı paneli: Finansal simülasyonlar ve risk değerlendirmesi.
   - Partner pilotları: Entegrasyon doğrulama raporları.

5. **Lansman ve Sonrası (T0 → T+8 hafta)**
   - Günlük erken uyarı metrik panosu (performans, müşteri desteği, SLA).
   - Tüm segmentlerle 2 haftalık retrospektif oturumlar.
   - Öğrenilen dersler raporu ve backlog güncellemesi.

## 4. Öneri Değerlendirme Süreci
1. **Toplama**
   - Kanallar: Anketler (Likert), yapılandırılmış görüşmeler, müşteri kullanım analitiği, destek kayıtları, yatırımcı/partner oturum notları.
   - Her öneri için minimum veri kümesi: Problemin tanımı, gözlenen etki, önerilen çözüm, destekleyici kanıt.

2. **Ön Eleme (48 saat)**
   - Veri analisti ve ürün lideri tarafından “somutluk kontrol listesi”:
     - Ölçülebilir metrikle bağlantısı var mı?
     - Tekrarlayan bir sinyal mi (≥3 bağımsız kaynak)?
     - Hipotez testine uygun mu?

3. **Test Tasarımı (1 hafta)**
   - Uygun test türleri: Kullanılabilirlik testi, A/B testi, kohort analizi, finansal modelleme, operasyonel pilot.
   - Başarı kriterleri: Etki büyüklüğü, hata azalımı, memnuniyet artışı, maliyet/ROI göstergeleri.

4. **Skorlama ve Önceliklendirme**
   - Skor Kartı: `Etki (1-5) × Kanıt Düzeyi (1-5) × Uygulanabilirlik (1-5)`.
   - Kritik eşiğin altındaki öneriler backlog’a “izlemeye alınan” olarak işlenir.
   - Skor 80 üstü öneriler için hızlı uygulama süreci.

5. **Karar ve Aksiyon**
   - Orkestra şefi moderasyonuyla iki haftada bir karar oturumu.
   - Onaylanan aksiyonların RACI tablosu ve teslim tarihleri.
   - Test sonuçları ve karar gerekçeleri Confluence/Notion üzerinde arşivlenir.

## 5. Organizasyon ve Yönetim Modeli
- **Orkestra Şefi (Program Yöneticisi)**: Süreci uçtan uca yönetir, toplantıları planlar, raporlamayı konsolide eder.
- **Ürün Sahibi**: Backlog güncellemeleri ve teslim takibi.
- **Veri Analisti**: Ölçüm tasarımı, veri doğrulama, metrik panolar.
- **Müşteri Araştırma Uzmanı**: Görüşme kılavuzları, panel yönetimi.
- **Partner İlişkileri Lideri**: Partner ve yatırımcı oturumları koordinasyonu.
- **Pazarlama Lead**: Mesaj testleri, lansman içerikleri.

### Toplantı Yapısı
| Sıklık | Toplantı | Katılımcılar | Amaç |
| --- | --- | --- | --- |
| Haftalık | Operasyonel Senkron | Çekirdek ekip + ilgili paydaşlar | Test durum güncellemesi, riskler.
| 2 Haftalık | Karar Oturumu | Orkestra şefi, ürün sahibi, veri analisti, yatırımcı temsilcisi | Öneri skorlama sonuçları, aksiyon kararları.
| Aylık | Strateji Revizyonu | Üst yönetim, pazarlama, partner liderleri | Yol haritası uyumu, kaynak planlaması.

## 6. Ölçümleme ve Raporlama
- **Metrikler**
  - Net Promoter Score (NPS), Görev Tamamlama Süresi, Hata oranı, Destek bileti hacmi.
  - Finansal: CAC/LTV projeksiyonu, yatırımcı memnuniyet skoru.
  - İç süreç: SLA uyumu, aksiyon tamamlama oranı.
- **Raporlama Araçları**: BI panosu (Looker/Power BI), haftalık özet e-postaları, aylık yatırımcı raporları.
- **İzlenebilirlik**: Her öneri için benzersiz ID, test sonuçları ve karar logu.

## 7. Risk Yönetimi ve Kontrol Noktaları
- Paydaş bağlılığını korumak için net teşvikler (panel ödülleri, bilgi paylaşımı).
- Veri gizliliği ve sözleşmeler: NDA, veri işlem sözleşmeleri, erişim kontrol listeleri.
- Beklenmedik sonuçlar için “çevik sprint” tamponu (2 hafta esnek kapasite).

## 8. İletişim Planı
- **İç İletişim**: Slack kanal seti (#feedback-orkestra, #test-sonuclari), haftalık notlar.
- **Dış İletişim**: Panel bültenleri, yatırımcı brifingleri, partner roadshow’ları.
- **Yükseltme Mekanizması**: Kritik riskler için 24 saat içinde üst yönetime eskalasyon.

## 9. Başlangıç Yol Haritası (Örnek)
| Hafta | Aktivite | Çıktı |
| --- | --- | --- |
| T-16 | Orkestra şefi atanması, çekirdek ekibin kurulması | Organizasyon şeması, charter.
| T-14 | Somutluk kontrol listesi ve skor kartı taslağı | Onaylı süreç dokümanı.
| T-12 | Panel ve partner seçimleri, NDA’lar | Katılımcı listesi.
| T-10 | Alfa test planı, ölçüm altyapısı | Test planı, dashboard şablonu.
| T-8  | Alfa başlatma, ilk veri toplama | Haftalık rapor 1.
| T-4  | Beta hazırlık, pazarlama testleri | Beta raporu, pazarlama önerileri.
| T-1  | Lansman provası, yatırımcı güncellemesi | Lansman check-list.
| T+2 | Post-lansman retrosu, backlog güncellemesi | Öğrenilen dersler raporu.

## 10. Sürekli İyileştirme
- Her çeyrekte süreç denetimi: KPI performansı, paydaş geri bildirimi, metodoloji güncellemeleri.
- Deney tasarımları için bilgi havuzu: Test sonuçlarının kataloglanması, tekrar kullanım.
- Eğitim programı: Yeni katılımcılar için onboarding rehberi, veri okuryazarlığı çalışmaları.

## 11. Ekip Kültürü ve Bilgi Yönetimi
- **Ekip Kültürü Günlüğü**: Her sprint sonunda ekip, "en iyi nasıl çalıştık" anlatılarını, karşılaşılan engelleri ve çözüm yollarını ortak bir günlükte toplar. Bu günlük, davranışsal sezgileri, ritüelleri ve iletişim kalıplarını canlı tutar.
- **Know-How Defteri**: Somut bir konuda yeni bir yaklaşım veya araç geliştirildiğinde, test sonuçları ve uygulanabilirlik adımlarıyla birlikte deftere eklenir. Başlık, tarih, sorumlu kişi ve ilgili metrikler mutlaka belirtilir.
- **Onay Akışı**: Yeni bir kayıt açıldığında orkestra şefi ve konu uzmanı tarafından 48 saat içinde doğrulanır. Gerekirse ek testler planlanır ve sonuçları deftere bağlanır.
- **Erişim ve Sürümleme**: Bilgi bankası, paylaşılan bir bilgi yönetim aracı (Notion, Confluence vb.) üzerinde sürüm kontrollü tutulur. Her güncelleme için değişiklik notu ve referans test ID'si eklenir.
- **Yeni Üyeler İçin Kullanım**: Onboarding sürecinin bir parçası olarak ekip kültürü günlüğü ve know-how defteri gözden geçirilir; yeni gelenler önceki öğrenimleri hızla içselleştirir.
- **Kurumsal Hazine Yaklaşımı**: Kayıtlı bilgi, firmanın entelektüel sermayesi kabul edilir. Erişim politikaları, kritik bilgiyi korurken ekip içi paylaşımı teşvik edecek şekilde tanımlanır.

---
Bu yapı, orkestra şefi tarafından yönetilerek tüm paydaşlardan gelen önerilerin sistematik biçimde toplanması, test edilmesi ve sayısallaştırılarak karar süreçlerine entegre edilmesini sağlar.
