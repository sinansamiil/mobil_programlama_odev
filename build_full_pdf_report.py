import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Font Tanımlamaları (Türkçe karakter tam desteği)
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))
pdfmetrics.registerFont(TTFont('Consolas', 'C:/Windows/Fonts/consola.ttf'))
pdfmetrics.registerFont(TTFont('Consolas-Bold', 'C:/Windows/Fonts/consolab.ttf'))

class NumberedCanvas(canvas.Canvas):
    """Her sayfanın üstüne ve altına dinamik başlık ve sayfa numarası ekler"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Arial", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Üst bilgi (Kapak sayfası hariç)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(1.4 * cm, A4[1] - 1.0 * cm, A4[0] - 1.4 * cm, A4[1] - 1.0 * cm)
            self.drawString(1.4 * cm, A4[1] - 0.85 * cm, "Öğrenci Asistanı - Flutter & SQLite Mobil Uygulama Kapsamlı Teknik Raporu")
            self.drawRightString(A4[0] - 1.4 * cm, A4[1] - 0.85 * cm, "Sinan Şamil Köylü | 240211019")
        
        # Alt bilgi
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(1.4 * cm, 1.1 * cm, A4[0] - 1.4 * cm, 1.1 * cm)
        
        self.drawString(1.4 * cm, 0.7 * cm, "Yazılım Mühendisliği Bölümü - Mobil Programlama Dersi Proje Dokümantasyonu")
        page_text = f"Sayfa {self._pageNumber} / {page_count}"
        self.drawRightString(A4[0] - 1.4 * cm, 0.7 * cm, page_text)
        self.restoreState()

def create_report():
    output_pdf = "ogrenci_asistani_detayli_teknik_rapor.pdf"
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=1.4 * cm,
        rightMargin=1.4 * cm,
        topMargin=1.4 * cm,
        bottomMargin=1.6 * cm,
    )

    styles = getSampleStyleSheet()

    # Tipografi ve Renk Paleti Stilleri
    doc_title = ParagraphStyle(
        'DocTitle',
        fontName='Arial-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4,
    )
    doc_subtitle = ParagraphStyle(
        'DocSubtitle',
        fontName='Arial-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#E11D48'),
        spaceAfter=12,
    )
    sec_title = ParagraphStyle(
        'SecTitle',
        fontName='Arial-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )
    subsec_title = ParagraphStyle(
        'SubSecTitle',
        fontName='Arial-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#BE123C'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
    )
    body = ParagraphStyle(
        'Body',
        fontName='Arial',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5,
    )
    th_style = ParagraphStyle(
        'TH',
        fontName='Arial-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white,
    )
    tc_bold = ParagraphStyle(
        'TCBold',
        fontName='Arial-Bold',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor('#0F172A'),
    )
    tc_normal = ParagraphStyle(
        'TCNormal',
        fontName='Arial',
        fontSize=7.6,
        leading=10,
        textColor=colors.HexColor('#334155'),
    )
    tc_prop_name = ParagraphStyle(
        'TCPropName',
        fontName='Consolas-Bold',
        fontSize=7.4,
        leading=9.5,
        textColor=colors.HexColor('#9F1239'),
    )
    tc_prop_desc = ParagraphStyle(
        'TCPropDesc',
        fontName='Arial',
        fontSize=7.4,
        leading=9.8,
        textColor=colors.HexColor('#334155'),
    )
    code_snippet_style = ParagraphStyle(
        'CodeSnippet',
        fontName='Consolas',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#0369A1'),
    )

    story = []

    # ==================== KAPAK & KÜNYE (SAYFA 1) ====================
    story.append(Paragraph("MOBİL PROGRAMLAMA PROJESİ TEKNİK RAPORU", doc_title))
    story.append(Paragraph("Öğrenci Asistanı: Akıllı Kampüs Cüzdanı, Ders & Görev Takip Sistemi", doc_subtitle))

    info_card_data = [
        [
            Paragraph("<b>Öğrenci Adı Soyadı:</b> Sinan Şamil Köylü", body),
            Paragraph("<b>Öğrenci Numarası:</b> 240211019", body),
            Paragraph("<b>Bölüm:</b> Yazılım Mühendisliği", body),
        ],
        [
            Paragraph("<b>Ders:</b> Mobil Programlama", body),
            Paragraph("<b>Framework:</b> Flutter 3.47+ & Dart", body),
            Paragraph("<b>Veritabanı:</b> SQLite (sqflite_ffi) + JSON", body),
        ],
        [
            Paragraph("<b>Mimari:</b> Katmanlı Mimari (Clean Layered)", body),
            Paragraph("<b>Durum Yönetimi:</b> StatefulWidget + setState", body),
            Paragraph("<b>Tasarım Dili:</b> Modern Material 3 & FinTech UI", body),
        ]
    ]
    info_table = Table(info_card_data, colWidths=[6.1 * cm, 6.0 * cm, 6.1 * cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1.2, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    # ==================== 1. BÖLÜM: PROJE ÖZETİ VE AMACI ====================
    story.append(Paragraph("1. Projenin Amacı, Vizyonu ve Çözdüğü Problemler", sec_title))
    p1 = (
        "<b>Öğrenci Asistanı</b>, üniversite öğrencilerinin akademik hayatları boyunca karşılaştıkları iki hayati yönetim "
        "sorununu tek bir entegre mobil platformda çözmek üzere geliştirilmiştir: <b>1) Finansal Harcama & Bütçe Yönetimi</b> "
        "(KYK bursu, aile harçlığı, yemekhane kartı dolumu, kitap/kırtasiye harcamaları) ve <b>2) Akademik Görev & Ders Takibi</b> "
        "(ders ödevleri, laboratuvar raporları, proje teslimleri ve sınav takvimleri)."
    )
    story.append(Paragraph(p1, body))

    p2 = (
        "<b>Öne Çıkan Mühendislik Hedefleri:</b><br/>"
        "• <b>%100 Yerel ve Güvenli Çalışma:</b> Uygulama herhangi bir harici bulut sunucusuna veya internet bağlantısına bağımlı olmadan, "
        "cihaz üzerindeki ilişkisel <b>SQLite</b> motorunda tam performansla çalışır.<br/>"
        "• <b>FinTech Seviyesinde Kullanıcı Deneyimi:</b> Bankacılık uygulamalarında kullanılan tek dokunuşla bakiye gizleme (••••••), "
        "canlı harcama oranı ilerleme çubuğu (progress bar) ve kategorik bütçe dağılım analizi.<br/>"
        "• <b>İlişkisel Veri Bütünlüğü:</b> Kullanıcı tablosu ile işlemler ve görevler arasında yabancı anahtar (Foreign Key) "
        "ve basamaklı silme (ON DELETE CASCADE) güvencesi.<br/>"
        "• <b>JSON Veri Yedekleme & Kod İnceleme:</b> Veritabanındaki tüm ilişkisel verilerin tek dokunuşla standart .json dosyasına "
        "dışa aktarılması (export) ve uygulama içi kod terminaliyle anlık doğrulanabilmesi."
    )
    story.append(Paragraph(p2, body))
    story.append(Spacer(1, 8))

    # ==================== 2. BÖLÜM: MİMARİ VE KLASÖR HİYERARŞİSİ ====================
    story.append(Paragraph("2. Katmanlı Mimari ve Klasör Hiyerarşisi", sec_title))
    p3 = (
        "Proje, endüstri standardı olan <b>Clean Layered Architecture (Katmanlı Mimari)</b> prensiplerine sadık kalınarak "
        "modüler bir yapıda inşa edilmiştir. Kod tabanı işlevlerine göre 4 ana katmana ayrılmıştır:"
    )
    story.append(Paragraph(p3, body))

    arch_table_data = [
        [Paragraph("<b>Katman / Dizin</b>", th_style), Paragraph("<b>İçerik ve Görevi</b>", th_style), Paragraph("<b>Teknik Bileşenler ve Prensipler</b>", th_style)],
        [
            Paragraph("<b>lib/models/</b>", tc_bold),
            Paragraph("<b>UserModel, TransactionModel, TaskModel:</b> Saf Dart sınıfları. Veritabanı tablolarındaki satırları nesneye, nesneleri Map ve JSON yapılarına dönüştürür.", tc_normal),
            Paragraph("toMap(), fromMap(), toJson(), fromJson(), copyWith() metotları. Immutable veri tasarımı.", tc_normal),
        ],
        [
            Paragraph("<b>lib/database/</b>", tc_bold),
            Paragraph("<b>DBHelper:</b> Singleton desenli SQLite yöneticisi. Tablo kurulumu, migration ve SQL sorguları.<br/><b>JsonService:</b> Yerel dosya sistemi (File I/O) ve JSON serileştirme.", tc_normal),
            Paragraph("sqflite, sqflite_common_ffi, path_provider, PRAGMA foreign_keys = ON, aggregate SQL (SUM, COUNT).", tc_normal),
        ],
        [
            Paragraph("<b>lib/screens/</b>", tc_bold),
            Paragraph("<b>LoginScreen, RegisterScreen, HomeScreen:</b> Uygulamanın tam ekran görünümleri. Form doğrulama, sekme navigasyonu ve kullanıcı etkileşimleri.", tc_normal),
            Paragraph("StatefulWidget yaşam döngüsü (initState, dispose, setState), Form GlobalKey, SharedPreferences.", tc_normal),
        ],
        [
            Paragraph("<b>lib/widgets/</b>", tc_bold),
            Paragraph("<b>CustomTextField:</b> Özel animasyonlu ve odaklanmalı input.<br/><b>AddTransactionModal & AddTaskModal:</b> Alttan açılan şık veri giriş pencereleri.", tc_normal),
            Paragraph("showModalBottomSheet, InputDecoration stil kapsülleme, DatePicker, ChoiceChip/ActionChip.", tc_normal),
        ],
    ]
    arch_t = Table(arch_table_data, colWidths=[3.2 * cm, 9.8 * cm, 5.2 * cm])
    arch_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(arch_t)

    # SAYFA 1 BİTİŞİ -> SAYFA 2 BAŞLANGICI
    story.append(PageBreak())

    # ==================== 3. BÖLÜM: VERİTABANI VE İLİŞKİSEL ŞEMA (SAYFA 2) ====================
    story.append(Paragraph("3. SQLite Veritabanı Mimarisi ve İlişkisel Veri Şeması", sec_title))
    p4 = (
        "Uygulamada SQLite veritabanı <b>ogrenci_asistani.db</b> adıyla saklanmakta olup ilişkisel bütünlük "
        "<b>PRAGMA foreign_keys = ON</b> komutuyla garantiye alınmıştır. Bire-çok (1-to-N) ilişki mimarisi uygulanmıştır; "
        "bir kullanıcının birden fazla finans işlemi ve ders görevi olabilir. Kullanıcı silindiğinde basamaklı silme (CASCADE) "
        "sayesinde bağımlı kayıtlar da otomatik olarak temizlenir."
    )
    story.append(Paragraph(p4, body))
    story.append(Spacer(1, 4))

    db_schema_data = [
        [Paragraph("<b>Tablo Adı</b>", th_style), Paragraph("<b>Sütunlar (Kolonlar) & Tipleri</b>", th_style), Paragraph("<b>İlişki & Kısıtlamalar (Constraints)</b>", th_style)],
        [
            Paragraph("<b>users</b><br/>(Kullanıcılar)", tc_bold),
            Paragraph(
                "• <b>id:</b> INTEGER PRIMARY KEY AUTOINCREMENT<br/>"
                "• <b>name:</b> TEXT NOT NULL<br/>"
                "• <b>email:</b> TEXT UNIQUE NOT NULL<br/>"
                "• <b>password:</b> TEXT NOT NULL<br/>"
                "• <b>student_number:</b> TEXT<br/>"
                "• <b>department:</b> TEXT<br/>"
                "• <b>created_at:</b> TEXT NOT NULL",
                tc_normal
            ),
            Paragraph("Ana kullanıcı tablosu. E-posta adresi tekildir (UNIQUE). Diğer tablolar bu tablonun id alanına bağlanır.", tc_normal),
        ],
        [
            Paragraph("<b>transactions</b><br/>(Finans İşlemleri)", tc_bold),
            Paragraph(
                "• <b>id:</b> INTEGER PRIMARY KEY AUTOINCREMENT<br/>"
                "• <b>user_id:</b> INTEGER NOT NULL<br/>"
                "• <b>title:</b> TEXT NOT NULL<br/>"
                "• <b>amount:</b> REAL NOT NULL<br/>"
                "• <b>type:</b> TEXT NOT NULL ('income' / 'expense')<br/>"
                "• <b>category:</b> TEXT NOT NULL<br/>"
                "• <b>date:</b> TEXT NOT NULL",
                tc_normal
            ),
            Paragraph("<b>FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE</b><br/>Kullanıcı silindiğinde tüm gelir/gider kayıtları otomatik temizlenir.", tc_normal),
        ],
        [
            Paragraph("<b>tasks</b><br/>(Ders & Ödevler)", tc_bold),
            Paragraph(
                "• <b>id:</b> INTEGER PRIMARY KEY AUTOINCREMENT<br/>"
                "• <b>user_id:</b> INTEGER NOT NULL<br/>"
                "• <b>course_name:</b> TEXT NOT NULL<br/>"
                "• <b>title:</b> TEXT NOT NULL<br/>"
                "• <b>due_date:</b> TEXT NOT NULL<br/>"
                "• <b>priority:</b> TEXT NOT NULL ('Yüksek'/'Orta'/'Düşük')<br/>"
                "• <b>is_completed:</b> INTEGER NOT NULL DEFAULT 0",
                tc_normal
            ),
            Paragraph("<b>FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE</b><br/>is_completed alanı SQLite'ta boolean temsili için 0 veya 1 olarak saklanır.", tc_normal),
        ],
    ]
    db_t = Table(db_schema_data, colWidths=[3.2 * cm, 8.8 * cm, 6.2 * cm])
    db_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#BE123C')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(db_t)
    story.append(Spacer(1, 8))

    # JSON Dışa Aktarma Standartı
    story.append(Paragraph("<b>JSON Veri Yedekleme Formatı ve Serileştirme Standardı:</b>", subsec_title))
    p_json_desc = (
        "JsonService sınıfı, veritabanındaki tüm ilişkisel tabloları hiyerarşik bir JSON ağacına dönüştürerek "
        "<code>getApplicationDocumentsDirectory()/ogrenci_asistani_yedek.json</code> dosyasına kaydeder. "
        "Dosya formatı aşağıdaki gibidir:"
    )
    story.append(Paragraph(p_json_desc, body))

    json_preview_code = (
        "{\n"
        '  "proje_adi": "Öğrenci Asistanı - Flutter SQLite & JSON",\n'
        '  "olusturucu": "Sinan Şamil Köylü",\n'
        '  "yedekleme_tarihi": "2026-10-23T18:41:15",\n'
        '  "toplam_kullanici": 2,\n'
        '  "kullanici_verileri": [\n'
        '    {\n'
        '      "user": { "id": 2, "name": "Sinan Samil Koylu", "email": "koylusinansamil@gmail.com", ... },\n'
        '      "transactions": [ { "id": 5, "title": "burs", "amount": 4000.0, "type": "income", ... } ],\n'
        '      "tasks": [ { "id": 4, "course_name": "mobil programlama", "priority": "Yüksek", ... } ]\n'
        '    }\n'
        '  ]\n'
        "}"
    )
    json_box = Table([[Paragraph(json_preview_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_snippet_style)]], colWidths=[18.2 * cm])
    json_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0F172A')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#38BDF8')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(json_box)

    # SAYFA 2 BİTİŞİ -> SAYFA 3 BAŞLANGICI
    story.append(PageBreak())

    # ==================== 4. BÖLÜM: KULLANILAN WIDGET'LARIN DETAYLI TEKNİK KATALOĞU (SAYFA 3) ====================
    story.append(Paragraph("4. Projede Kullanılan Tüm Widget'lar ve Kullanım Amaçları", sec_title))
    p_w_intro = (
        "Projeyi inşa ederken kullanıcı arayüzünü zenginleştirmek, Material 3 standartlarına tam uyum sağlamak ve yüksek performans "
        "elde etmek amacıyla Flutter SDK'sının güçlü widget kütüphanesinden yararlanılmıştır. Aşağıda projede aktif olarak kullanılan "
        "tüm widget'lar sınıflandırılarak <b>ne için ve hangi amaçla kullanıldıkları</b> ayrıntılı olarak dökümante edilmiştir:"
    )
    story.append(Paragraph(p_w_intro, body))
    story.append(Spacer(1, 4))

    all_widgets_data = [
        [Paragraph("<b>Widget Adı</b>", th_style), Paragraph("<b>Kategori</b>", th_style), Paragraph("<b>Projedeki Kullanım Amacı ve Üstlendiği Fonksiyon</b>", th_style)],
        
        [
            Paragraph("<b>Scaffold</b>", tc_bold),
            Paragraph("Düzen (Layout)", tc_normal),
            Paragraph("Tüm ekranların ana yapı iskelesidir. Sayfanın arka plan rengini, gövdesini (body), alt navigasyon barını ve yüzen aksiyon butonunu (FAB) tek merkezde birleştirir.", tc_normal)
        ],
        [
            Paragraph("<b>SafeArea</b>", tc_bold),
            Paragraph("Düzen (Layout)", tc_normal),
            Paragraph("Mobil cihazların üst çentik (notch), durum çubuğu (status bar) ve alt ev göstergesi alanlarının içerikle çakışmasını engellemek için ekranı güvenli sınırlara hapseder.", tc_normal)
        ],
        [
            Paragraph("<b>Stack & Positioned</b>", tc_bold),
            Paragraph("Düzen (Layout)", tc_normal),
            Paragraph("Öğeleri üst üste bindirmek için kullanılmıştır. Özellikle ana ekranın arka planındaki yumuşak radyal ışık parıltılarını (ambient glow efektleri) ve profil avatarının üzerindeki yeşil onay rozetini konumlandırmak için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>Container</b>", tc_bold),
            Paragraph("Düzen & Stil", tc_normal),
            Paragraph("Kutusal modelleme. Kartların kenar yuvarlatmaları (BorderRadius), arka plan degrade geçişleri (LinearGradient), gölgelendirmeleri (BoxShadow) ve iç/dış boşlukları Container ile sağlanmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>Column & Row</b>", tc_bold),
            Paragraph("Düzen (Flex)", tc_normal),
            Paragraph("Arayüz elemanlarını dikey (Column) ve yatay (Row) eksende hizalamak. Bilgi kartları, buton grupları ve başlık satırlarının kusursuz yerleşimi için ana flex yöneticileridir.", tc_normal)
        ],
        [
            Paragraph("<b>Expanded & Spacer</b>", tc_bold),
            Paragraph("Esneklik (Flex)", tc_normal),
            Paragraph("Satır ve sütunlar içinde kalan boşluğu dinamik olarak doldurmak; örneğin işlem kartlarında başlık metnini sola yaslarken tutar bilgisini en sağa itmek için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>SizedBox & Padding</b>", tc_bold),
            Paragraph("Boşluklandırma", tc_normal),
            Paragraph("Bileşenler arasına sabit pixel cinsinden nefes alma boşlukları koymak ve ekran kenarlarından düzenli iç boşluk (örneğin yatayda 20px) bırakmak için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>SingleChildScrollView</b>", tc_bold),
            Paragraph("Kaydırma (Scroll)", tc_normal),
            Paragraph("Form ekranlarında klavye açıldığında piksel taşma hatalarını (Bottom Overflow) önlemek ve profil/cüzdan sekmelerinin dikeyde rahatça kaydırılmasını sağlamak için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>ListView.builder</b>", tc_bold),
            Paragraph("Dinamik Liste", tc_normal),
            Paragraph("SQLite'tan gelen yüzlerce harcama ve ödev kaydını sadece ekranda görünen kadar belleğe alarak (lazy loading) son derece akıcı ve bellek dostu bir listeleme performansı sunar.", tc_normal)
        ],
        [
            Paragraph("<b>RefreshIndicator</b>", tc_bold),
            Paragraph("Etkileşim (Pull)", tc_normal),
            Paragraph("Kullanıcının ekranı yukarıdan aşağıya doğru parmağıyla çekerek SQLite veritabanındaki tüm bakiye, gelir, gider ve ödev verilerini anında yeniden sorgulaması için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>Form & GlobalKey</b>", tc_bold),
            Paragraph("Form Yönetimi", tc_normal),
            Paragraph("Giriş, kayıt ve ekleme ekranlarındaki tüm girdi alanlarını tek bir grup altında toplar; `_formKey.currentState!.validate()` çağrısıyla tek seferde tüm validasyon kurallarını tetikler.", tc_normal)
        ],
        [
            Paragraph("<b>TextFormField</b>", tc_bold),
            Paragraph("Girdi (Input)", tc_normal),
            Paragraph("E-posta, şifre, ad soyad, tutar ve ders adı gibi metinsel girdileri almak; düzenleme denetleyicisi (TextEditingController) ve doğrulama mantığı (validator) çalıştırmak için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>DropdownButtonFormField</b>", tc_bold),
            Paragraph("Seçici (Picker)", tc_normal),
            Paragraph("Harcama ekleme modalında kategorileri (Yemek, Ulaşım, Burs, Kitap vb.) ikonlarıyla birlikte açılır bir menüden seçtirmek için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>Checkbox</b>", tc_bold),
            Paragraph("Seçim (Toggle)", tc_normal),
            Paragraph("Ödev kartlarında görevin tamamlanıp tamamlanmadığını (is_completed 0/1) tek dokunuşla değiştirmek ve Login ekranında 'Beni Hatırla' tercihini yönetmek için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>ChoiceChip & ActionChip</b>", tc_bold),
            Paragraph("Hızlı Çipler", tc_normal),
            Paragraph("Ödev öncelik seviyesi seçimi (Yüksek 🔴, Orta 🟡, Düşük 🟢); emülatörde hızlı Türkçe karakter (ç, ğ, ı, ö, ş, ü) ve e-posta uzantısı (@gmail.com) ekleme butonları olarak kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>ElevatedButton</b>", tc_bold),
            Paragraph("Aksiyon Butonu", tc_normal),
            Paragraph("Giriş Yap, Kayıt Ol, İşlemi Kaydet ve JSON Dışa Aktar gibi yüksek öncelikli birincil (primary) eylemleri vurgulamak ve gölgeli tıklanma hissi vermek için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>FloatingActionButton</b>", tc_bold),
            Paragraph("Yüzen Aksiyon", tc_normal),
            Paragraph("Ekranın sağ alt köşesinde havada duran, degrade renkli özel '+ İşlem Ekle' ve '+ Ödev Ekle' butonudur. Kullanıcının her an hızlı veri girmesini sağlar.", tc_normal)
        ],
        [
            Paragraph("<b>Dismissible</b>", tc_bold),
            Paragraph("Kaydırarak Silme", tc_normal),
            Paragraph("İşlem veya ödev kartını parmakla sola/sağa kaydırarak veritabanından kalıcı olarak silmeyi sağlar. Arkada kırmızı çöp kutusu ikonu çıkarır.", tc_normal)
        ],
        [
            Paragraph("<b>NavigationBar & Badge</b>", tc_bold),
            Paragraph("Menü & Rozet", tc_normal),
            Paragraph("Ekranın altında yüzen modern 3 sekmeli Material 3 navigasyon dock'u. Ödevler simgesinin üzerinde bekleyen ödev sayısını canlı kırmızı bir Badge (rozet) olarak gösterir.", tc_normal)
        ],
        [
            Paragraph("<b>LinearProgressIndicator</b>", tc_bold),
            Paragraph("İlerleme Çubuğu", tc_normal),
            Paragraph("Aylık harcama/bütçe oranını (%2.5 harcandı) ve ödevlerin tamamlanma yüzdesini (1/4 Tamam) görsel olarak dolan renkli bir bar şeklinde sunmak için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>showModalBottomSheet</b>", tc_bold),
            Paragraph("Açılır Modal", tc_normal),
            Paragraph("Yeni harcama ekleme, ödev ekleme ve harcama kategorik dağılım analizini sayfa değiştirmeden alttan şık yuvarlatılmış kartlar olarak açmak için kullanılmıştır.", tc_normal)
        ],
        [
            Paragraph("<b>AlertDialog & SnackBar</b>", tc_bold),
            Paragraph("Diyalog & Toast", tc_normal),
            Paragraph("Güvenli oturum kapatma onayı, JSON yedekleme önizleme penceresi ve işlem başarı/hata bildirimlerini (yeşil/kırmızı kayan bildirimler) göstermek için kullanılmıştır.", tc_normal)
        ],
    ]

    w_table = Table(all_widgets_data, colWidths=[3.6 * cm, 2.8 * cm, 11.8 * cm])
    w_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(w_table)

    # SAYFA 3 BİTİŞİ -> SAYFA 4 BAŞLANGICI
    story.append(PageBreak())

    # ==================== 5. BÖLÜM: KULLANILAN PROPERTY'LER VE TERCİH NEDENLERİ (SAYFA 4) ====================
    story.append(Paragraph("5. Kullanılan Kritik Property'ler (Özellikler) ve Tercih Nedenleri", sec_title))
    p_prop_intro = (
        "Flutter'da bir widget'ın davranışı, görsel dili ve işletim sistemiyle etkileşimi parametreleri (properties) "
        "üzerinden yapılandırılır. Kullanıcı talebinde özellikle belirtildiği üzere, bu projede yer alan kritik property'ler, "
        "aldıkları değerler ve <b>bu değerlerin neden seçildiği</b> aşağıda derinlemesine incelenmiştir:"
    )
    story.append(Paragraph(p_prop_intro, body))
    story.append(Spacer(1, 4))

    props_data = [
        [Paragraph("<b>Widget & Property Adı</b>", th_style), Paragraph("<b>Atanan Değer / Tip</b>", th_style), Paragraph("<b>Neden Kullanıldı? (Mühendislik Gerekçesi)</b>", th_style)],
        
        [
            Paragraph("<b>TextFormField</b><br/><code>controller</code>", tc_prop_name),
            Paragraph("TextEditingController", tc_normal),
            Paragraph("Kullanıcının girdiği metne anlık olarak erişebilmek, emülatörde hızlı çip butonlarına basıldığında metin sonuna karakter eklemek ve SharedPreferences'tan 'Beni Hatırla' e-postasını doldurmak için zorunludur.", tc_prop_desc),
        ],
        [
            Paragraph("<b>TextFormField</b><br/><code>validator</code>", tc_prop_name),
            Paragraph("String? Function(String?)", tc_normal),
            Paragraph("Kullanıcı boş değer girmesin, e-posta formatı regex ile doğrulansın ve şifre en az 6 karakter olsun diye çalıştırılır. Hatalı durumlarda kırmızı uyarı mesajı döndürür.", tc_prop_desc),
        ],
        [
            Paragraph("<b>TextFormField</b><br/><code>obscureText</code>", tc_prop_name),
            Paragraph("bool (true / false)", tc_normal),
            Paragraph("Şifre karakterlerini gizleyerek yıldız veya nokta (••••••) olarak maskelemek için kullanılır. Göz ikonuna tıklandığında setState ile tersine çevrilerek (toggle) görünürlük sağlanır.", tc_prop_desc),
        ],
        [
            Paragraph("<b>TextFormField</b><br/><code>keyboardType</code>", tc_prop_name),
            Paragraph("TextInputType.number / emailAddress", tc_normal),
            Paragraph("Tutar girişinde kullanıcının karşısına sadece sayısal klavyenin açılmasını sağlayarak hatalı harf girişini engeller; e-posta alanında ise '@' işaretini içeren klavye tipini tetikler.", tc_prop_desc),
        ],
        [
            Paragraph("<b>InputDecoration</b><br/><code>prefixIcon & suffixIcon</code>", tc_prop_name),
            Paragraph("Widget (Container / Icon)", tc_normal),
            Paragraph("Kullanıcıya alanın işlevini görsel olarak anlatmak için sol tarafa renkli ikon kutusu yerleştirir; sağ tarafa ise şifre açma/kapama göz ikonunu konumlandırır.", tc_prop_desc),
        ],
        [
            Paragraph("<b>InputDecoration</b><br/><code>filled & fillColor</code>", tc_prop_name),
            Paragraph("true & Colors.white", tc_normal),
            Paragraph("Varsayılan şeffaf arka plan yerine temiz beyaz bir form alanı elde etmek ve açık gri arayüzde formların belirginleşmesini sağlamak için kullanılır.", tc_prop_desc),
        ],
        [
            Paragraph("<b>InputDecoration</b><br/><code>focusedBorder & errorBorder</code>", tc_prop_name),
            Paragraph("OutlineInputBorder(BorderSide)", tc_normal),
            Paragraph("Kullanıcı alana tıkladığında kenarlık rengini kurumsal gül kırmızısına (#E11D48), hatalı giriş yapıldığında ise canlı kırmızıya (#EF4444) dönüştürerek interaktif geri bildirim verir.", tc_prop_desc),
        ],
        [
            Paragraph("<b>BoxDecoration</b><br/><code>borderRadius: BorderRadius.circular</code>", tc_prop_name),
            Paragraph("Radius.circular(16 ile 28)", tc_normal),
            Paragraph("Keskin, sert ve köşeli tasarımlar yerine modern Material 3 standardı olan yumuşak kıvrımlı yüzeyler sunmak ve mobil dokunmatik hissini iyileştirmek için kullanılmıştır.", tc_prop_desc),
        ],
        [
            Paragraph("<b>BoxDecoration</b><br/><code>boxShadow: [BoxShadow]</code>", tc_prop_name),
            Paragraph("blurRadius: 14, offset: Offset(0, 6)", tc_normal),
            Paragraph("Kartların ve butonların z-ekseninde havada süzülüyormuş gibi 3 boyutlu derinlik (elevation) kazanması ve profesyonel FinTech havası oluşturması için düşük opaklıklı siyah gölge verilmiştir.", tc_prop_desc),
        ],
        [
            Paragraph("<b>BoxDecoration</b><br/><code>gradient: LinearGradient</code>", tc_prop_name),
            Paragraph("colors: [Color(1), Color(2)]", tc_normal),
            Paragraph("Düz, sıkıcı renkler yerine canlı ve enerjik ton geçişleri (Pembe-Kırmızı-Bordo) sağlamak; bakiye kartında ve butonlarda göz alıcı bir estetik oluşturmak için kullanılmıştır.", tc_prop_desc),
        ],
        [
            Paragraph("<b>SingleChildScrollView</b><br/><code>physics: AlwaysScrollableScrollPhysics</code>", tc_prop_name),
            Paragraph("ScrollPhysics", tc_normal),
            Paragraph("Ekrandaki içerik az olsa veya liste kısa kalsa dahi kullanıcının ekranı aşağı doğru çekebilmesini ve RefreshIndicator'ın her koşulda sorunsuz tetiklenebilmesini garanti altına alır.", tc_prop_desc),
        ],
        [
            Paragraph("<b>showModalBottomSheet</b><br/><code>isScrollControlled: true</code>", tc_prop_name),
            Paragraph("bool (true)", tc_normal),
            Paragraph("Modal pencerenin sadece ekranın yarısında sıkışıp kalmasını önler; formun kendi yüksekliği kadar veya ekranın %85'ine kadar uzamasına ve klavye açıldığında yukarı kaymasına izin verir.", tc_prop_desc),
        ],
        [
            Paragraph("<b>Dismissible</b><br/><code>confirmDismiss & onDismissed</code>", tc_prop_name),
            Paragraph("Future&lt;bool&gt; Function & VoidCallback", tc_normal),
            Paragraph("Kullanıcı kaydı yanlışlıkla kaydırıp silmesin diye silme onayı sağlar; onaylandığında ise SQLite veritabanındaki deleteTransaction veya deleteTask sorgusunu çalıştırır.", tc_prop_desc),
        ],
        [
            Paragraph("<b>NavigationBar</b><br/><code>selectedIndex & onDestinationSelected</code>", tc_prop_name),
            Paragraph("int & ValueChanged&lt;int&gt;", tc_normal),
            Paragraph("Alt menüdeki aktif sekmenin vurgulanmasını kontrol eder ve tıklandığında _currentTabIndex değerini güncelleyerek ilgili sayfa gövdesini yeniden çizer.", tc_prop_desc),
        ],
        [
            Paragraph("<b>LinearProgressIndicator</b><br/><code>minHeight & valueColor</code>", tc_prop_name),
            Paragraph("double (6-8) & AlwaysStoppedAnimation", tc_normal),
            Paragraph("İlerleme çubuğunun kalınlığını belirgin kılmak ve bütçe aşımına ya da kategoriye göre rengini dinamik olarak değiştirmek (yeşil, sarı, turuncu) için kullanılmıştır.", tc_prop_desc),
        ],
    ]

    p_table = Table(props_data, colWidths=[4.0 * cm, 3.6 * cm, 10.6 * cm])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#BE123C')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(p_table)

    # SAYFA 4 BİTİŞİ -> SAYFA 5 BAŞLANGICI
    story.append(PageBreak())

    # ==================== 6. BÖLÜM: EKRAN EKRAN İNCELEME VE GÖRSELLER (SAYFALAR 5 - 13) ====================
    screens_config = [
        {
            "num": "1",
            "title": "Giriş Yap Ekranı (Login Screen)",
            "img_path": "screenshots/01_giris_ekrani.png",
            "purpose": (
                "Kullanıcının kayıtlı e-posta ve şifresiyle sisteme güvenli giriş yapmasını sağlar. "
                "SharedPreferences entegrasyonuyla <b>'Beni Hatırla'</b> tercihi yönetilir. "
                "Emülatör ve mobil klavyelerde veri girişini hızlandırmak için hazır e-posta tamamlama çipleri (+ @, + @gmail.com, + @hotmail.com) içerir."
            ),
            "widgets": [
                ("Scaffold, SafeArea, SingleChildScrollView", "Klavye açıldığında taşmayı önleyen esnek ve güvenli sayfa yapısı."),
                ("Form & GlobalKey<FormState>", "E-posta ve şifre kurallarını tek tuşla doğrulayan form yöneticisi."),
                ("CustomTextField", "Özel degrade ikonlu, gölgeli ve yuvarlatılmış e-posta ve şifre kutuları."),
                ("Checkbox & CheckboxListTile", "'Beni Hatırla' tercihini yakalayan ve SharedPreferences'a kaydeden seçim."),
                ("ElevatedButton", "Degrade renkli, sağa ok ikonlu birincil 'Giriş Yap' butonu."),
                ("ActionChip", "E-posta kutusuna tek tıkla @gmail.com veya @ ekleyen yardımcı çipler."),
            ],
            "properties": [
                ("obscureText: _obscurePassword", "Şifrenin gizlenmesini sağlar; göz butonuna basılınca tersine döner."),
                ("keyboardType: emailAddress", "Klavyenin e-posta formatında (@ sembollü) açılmasını sağlar."),
                ("validator: (value) => ...", "Boş geçilmezlik ve geçerli e-posta regex kontrolü yapar."),
                ("borderRadius: BorderRadius.circular(16)", "Form giriş kutularına ve butonlara modern estetik hatlar verir."),
            ]
        },
        {
            "num": "2",
            "title": "Kayıt Ol Ekranı (Register Screen)",
            "img_path": "screenshots/02_kayit_ekrani.png",
            "purpose": (
                "Yeni öğrencilerin sisteme hesap açmasını sağlar. Ad Soyad, Öğrenci No, Bölüm, E-posta ve Şifre bilgileri toplanır. "
                "SQLite üzerinde e-posta adresi benzersizlik (UNIQUE) kontrolünden geçirilir; mükerrer kayıtlar engellenir. "
                "Hızlı Türkçe karakter çipleri (ç, ğ, ı, ö, ş, ü) sunar."
            ),
            "widgets": [
                ("Form & GlobalKey", "5 farklı giriş kutusunun bütünsel doğrulanması."),
                ("CustomTextField (5 Adet)", "Ad Soyad, Öğrenci No, Bölüm, E-posta ve Şifre için özelleştirilmiş inputlar."),
                ("ActionChip (Türkçe Harfler)", "Emülatörde klavyede zor bulunan ç, ğ, ı, ö, ş, ü harflerini tek dokunuşla ekleme."),
                ("ElevatedButton", "Formu doğrulayıp SQLite users tablosuna kaydeden 'Hesap Oluştur' butonu."),
                ("SnackBar", "Kayıt başarılı veya mükerrer e-posta uyarısını kullanıcıya bildiren toast."),
            ],
            "properties": [
                ("conflictAlgorithm: abort", "SQLite'ta aynı e-posta varsa kaydı reddeder ve -1 döner."),
                ("validator: şifre length >= 6", "Şifre güvenliği için en az 6 karakter zorunluluğu."),
                ("contentPadding: symmetric(16, 15)", "Giriş alanlarının iç ferahlığını ve okunabilirliğini sağlar."),
                ("prefixIcon: Icons.badge_rounded vb.", "Öğrenci no için kimlik, bölüm için okul ikonu ile zenginleştirme."),
            ]
        },
        {
            "num": "3",
            "title": "Ana Ekran: Cüzdanım Sekmesi (Wallet Dashboard)",
            "img_path": "screenshots/03_cuzdan_sekmesi.png",
            "purpose": (
                "Uygulamanın finans yönetim merkezidir. Üstte öğrenci karşılama ve cüzdan özeti kartı, ortada net bütçe bakiyesi (₺), "
                "FinTech bakiye gizleme göz ikonu, aylık harcama ilerleme çubuğu, hızlı aksiyon barı (Gelir/Gider Ekle, Analiz, Yenile) "
                "ve kaydırarak silinebilen (Dismissible) son işlem listesi yer alır."
            ),
            "widgets": [
                ("Stack & Positioned (Glow)", "Arka plandaki şık radyal ışık parıltıları."),
                ("LinearProgressIndicator", "Aylık harcamanın bütçeye oranını yüzde olarak dolan çubukla gösterme."),
                ("IconButton (Bakiye Gizleme)", "Bakiyeyi '••••••' veya '₺3.900,00' olarak anlık değiştirme."),
                ("Row & Action Buttons", "Gelir Ekle, Gider Ekle, Analiz ve Yenile hızlı erişim butonları."),
                ("Dismissible & ListTile", "İşlemleri parmakla sağa/sola kaydırarak SQLite'tan silme jesti."),
                ("FloatingActionButton", "Sağ altta degrade renkli '+ İşlem Ekle' yüzen butonu."),
            ],
            "properties": [
                ("LinearGradient: [Red, Rose, Crimson]", "Üst kartta ve FAB butonunda dikkat çekici FinTech renk geçişi."),
                ("NumberFormat.currency(symbol: '₺')", "Rakamların Türk Lirası para birimi standardında biçimlendirilmesi."),
                ("confirmDismiss & onDismissed", "Kaydırma ile SQLite'tan deleteTransaction sorgusu tetikleme."),
                ("physics: AlwaysScrollableScrollPhysics", "İşlem sayısı az olsa da aşağı çekerek yenileme (pull-to-refresh)."),
            ]
        },
        {
            "num": "4",
            "title": "Ana Ekran: Ödevlerim Sekmesi (Task Manager)",
            "img_path": "screenshots/04_odev_sekmesi.png",
            "purpose": (
                "Akademik görev ve ödev takip merkezidir. Üstteki lacivert kartta tamamlanma yüzdesi barı (1/4 Tamam) "
                "ve kalan teslim sayısı gösterilir. Filtre çipleriyle (Tümü, Bekleyenler, Tamamlananlar) liste dinamik filtrelenir. "
                "Ödev kartlarındaki renkli öncelik etiketleri (Yüksek 🔴, Orta 🟡, Düşük 🟢) aciliyeti belirtir."
            ),
            "widgets": [
                ("Container (Koyu Lacivert Kart)", "Ders & Ödev ilerlemesini vurgulayan özel koyu tema özet kartı."),
                ("LinearProgressIndicator", "Tamamlanan ödev oranını yeşil renkle dolduran ilerleme barı."),
                ("ChoiceChip (3 Adet Filtre)", "Tümü, Bekleyenler (3) ve Tamamlananlar (1) anlık filtreleme butonları."),
                ("Checkbox & ListTile", "Ödev tamamlandı durumunu (0/1) tek tıkla SQLite'ta güncelleyen kutu."),
                ("Container (Öncelik Rozeti)", "Ödevin aciliyetine göre dinamik renklenen şık çip."),
                ("FloatingActionButton", "Sağ altta yüzen '+ Ödev Ekle' butonu."),
            ],
            "properties": [
                ("is_completed: isCompleted ? 1 : 0", "SQLite'ta boolean değeri tamsayı bit olarak güncelleme."),
                ("orderBy: 'is_completed ASC, id DESC'", "Tamamlanmamış acil ödevleri daima listenin en üstünde gösterme."),
                ("valueColor: AlwaysStoppedAnimation", "Tamamlanma barını canlı zümrüt yeşili (#10B981) ile boyama."),
                ("borderRadius: BorderRadius.circular(18)", "Ödev kartlarına yumuşak kenarlık ve hafif gölge verme."),
            ]
        },
        {
            "num": "5",
            "title": "Ana Ekran: Yönetim & JSON Sekmesi (Profile & Hub)",
            "img_path": "screenshots/05_profil_sekmesi.png",
            "purpose": (
                "Öğrencinin profil bilgilerini (Ad Soyad, E-posta, Bölüm, Öğrenci No), SQLite veritabanının anlık durum "
                "istatistiklerini (toplam kullanıcı, işlem ve görev sayıları) ve tek dokunuşla tüm sistemi yedekleyen "
                "JSON Dışa Aktarma Hub'ını sunar. Güvenli oturum kapatma diyaloğu içerir."
            ),
            "widgets": [
                ("CircleAvatar & Badge", "Öğrencinin adının baş harfini taşıyan ve yeşil onay rozeti olan büyük avatar."),
                ("Container (İstatistik Kutuları)", "SQLite'tan canlı COUNT(*) sorgularıyla beslenen renkli sayaç hapları."),
                ("Container (Siyah Degrade Hub)", "JSON dışa aktarma mekanizmasını barındıran koyu şık kart."),
                ("ElevatedButton.icon", "JSON dosyasını üretip ekranda önizleme diyaloğunu açan buton."),
                ("OutlinedButton (Çıkış Yap)", "Oturumu güvenle kapatmak için onay diyalogu tetikleyen buton."),
            ],
            "properties": [
                ("getDatabaseStats(): rawQuery('SELECT COUNT(*)')", "SQLite tablolarındaki toplam satır sayısını canlı okur."),
                ("boxShadow: blurRadius 14, offset (0, 6)", "Kartlara temiz ve ferah derinlik hissi katar."),
                ("AlertDialog: Çıkış Yapılsın mı?", "Yanlışlıkla çıkış yapılmasını engelleyen onay penceresi."),
                ("Navigator.pushReplacement", "Çıkış yapılınca geçmişi temizleyip Login ekranına yönlendirir."),
            ]
        },
        {
            "num": "6",
            "title": "Yeni İşlem Ekleme Modalı (Add Transaction Modal)",
            "img_path": "screenshots/06_yeni_islem_modal.png",
            "purpose": (
                "Kullanıcının bütçesine yeni bir gelir veya gider kaydı eklemesini sağlar. "
                "Gider (-) ve Gelir (+) arasında tek tıkla geçiş yapılır. Tutar, başlık, kategori seçici "
                "ve sistem takviminden tarih seçimi (DatePicker) bileşenlerini barındırır."
            ),
            "widgets": [
                ("showModalBottomSheet", "Alttan açılan şık yuvarlatılmış (28px) pencere."),
                ("AnimatedContainer (Tür Seçici)", "Gider ve Gelir arasında pürüzsüz geçiş sağlayan buton çubuğu."),
                ("TextFormField (Tutar ve Başlık)", "İşlem adı ve ₺ tutarı girişi."),
                ("DropdownButtonFormField", "Yemek, Ulaşım, Kitap, Burs gibi kategorileri ikonlarıyla sunan seçici."),
                ("InkWell & showDatePicker", "İşlem tarihini takvimden seçtiren interaktif tarih kutusu."),
                ("ElevatedButton (Kaydet)", "İşlemi SQLite transactions tablosuna yazıp cüzdanı yenileyen buton."),
            ],
            "properties": [
                ("isScrollControlled: true", "Modalın klavye açıldığında yukarı esnemesini sağlar."),
                ("firstDate: 2025, lastDate: 2030", "DatePicker için geçerli tarih aralığı tanımlaması."),
                ("amount.replaceAll(',', '.')", "Türkçe virgüllü ondalık sayıları double veri tipine dönüştürme."),
                ("Navigator.pop(context, true)", "Kayıt başarılıysa ana ekrana 'true' dönerek anlık yenileme tetikler."),
            ]
        },
        {
            "num": "7",
            "title": "Yeni Ödev Ekleme Modalı (Add Task Modal)",
            "img_path": "screenshots/07_yeni_odev_modal.png",
            "purpose": (
                "Öğrencinin yeni bir ders görevi veya sınav teslimi oluşturmasını sağlar. "
                "Ders adı için hızlı ders seçim çipleri (Mobil Programlama, Veritabanı, Yazılım Müh.) sunar. "
                "Öncelik derecesi (Yüksek, Orta, Düşük) ve son teslim tarihi takvim seçicisi içerir."
            ),
            "widgets": [
                ("showModalBottomSheet", "Yuvarlatılmış üst köşelere sahip alttan açılır pencere."),
                ("SingleChildScrollView", "Ekran boyutu küçük cihazlarda formun kaydırılabilmesini sağlar."),
                ("ActionChip (Hızlı Ders Çipleri)", "Ders adını tek dokunuşla TextFormField'a kopyalayan butonlar."),
                ("ChoiceChip (Öncelik Düzeyi)", "Yüksek, Orta, Düşük önceliklerini renkli butonlarla seçtiren yapı."),
                ("InkWell & showDatePicker", "Son teslim tarihini takvim diyaloğundan seçtiren bileşen."),
                ("ElevatedButton (Görevi Listeye Ekle)", "Görevi tasks tablosuna ekleyen birincil buton."),
            ],
            "properties": [
                ("initialDate: now.add(Duration(days: 3))", "Varsayılan teslim tarihini 3 gün sonraya ayarlama."),
                ("selectedColor: Color(0xFFFEF3C7)", "Seçili öncelik çipine canlı arka plan vurgusu verme."),
                ("priority: 'Yüksek' | 'Orta' | 'Düşük'", "Ödevin önem derecesini metinsel olarak saklama."),
                ("isCompleted: false", "Yeni eklenen görevlerin varsayılan olarak 'bekliyor' durumunda açılması."),
            ]
        },
        {
            "num": "8",
            "title": "Kategori Harcama Dağılım Modalı (Category Analysis)",
            "img_path": "screenshots/08_kategori_analiz_modal.png",
            "purpose": (
                "Kullanıcının yaptığı tüm harcamaları kategorilerine göre gruplayarak (Yemek, Ulaşım, Kitap vb.) "
                "toplam harcama tutarlarını ve harcama içindeki yüzdesel oranlarını (%100.0) renkli ilerleme çubuklarıyla "
                "analitik olarak görselleştirir. Öğrencinin parasını nereye harcadığını net görmesini sağlar."
            ),
            "widgets": [
                ("showModalBottomSheet", "Alttan açılan detaylı analiz penceresi."),
                ("Column & Row (Dinamik Liste)", "Kategori haritalamasındaki (Map) verileri dönerek liste oluşturma."),
                ("LinearProgressIndicator", "Kategorinin toplam harcamadaki yüzdesini gösteren renkli çubuk."),
                ("Icon & Container", "Her kategoriye özel renk ve simge kutusu (Yemek için çatal-bıçak, Ulaşım için otobüs)."),
                ("IconButton (Kapat)", "Modaldan çıkışı sağlayan çarpı ikonu."),
            ],
            "properties": [
                ("ratio = entry.value / _totalExpense", "Kategorinin toplam harcama içindeki payını hesaplama (0.0 - 1.0)."),
                ("toStringAsFixed(1)", "Harcama yüzdesini virgülden sonra 1 basamakla (%25.4) biçimlendirme."),
                ("categoryMap.entries.map(...)", "SQL'den gelen verileri dinamik grafik barlarına haritalama."),
                ("valueColor: AlwaysStoppedAnimation(catColor)", "Her kategoriye kendine has pastel renk atama."),
            ]
        },
        {
            "num": "9",
            "title": "JSON Dışa Aktarma & Kod Önizleme Diyaloğu",
            "img_path": "screenshots/09_json_yedekleme_modal.png",
            "purpose": (
                "SQLite veritabanındaki tüm tabloları (users, transactions, tasks) ilişkisel olarak çekip "
                "standart .json formatında cihazın yerel depolama dizinine kaydeder (ogrenci_asistani_yedek.json). "
                "Ekranda açılan koyu renkli terminal penceresinde JSON içeriğini renkli monospace fontla önizletir."
            ),
            "widgets": [
                ("showDialog & AlertDialog", "Merkezi açılır sistem diyaloğu."),
                ("Container (Terminal Penceresi)", "Koyu lacivert (#0F172A) arka planlı kod kutusu."),
                ("SingleChildScrollView", "Yüzlerce satırlık JSON metnini kutu içinde akıcı kaydırma."),
                ("Text (Monospace Syntax)", "Consolas / Monospace yazı tipiyle kod renklendirmesi."),
                ("ElevatedButton (Kapat)", "Önizleme diyaloğunu sonlandıran onay butonu."),
            ],
            "properties": [
                ("JsonEncoder.withIndent('  ')", "JSON verisini 2 boşluk girintili, okunabilir formatta serileştirme."),
                ("getApplicationDocumentsDirectory()", "Dosyayı işletim sisteminin güvenli yerel hafızasına kaydetme."),
                ("fontFamily: 'monospace'", "Kodların gerçek bir IDE terminalindeymiş gibi hizalı gösterimi."),
                ("color: Color(0xFF38BDF8)", "JSON metnini göz yormayan açık mavi/cyan renkle vurgulama."),
            ]
        },
    ]

    for screen in screens_config:
        story.append(Paragraph(f"6.{screen['num']}. {screen['title']}", sec_title))
        story.append(Spacer(1, 2))

        # Sol sütun: Mobil Ekran Görüntüsü (Etrafında ince estetik çerçeve)
        img_element = Image(screen['img_path'], width=5.8 * cm, height=12.9 * cm)
        
        # Ekran görüntüsü çerçevesi
        img_frame = Table([[img_element]], colWidths=[5.9 * cm])
        img_frame.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#CBD5E1')),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        right_flowables = []
        
        # Ekran Amacı
        right_flowables.append(Paragraph("<b>Ekran Amacı ve Yapılan İşlemler:</b>", subsec_title))
        right_flowables.append(Paragraph(screen['purpose'], body))
        right_flowables.append(Spacer(1, 2))

        # Kullanılan Widget'lar Mini Tablo
        right_flowables.append(Paragraph("<b>Kullanılan Başlıca Widget'lar ve Rolleri:</b>", subsec_title))
        w_sub_data = [[Paragraph("<b>Widget</b>", th_style), Paragraph("<b>Kullanım Amacı</b>", th_style)]]
        for w_name, w_role in screen['widgets']:
            w_sub_data.append([Paragraph(w_name, tc_bold), Paragraph(w_role, tc_normal)])
        
        w_sub_t = Table(w_sub_data, colWidths=[3.8 * cm, 8.2 * cm])
        w_sub_t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2.2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ]))
        right_flowables.append(w_sub_t)
        right_flowables.append(Spacer(1, 3))

        # Kullanılan Property'ler Mini Tablo
        right_flowables.append(Paragraph("<b>Öne Çıkan Property'ler ve Tercih Sebepleri:</b>", subsec_title))
        p_sub_data = [[Paragraph("<b>Property & Değeri</b>", th_style), Paragraph("<b>Neden Seçildi? (Teknik Gerekçe)</b>", th_style)]]
        for p_name, p_reason in screen['properties']:
            p_sub_data.append([Paragraph(p_name, tc_prop_name), Paragraph(p_reason, tc_prop_desc)])
        
        p_sub_t = Table(p_sub_data, colWidths=[4.2 * cm, 7.8 * cm])
        p_sub_t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#BE123C')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 2.2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ]))
        right_flowables.append(p_sub_t)

        # İki Sütunlu Ana Tablo
        layout_data = [[img_frame, right_flowables]]
        layout_t = Table(layout_data, colWidths=[6.1 * cm, 12.1 * cm])
        layout_t.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(layout_t)
        story.append(PageBreak())

    # ==================== 7. BÖLÜM: TEST, DOĞRULAMA VE GÜVENLİK (SAYFA 14) ====================
    story.append(Paragraph("7. Güvenlik, Veri Doğrulama ve Test Mekanizmaları", sec_title))
    p_sec = (
        "Projeyi geliştirirken yalnızca görsel arayüze değil, arka plandaki yazılım güvenliği, veri bütünlüğü "
        "ve otomatik test edilebilirlik standartlarına azami özen gösterilmiştir:"
    )
    story.append(Paragraph(p_sec, body))

    sec_data = [
        [
            Paragraph("<b>Güvenlik / Test Alanı</b>", th_style),
            Paragraph("<b>Uygulanan Yöntem & Kütüphane</b>", th_style),
            Paragraph("<b>Sağlanan Koruma ve Avantaj</b>", th_style),
        ],
        [
            Paragraph("<b>SQL Enjeksiyon Koruması<br/>(SQL Injection Defense)</b>", tc_bold),
            Paragraph("sqflite parametrik sorguları<br/><code>whereArgs: [email, password]</code>", tc_normal),
            Paragraph("Kullanıcı girdileri asla ham SQL dizesiyle birleştirilmez (string concatenation yapılmaz). Bu sayede tırnak işareti veya özel karakterlerle SQL açığı oluşturulması %100 engellenir.", tc_normal),
        ],
        [
            Paragraph("<b>İlişkisel Veri Bütünlüğü<br/>(Cascade Deletion)</b>", tc_bold),
            Paragraph("SQLite PRAGMA foreign_keys = ON & ON DELETE CASCADE", tc_normal),
            Paragraph("Kullanıcı hesabı silindiğinde yetim veri (orphaned data) kalmaz; kullanıcıya ait tüm gelir, gider ve ders görevleri ilişkisel olarak veritabanı seviyesinde temizlenir.", tc_normal),
        ],
        [
            Paragraph("<b>Form Validasyon Motoru<br/>(Input Validation)</b>", tc_bold),
            Paragraph("GlobalKey&lt;FormState&gt; & RegExp Kontrolleri", tc_normal),
            Paragraph("Geçersiz e-posta formatları (@ ve domain eksikliği), 6 karakterden kısa şifreler veya sıfırdan küçük harcama tutarları daha veritabanına ulaşmadan arayüzde yakalanarak engellenir.", tc_normal),
        ],
        [
            Paragraph("<b>Otomatik Widget Testleri<br/>(Automated Testing)</b>", tc_bold),
            Paragraph("flutter_test & RenderRepaintBoundary toImage", tc_normal),
            Paragraph("Uygulamanın bileşenleri, mock SharedPreferences ve FFI veritabanı ile otomatik testlerden geçirilmiş; duman testleri (smoke tests) ve ekran yakalama testleri başarıyla koşturulmuştur.", tc_normal),
        ],
    ]
    sec_t = Table(sec_data, colWidths=[4.2 * cm, 4.8 * cm, 9.2 * cm])
    sec_t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(sec_t)
    story.append(Spacer(1, 10))

    # ==================== 8. BÖLÜM: SONUÇ VE KAZANIMLAR ====================
    story.append(Paragraph("8. Sonuç, Öğrenim Kazanımları ve Değerlendirme", sec_title))
    conclusion_text = (
        "Bu proje kapsamında modern mobil yazılım geliştirme ekosisteminin lider teknolojisi olan <b>Flutter & Dart</b> "
        "kullanılarak, gerçek dünya problemlerini çözen, katmanlı mimariye (Layered Architecture) sahip, veri kalıcılığı "
        "yerel <b>SQLite ve JSON File I/O</b> ile sağlanan, kullanıcı deneyimi üst seviyede bir mobil uygulama başarıyla ortaya konulmuştur.<br/><br/>"
        "<b>Elde Edilen Temel Mühendislik Kazanımları:</b><br/>"
        "1. <b>Flutter Widget Yaşam Döngüsü:</b> StatelessWidget ve StatefulWidget arasındaki farklar, `initState`, `build`, `dispose` "
        "metotları ve `setState` üzerinden reaktif UI güncelleme mantığı derinlemesine kavranmıştır.<br/>"
        "2. <b>İlişkisel Veritabanı ve CRUD İşlemleri:</b> SQLite üzerinde CREATE TABLE, INSERT, SELECT, UPDATE, DELETE komutları; "
        "yabancı anahtar (Foreign Key) kısıtlamaları ve aggregate (SUM, COUNT) sorguları pratik edilmiştir.<br/>"
        "3. <b>Dosya Sistemi ve JSON Serileştirme:</b> Dart'ın `dart:convert` kütüphanesiyle nesne-JSON dönüşümleri ve `path_provider` "
        "aracılığıyla cihazın yerel depolama alanına fiziksel dosya yazma/okuma operasyonları tamamlanmıştır.<br/>"
        "4. <b>FinTech ve Material 3 Tasarım Standartları:</b> Degrade geçişler, bakiye gizleme mekanizması, ilerleme çubukları, "
        "animasyonlu kaydırmalı silme (Dismissible) ve alt navigasyon dock'u ile profesyonel bir arayüz tecrübesi kazanılmıştır.<br/><br/>"
        "Sonuç olarak, <b>Öğrenci Asistanı</b> projesi hem kod kalitesi, hem veri güvenliği, hem de arayüz zarafeti açısından "
        "üniversite Mobil Programlama dersinin tüm teknik ve işlevsel kazanımlarını eksiksiz olarak karşılamaktadır."
    )
    story.append(Paragraph(conclusion_text, body))

    # PDF İnşa Et
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Detayli PDF Raporu Basariyla Uretildi: {os.path.abspath(output_pdf)}")

if __name__ == "__main__":
    create_report()
