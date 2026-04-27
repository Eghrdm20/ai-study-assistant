import os
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
        "تصحيح جواب"
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


# أمثلة جاهزة
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


# مربع الكتابة
user_input = st.text_area(
    "اكتب الدرس أو النص أو السؤال هنا:",
    value=example,
    height=180
)


# بناء الـ Prompt حسب نوع المساعدة
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


# زر الإرسال
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
