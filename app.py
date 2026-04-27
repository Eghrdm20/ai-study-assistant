import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

st.title("📚 AI Study Assistant")
st.write("مساعد ذكي يساعدك على شرح الدروس، تلخيص النصوص، وإنشاء أسئلة للمراجعة.")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.warning("ضع مفتاح Gemini API في ملف .env باسم GEMINI_API_KEY")
    st.stop()

client = genai.Client(api_key=api_key)

task_type = st.selectbox(
    "اختر نوع المساعدة:",
    ["شرح درس", "تلخيص نص", "إنشاء أسئلة للمراجعة"]
)

language = st.selectbox(
    "اختر اللغة:",
    ["العربية", "الفرنسية", "الإنجليزية"]
)

user_input = st.text_area(
    "اكتب الدرس أو النص أو السؤال هنا:",
    height=180
)

def build_prompt(task, lang, text):
    if task == "شرح درس":
        return f"""
أنت مساعد دراسي ذكي.
اشرح الدرس التالي باللغة {lang} بطريقة سهلة ومنظمة.
استعمل:
1. شرح مبسط
2. مثال
3. أهم النقاط
4. تمرين صغير في النهاية

الدرس أو السؤال:
{text}
"""

    if task == "تلخيص نص":
        return f"""
أنت مساعد دراسي ذكي.
لخص النص التالي باللغة {lang}.
اجعل الجواب يحتوي على:
1. ملخص قصير
2. أهم الأفكار
3. كلمات مفتاحية للمراجعة

النص:
{text}
"""

    if task == "إنشاء أسئلة للمراجعة":
        return f"""
أنت مساعد دراسي ذكي.
أنشئ أسئلة مراجعة باللغة {lang} حول الموضوع التالي.
اجعل الأسئلة متنوعة:
1. أسئلة مباشرة
2. أسئلة اختيار من متعدد
3. سؤال تطبيقي

الموضوع:
{text}
"""

if st.button("إرسال"):
    if user_input.strip() == "":
        st.error("اكتب شيئًا أولًا.")
    else:
        with st.spinner("جاري توليد الجواب..."):
            prompt = build_prompt(task_type, language, user_input)

            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )

            st.subheader("الجواب:")
            st.write(response.text)
