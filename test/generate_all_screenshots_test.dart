import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:path_provider_platform_interface/path_provider_platform_interface.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'package:ogrenci_asistani/database/db_helper.dart';
import 'package:ogrenci_asistani/models/user_model.dart';
import 'package:ogrenci_asistani/screens/login_screen.dart';
import 'package:ogrenci_asistani/screens/register_screen.dart';
import 'package:ogrenci_asistani/screens/home_screen.dart';

class FakePathProviderPlatform extends Fake
    with MockPlatformInterfaceMixin
    implements PathProviderPlatform {
  @override
  Future<String?> getApplicationDocumentsPath() async {
    return Directory.current.path;
  }
}

Future<void> loadFonts() async {
  const fontFolder = 'C:/src/flutter/bin/cache/artifacts/material_fonts';

  final robotoReg = File('$fontFolder/roboto-regular.ttf').readAsBytesSync();
  final robotoLoader = FontLoader('Roboto')
    ..addFont(Future.value(ByteData.view(robotoReg.buffer)));
  final robotoBold = File('$fontFolder/roboto-bold.ttf').readAsBytesSync();
  robotoLoader.addFont(Future.value(ByteData.view(robotoBold.buffer)));
  final robotoMed = File('$fontFolder/roboto-medium.ttf').readAsBytesSync();
  robotoLoader.addFont(Future.value(ByteData.view(robotoMed.buffer)));
  await robotoLoader.load();

  final iconFont = File('$fontFolder/materialicons-regular.otf').readAsBytesSync();
  final iconLoader = FontLoader('MaterialIcons')
    ..addFont(Future.value(ByteData.view(iconFont.buffer)));
  await iconLoader.load();
}

Future<void> saveScreenshot(GlobalKey key, String filename) async {
  final boundary = key.currentContext!.findRenderObject() as RenderRepaintBoundary;
  final image = await boundary.toImage(pixelRatio: 1.0);
  final byteData = await image.toByteData(format: ui.ImageByteFormat.png);

  final dir = Directory('screenshots');
  if (!dir.existsSync()) dir.createSync();

  File('screenshots/$filename').writeAsBytesSync(byteData!.buffer.asUint8List());
  print('Saved screenshots/$filename (${File('screenshots/$filename').lengthSync()} bytes)');
}

Widget wrapApp(Widget child, GlobalKey key) {
  return MaterialApp(
    debugShowCheckedModeBanner: false,
    theme: ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFFE11D48),
        primary: const Color(0xFFE11D48),
        secondary: const Color(0xFF10B981),
        surface: Colors.white,
      ),
      scaffoldBackgroundColor: const Color(0xFFF9FAFB),
      fontFamily: 'Roboto',
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
        scrolledUnderElevation: 0,
      ),
    ),
    builder: (ctx, c) => RepaintBoundary(key: key, child: c!),
    home: child,
  );
}

void main() {
  setUpAll(() async {
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;
    PathProviderPlatform.instance = FakePathProviderPlatform();
    SharedPreferences.setMockInitialValues({});
    await loadFonts();
  });

  testWidgets('Capture 01 Login and 02 Register', (tester) async {
    await tester.runAsync(() async {
      tester.view.physicalSize = const Size(412 * 2, 915 * 2);
      tester.view.devicePixelRatio = 2.0;

      // 1. Login Screen
      final loginKey = GlobalKey();
      await tester.pumpWidget(wrapApp(const LoginScreen(), loginKey));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 200));
      await saveScreenshot(loginKey, '01_giris_ekrani.png');

      // 2. Register Screen
      final regKey = GlobalKey();
      await tester.pumpWidget(wrapApp(const RegisterScreen(), regKey));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 200));
      await saveScreenshot(regKey, '02_kayit_ekrani.png');
    });
  });

  testWidgets('Capture 03 Wallet, 06 Add Trans, 08 Category Breakdown', (tester) async {
    await tester.runAsync(() async {
      tester.view.physicalSize = const Size(412 * 2, 915 * 2);
      tester.view.devicePixelRatio = 2.0;

      final user = await DBHelper().getUserById(2);
      final homeKey = GlobalKey();
      await tester.pumpWidget(wrapApp(HomeScreen(currentUser: user!), homeKey));

      await Future.delayed(const Duration(milliseconds: 600));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      // 03 Cüzdan Sekmesi
      await saveScreenshot(homeKey, '03_cuzdan_sekmesi.png');

      // 08 Kategori Analiz Modalı
      final analizBtn = find.text('Analiz');
      if (analizBtn.evaluate().isNotEmpty) {
        await tester.tap(analizBtn);
        await tester.pump();
        await tester.pump(const Duration(milliseconds: 400));
        await saveScreenshot(homeKey, '08_kategori_analiz_modal.png');

        // Kapat
        final closeBtn = find.byIcon(Icons.close_rounded);
        if (closeBtn.evaluate().isNotEmpty) {
          await tester.tap(closeBtn);
          await tester.pump();
          await tester.pump(const Duration(milliseconds: 400));
        }
      }

      // 06 Yeni İşlem Ekle Modalı
      final fab = find.byType(FloatingActionButton);
      if (fab.evaluate().isNotEmpty) {
        await tester.tap(fab);
        await tester.pump();
        await tester.pump(const Duration(milliseconds: 400));
        await saveScreenshot(homeKey, '06_yeni_islem_modal.png');
      }
    });
  });

  testWidgets('Capture 04 Tasks, 07 Add Task', (tester) async {
    await tester.runAsync(() async {
      tester.view.physicalSize = const Size(412 * 2, 915 * 2);
      tester.view.devicePixelRatio = 2.0;

      final user = await DBHelper().getUserById(2);
      final homeKey = GlobalKey();
      await tester.pumpWidget(wrapApp(HomeScreen(currentUser: user!), homeKey));

      await Future.delayed(const Duration(milliseconds: 600));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      // Ödevler sekmesine geç
      final odevlerTab = find.text('Ödevlerim');
      if (odevlerTab.evaluate().isNotEmpty) {
        await tester.tap(odevlerTab);
        await tester.pump();
        await tester.pump(const Duration(milliseconds: 400));
        await saveScreenshot(homeKey, '04_odev_sekmesi.png');

        // 07 Yeni Ödev Ekle Modalı
        final fab = find.byType(FloatingActionButton);
        if (fab.evaluate().isNotEmpty) {
          await tester.tap(fab);
          await tester.pump();
          await tester.pump(const Duration(milliseconds: 400));
          await saveScreenshot(homeKey, '07_yeni_odev_modal.png');
        }
      }
    });
  });

  testWidgets('Capture 05 Profile, 09 JSON Export', (tester) async {
    await tester.runAsync(() async {
      tester.view.physicalSize = const Size(412 * 2, 915 * 2);
      tester.view.devicePixelRatio = 2.0;

      final user = await DBHelper().getUserById(2);
      final homeKey = GlobalKey();
      await tester.pumpWidget(wrapApp(HomeScreen(currentUser: user!), homeKey));

      await Future.delayed(const Duration(milliseconds: 600));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      // Profil sekmesine geç
      final profilTab = find.text('Yönetim & JSON');
      if (profilTab.evaluate().isNotEmpty) {
        await tester.tap(profilTab);
        await tester.pump();
        await tester.pump(const Duration(milliseconds: 400));
        await saveScreenshot(homeKey, '05_profil_sekmesi.png');

        // 09 JSON Yedekleme Dışa Aktar Butonu
        final jsonBtn = find.text('JSON Dosyası Olarak Dışa Aktar');
        if (jsonBtn.evaluate().isNotEmpty) {
          await tester.tap(jsonBtn);
          await tester.pump();
          await tester.pump(const Duration(milliseconds: 500));
          await saveScreenshot(homeKey, '09_json_yedekleme_modal.png');
        }
      }
    });
  });
}
