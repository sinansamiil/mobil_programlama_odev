import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import '../models/user_model.dart';
import '../models/transaction_model.dart';
import '../models/task_model.dart';

class DBHelper {
  static final DBHelper _instance = DBHelper._internal();
  factory DBHelper() => _instance;
  DBHelper._internal();

  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    // Desktop (Windows/Linux) FFI initialization
    if (!kIsWeb && (Platform.isWindows || Platform.isLinux)) {
      sqfliteFfiInit();
      databaseFactory = databaseFactoryFfi;
    }

    String path;
    if (!kIsWeb && (Platform.isWindows || Platform.isLinux)) {
      final appDocDir = await getApplicationDocumentsDirectory();
      path = join(appDocDir.path, 'ogrenci_asistani.db');
    } else {
      final databasesPath = await getDatabasesPath();
      path = join(databasesPath, 'ogrenci_asistani.db');
    }

    return await openDatabase(
      path,
      version: 1,
      onCreate: _onCreate,
      onConfigure: _onConfigure,
    );
  }

  Future<void> _onConfigure(Database db) async {
    // Foreign key constraints support in SQLite
    await db.execute('PRAGMA foreign_keys = ON');
  }

  Future<void> _onCreate(Database db, int version) async {
    // 1. Users Table
    await db.execute('''
      CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        student_number TEXT,
        department TEXT,
        created_at TEXT NOT NULL
      )
    ''');

    // 2. Transactions Table (Income & Expense)
    await db.execute('''
      CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
      )
    ''');

    // 3. Tasks Table (Assignments & Exams)
    await db.execute('''
      CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_name TEXT NOT NULL,
        title TEXT NOT NULL,
        due_date TEXT NOT NULL,
        priority TEXT NOT NULL,
        is_completed INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
      )
    ''');
  }

  // ==================== USER OPERATIONS ====================

  Future<int> registerUser(UserModel user) async {
    final db = await database;
    try {
      final map = user.toMap();
      map['email'] = (map['email'] as String).trim().toLowerCase();
      final id = await db.insert(
        'users',
        map,
        conflictAlgorithm: ConflictAlgorithm.abort,
      );
      return id;
    } catch (e) {
      // Typically email uniqueness violation
      return -1;
    }
  }

  Future<void> clearAllData() async {
    final db = await database;
    await db.delete('tasks');
    await db.delete('transactions');
    await db.delete('users');
  }

  Future<UserModel?> loginUser(String email, String password) async {
    final db = await database;
    final cleanEmail = email.trim().toLowerCase();
    final List<Map<String, dynamic>> results = await db.query(
      'users',
      where: 'email = ? AND password = ?',
      whereArgs: [cleanEmail, password],
      limit: 1,
    );

    if (results.isNotEmpty) {
      return UserModel.fromMap(results.first);
    }
    return null;
  }

  Future<UserModel?> getUserByEmail(String email) async {
    final db = await database;
    final cleanEmail = email.trim().toLowerCase();
    final List<Map<String, dynamic>> results = await db.query(
      'users',
      where: 'email = ?',
      whereArgs: [cleanEmail],
      limit: 1,
    );

    if (results.isNotEmpty) {
      return UserModel.fromMap(results.first);
    }
    return null;
  }

  Future<UserModel?> getUserById(int id) async {
    final db = await database;
    final List<Map<String, dynamic>> results = await db.query(
      'users',
      where: 'id = ?',
      whereArgs: [id],
      limit: 1,
    );

    if (results.isNotEmpty) {
      return UserModel.fromMap(results.first);
    }
    return null;
  }

  Future<List<UserModel>> getAllUsers() async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query('users', orderBy: 'id DESC');
    return maps.map((m) => UserModel.fromMap(m)).toList();
  }

  // ==================== TRANSACTION OPERATIONS ====================

  Future<int> insertTransaction(TransactionModel item) async {
    final db = await database;
    return await db.insert('transactions', item.toMap());
  }

  Future<List<TransactionModel>> getTransactions(int userId) async {
    final db = await database;
    final List<Map<String, dynamic>> maps = await db.query(
      'transactions',
      where: 'user_id = ?',
      whereArgs: [userId],
      orderBy: 'id DESC',
    );
    return maps.map((m) => TransactionModel.fromMap(m)).toList();
  }

  Future<int> deleteTransaction(int id) async {
    final db = await database;
    return await db.delete(
      'transactions',
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<double> getTotalIncome(int userId) async {
    final db = await database;
    final result = await db.rawQuery(
      "SELECT SUM(amount) as total FROM transactions WHERE user_id = ? AND type = 'income'",
      [userId],
    );
    final value = result.first['total'];
    return (value != null) ? (value as num).toDouble() : 0.0;
  }

  Future<double> getTotalExpense(int userId) async {
    final db = await database;
    final result = await db.rawQuery(
      "SELECT SUM(amount) as total FROM transactions WHERE user_id = ? AND type = 'expense'",
      [userId],
    );
    final value = result.first['total'];
    return (value != null) ? (value as num).toDouble() : 0.0;
  }

  Future<double> getTotalBalance(int userId) async {
    final income = await getTotalIncome(userId);
    final expense = await getTotalExpense(userId);
    return income - expense;
  }

  // ==================== TASK OPERATIONS ====================

  Future<int> insertTask(TaskModel item) async {
    final db = await database;
    return await db.insert('tasks', item.toMap());
  }

  Future<List<TaskModel>> getTasks(int userId, {String filter = 'all'}) async {
    final db = await database;
    String whereClause = 'user_id = ?';
    List<dynamic> whereArgs = [userId];

    if (filter == 'pending') {
      whereClause += ' AND is_completed = 0';
    } else if (filter == 'completed') {
      whereClause += ' AND is_completed = 1';
    }

    final List<Map<String, dynamic>> maps = await db.query(
      'tasks',
      where: whereClause,
      whereArgs: whereArgs,
      orderBy: 'is_completed ASC, id DESC',
    );
    return maps.map((m) => TaskModel.fromMap(m)).toList();
  }

  Future<int> toggleTaskStatus(int id, bool isCompleted) async {
    final db = await database;
    return await db.update(
      'tasks',
      {'is_completed': isCompleted ? 1 : 0},
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<int> deleteTask(int id) async {
    final db = await database;
    return await db.delete(
      'tasks',
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  Future<int> getPendingTasksCount(int userId) async {
    final db = await database;
    final result = await db.rawQuery(
      'SELECT COUNT(*) as count FROM tasks WHERE user_id = ? AND is_completed = 0',
      [userId],
    );
    return Sqflite.firstIntValue(result) ?? 0;
  }

  // ==================== DEMO SEED DATA ====================

  Future<void> seedDemoData(int userId) async {
    final db = await database;

    // Check if user already has data
    final existingTrans = await db.query('transactions', where: 'user_id = ?', whereArgs: [userId]);
    if (existingTrans.isNotEmpty) return;

    // Sample initial transactions
    final now = DateTime.now();
    final dateStr = "${now.day.toString().padLeft(2, '0')}.${now.month.toString().padLeft(2, '0')}.${now.year}";

    await db.insert('transactions', {
      'user_id': userId,
      'title': 'Aylık KYK / Aile Harçlığı',
      'amount': 4500.0,
      'type': 'income',
      'category': 'Burs & Harçlık',
      'date': dateStr,
    });

    await db.insert('transactions', {
      'user_id': userId,
      'title': 'Üniversite Yemekhane Yüklemesi',
      'amount': 350.0,
      'type': 'expense',
      'category': 'Yemek',
      'date': dateStr,
    });

    await db.insert('transactions', {
      'user_id': userId,
      'title': 'Flutter Mobil Ders Kitabı & Fotokopi',
      'amount': 220.0,
      'type': 'expense',
      'category': 'Kırtasiye & Kitap',
      'date': dateStr,
    });

    // Sample initial tasks
    await db.insert('tasks', {
      'user_id': userId,
      'course_name': 'Mobil Programlama',
      'title': 'Flutter SQLite & Login Ödevi Teslimi',
      'due_date': '24.10.2026',
      'priority': 'Yüksek',
      'is_completed': 1,
    });

    await db.insert('tasks', {
      'user_id': userId,
      'course_name': 'Veritabanı Yönetimi',
      'title': 'İlişkisel Veritabanı ER Diyagramı Çizimi',
      'due_date': '28.10.2026',
      'priority': 'Orta',
      'is_completed': 0,
    });

    await db.insert('tasks', {
      'user_id': userId,
      'course_name': 'Yazılım Mühendisliği',
      'title': 'Sprint 2 Görevlerinin İncelenmesi',
      'due_date': '30.10.2026',
      'priority': 'Düşük',
      'is_completed': 0,
    });
  }

  // ==================== STATS FOR TEACHER ====================

  Future<Map<String, int>> getDatabaseStats() async {
    final db = await database;
    final usersCount = Sqflite.firstIntValue(await db.rawQuery('SELECT COUNT(*) FROM users')) ?? 0;
    final transCount = Sqflite.firstIntValue(await db.rawQuery('SELECT COUNT(*) FROM transactions')) ?? 0;
    final tasksCount = Sqflite.firstIntValue(await db.rawQuery('SELECT COUNT(*) FROM tasks')) ?? 0;

    return {
      'users': usersCount,
      'transactions': transCount,
      'tasks': tasksCount,
    };
  }
}
