import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ogrenci_asistani/screens/login_screen.dart';

void main() {
  testWidgets('Capture Login Screen with Real Font', (tester) async {
    final fontData = File('C:/Windows/Fonts/arial.ttf').readAsBytesSync();
    final fontLoader = FontLoader('Roboto')..addFont(Future.value(ByteData.view(fontData.buffer)));
    await fontLoader.load();

    final boldData = File('C:/Windows/Fonts/arialbd.ttf').readAsBytesSync();
    final boldLoader = FontLoader('Roboto')..addFont(Future.value(ByteData.view(boldData.buffer)));
    await boldLoader.load();

    // Material Icons font loader
    // Check if material icons font exists in flutter cache or unit test assets
    print('Fonts loaded successfully');
  });
}
