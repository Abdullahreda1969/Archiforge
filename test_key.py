import google.generativeai as genai
import yaml
from pathlib import Path

def test_api():
    # 1. تحميل المفتاح من ملفك الـ YAML
    config_path = Path.home() / ".archiforge_config.yaml"
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            api_key = config.get("gemini_api_key")
    except Exception as e:
        print(f"❌ تعذر قراءة ملف الإعدادات: {e}")
        return

    if not api_key:
        print("❌ لم يتم العثور على المفتاح داخل ملف YAML!")
        return

    print(f"🔑 جاري فحص المفتاح: {api_key[:5]}...{api_key[-5:]}")
    genai.configure(api_key=api_key)

    print("\n🔍 الموديلات المتاحة لحسابك:")
    print("-" * 30)
    
    try:
        # محاولة سرد الموديلات التي تدعم إنشاء المحتوى
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ {m.name}")
                available_models.append(m.name)
        
        if not available_models:
            print("⚠️ غريب! لم يتم العثور على موديلات تدعم generateContent.")
        else:
            print("-" * 30)
            print(f"\n💡 اقتراح: استخدم الموديل الأول في القائمة أعلاه.")
            
    except Exception as e:
        print(f"❌ فشل الاتصال بالـ API: {e}")

if __name__ == "__main__":
    test_api()