# Agentic AI Assistant

تطبيق وكيل ذكاء اصطناعي عملي وخفيف، مبني على Python وGemini اختياريًا. يعمل في وضعين:

- **وضع محلي دون مفتاح API:** ينفذ الحساب والوقت والتلخيص الاحتياطي ويحفظ ذاكرة المحادثة.
- **وضع Gemini:** يستخدم Gemini للتخطيط وصياغة الإجابة النهائية، مع قصر تنفيذ الأدوات على سجل أدوات آمن.

## التشغيل السريع

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m src.main "احسب 25 * 4"
python -m src.main
```

لتمكين Gemini، ضع `GOOGLE_API_KEY` في `.env`. لا تضع المفتاح داخل Git.

## واجهة الويب الاختيارية

```bash
streamlit run src/app.py
```

## الأدوات الحالية

- `calculate`: حساب آمن باستخدام AST، دون `eval`.
- `current_time`: إرجاع الوقت الحالي بصيغة ISO.
- `summarize_text`: تلخيص احتياطي محلي.

يمكن إضافة أدوات جديدة إلى `src/tools/builtin.py` ثم إدراجها في سجل الأدوات وقواعد التحقق في المخطط.

## الاختبارات

```bash
pytest -q
python -m compileall -q src
```

## التصميم

1. `planner.py` يحول الطلب إلى خطوات JSON مقيدة.
2. `executor.py` ينفذ الأدوات المسجلة فقط.
3. `memory.py` يحفظ آخر الرسائل في JSON محلي.
4. `agent.py` ينسق التخطيط والتنفيذ والإجابة.
5. `tools/gemini_tool.py` يعزل تكامل Gemini ويقدم خطأ واضحًا عند غياب المفتاح.

هذا التطبيق ليس بديلًا عن خبير قانوني أو طبي أو مالي، ولا ينفذ أوامر نظام أو شيفرة يرسلها المستخدم.
