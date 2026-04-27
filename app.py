import os
import json
import re
import streamlit as st
from google import genai


# إعداد الصفحة
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)


# العنوان
st.title("📚 AI Study Assistant")

st.write(
    "مساعد ذكي يساعدك على شرح الدروس، تلخيص النصوص، "
    "وإنشاء أسئلة للمراجعة بطريقة سهلة ومنظمة."
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


# اختيارات المستخدم
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
        "الإنجليزية"
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


# دالة استخراج JSON من رد Gemini
def extract_json(text):
    text = text.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return json.loads(text)


# دالة إنشاء Prompt للـ Quiz
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
    st.markdown("## 🧠 Quiz Mode")
    st.write("اكتب موضوعًا، ثم سيقوم التطبيق بإنشاء اختبار تفاعلي لك.")

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

    if st.button("إنشاء Quiz"):
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
        st.markdown("## الأسئلة")

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

        if st.button("تصحيح Quiz"):
            score = 0
            st.session_state.quiz_submitted = True

            st.markdown("## النتيجة")

            for i, q in enumerate(st.session_state.quiz_questions):
                correct_index = q["answer_index"]
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
                st.success("ممتاز جدًا! مستواك رائع.")
            elif percentage >= 50:
                st.info("جيد، لكن تحتاج إلى مراجعة بعض النقاط.")
            else:
                st.warning("تحتاج إلى مراجعة الدرس مرة أخرى.")

    if st.button("مسح Quiz"):
        st.session_state.quiz_questions = []
        st.session_state.quiz_submitted = False
        st.rerun()


# باقي المهام العادية
else:
    st.markdown("### أمثلة يمكنك تجربتها:")

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

    if st.button("إرسال"):
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

                    st.markdown("## الجواب:")
                    st.write(response.text)

                except Exception as e:
                    st.error("حدث خطأ أثناء توليد الجواب.")
                    st.write("تفاصيل الخطأ:")
                    st.code(str(e))


# معلومات أسفل الصفحة
st.markdown("---")
st.caption("تم إنشاء هذا التطبيق باستعمال Streamlit و Google Gemini API.")
