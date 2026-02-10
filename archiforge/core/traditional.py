import shutil
import os
from pathlib import Path

class TraditionalEngine:
    def __init__(self):
        # تحديد مسار القوالب بالنسبة لموقع الملف الحالي
        self.blueprints_path = Path(__file__).parent.parent.parent / "blueprints"

    def forge(self, lang: str, project_name: str):
        target_path = Path.cwd() / project_name
        template_source = self.blueprints_path / lang

        if not template_source.exists():
            raise FileNotFoundError(f"لم يتم العثور على قالب للغة: {lang}")

        # 1. نسخ المجلد بالكامل
        shutil.copytree(template_source, target_path, dirs_exist_ok=True)

        # 2. تخصيص الملفات (تبديل اسم المشروع داخل README مثلاً)
        self._customize_project(target_path, project_name)
        
        return target_path

    def _customize_project(self, target_path, project_name):
        for root, _, files in os.walk(target_path):
            for file in files:
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8')
                    # استبدال كلمة placeholder باسم المشروع الحقيقي
                    new_content = content.replace("{{PROJECT_NAME}}", project_name)
                    file_path.write_text(new_content, encoding='utf-8')
                except: 
                    pass # لتجنب الملفات غير النصية
    
    # أضف هذه الدالة داخل كلاس TraditionalEngine في ملف traditional.py

    def list_available_blueprints(self):
        """إحضار قائمة بكافة القوالب الموجودة في مجلد blueprints"""
        if not self.blueprints_path.exists():
            return []
        
        # جلب أسماء المجلدات فقط وتجاهل الملفات المخفية
        return [d.name for d in self.blueprints_path.iterdir() if d.is_dir() and not d.name.startswith('.')]