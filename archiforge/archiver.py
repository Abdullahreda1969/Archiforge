import shutil
import os
from pathlib import Path
from datetime import datetime

def make_release_archive(version):
    """يؤرشف الكود الحالي في مجلد releases"""
    # تحديد المسارات
    root_dir = Path.cwd()
    releases_dir = root_dir / "releases"
    releases_dir.mkdir(exist_ok=True)

    # اسم الملف المضغوط (مثال: archiforge_v0.4.1_2026-02-11.zip)
    date_str = datetime.now().strftime("%Y-%m-%d")
    archive_name = f"archiforge_v{version}_{date_str}"
    archive_path = releases_dir / archive_name

    try:
        # ضغط مجلد الكود الأساسي والقوالب وpyproject.toml
        # سنقوم بإنشاء مجلد مؤقت للتجميع قبل الضغط لضمان نظافة الأرشيف
        temp_dir = releases_dir / "temp_build"
        temp_dir.mkdir(exist_ok=True)

        # نسخ الملفات الضرورية فقط للأرشيف
        dirs_to_copy = ['archiforge', 'blueprints']
        files_to_copy = ['pyproject.toml', 'README.md', 'MANIFEST.in']

        for d in dirs_to_copy:
            if (root_dir / d).exists():
                shutil.copytree(root_dir / d, temp_dir / d, dirs_exist_ok=True)
        
        for f in files_to_copy:
            if (root_dir / f).exists():
                shutil.copy2(root_dir / f, temp_dir / f)

        # إنشاء الملف المضغوط
        shutil.make_archive(str(archive_path), 'zip', root_dir=temp_dir)
        
        # حذف المجلد المؤقت
        shutil.rmtree(temp_dir)
        
        return True, archive_path
    except Exception as e:
        return False, str(e)