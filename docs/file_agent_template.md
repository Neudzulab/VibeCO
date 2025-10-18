# Dosya Agent Kılavuzu Şablonu

- Eşik: Otomatik kılavuz gereksinimi `wc -l` çıktısına göre 120 satırı aşan veya karmaşık
  akışlar içeren dosyalar için tetiklenir.
- Her modülün en üstünde aşağıdaki bölümler Markdown ya da çok satırlı yorum olarak
  yer almalıdır:

```
Amaç:
- Modülün ana sorumluluğu ve dışa bağımlılıkları.

Ana Akış:
- Birincil fonksiyonların/endpointlerin birbirleriyle etkileşimi.

İlgili Testler:
- Otomatik testlerin adı veya kapsamı; test yoksa manuel doğrulama notu.
```

- Bölümler kısa, madde işaretli ve güncel tutulmalıdır; önemli API/CLI değişikliklerinde
  ilgili maddeleri güncelleyin.
- Yeni dosyalar eklerken bu şablonu PR açıklamasında referans verin ve varsa test
  bağlantılarını ekleyin.
