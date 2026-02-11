import click
import os
import subprocess
from .core.ai_engine import AIEngine  # استيراد نسبي
from .utils import get_config, save_config, LOGO  # استيراد نسبي

@click.group()
def cli():
    """Archiforge: Build your future, folder by folder."""
    # طباعة الشعار عند تشغيل الأداة
    click.clear()
    click.echo(LOGO)

@cli.command()
@click.argument('prompt')
def imagine(prompt):
    """الذكاء الاصطناعي يتخيل المشروع وينشئ الملفات لك."""
    config = get_config()
    api_key = config.get('gemini_api_key')

    if not api_key:
        click.secho("❌ لم يتم ضبط مفتاح API. استخدم: archiforge configure-ai", fg="red")
        return

    click.echo(f"🤔 جاري التفكير في: {prompt}...")
    
    ai = AIEngine(api_key)
    result = ai.imagine(prompt)

    if "error" in result:
        click.secho(f"❌ حدث خطأ من AI: {result['error']}", fg="red")
        return

    project_name = result.get('project_name', 'new_archiforge_project')
    files = result.get('files', [])

    # إنشاء مجلد المشروع الرئيسي
    if not os.path.exists(project_name):
        os.makedirs(project_name)

    click.echo(f"🏗️ جاري بناء مشروع: {project_name}...")

    for file_info in files:
        path = file_info['path']
        content = file_info['content']
        
        # المسار الكامل للملف
        full_file_path = os.path.join(project_name, path)
        
        # --- التحديث السحري: إنشاء المجلدات الفرعية تلقائياً ---
        sub_folder = os.path.dirname(full_file_path)
        if sub_folder and not os.path.exists(sub_folder):
            os.makedirs(sub_folder, exist_ok=True)
        
        # كتابة محتوى الملف
        with open(full_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        click.echo(f"  📄 تم إنشاء: {path}")

    click.secho(f"\n✨ تم بنجاح! المشروع جاهز في مجلد '{project_name}'.", fg="green", bold=True)

    # --- ميزة الإصدار 0.4.2: الفتح التلقائي في VS Code ---
    if click.confirm("\n🚀 هل تريد فتح المشروع في VS Code الآن؟", default=True):
        try:
            # استخدام shell=True للتوافق مع ويندوز
            subprocess.run(['code', os.path.abspath(project_name)], shell=True)
        except Exception as e:
            click.echo(f"⚠️ تعذر فتح VS Code تلقائياً: {e}")

@cli.command()
def configure_ai():
    """ضبط إعدادات الذكاء الاصطناعي."""
    api_key = click.prompt("أدخل مفتاح Gemini API الخاص بك", hide_input=True)
    save_config({'gemini_api_key': api_key})
    click.secho("✅ تم حفظ الإعدادات بنجاح!", fg="green")

if __name__ == "__main__":
    cli()