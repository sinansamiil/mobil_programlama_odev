import 'package:flutter/material.dart';

import '../database/db_helper.dart';
import '../models/user_model.dart';
import '../widgets/custom_text_field.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _studentNumberController = TextEditingController();
  final _departmentController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  bool _obscurePassword = true;
  bool _obscureConfirmPassword = true;
  bool _isLoading = false;

  Future<void> _handleRegister() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    final email = _emailController.text.trim();
    final db = DBHelper();

    // E-posta daha önce kayıt edilmiş mi kontrol et
    final existingUser = await db.getUserByEmail(email);
    if (existingUser != null) {
      setState(() => _isLoading = false);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text(
            'Bu e-posta adresiyle zaten kayıtlı bir hesap var!',
          ),
          backgroundColor: const Color(0xFFEF4444),
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
      );
      return;
    }

    final newUser = UserModel(
      name: _nameController.text.trim(),
      email: email,
      password: _passwordController.text,
      studentNumber: _studentNumberController.text.trim().isEmpty
          ? 'Öğrenci'
          : _studentNumberController.text.trim(),
      department: _departmentController.text.trim().isEmpty
          ? 'Mühendislik Fakültesi'
          : _departmentController.text.trim(),
      createdAt: DateTime.now().toIso8601String(),
    );

    final resultId = await db.registerUser(newUser);

    setState(() => _isLoading = false);

    if (!mounted) return;

    if (resultId > 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Row(
            children: [
              Icon(Icons.check_circle_rounded, color: Colors.white),
              SizedBox(width: 10),
              Expanded(
                child: Text(
                  'Kayıt başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.',
                ),
              ),
            ],
          ),
          backgroundColor: const Color(0xFF10B981),
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
      );
      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: const Text('Kayıt oluşturulurken bir hata oluştu.'),
          backgroundColor: const Color(0xFFEF4444),
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
      );
    }
  }

  void _appendNameChar(String char) {
    _nameController.text = '${_nameController.text}$char';
    _nameController.selection = TextSelection.fromPosition(
      TextPosition(offset: _nameController.text.length),
    );
  }

  void _appendEmailText(String text) {
    final current = _emailController.text;
    if (text == '@') {
      _emailController.text = '$current@';
    } else if (text.startsWith('@')) {
      if (current.contains('@')) {
        final prefix = current.split('@')[0];
        _emailController.text = '$prefix$text';
      } else {
        _emailController.text = '$current$text';
      }
    } else {
      _emailController.text = '$current$text';
    }
    _emailController.selection = TextSelection.fromPosition(
      TextPosition(offset: _emailController.text.length),
    );
  }

  Widget _buildQuickInsertChip(String label, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(right: 6),
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: const Color(0xFFE2E8F0)),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.02),
              blurRadius: 4,
              offset: const Offset(0, 1),
            ),
          ],
        ),
        child: Text(
          label,
          style: const TextStyle(
            color: Color(0xFFE11D48),
            fontSize: 11.5,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
    );
  }

  Widget _buildCharChip(String char) {
    return GestureDetector(
      onTap: () => _appendNameChar(char),
      child: Container(
        margin: const EdgeInsets.only(right: 5),
        padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 5),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: const Color(0xFFE2E8F0)),
        ),
        child: Text(
          char,
          style: const TextStyle(
            color: Color(0xFFE11D48),
            fontSize: 13,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _nameController.dispose();
    _studentNumberController.dispose();
    _departmentController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: Container(
          margin: const EdgeInsets.only(left: 12),
          child: IconButton(
            icon: Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: const Color(0xFFE2E8F0)),
              ),
              child: const Icon(
                Icons.arrow_back_ios_new_rounded,
                color: Color(0xFF1E293B),
                size: 16,
              ),
            ),
            onPressed: () => Navigator.pop(context),
          ),
        ),
        title: const Text(
          'Öğrenci Kayıt Formu',
          style: TextStyle(
            color: Color(0xFF1E293B),
            fontSize: 17,
            fontWeight: FontWeight.w800,
          ),
        ),
        centerTitle: true,
      ),
      body: Stack(
        children: [
          // Arka plan ortam gradyanı
          Positioned(
            top: -40,
            right: -40,
            child: Container(
              width: 220,
              height: 220,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: RadialGradient(
                  colors: [
                    const Color(0xFFFF2E56).withValues(alpha: 0.14),
                    Colors.transparent,
                  ],
                ),
              ),
            ),
          ),

          SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Başlık Bilgisi
                    const Text(
                      'Hesap Oluşturun ✨',
                      style: TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.w900,
                        color: Color(0xFF0F172A),
                        letterSpacing: -0.6,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      'Öğrenci Asistanı ile bütçenizi ve derslerinizi tek yerden yönetin.',
                      style: TextStyle(fontSize: 13.5, color: Colors.grey.shade600),
                    ),
                    const SizedBox(height: 24),

                    // Ad Soyad
                    CustomTextField(
                      controller: _nameController,
                      label: 'Ad Soyad',
                      hint: 'Örn: Sinan Şamil Köylü',
                      prefixIcon: Icons.person_outline_rounded,
                      validator: (val) {
                        if (val == null || val.trim().isEmpty) {
                          return 'Lütfen adınızı ve soyadınızı yazın.';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 8),

                    // Türkçe Karakter Ekleme Çubuğu (Emülatör Klavye Kolaylığı)
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          Text(
                            'Türkçe Harfler: ',
                            style: TextStyle(
                              fontSize: 11,
                              color: Colors.grey.shade500,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          _buildCharChip('ç'),
                          _buildCharChip('ğ'),
                          _buildCharChip('ı'),
                          _buildCharChip('ö'),
                          _buildCharChip('ş'),
                          _buildCharChip('ü'),
                          _buildCharChip('Ç'),
                          _buildCharChip('Ğ'),
                          _buildCharChip('İ'),
                          _buildCharChip('Ö'),
                          _buildCharChip('Ş'),
                          _buildCharChip('Ü'),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Bölüm & Öğrenci No yan yana
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          flex: 3,
                          child: CustomTextField(
                            controller: _departmentController,
                            label: 'Bölüm',
                            hint: 'Yazılım Müh.',
                            prefixIcon: Icons.school_outlined,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          flex: 2,
                          child: CustomTextField(
                            controller: _studentNumberController,
                            label: 'Öğrenci No',
                            hint: '240211019',
                            prefixIcon: Icons.badge_outlined,
                            keyboardType: TextInputType.number,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),

                    // E-posta
                    CustomTextField(
                      controller: _emailController,
                      label: 'E-posta Adresi',
                      hint: 'ornek@ogrenci.edu.tr',
                      prefixIcon: Icons.email_outlined,
                      suffixIcon: TextButton(
                        onPressed: () => _appendEmailText('@'),
                        style: TextButton.styleFrom(
                          minimumSize: const Size(36, 36),
                          padding: EdgeInsets.zero,
                        ),
                        child: const Text(
                          '@',
                          style: TextStyle(
                            color: Color(0xFFE11D48),
                            fontWeight: FontWeight.w900,
                            fontSize: 18,
                          ),
                        ),
                      ),
                      keyboardType: TextInputType.emailAddress,
                      validator: (val) {
                        if (val == null || val.trim().isEmpty) {
                          return 'Lütfen e-posta adresinizi girin.';
                        }
                        if (!val.contains('@') || !val.contains('.')) {
                          return 'Geçerli bir e-posta adresi yazın.';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 8),

                    // Emülatör Kolaylığı: Hızlı @ ve Domain Ekleme Butonları
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: [
                          Text(
                            'Hızlı Domain: ',
                            style: TextStyle(
                              fontSize: 11,
                              color: Colors.grey.shade500,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          _buildQuickInsertChip('@', () => _appendEmailText('@')),
                          _buildQuickInsertChip('@gmail.com', () => _appendEmailText('@gmail.com')),
                          _buildQuickInsertChip('@hotmail.com', () => _appendEmailText('@hotmail.com')),
                          _buildQuickInsertChip('@ogr.edu.tr', () => _appendEmailText('@ogr.edu.tr')),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Şifre
                    CustomTextField(
                      controller: _passwordController,
                      label: 'Şifre',
                      hint: 'En az 6 karakter',
                      prefixIcon: Icons.lock_outline_rounded,
                      obscureText: _obscurePassword,
                      suffixIcon: IconButton(
                        icon: Icon(
                          _obscurePassword
                              ? Icons.visibility_off_outlined
                              : Icons.visibility_outlined,
                          color: Colors.grey.shade500,
                          size: 20,
                        ),
                        onPressed: () {
                          setState(() => _obscurePassword = !_obscurePassword);
                        },
                      ),
                      validator: (val) {
                        if (val == null || val.isEmpty) {
                          return 'Lütfen şifre belirleyin.';
                        }
                        if (val.length < 6) {
                          return 'Şifre en az 6 karakter olmalıdır.';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),

                    // Şifre Tekrar
                    CustomTextField(
                      controller: _confirmPasswordController,
                      label: 'Şifre Tekrarı',
                      hint: 'Şifrenizi doğrulayın',
                      prefixIcon: Icons.lock_reset_rounded,
                      obscureText: _obscureConfirmPassword,
                      suffixIcon: IconButton(
                        icon: Icon(
                          _obscureConfirmPassword
                              ? Icons.visibility_off_outlined
                              : Icons.visibility_outlined,
                          color: Colors.grey.shade500,
                          size: 20,
                        ),
                        onPressed: () {
                          setState(
                            () =>
                                _obscureConfirmPassword = !_obscureConfirmPassword,
                          );
                        },
                      ),
                      validator: (val) {
                        if (val == null || val.isEmpty) {
                          return 'Lütfen şifrenizi tekrar girin.';
                        }
                        if (val != _passwordController.text) {
                          return 'Şifreler birbiriyle eşleşmiyor!';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 28),

                    // Kayıt Ol Butonu
                    Container(
                      decoration: BoxDecoration(
                        gradient: const LinearGradient(
                          colors: [Color(0xFFFF2E56), Color(0xFFE11D48), Color(0xFFBE123C)],
                        ),
                        borderRadius: BorderRadius.circular(16),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFFE11D48).withValues(alpha: 0.38),
                            blurRadius: 18,
                            offset: const Offset(0, 8),
                          ),
                        ],
                      ),
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _handleRegister,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.transparent,
                          shadowColor: Colors.transparent,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                        ),
                        child: _isLoading
                            ? const SizedBox(
                                height: 22,
                                width: 22,
                                child: CircularProgressIndicator(
                                  color: Colors.white,
                                  strokeWidth: 2.5,
                                ),
                              )
                            : const Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                    'Kayıt Ol ve Tamamla',
                                    style: TextStyle(
                                      fontSize: 16,
                                      fontWeight: FontWeight.w800,
                                      color: Colors.white,
                                      letterSpacing: -0.2,
                                    ),
                                  ),
                                  SizedBox(width: 8),
                                  Icon(Icons.check_circle_rounded, color: Colors.white, size: 18),
                                ],
                              ),
                      ),
                    ),
                    const SizedBox(height: 22),

                    // Giriş Yap Bağlantısı
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          'Zaten bir hesabınız var mı? ',
                          style: TextStyle(
                            color: Colors.grey.shade600,
                            fontSize: 14,
                          ),
                        ),
                        GestureDetector(
                          onTap: () => Navigator.pop(context),
                          child: const Text(
                            'Giriş Yap',
                            style: TextStyle(
                              color: Color(0xFFE11D48),
                              fontSize: 14,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
