# بنية Agentic AI Assistant

```text
CLI (python -m src.main) أو Streamlit (src/app.py)
                    │
                    ▼
              Agent.run()
          ┌─────────┼─────────┐
          ▼         ▼         ▼
      Memory      Planner   Executor
       JSON       Gemini/    سجل أدوات
                  fallback   آمن
                              │
                ┌─────────────┴─────────────┐
                ▼             ▼             ▼
           calculate     current_time   summarize_text
```

## المكونات

- **الواجهة:** CLI للمحطات والمهام السريعة، وStreamlit للمحادثة المرئية.
- **Agent:** ينسق دورة الطلب، يستعيد الذاكرة، ينفذ الخطة، ثم يصيغ النتيجة.
- **Planner:** يطلب خطة JSON مقيدة من Gemini عند توفر المفتاح، ويستخدم قواعد محلية عند عدم توفره.
- **Executor:** ينفذ الأدوات الموجودة في سجل ثابت فقط؛ لا يستخدم `eval` ولا ينفذ أوامر نظام.
- **Memory:** يحفظ آخر الرسائل في `data/memory.json` مع تحديد عدد الرسائل.
- **Gemini adapter:** يعزل تكامل النموذج ويحوّل أخطاء الاتصال إلى fallback مفهوم.

## حدود الأمان

لا توجد أداة لتنفيذ shell أو قراءة ملفات عشوائية أو إرسال طلبات خارجية. إضافة أي أداة جديدة تتطلب تسجيلها في `tool_registry()` وإدراجها في قائمة التحقق داخل `planner.py`.
