import os
import json
import streamlit as st
from google import genai


# إعداد الصفحة
st.set_page_config(
    page_title="AI Study Assistant Morocco",
    page_icon="🇲🇦",
    layout="centered"
)


# CSS لتطوير الشكل بطابع مغربي
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 150, 136, 0.18), transparent 30%),
            radial-gradient(circle at bottom right, rgba(193, 39, 45, 0.20), transparent 30%),
            linear-gradient(135deg, #fff8ef 0%, #f7efe3 45%, #fffaf3 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }

    .moroccan-hero {
        background: linear-gradient(135deg, #b11226 0%, #006233 100%);
        color: white;
        padding: 28px 24px;
        border-radius: 28px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.18);
        margin-bottom: 26px;
        border: 3px solid #d4af37;
        position: relative;
        overflow: hidden;
    }

    .moroccan-hero::before {
        content: "✦ ✧ ✦ ✧ ✦ ✧ ✦";
        position: absolute;
        top: 12px;
        left: 20px;
        font-size: 22px;
        color: rgba(255, 215, 0, 0.45);
        letter-spacing: 8px;
    }

    .moroccan-hero h1 {
        font-size: 44px;
        margin: 0;
        font-weight: 800;
        line-height: 1.25;
    }

    .moroccan-hero p {
        font-size: 19px;
        line-height: 1.8;
        margin-top: 14px;
        margin-bottom: 0;
        color: #fff7df;
    }

    .moroccan-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.16);
        color: #ffe9a6;
        padding: 7px 14px;
        border-radius: 999px;
        font-weight: 700;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.35);
    }

    .section-card {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(212, 175, 55, 0.45);
        border-radius: 24px;
        padding: 20px;
        margin: 18px 0;
        box-shadow: 0 8px 24px rgba(93, 64, 55, 0.10);
    }

    .section-title {
        color: #8b1e2d;
        font-size: 25px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .small-note {
        color: #5d4037;
        font-size: 16px;
        line-height: 1.8;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stRadio"] label {
        color: #5a1f1f !important;
        font-weight: 800 !important;
        font-size: 18px !important;
    }

    .stSelectbox div,
    .stTextArea textarea {
        border-radius: 18px !important;
    }

    textarea {
        background-color: #fffdf7 !important;
        border: 2px solid rgba(177, 18, 38, 0.18) !important;
        color: #2d2d35 !important;
        font-size: 18px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #b11226 0%, #006233 100%);
        color: white;
        border: none;
        border-radius: 18px;
        padding: 0.75rem 1.4rem;
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 8px 18px rgba(0, 98, 51, 0.25);
        transition: 0.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(177, 18, 38, 0.28);
        color: #fff7d6;
    }

    .result-box {
        background: #fffdf7;
        border-right: 6px solid #006233;
        border-left: 6px solid #b11226;
        border-radius: 22px;
        padding: 22px;
        margin-top: 20px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.08);
    }

    .quiz-box {
        background: linear-gradient(135deg, rgba(0, 98, 51, 0.08), rgba(177, 18, 38, 0.08));
        border: 2px dashed rgba(212, 175, 55, 0.7);
        border-radius: 24px;
        padding: 20px;
        margin: 18px 0;
    }

    .footer {
        text-align: center;
        color: #7a5b2e;
        font-size: 14px;
        margin-top: 30px;
        padding: 16px;
    }

    div[data-testid="stAlert"] {
        border-radius: 18px;
    }

    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
        margin: 30px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# الهيدر المغربي
st.markdown(
    """
    <div class="moroccan-hero">
        <div class="moroccan-badge">🇲🇦 Moroccan Study Assistant</div>
        <h1>📚 AI Study Assistant</h1>
        <p>
            مساعد دراسي ذكي بطابع مغربي يساعدك على شرح الدروس، تلخيص النصوص،
            إنشاء أسئلة للمراجعة، واختبار معلوماتك بطريقة سهلة ومنظمة.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# جلب مفتاح Gemini API
api_key = os.getenv("GEMINI_API_KEY")

try:
    api_key = api_key or st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    st.error("لم يتم العثور على GEMINI_API_KEY. أضفه في Streamlit Secrets.")
    st.stop()


# إنشاء عميل Gemini
client = genai.Client(api_key=api_key)


# بطاقة الإعدادات
st.markdown(
    """
    <div class="section-card">
        <div class="section-title">⚙️ إعدادات المساعدة</div>
        <div class="small-note">
            اختر نوع المساعدة، اللغة، والمستوى الدراسي حتى تحصل على جواب مناسب لك.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


task_type = st.selectbox(
    "اختر نوع المساعدة:",
    [
        "شرح درس",
        "تلخيص نص",
        "إنشاء أسئلة للمراجعة",
        "تبسيط مفهوم",
        "تصحيح جواب",
        "Quiz Mode"
    ]
)

language = st.selectbox(
    "اختر اللغة:",
    [
        "العربية",
        "الفرنسية",
        "الإنجليزية",
        "الدارجة المغربية"
    ]
)

level = st.selectbox(
    "اختر المستوى الدراسي:",
    [
        "ابتدائي",
        "إعدادي",
        "ثانوي",
        "جامعي"
    ]
)


# دالة بناء Prompt للمهام العادية
def build_prompt(task, lang, student_level, text):
    if task == "شرح درس":
        return f"""
أنت مساعد دراسي ذكي.

اشرح الدرس التالي باللغة {lang}.
اجعل الشرح مناسبًا لمستوى {student_level}.
استعمل أسلوبًا واضحًا ومنظمًا.

نظم الجواب بهذا الشكل:
1. شرح بسيط وواضح
2. مثال تطبيقي
3. أهم النقاط التي يجب حفظها
4. تمرين صغير في النهاية
5. نصيحة للمراجعة

الدرس أو السؤال:
{text}
"""

    elif task == "تلخيص نص":
        return f"""
أنت مساعد دراسي ذكي.

لخص النص التالي باللغة {lang}.
اجعل الملخص مناسبًا لمستوى {student_level}.

نظم الجواب بهذا الشكل:
1. ملخص قصير
2. أهم الأفكار
3. كلمات مفتاحية
4. أسئلة صغيرة للمراجعة

النص:
{text}
"""

    elif task == "إنشاء أسئلة للمراجعة":
        return f"""
أنت مساعد دراسي ذكي.

أنشئ أسئلة مراجعة باللغة {lang}.
اجعل الأسئلة مناسبة لمستوى {student_level}.

نظم الجواب بهذا الشكل:
1. أسئلة مباشرة
2. أسئلة اختيار من متعدد مع الأجوبة
3. أسئلة صح أو خطأ مع التصحيح
4. سؤال تطبيقي
5. الأجوبة النموذجية

الموضوع:
{text}
"""

    elif task == "تبسيط مفهوم":
        return f"""
أنت مساعد دراسي ذكي.

بسط المفهوم التالي باللغة {lang}.
اجعل الشرح مناسبًا لمستوى {student_level}.

نظم الجواب بهذا الشكل:
1. تعريف بسيط
2. شرح كأنني مبتدئ
3. مثال من الحياة اليومية
4. مثال دراسي
5. خلاصة قصيرة

المفهوم:
{text}
"""

    elif task == "تصحيح جواب":
        return f"""
أنت مساعد دراسي ذكي.

صحح جواب الطالب التالي باللغة {lang}.
اجعل التصحيح مناسبًا لمستوى {student_level}.

نظم الجواب بهذا الشكل:
1. هل الجواب صحيح أم خطأ؟
2. شرح الخطأ إن وجد
3. الجواب الصحيح
4. نصيحة لتحسين الإجابة

جواب الطالب:
{text}
"""

    else:
        return f"""
أجب عن السؤال التالي باللغة {lang}
وبطريقة مناسبة لمستوى {student_level}:

{text}
"""


# استخراج JSON من رد Gemini
def extract_json(text):
    text = text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return json.loads(text)


# Prompt خاص بالـ Quiz
def build_quiz_prompt(lang, student_level, topic, count):
    return f"""
أنت مساعد دراسي ذكي.

أنشئ اختبار Quiz باللغة {lang}.
المستوى الدراسي: {student_level}
الموضوع: {topic}
عدد الأسئلة: {count}

يجب أن تكون الأسئلة اختيار من متعدد.
كل سؤال يجب أن يحتوي على 4 اختيارات.
يجب أن يكون هناك جواب صحيح واحد فقط.

أرجع النتيجة بصيغة JSON فقط بدون أي شرح خارج JSON.

استعمل هذا الشكل بالضبط:

{{
  "questions": [
    {{
      "question": "نص السؤال هنا",
      "choices": ["اختيار 1", "اختيار 2", "اختيار 3", "اختيار 4"],
      "answer_index": 0,
      "explanation": "شرح مختصر للجواب الصحيح"
    }}
  ]
}}
"""


# وضع Quiz
if task_type == "Quiz Mode":
    st.markdown(
        """
        <div class="quiz-box">
            <div class="section-title">🧠 Quiz Mode</div>
            <div class="small-note">
                اكتب موضوعًا وسيقوم التطبيق بإنشاء اختبار تفاعلي لك مع التصحيح والشرح.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    quiz_topic = st.text_area(
        "اكتب موضوع الاختبار:",
        height=120,
        placeholder="مثال: المتطابقات الهامة، الجهاز الهضمي، الحرب العالمية الثانية..."
    )

    quiz_count = st.selectbox(
        "اختر عدد الأسئلة:",
        [3, 5, 10]
    )

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    if st.button("✨ إنشاء Quiz"):
        if quiz_topic.strip() == "":
            st.warning("اكتب موضوع الاختبار أولًا.")
        else:
            with st.spinner("جاري إنشاء الاختبار..."):
                try:
                    prompt = build_quiz_prompt(
                        language,
                        level,
                        quiz_topic,
                        quiz_count
                    )

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    quiz_data = extract_json(response.text)

                    st.session_state.quiz_questions = quiz_data["questions"]
                    st.session_state.quiz_submitted = False

                    st.success("تم إنشاء الاختبار بنجاح. أجب عن الأسئلة بالأسفل.")

                except Exception as e:
                    st.error("حدث خطأ أثناء إنشاء الاختبار.")
                    st.write("تفاصيل الخطأ:")
                    st.code(str(e))

    if st.session_state.quiz_questions:
        st.markdown("## 📝 الأسئلة")

        user_answers = []

        for i, q in enumerate(st.session_state.quiz_questions):
            st.markdown(f"### السؤال {i + 1}")
            st.write(q["question"])

            answer = st.radio(
                "اختر الجواب:",
                q["choices"],
                key=f"question_{i}"
            )

            selected_index = q["choices"].index(answer)
            user_answers.append(selected_index)

        if st.button("✅ تصحيح Quiz"):
            score = 0
            st.session_state.quiz_submitted = True

            st.markdown("## 🏆 النتيجة")

            for i, q in enumerate(st.session_state.quiz_questions):
                correct_index = int(q["answer_index"])
                selected_index = user_answers[i]

                st.markdown(f"### السؤال {i + 1}")

                if selected_index == correct_index:
                    score += 1
                    st.success("إجابة صحيحة ✅")
                else:
                    st.error("إجابة خاطئة ❌")

                st.write("**السؤال:**", q["question"])
                st.write("**جوابك:**", q["choices"][selected_index])
                st.write("**الجواب الصحيح:**", q["choices"][correct_index])
                st.write("**الشرح:**", q["explanation"])

            st.markdown("---")
            st.markdown(f"## درجتك: {score} / {len(st.session_state.quiz_questions)}")

            percentage = int((score / len(st.session_state.quiz_questions)) * 100)

            if percentage >= 80:
                st.balloons()
                st.success("ممتاز بزاف! مستواك رائع 🇲🇦")
            elif percentage >= 50:
                st.info("مزيان، ولكن خاصك تراجع بعض النقاط.")
            else:
                st.warning("خاصك تراجع الدرس مرة أخرى وتحاول من جديد.")

    if st.button("🗑️ مسح Quiz"):
        st.session_state.quiz_questions = []
        st.session_state.quiz_submitted = False
        st.rerun()


# باقي المهام العادية
else:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">🌟 أمثلة يمكنك تجربتها</div>
            <div class="small-note">
                اختر مثالًا جاهزًا أو اكتب سؤالك بنفسك في المربع.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    example = st.selectbox(
        "اختر مثالًا أو اكتب سؤالك بنفسك:",
        [
            "",
            "اشرح لي درس المتطابقات الهامة مع أمثلة",
            "لخص لي درس الجهاز الهضمي",
            "أعطني 10 أسئلة حول درس الحرب العالمية الثانية",
            "اشرح لي المعادلات من الدرجة الأولى",
            "بسط لي مفهوم الطاقة الكهربائية"
        ]
    )

    user_input = st.text_area(
        "اكتب الدرس أو النص أو السؤال هنا:",
        value=example,
        height=180
    )

    if st.button("🚀 إرسال"):
        if user_input.strip() == "":
            st.warning("اكتب شيئًا أولًا.")
        else:
            with st.spinner("جاري توليد الجواب..."):
                try:
                    prompt = build_prompt(task_type, language, level, user_input)

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.markdown(
                        """
                        <div class="result-box">
                            <h2>📌 الجواب</h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.write(response.text)

                except Exception as e:
                    st.error("حدث خطأ أثناء توليد الجواب.")
                    st.write("تفاصيل الخطأ:")
                    st.code(str(e))


# الفوتر
st.markdown(
    """
    <div class="footer">
        🇲🇦 AI Study Assistant — تصميم مستوحى من الألوان المغربية والزليج التقليدي<br>
        تم إنشاؤه باستعمال Streamlit و Google Gemini API
    </div>
    """,
    unsafe_allow_html=True
)
