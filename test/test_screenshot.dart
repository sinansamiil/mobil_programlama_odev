import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ogrenci_asistani/main.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';

Future<void> loadFonts() async {
  const fontFolder = 'C:/src/flutter/bin/cache/artifacts/material_fonts';

  final robotoReg = File('$fontFolder/roboto-regular.ttf').readAsBytesSync();
  final robotoLoader = FontLoader('Roboto')
    ..addFont(Future.value(ByteData.view(robotoReg.buffer)));
  final robotoBold = File('$fontFolder/roboto-bold.ttf').readAsBytesSync();
  robotoLoader.addFont(Future.value(ByteData.view(robotoBold.buffer)));
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
  });

  testWidgets('Capture Login Screen to PNG', (tester) async {
    await loadFonts();

    final key = GlobalKey();
    tester.view.physicalSize = const Size(412 * 2, 915 * 2);
    tester.view.devicePixelRatio = 2.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(
      RepaintBoundary(
        key: key,
        child: const KampusAsistaniApp(),
      ),
    );
    await tester.pumpAndSettle();

    final boundary = key.currentContext!.findRenderObject() as RenderRepaintBoundary;
    final image = await boundary.toImage(pixelRatio: 1.0);
    final byteData = await image.toByteData(format: ui.ImageByteFormat.png);

    final dir = Directory('screenshots');
    if (!dir.existsSync()) dir.createSync();

    File('screenshots/01_login_screen.png').writeAsBytesSync(byteData!.buffer.asUint8List());
    print('Screenshot saved: ${File('screenshots/01_login_screen.png').lengthSync()} bytes');
  });
}
