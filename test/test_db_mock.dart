import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:path_provider_platform_interface/path_provider_platform_interface.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';
import 'package:ogrenci_asistani/database/db_helper.dart';

class FakePathProviderPlatform extends Fake
    with MockPlatformInterfaceMixin
    implements PathProviderPlatform {
  @override
  Future<String?> getApplicationDocumentsPath() async {
    return Directory.current.path;
  }
}

void main() {
  test('Test DBHelper with mocked path provider', () async {
    PathProviderPlatform.instance = FakePathProviderPlatform();
    final dbHelper = DBHelper();
    final stats = await dbHelper.getDatabaseStats();
    print('DB stats: $stats');
  });
}
