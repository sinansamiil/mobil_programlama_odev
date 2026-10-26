import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Türkçe karakter destekli sistem fontlarını kaydet
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'C:/Windows/Fonts/ariali.ttf'))

class NumberedCanvas(canvas.Canvas):
    """Her sayfanın altına toplam sayfa sayısını ve alt bilgiyi ekler"""
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
        
        # Üst çizgi ve alt bilgi
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(1.5 * cm, 1.2 * cm, A4[0] - 1.5 * cm, 1.2 * cm)
        
        # Sol alt bilgi
        self.drawString(1.5 * cm, 0.8 * cm, "Öğrenci Asistanı - Mobil Programlama Projesi Teknik Raporu")
        # Sağ alt sayfa numarası
        page_text = f"Sayfa {self._pageNumber} / {page_count}"
        self.drawRightString(A4[0] - 1.5 * cm, 0.8 * cm, page_text)
        self.restoreState()

def generate_report():
    output_filename = "teknik_rapor.pdf"
    
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.8 * cm,
    )
    
    styles = getSampleStyleSheet()
    
    # Özel Stiller
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Arial-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=0, # Left
        spaceAfter=3,
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Arial-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#E11D48'),
        alignment=0,
        spaceAfter=12,
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        fontName='Arial-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )
    
    subsection_heading = ParagraphStyle(
        'SubSectionHeading',
        fontName='Arial-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#BE123C'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        fontName='Arial',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5,
    )
    
    bullet_style = ParagraphStyle(
        'DocBullet',
        fontName='Arial',
        fontSize=8.8,
        leading=12.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=10,
        spaceAfter=3,
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Arial-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Arial-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0F172A'),
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Arial',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#334155'),
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        fontName='Arial-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#E11D48'),
    )
    
    story = []
    
    # ==================== 1. BAŞLIK VE KÜNYE BÖLÜMÜ ====================
    story.append(Paragraph("MOBİL PROGRAMLAMA PROJESİ TEKNİK RAPORU", title_style))
    story.append(Paragraph("Öğrenci Asistanı: Akıllı Kampüs Cüzdanı & Ders Takip Sistemi", subtitle_style))
    
    # Bilgi Kartı Tablosu
    info_data = [
        [
            Paragraph("<b>Öğrenci:</b> Sinan Şamil Köylü", body_style),
            Paragraph("<b>Öğrenci No:</b> 240211019", body_style),
            Paragraph("<b>Bölüm:</b> Yazılım Mühendisliği", body_style),
        ],
        [
            Paragraph("<b>Ders:</b> Mobil Programlama", body_style),
            Paragraph("<b>Platform:</b> Flutter & Dart", body_style),
            Paragraph("<b>Veritabanı:</b> SQLite (sqflite) + JSON", body_style),
        ]
    ]
    info_table = Table(info_data, colWidths=[6.2 * cm, 5.5 * cm, 6.3 * cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))
    
    # ==================== 2. PROJE ÖZETİ VE AMACI ====================
    story.append(Paragraph("1. Proje Özeti ve Amacı", section_heading))
    summary_text = (
        "<b>Öğrenci Asistanı</b>, üniversite öğrencilerinin kampüs yaşamlarındaki iki kritik ihtiyacı tek bir modern çatı "
        "altında toplayan yerel bir mobil uygulamadır: <b>Finans & Cüzdan Yönetimi</b> (öğrenci bütçesi, burs, yemekhane, harçlık takibi) "
        "ve <b>Akademik Görev Takibi</b> (ödevler, projeler, sınav teslimleri). Uygulama harici bir internet bağlantısına veya uzaktaki "
        "bir sunucuya bağımlı olmaksızın, tamamen yerel <b>SQLite veritabanı</b> üzerinde güvenle çalışmakta, verilerin anlık "
        "olarak <b>JSON formatında dışa aktarılmasını (backup)</b> sağlamaktadır."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 6))
    
    # ==================== 3. MODÜLLER VE GELİŞTİRİLEN İŞLEVLER ====================
    story.append(Paragraph("2. Geliştirilen Modüller ve Yapılan İşler", section_heading))
    
    modules_data = [
        [
            Paragraph("<b>Modül</b>", table_header_style),
            Paragraph("<b>Yapılan İşler ve Fonksiyonlar</b>", table_header_style),
            Paragraph("<b>Teknik Detaylar & Veritabanı</b>", table_header_style),
        ],
        [
            Paragraph("<b>Giriş & Kayıt<br/>(Kimlik Doğrulama)</b>", table_cell_bold),
            Paragraph(
                "• Kullanıcı kayıt ve güvenli giriş sistemi.<br/>"
                "• 'Beni Hatırla' fonksiyonu ile e-posta hatırlama.<br/>"
                "• Şifre gizleme/gösterme, dinamik form validasyonları.<br/>"
                "• Emülatör kolaylığı: Hızlı Türkçe harf ve domain ekleme çipleri.",
                table_cell_style
            ),
            Paragraph("SQLite <i>users</i> tablosu, SharedPreferences (remember_me), Regex e-posta kontrolü.", table_cell_style),
        ],
        [
            Paragraph("<b>Cüzdan & Bütçe<br/>(Finans Yönetimi)</b>", table_cell_bold),
            Paragraph(
                "• Gelir / Gider CRUD işlemleri (Ekleme, Listeleme, Silme).<br/>"
                "• Anlık toplam bakiye, toplam gelir ve gider hesaplaması.<br/>"
                "• FinTech tarzı bakiye gizleme (••••••) göz ikonu.<br/>"
                "• Aylık harcama/bütçe oranı ilerleme çubuğu (progress bar).<br/>"
                "• Hızlı Aksiyon Barı (Gelir Ekle, Gider Ekle, Analiz, Yenile).<br/>"
                "• Kategorik Harcama Dağılımı modalı (kategori yüzdeleri).<br/>"
                "• Kaydırarak işlem silme (Dismissible) ve Tümü/Gelir/Gider filtreleri.",
                table_cell_style
            ),
            Paragraph("SQLite <i>transactions</i> tablosu, dinamik aggregate sorguları (SUM, GROUP BY), Dismissible widget.", table_cell_style),
        ],
        [
            Paragraph("<b>Ödev & Ders<br/>(Görev Takibi)</b>", table_cell_bold),
            Paragraph(
                "• Ders ödevi ve teslim görevleri yönetimi.<br/>"
                "• Öncelik derecelendirmesi (Yüksek 🔴, Orta 🟡, Düşük 🟢).<br/>"
                "• Son teslim tarihi seçici (DatePicker).<br/>"
                "• Tek dokunuşla tamamlandı/bekliyor durumu (Checkbox toggle).<br/>"
                "• Tamamlanma yüzdesi çubuğu ve kalan ödev sayacı.<br/>"
                "• Filtreleme: Tümü, Bekleyenler, Tamamlananlar.",
                table_cell_style
            ),
            Paragraph("SQLite <i>tasks</i> tablosu, boolean bit saklama, dinamik filtreleme sorguları.", table_cell_style),
        ],
        [
            Paragraph("<b>Yönetim & JSON<br/>(Veri Yedekleme)</b>", table_cell_bold),
            Paragraph(
                "• Öğrenci kimlik bilgileri ve bölüm/öğrenci no görüntüleme.<br/>"
                "• SQLite canlı veritabanı istatistikleri (kullanıcı, işlem, ödev).<br/>"
                "• <b>JSON Dışa Aktarma:</b> Tüm veritabanının yerel hafızaya .json olarak kaydedilmesi ve kod önizleme modalı.<br/>"
                "• Güvenli oturum kapatma ve onay diyalogları.",
                table_cell_style
            ),
            Paragraph("JsonService, dart:convert, path_provider (getApplicationDocumentsDirectory), AlertDialog.", table_cell_style),
        ],
    ]
    
    modules_table = Table(modules_data, colWidths=[3.6 * cm, 10.2 * cm, 4.2 * cm])
    modules_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E11D48')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(modules_table)
    story.append(PageBreak())
    
    # ==================== 4. KULLANILAN WIDGET'LARIN TEKNİK SINIFLANDIRILMASI ====================
    story.append(Paragraph("3. Projede Kullanılan Başlıca Flutter Widget'ları", section_heading))
    widgets_intro = (
        "Proje geliştirilirken Flutter'ın modern <b>Material 3</b> standartlarına uygun, temiz mimariyi destekleyen ve kullanıcı deneyimini "
        "en üst düzeye çıkaran widget'lar kullanılmıştır. Aşağıda projede yer alan başlıca widget'lar işlevsel kategorilerine göre özetlenmiştir:"
    )
    story.append(Paragraph(widgets_intro, body_style))
    story.append(Spacer(1, 4))
    
    widgets_data = [
        [
            Paragraph("<b>Kategori</b>", table_header_style),
            Paragraph("<b>Kullanılan Widget'lar</b>", table_header_style),
            Paragraph("<b>Projedeki Kullanım Amacı ve İşlevi</b>", table_header_style),
        ],
        [
            Paragraph("<b>Düzen & Yapı<br/>(Layout)</b>", table_cell_bold),
            Paragraph("Scaffold, SafeArea, Container, Column, Row, Expanded, SizedBox, Spacer, Stack, Positioned", table_cell_bold),
            Paragraph(
                "Ekranların ana iskeletini oluşturma; sistem çentiklerinden koruma; dikey ve yatay esnek dizilim; "
                "kart arka plan parıltıları (ambient glow) ve filigran halkalarının katmanlı gösterimi.",
                table_cell_style
            ),
        ],
        [
            Paragraph("<b>Listeleme & Kaydırma<br/>(Scrolling)</b>", table_cell_bold),
            Paragraph("SingleChildScrollView, ListView.builder, RefreshIndicator", table_cell_bold),
            Paragraph(
                "Harcama ve ödev listelerinin dinamik ve bellek dostu şekilde oluşturulması; "
                "klavye açıldığında formların taşmasını engelleme ve aşağı çekerek yenileme mekanizması.",
                table_cell_style
            ),
        ],
        [
            Paragraph("<b>Form & Veri Girişi<br/>(Input & Forms)</b>", table_cell_bold),
            Paragraph("Form, TextFormField, DropdownButtonFormField, Checkbox, ChoiceChip, ActionChip", table_cell_bold),
            Paragraph(
                "GlobalKey ile form doğrulama (validation); tutar, başlık ve şifre girişleri; kategori/öncelik seçimi; "
                "ödev tamamlandı durumu ve hızlı filtre/Türkçe karakter ekleme çipleri.",
                table_cell_style
            ),
        ],
        [
            Paragraph("<b>Buton & Etkileşim<br/>(Actions)</b>", table_cell_bold),
            Paragraph("ElevatedButton, OutlinedButton, TextButton, IconButton, FloatingActionButton, GestureDetector, Dismissible", table_cell_bold),
            Paragraph(
                "Kayıt/giriş aksiyonları; yüzen işlem ve ödev ekleme butonu; şifre ve bakiye gizleme tıklamaları; "
                "işlem ve ödev kayıtlarını parmakla sağa/sola kaydırarak silme (Dismissible).",
                table_cell_style
            ),
        ],
        [
            Paragraph("<b>Diyalog & Modallar<br/>(Overlays)</b>", table_cell_bold),
            Paragraph("showModalBottomSheet, showDatePicker, showDialog, AlertDialog, SnackBar", table_cell_bold),
            Paragraph(
                "Alttan açılan şık yuvarlatılmış işlem/ödev ekleme ve kategori analiz pencereleri; takvimden teslim tarihi seçimi; "
                "çıkış onay pencereleri; JSON dosya önizleme ekranı ve durum bildirim toast'ları.",
                table_cell_style
            ),
        ],
        [
            Paragraph("<b>Navigasyon & Menü<br/>(Navigation)</b>", table_cell_bold),
            Paragraph("NavigationBar, NavigationDestination, Badge, Navigator", table_cell_bold),
            Paragraph(
                "Ekranın altında havada asılı duran (floating dock) modern 3 sekmeli menü; "
                "bekleyen ödev sayısını anlık gösteren bildirim rozeti (Badge); sayfalar arası geçiş yönetimi.",
                table_cell_style
            ),
        ],
        [
            Paragraph("<b>Görsel & İndikatör<br/>(Visual & Style)</b>", table_cell_bold),
            Paragraph("Text, Icon, CircleAvatar, LinearProgressIndicator, BoxDecoration, LinearGradient, BoxShadow", table_cell_bold),
            Paragraph(
                "Dinamik tipografi; sembol ve kategori ikonları; öğrenci profil avatarları; "
                "aylık harcama oranı ve ödev tamamlama yüzdesi çubukları; çok katmanlı degrade ve gölgeler.",
                table_cell_style
            ),
        ],
    ]
    
    widgets_table = Table(widgets_data, colWidths=[3.2 * cm, 6.2 * cm, 8.6 * cm])
    widgets_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(widgets_table)
    story.append(Spacer(1, 10))
    
    # ==================== 5. MİMARİ VE KULLANILAN PAKETLER ====================
    story.append(Paragraph("4. Mimari Yapı ve Kullanılan Paketler", section_heading))
    
    arch_data = [
        [
            Paragraph("<b>Klasör / Katman</b>", table_header_style),
            Paragraph("<b>İçerik ve Görevi</b>", table_header_style),
            Paragraph("<b>Kullanılan Paketler</b>", table_header_style),
        ],
        [
            Paragraph("<b>models/</b>", table_cell_bold),
            Paragraph("UserModel, TransactionModel, TaskModel (Veri sınıfları, toMap / fromMap metotları).", table_cell_style),
            Paragraph("sqflite: ^2.4.4+2 (Veritabanı CRUD)", table_cell_style),
        ],
        [
            Paragraph("<b>database/</b>", table_cell_bold),
            Paragraph("DBHelper (SQLite şema, migration, CRUD fonksiyonları), JsonService (JSON export ve dosya yazma).", table_cell_style),
            Paragraph("sqflite_common_ffi (Masaüstü FFI)", table_cell_style),
        ],
        [
            Paragraph("<b>screens/</b>", table_cell_bold),
            Paragraph("LoginScreen (Giriş), RegisterScreen (Kayıt), HomeScreen (3 sekmeli ana merkez).", table_cell_style),
            Paragraph("shared_preferences: ^2.5.6 (Oturum hafızası)", table_cell_style),
        ],
        [
            Paragraph("<b>widgets/</b>", table_cell_bold),
            Paragraph("CustomTextField (Özel stilli input), AddTransactionModal, AddTaskModal (Arayüz modalları).", table_cell_style),
            Paragraph("intl: ^0.20.3 (₺ Para ve Tarih formatı)", table_cell_style),
        ],
    ]
    
    arch_table = Table(arch_data, colWidths=[3.2 * cm, 9.8 * cm, 5.0 * cm])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#475569')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(arch_table)
    story.append(Spacer(1, 10))
    
    # ==================== 6. SONUÇ VE KAZANIMLAR ====================
    story.append(Paragraph("5. Sonuç ve Proje Çıktıları", section_heading))
    conclusion_text = (
        "Bu projede Flutter ve Dart kullanılarak katmanlı mimariye (Layered Architecture) sahip, veri kalıcılığı yerel "
        "SQLite ve SharedPreferences ile güvence altına alınmış, kullanıcı deneyimi yüksek seviyede bir mobil uygulama ortaya "
        "konulmuştur. Temel CRUD işlemlerinin yanı sıra dinamik filtreleme, hesaplama motorları (bütçe oranı, görev yüzdesi), "
        "FinTech seviyesinde bakiye gizleme ve JSON veri yedekleme mekanizmaları başarıyla entegre edilmiştir."
    )
    story.append(Paragraph(conclusion_text, body_style))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Rapor basariyla olusturuldu: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    generate_report()
