import 'package:flutter_test/flutter_test.dart';
import 'package:ogrenci_asistani/main.dart';

void main() {
  testWidgets('Kampus Asistani smoke test - Login Screen loads', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const KampusAsistaniApp());

    // Login ekranındaki başlıkların ve alanların yüklendiğini doğrula
    expect(find.text('Öğrenci Asistanı'), findsOneWidget);
    expect(find.text('Giriş Yap'), findsOneWidget);
    expect(find.text('Kayıt Olun'), findsOneWidget);
  });
}
