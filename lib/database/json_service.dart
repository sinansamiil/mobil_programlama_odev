import 'dart:convert';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart';
import 'db_helper.dart';

class JsonService {
  static const String backupFileName = 'ogrenci_asistani_yedek.json';

  /// Veritabanındaki tüm kullanıcıları, harcamaları ve görevleri
  /// JSON formatında bir dosyaya kaydeder.
  static Future<Map<String, dynamic>> exportDataToJsonFile() async {
    final dbHelper = DBHelper();
    final users = await dbHelper.getAllUsers();
    
    // Tüm kullanıcıların ilişkisel verilerini topla
    List<Map<String, dynamic>> exportData = [];

    for (var user in users) {
      if (user.id == null) continue;
      final trans = await dbHelper.getTransactions(user.id!);
      final tasks = await dbHelper.getTasks(user.id!);

      exportData.add({
        'user': user.toJson(),
        'transactions': trans.map((t) => t.toJson()).toList(),
        'tasks': tasks.map((t) => t.toJson()).toList(),
      });
    }

    final fullBackup = {
      'proje_adi': 'Öğrenci Asistanı - Flutter SQLite & JSON',
      'olusturucu': 'Sinan Şamil Köylü',
      'yedekleme_tarihi': DateTime.now().toIso8601String(),
      'toplam_kullanici': users.length,
      'kullanici_verileri': exportData,
    };

    final jsonString = const JsonEncoder.withIndent('  ').convert(fullBackup);

    // Dosyaya yazma işlemi (File I/O)
    final directory = await getApplicationDocumentsDirectory();
    final filePath = join(directory.path, backupFileName);
    final file = File(filePath);
    await file.writeAsString(jsonString, flush: true);

    return {
      'filePath': filePath,
      'jsonString': jsonString,
      'totalUsers': users.length,
      'fileSize': await file.length(),
    };
  }

  /// Daha önce kaydedilmiş JSON dosyasının içeriğini okur.
  static Future<String?> readJsonBackupFile() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final filePath = join(directory.path, backupFileName);
      final file = File(filePath);
      if (await file.exists()) {
        return await file.readAsString();
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}
