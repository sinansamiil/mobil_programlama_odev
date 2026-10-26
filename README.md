# 🎓 Öğrenci Asistanı (Cüzdan & Ders/Ödev Planlayıcısı)

Bu proje, **Mobil Programlama Dersi** kapsamında geliştirilmiş; güvenli kimlik doğrulama, yerel ilişkisel veritabanı (SQLite) ve JSON dosya depolama yeteneklerine sahip tam teşekküllü bir mobil öğrenci asistanı uygulamasıdır.

---

## 🌟 Projenin Amacı ve Özellikleri

Hocanın talep ettiği temel **Kayıt Ol (Register)** ve **Giriş Yap (Login)** gereksinimlerinin yanı sıra, öğrencinin günlük kampüs hayatında gerçekten işine yarayacak iki güçlü modül bir araya getirilmiştir:

1. **💳 Öğrenci Cüzdanı (Finans & Bütçe Yönetimi):**
   - Toplam Bakiye, Toplam Gelir (+) ve Toplam Gider (-) hesaplamaları.
   - Kategorilere göre harcama/gelir ekleme (Yemek, Ulaşım, Kitap & Kırtasiye, Kahve & Sosyal, Burs vb.).
   - Liste üzerinden sola kaydırarak silme (Dismissible).

2. **📝 Ders & Ödev Planlayıcısı (Akademik Takip):**
   - Ders adı, teslim tarihi (`DatePicker`) ve öncelik derecesi (Acil / Orta / Düşük) belirleme.
   - Tamamlanan / Bekleyen görev filtrelemesi.
   - Checkbox ile tek tıkla veritabanında görev durumunu güncelleme.

3. **👋 Kişiselleştirilmiş Karşılama Kartı:**
   - Ana ekranın üstünde modern degrade zeminli karşılama:
     > *"Merhaba, Sinan Şamil Köylü 👋"*
     > *"Bilgisayar Mühendisliği • No: 20241050"*
   - Hızlı bakiye ve bekleyen ödev sayaçları.

4. **💾 JSON & SQLite Kalıcı Veri Depolama:**
   - **SQLite (`sqflite`):** İlişkisel tablolar (`users`, `transactions`, `tasks`) ve `FOREIGN KEY` bağlantısı.
   - **JSON Dosya Depolama (`JsonService`):** Veritabanındaki tüm kayıtları tek tuşla cihazın dosya sistemine (`ogrenci_asistani_yedek.json`) yazar ve ekranda biçimlendirilmiş (pretty-printed) JSON önizlemesi sunar.

---

## 🗄️ Veritabanı Mimarisi (SQLite)

Veritabanı dosyası: `ogrenci_asistani.db`

### 1. `users` Tablosu
| Sütun | Tip | Açıklama |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Kullanıcı ID |
| `name` | TEXT NOT NULL | Ad Soyad (Örn: Sinan Şamil Köylü) |
| `email` | TEXT UNIQUE NOT NULL | E-posta adresi |
| `password` | TEXT NOT NULL | Kullanıcı şifresi |
| `student_number` | TEXT | Öğrenci numarası |
| `department` | TEXT | Öğrencinin bölümü |
| `created_at` | TEXT NOT NULL | Kayıt tarihi |

### 2. `transactions` Tablosu (Finans)
| Sütun | Tip | Açıklama |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | İşlem ID |
| `user_id` | INTEGER (FOREIGN KEY) | Giriş yapan kullanıcının ID'si |
| `title` | TEXT NOT NULL | Açıklama / Başlık |
| `amount` | REAL NOT NULL | Tutar (₺) |
| `type` | TEXT NOT NULL | `income` (Gelir) veya `expense` (Gider) |
| `category` | TEXT NOT NULL | Harcama kategorisi |
| `date` | TEXT NOT NULL | İşlem tarihi |

### 3. `tasks` Tablosu (Ödev & Dersler)
| Sütun | Tip | Açıklama |
|---|---|---|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Görev ID |
| `user_id` | INTEGER (FOREIGN KEY) | Giriş yapan kullanıcının ID'si |
| `course_name` | TEXT NOT NULL | Ders adı (Örn: Mobil Programlama) |
| `title` | TEXT NOT NULL | Ödev açıklaması |
| `due_date` | TEXT NOT NULL | Son teslim tarihi |
| `priority` | TEXT NOT NULL | `Yüksek`, `Orta`, `Düşük` |
| `is_completed` | INTEGER NOT NULL (0 / 1) | Tamamlandı mı? |

---

## 📂 Proje Dizin Yapısı

```
lib/
├── main.dart                      # Uygulama başlangıcı, tema ve platform desteği
├── models/
│   ├── user_model.dart            # Öğrenci kullanıcı modeli
│   ├── transaction_model.dart     # Gelir/Gider modeli
│   └── task_model.dart            # Ders/Ödev modeli
├── database/
│   ├── db_helper.dart             # SQLite CRUD işlemleri ve demo veri yükleyici
│   └── json_service.dart          # JSON dosyası oluşturma ve dışa aktarma servisi
├── screens/
│   ├── login_screen.dart          # Giriş ekranı (Beni Hatırla + Hızlı Demo Girişi)
│   ├── register_screen.dart       # Kayıt ekranı (Validasyonlar + SQLite kaydı)
│   └── home_screen.dart           # Dashboard (Üst kart, Cüzdan, Ödevler, Profil & JSON)
└── widgets/
    ├── custom_text_field.dart     # Şık form girdi bileşeni
    ├── add_transaction_modal.dart # Gelir/Gider ekleme alt penceresi
    └── add_task_modal.dart        # Yeni ödev ekleme alt penceresi
```

---

## 🚀 Projeyi Çalıştırma

Projeyi emülatörde, fiziksel telefonda veya Windows masaüstünde çalıştırmak için terminalde şu komutları kullanabilirsiniz:

```bash
# Bağımlılıkları yükle
flutter pub get

# Testleri çalıştır
flutter test

# Uygulamayı başlat
flutter run
```

---

## 💡 Hocaya Sunum İpuçları
1. **Kayıt Akışı:** Önce **Kayıt Ol** ekranına giderek kendi bilgilerinizi (Sinan Şamil Köylü vb.) yazın. Şifre eşleşme ve e-posta kontrollerini hocaya gösterin.
2. **Giriş & Beni Hatırla:** Kayıt olunan bilgilerle giriş yapın, **Beni Hatırla** kutucuğunun çalıştığını gösterin.
3. **Cüzdan Testi:** Bir gelir (Örn: 500 TL Harçlık) ve gider ekleyip bakiyenin anında `SUM` formülüyle güncellendiğini gösterin.
4. **Ödev Tamamlama:** "Mobil Programlama Ödevi" görevine tik atarak veritabanında `is_completed` durumunun değiştiğini gösterin.
5. **JSON Dışa Aktarma:** "Yönetim & JSON" sekmesine geçip **"Verileri JSON Dosyası Olarak Kaydet & İncele"** butonuna basarak, hocanın istediği JSON dosyasının oluşturulduğunu ve içeriğini canlı olarak gösterin!
