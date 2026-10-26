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

  // Consolas for monospace font
  final monoFont = File('C:/Windows/Fonts/consola.ttf').readAsBytesSync();
  final monoLoader = FontLoader('monospace')
    ..addFont(Future.value(ByteData.view(monoFont.buffer)));
  await monoLoader.load();
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

  testWidgets('Capture 09 JSON Export Dialog with Monospace Font', (tester) async {
    await tester.runAsync(() async {
      tester.view.physicalSize = const Size(412 * 2, 915 * 2);
      tester.view.devicePixelRatio = 2.0;

      final user = await DBHelper().getUserById(2);
      final homeKey = GlobalKey();
      await tester.pumpWidget(wrapApp(HomeScreen(currentUser: user!), homeKey));

      await Future.delayed(const Duration(milliseconds: 600));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      final profilTab = find.text('Yönetim & JSON');
      if (profilTab.evaluate().isNotEmpty) {
        await tester.tap(profilTab);
        await tester.pump();
        await tester.pump(const Duration(milliseconds: 400));

        await tester.drag(find.byType(SingleChildScrollView), const Offset(0, -350));
        await tester.pump();
        await tester.pump(const Duration(milliseconds: 300));

        final jsonBtn = find.text('Verileri JSON Olarak Dışa Aktar & Görüntüle');
        if (jsonBtn.evaluate().isNotEmpty) {
          await tester.tap(jsonBtn);
          await Future.delayed(const Duration(milliseconds: 600));
          await tester.pump();
          await tester.pump(const Duration(milliseconds: 400));
          await saveScreenshot(homeKey, '09_json_yedekleme_modal.png');
        }
      }
    });
  });
}
