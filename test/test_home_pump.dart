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
}

void main() {
  setUpAll(() async {
    sqfliteFfiInit();
    databaseFactory = databaseFactoryFfi;
    PathProviderPlatform.instance = FakePathProviderPlatform();
    SharedPreferences.setMockInitialValues({});
    await loadFonts();
  });

  testWidgets('Test HomeScreen with real fonts in runAsync', (tester) async {
    await tester.runAsync(() async {
      final dbHelper = DBHelper();
      final user = await dbHelper.getUserById(2);

      tester.view.physicalSize = const Size(412 * 2, 915 * 2);
      tester.view.devicePixelRatio = 2.0;

      final key = GlobalKey();
      await tester.pumpWidget(
        MaterialApp(
          debugShowCheckedModeBanner: false,
          theme: ThemeData(
            useMaterial3: true,
            colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFFE11D48)),
            scaffoldBackgroundColor: const Color(0xFFF9FAFB),
            fontFamily: 'Roboto',
          ),
          builder: (ctx, child) => RepaintBoundary(key: key, child: child!),
          home: HomeScreen(currentUser: user!),
        ),
      );

      // Wait for SQLite query in initState to finish
      await Future.delayed(const Duration(milliseconds: 600));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 100));

      final boundary = key.currentContext!.findRenderObject() as RenderRepaintBoundary;
      final image = await boundary.toImage(pixelRatio: 1.0);
      final byteData = await image.toByteData(format: ui.ImageByteFormat.png);

      File('screenshots/03_cuzdan_sekmesi.png').writeAsBytesSync(byteData!.buffer.asUint8List());
      print('Saved 03_cuzdan_sekmesi.png: ${File('screenshots/03_cuzdan_sekmesi.png').lengthSync()} bytes');
    });
  });
}
