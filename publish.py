import subprocess
import sys
import os

# تأكد من إضافة هذا السطر في الأعلى تماماً
VERSION = "0.4.2"

def run_command(command, description):
    print(f"🚀 {description}...")
    # استخدام shell=True للتوافق مع PowerShell
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ فشلت عملية: {description}")
        sys.exit(1)

def main():
    # تأكد من استيراد الدالة هنا لتجنب مشاكل المسارات
    try:
        from archiforge.archiver import make_release_archive
    except ImportError:
        print("❌ فشل استيراد archiver. تأكد أنك في المجلد الرئيسي للمشروع.")
        sys.exit(1)

    print(f"📦 بدء عملية النشر للإصدار {VERSION}")

    # 1. الأرشفة أولاً
    success, path_or_error = make_release_archive(VERSION)
    if success:
        print(f"✅ تم حفظ نسخة الأرشيف في: {path_or_error}.zip")
    else:
        print(f"⚠️ فشلت الأرشفة: {path_or_error}")
        if input("هل تريد الاستمرار في الرفع رغم ذلك؟ (y/n): ") != 'y':
            return

    # 2. بناء الحزمة
    run_command("python -m build", "جاري بناء الحزمة (Build)")

    # 3. الرفع لـ PyPI
    run_command("python -m twine upload dist/*", "جاري الرفع إلى PyPI")

    print(f"\n🎊 مبروك! تمت الأرشفة والبناء والرفع للنسخة {VERSION} بنجاح.")

if __name__ == "__main__":
    main()