import click
import yaml
import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from archiforge.core.traditional import TraditionalEngine
from archiforge.core.ai_engine import AIEngine  # تأكد من إنشاء الملف كما اتفقنا
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()
trad_engine = TraditionalEngine()

# دالة مساعدة لتحميل المفتاح من الإعدادات
def get_api_key():
    config_path = Path.home() / ".archiforge_config.yaml"
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            return config.get("gemini_api_key")
    return None


# في أعلى ملف cli.py
LOGO = r"""
[bold cyan]
    _             _     _  __                       
   / \   _ __ ___| |__ (_)/ _| ___  _ __ __ _  ___ 
  / _ \ | '__/ __| '_ \| | |_ / _ \| '__/ _` |/ _ \
 / ___ \| | | (__| | | | |  _| (_) | | | (_| |  __/
/_/   \_\_|  \___|_| |_|_|_|  \___/|_|  \__, |\___|
                                        |___/      
[/bold cyan]
[dim]        --- Build your future, folder by folder ---[/dim]
"""

@click.group()
def cli():
    """Archiforge v0.4.0: أداة بناء المشاريع الذكية 🛠️"""
    # عرض الشعار عند تشغيل أي أمر
    console.print(LOGO)

@cli.command()
@click.option('--name', prompt='Project Name')
@click.option('--lang', type=click.Choice(trad_engine.list_available_blueprints(), case_sensitive=False), default='python')
def create(name, lang):
    """إنشاء مشروع جديد مع شريط تقدم وتفاعل ذكي"""
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        
        # مهمة وهمية ليعطي شعوراً بالسرعة والاحترافية
        task = progress.add_task(description=f"🏗️ جاري بناء {lang}...", total=100)
        
        try:
            # تنفيذ عملية النسخ
            path = trad_engine.forge(lang, name)
            
            # تحديث الشريط تدريجياً
            while not progress.finished:
                progress.update(task, advance=20)
                import time; time.sleep(0.1) # مجرد تأثير بصري بسيط

            console.print(f"\n[bold green]✅ تم بنجاح! استمتع ببناء مشروعك في: {path}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ خطأ غير متوقع: {e}[/bold red]")
        
        # --- ميزة Git التلقائية ---
            try:
                # 1. الدخول للمجلد وتشغيل git init
                subprocess.run(["git", "init"], cwd=str(path), check=True, capture_output=True)
                
                # 2. إضافة الملفات وعمل أول Commit (اختياري لكنه احترافي)
                subprocess.run(["git", "add", "."], cwd=str(path), check=True, capture_output=True)
                subprocess.run(["git", "commit", "-m", "Initial commit by Archiforge 🏗️"], cwd=str(path), check=True, capture_output=True)
                
                console.print("[dim]🔗 تم إنشاء مستودع Git وعمل Initial Commit...[/dim]")
            except Exception:
                console.print("[yellow]⚠️ تنبيه: تعذر تهيئة Git (تأكد من تثبيته لديك).[/yellow]")
        
        try:
            # محاولة فتح المجلد في VS Code
            subprocess.run(["code", str(path)], shell=True)
            console.print("[dim]🚀 تم فتح المشروع في VS Code تلقائياً...[/dim]")
        except Exception:
            pass # إذا لم يكن VS Code مثبتاً، لا نفعل شيئاً
        
@cli.command()
@click.argument('prompt')
@click.option('--name', prompt='Project Name')
def imagine(prompt, name):
    """تخيل وبناء مشروع مخصص بالكود (المحرك المبدع)"""
    api_key = get_api_key()
    if not api_key:
        console.print("[bold red]❌ مفتاح API غير موجود! استخدم أمر configure-ai أولاً.[/bold red]")
        return

    ai = AIEngine(api_key)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="🤔 جاري التفكير في معمارية المشروع...", total=None)
        try:
            # طلب الهيكل والكود من Gemini
            project_data = ai.imagine_project(prompt)
            
            # إنشاء المجلدات والملفات
            output_path = Path.cwd() / name
            output_path.mkdir(parents=True, exist_ok=True)
            
            for folder in project_data.get('directories', []):
                (output_path / folder).mkdir(parents=True, exist_ok=True)
            
            for file_path, content in project_data.get('files', {}).items():
                f_path = output_path / file_path
                f_path.parent.mkdir(parents=True, exist_ok=True)
                f_path.write_text(content, encoding='utf-8')
                
            console.print(f"[bold green]✨ ذكاء Archiforge أنجز المهمة! تم بناء '{name}' بنجاح مع الكود الأساسي.[/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ حدث خطأ أثناء التخيل: {e}[/bold red]")

@cli.command()
@click.option('--key', prompt='Enter your Gemini API Key', hide_input=True)
def configure_ai(key):
    """حفظ مفتاح Gemini API في إعدادات البرنامج"""
    config_path = Path.home() / ".archiforge_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump({"gemini_api_key": key}, f)
    console.print("[bold green]🔑 تم حفظ المفتاح بنجاح![/bold green]")
    
# أضف هذا الأمر في ملف cli.py

@cli.command(name="list")
def list_templates():
    """عرض كافة القوالب المتاحة في Archiforge"""
    templates = trad_engine.list_available_blueprints()
    
    if not templates:
        console.print("[bold red]⚠️ لا توجد قوالب متوفرة حالياً في مجلد blueprints.[/bold red]")
        return

    console.print("[bold cyan]📋 القوالب المتاحة حالياً:[/bold cyan]")
    from rich.table import Table
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("اسم القالب", style="yellow")
    table.add_column("الحالة", style="green")

    for t in templates:
        table.add_row(t, "جاهز للاستخدام ✅")

    console.print(table)


@cli.command()
@click.argument('project_name')
def delete(project_name):
    """حذف مشروع تم إنشاؤه بواسطة Archiforge"""
    project_path = Path.cwd() / project_name
    
    if not project_path.exists():
        console.print(f"[bold red]❌ خطأ: المجلد '{project_name}' غير موجود.[/bold red]")
        return

    # رسالة تأكيد للأمان
    if click.confirm(f"[bold yellow]⚠️ هل أنت متأكد أنك تريد حذف المجلد '{project_name}' بالكامل؟[/bold yellow]", abort=True):
        with console.status("[bold red]🗑️ جاري الحذف...[/bold red]"):
            try:
                import shutil
                shutil.rmtree(project_path)
                console.print(f"[bold green]✨ تم حذف '{project_name}' بنجاح. المكان أصبح نظيفاً الآن![/bold green]")
            except Exception as e:
                console.print(f"[bold red]❌ فشل الحذف: {e}[/bold red]")


if __name__ == "__main__":
    cli()