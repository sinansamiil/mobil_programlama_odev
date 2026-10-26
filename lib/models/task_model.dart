class TaskModel {
  final int? id;
  final int userId;
  final String courseName;
  final String title;
  final String dueDate;
  final String priority; // 'Yüksek' (Acil), 'Orta', 'Düşük'
  final bool isCompleted;

  TaskModel({
    this.id,
    required this.userId,
    required this.courseName,
    required this.title,
    required this.dueDate,
    this.priority = 'Orta',
    this.isCompleted = false,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'user_id': userId,
      'course_name': courseName,
      'title': title,
      'due_date': dueDate,
      'priority': priority,
      'is_completed': isCompleted ? 1 : 0,
    };
  }

  factory TaskModel.fromMap(Map<String, dynamic> map) {
    return TaskModel(
      id: map['id'] as int?,
      userId: map['user_id'] as int? ?? 0,
      courseName: map['course_name'] as String? ?? '',
      title: map['title'] as String? ?? '',
      dueDate: map['due_date'] as String? ?? '',
      priority: map['priority'] as String? ?? 'Orta',
      isCompleted: (map['is_completed'] as int? ?? 0) == 1,
    );
  }

  Map<String, dynamic> toJson() => toMap();

  factory TaskModel.fromJson(Map<String, dynamic> json) => TaskModel.fromMap(json);

  TaskModel copyWith({
    int? id,
    int? userId,
    String? courseName,
    String? title,
    String? dueDate,
    String? priority,
    bool? isCompleted,
  }) {
    return TaskModel(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      courseName: courseName ?? this.courseName,
      title: title ?? this.title,
      dueDate: dueDate ?? this.dueDate,
      priority: priority ?? this.priority,
      isCompleted: isCompleted ?? this.isCompleted,
    );
  }
}
