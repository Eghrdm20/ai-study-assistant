import os
import json
import time
import html
import hashlib
import random
import string
import streamlit as st
from google import genai
from google.genai import types
from supabase import create_client


# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="AI Soutien Scolaire Morocco",
    page_icon="🇲🇦",
    layout="centered"
)


# =========================
# CSS التصميم المغربي
# =========================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&family=Tajawal:wght@400;500;700;800&display=swap');

    :root {
        --morocco-red: #b11226;
        --morocco-green: #006233;
        --gold: #d4af37;
        --cream: #fff8ef;
        --text-dark: #2d1810;
        --text-medium: #5d4037;
    }

    html, body, [class*="css"] {
        font-family: 'Cairo', 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 98, 51, 0.12), transparent 35%),
            radial-gradient(circle at bottom right, rgba(177, 18, 38, 0.14), transparent 35%),
            linear-gradient(135deg, #fff8ef 0%, #fef5eb 45%, #fffaf5 100%);
        color: var(--text-dark);
    }

    .block-container {
        max-width: 960px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .moroccan-hero {
        background: linear-gradient(135deg, #b11226 0%, #c41230 30%, #006233 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 30px;
        box-shadow:
            0 18px 45px rgba(0, 0, 0, 0.22),
            0 0 0 3px #d4af37;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .moroccan-hero::before {
        content: "✦ ✧ ✦ ✧ ✦ ✧ ✦";
        position: absolute;
        top: 16px;
        left: 24px;
        font-size: 22px;
        color: rgba(255, 215, 0, 0.5);
        letter-spacing: 9px;
    }

    .moroccan-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        color: #ffe9a6;
        padding: 9px 18px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 14px;
        margin-bottom: 16px;
        border: 1px solid rgba(255, 255, 255, 0.35);
        position: relative;
        z-index: 1;
    }

    .moroccan-hero h1 {
        font-size: clamp(32px, 6vw, 52px);
        font-weight: 900;
        line-height: 1.25;
        margin-bottom: 14px;
        color: white;
        position: relative;
        z-index: 1;
    }

    .moroccan-hero p {
        font-size: 18px;
        line-height: 1.9;
        color: #fff7df;
        max-width: 720px;
        margin: 0;
        position: relative;
        z-index: 1;
    }

    .section-card {
        background: rgba(255, 255, 255, 0.92);
        border: 2px solid rgba(212, 175, 55, 0.35);
        border-radius: 26px;
        padding: 24px;
        margin: 24px 0;
        box-shadow: 0 10px 28px rgba(93, 64, 55, 0.10);
        position: relative;
        overflow: hidden;
    }

    .section-card::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        left: 0;
        height: 4px;
        background: linear-gradient(90deg, #b11226, #d4af37, #006233);
    }

    .section-title {
        color: #b11226;
        font-size: 26px;
        font-weight: 900;
        margin-bottom: 10px;
    }

    .small-note {
        color: #5d4037;
        font-size: 16px;
        line-height: 1.8;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stFileUploader"] label {
        color: #5a1f1f !important;
        font-weight: 800 !important;
        font-size: 17px !important;
    }

    textarea,
    input,
    div[data-baseweb="select"] > div {
        background: #fffdf7 !important;
        border-radius: 16px !important;
        color: #2d1810 !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #b11226 0%, #006233 100%);
        color: white !important;
        border: none;
        border-radius: 18px;
        padding: 0.8rem 1.4rem;
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 10px 25px rgba(177, 18, 38, 0.25);
        width: 100%;
    }

    .stButton > button:hover {
        color: #fff7d6 !important;
        transform: translateY(-2px);
    }

    div[role="radiogroup"] label,
    div[role="radiogroup"] label *,
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label *,
    div[data-testid="stRadio"] span,
    div[data-testid="stRadio"] p,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stCheckbox"] label *,
    div[data-testid="stCheckbox"] span,
    div[data-testid="stCheckbox"] p {
        color: #2d1810 !important;
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 700 !important;
    }

    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.90);
        border: 2px solid rgba(212, 175, 55, 0.35);
        border-radius: 14px;
        padding: 10px 14px;
        margin-bottom: 10px;
    }

    div[data-testid="stAlert"] {
        border-radius: 18px;
    }

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.92);
        border: 2px solid rgba(212, 175, 55, 0.25);
        border-radius: 18px;
        overflow: hidden;
        margin: 12px 0;
    }

    .danger-card {
        background: rgba(177, 18, 38, 0.08);
        border: 2px solid rgba(177, 18, 38, 0.25);
        border-radius: 22px;
        padding: 20px;
        margin: 24px 0;
    }

    .danger-title {
        color: #b11226;
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .teacher-card {
        background: rgba(0, 98, 51, 0.08);
        border: 2px solid rgba(0, 98, 51, 0.22);
        border-radius: 22px;
        padding: 20px;
        margin: 20px 0;
    }

    .teacher-title {
        color: #006233;
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 8px;
    }

    .code-box {
        background: #fffdf7;
        border: 2px dashed #d4af37;
        border-radius: 18px;
        padding: 18px;
        text-align: center;
        font-size: 26px;
        font-weight: 900;
        color: #b11226;
        letter-spacing: 3px;
        margin: 15px 0;
    }

    .footer {
        text-align: center;
        color: #7a5b2e;
        font-size: 14px;
        margin-top: 40px;
        padding: 24px;
        background: rgba(255, 255, 255, 0.65);
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.25);
        line-height: 1.9;
    }

    .footer-icons {
        font-size: 24px;
        margin-bottom: 10px;
        letter-spacing: 8px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .moroccan-hero {
            padding: 2rem 1.3rem;
            border-radius: 24px;
        }

        .section-card {
            padding: 20px;
            border-radius: 22px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# الهيدر
# =========================
st.markdown(
    """
    <div class="moroccan-hero">
        <div class="moroccan-badge">🇲🇦 Soutien Scolaire Intelligent</div>
        <h1>📚 منصة الدعم الذكي</h1>
        <p>
            منصة دعم مدرسية موجهة لتلاميذ الابتدائي والإعدادي في المغرب:
            شرح الدروس، تمارين، Quiz، سؤال بصورة، أقسام الأستاذ، وتتبع النتائج.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# إعدادات مدرسية
# =========================
PRIMARY_LEVELS = [
    "الأول ابتدائي",
    "الثاني ابتدائي",
    "الثالث ابتدائي",
    "الرابع ابتدائي",
    "الخامس ابتدائي",
    "السادس ابتدائي"
]

MIDDLE_LEVELS = [
    "الأولى إعدادي",
    "الثانية إعدادي",
    "الثالثة إعدادي"
]

PRIMARY_SUBJECTS = [
    "اللغة العربية",
    "اللغة الفرنسية",
    "الرياضيات",
    "النشاط العلمي",
    "الاجتماعيات",
    "التربية الإسلامية"
]

MIDDLE_SUBJECTS = [
    "اللغة العربية",
    "اللغة الفرنسية",
    "اللغة الإنجليزية",
    "الرياضيات",
    "الفيزياء والكيمياء",
    "علوم الحياة والأرض",
    "الاجتماعيات",
    "التربية الإسلامية"
]


def get_levels_for_cycle(cycle):
    if cycle == "الابتدائي":
        return PRIMARY_LEVELS
    return MIDDLE_LEVELS


def get_subjects_for_cycle(cycle):
    if cycle == "الابتدائي":
        return PRIMARY_SUBJECTS
    return MIDDLE_SUBJECTS


def school_context_selector(prefix="context"):
    school_cycle = st.selectbox(
        "السلك الدراسي:",
        ["الابتدائي", "الإعدادي"],
        key=f"{prefix}_cycle"
    )

    school_level = st.selectbox(
        "المستوى الدراسي:",
        get_levels_for_cycle(school_cycle),
        key=f"{prefix}_level"
    )

    subject = st.selectbox(
        "المادة:",
        get_subjects_for_cycle(school_cycle),
        key=f"{prefix}_subject"
    )

    return school_cycle, school_level, subject


def format_school_context(cycle, level, subject):
    return f"{cycle} | {level} | {subject}"


# =========================
# قراءة Secrets
# =========================
def get_secret(key, default=None):
    value = os.getenv(key)
    if value:
        return value

    try:
        return st.secrets[key]
    except Exception:
        return default


GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_SERVICE_ROLE_KEY")
APP_SECRET = get_secret("APP_SECRET", "change_this_secret")


if not GEMINI_API_KEY:
    st.error("لم يتم العثور على GEMINI_API_KEY في Streamlit Secrets.")
    st.stop()

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("لم يتم العثور على SUPABASE_URL أو SUPABASE_SERVICE_ROLE_KEY في Streamlit Secrets.")
    st.stop()


client = genai.Client(api_key=GEMINI_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================
# Gemini مع إعادة المحاولة
# =========================
def generate_with_retry(prompt, max_retries=3):
    models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite"
    ]

    last_error = None

    for model_name in models:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                if response.text:
                    return response.text

                raise Exception("Gemini returned an empty response.")

            except Exception as e:
                last_error = e
                error_text = str(e).lower()

                if (
                    "503" in error_text
                    or "unavailable" in error_text
                    or "overloaded" in error_text
                    or "model is overloaded" in error_text
                ):
                    time.sleep(2 + attempt * 2)
                    continue

                if (
                    "429" in error_text
                    or "resource_exhausted" in error_text
                    or "rate limit" in error_text
                    or "quota" in error_text
                ):
                    time.sleep(5 + attempt * 5)
                    continue

                raise e

    raise last_error


# =========================
# Gemini مع صورة + إعادة المحاولة
# =========================
def generate_with_retry_image(prompt, uploaded_image, max_retries=3):
    models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite"
    ]

    image_bytes = uploaded_image.getvalue()
    mime_type = uploaded_image.type or "image/jpeg"

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type
    )

    last_error = None

    for model_name in models:
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=[
                        image_part,
                        prompt
                    ]
                )

                if response.text:
                    return response.text

                raise Exception("Gemini returned an empty response.")

            except Exception as e:
                last_error = e
                error_text = str(e).lower()

                if (
                    "503" in error_text
                    or "unavailable" in error_text
                    or "overloaded" in error_text
                    or "model is overloaded" in error_text
                ):
                    time.sleep(2 + attempt * 2)
                    continue

                if (
                    "429" in error_text
                    or "resource_exhausted" in error_text
                    or "rate limit" in error_text
                    or "quota" in error_text
                ):
                    time.sleep(5 + attempt * 5)
                    continue

                raise e

    raise last_error


# =========================
# أدوات عامة
# =========================
def normalize_name(name):
    return " ".join(name.strip().lower().split())


def normalize_code(code):
    return "".join(code.strip().upper().split())


def hash_pin(pin):
    raw = f"{APP_SECRET}:{pin}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def extract_json(text):
    text = text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return json.loads(text)


def generate_class_code():
    chars = string.ascii_uppercase + string.digits

    for _ in range(20):
        code = "".join(random.choices(chars, k=6))
        existing = (
            supabase.table("classes")
            .select("id")
            .eq("class_code", code)
            .execute()
        )

        if not existing.data:
            return code

    return "".join(random.choices(chars, k=8))


# =========================
# حسابات التلاميذ
# =========================
def create_student(name, pin):
    name = name.strip()
    name_key = normalize_name(name)

    if not name or not pin:
        return False, "اكتب الاسم والرمز السري."

    if len(pin) < 4:
        return False, "الرمز السري يجب أن يحتوي على 4 أحرف أو أرقام على الأقل."

    existing = (
        supabase.table("students")
        .select("*")
        .eq("name_key", name_key)
        .execute()
    )

    if existing.data:
        return False, "هذا الاسم مسجل من قبل. جرّب تسجيل الدخول."

    result = (
        supabase.table("students")
        .insert({
            "name": name,
            "name_key": name_key,
            "pin_hash": hash_pin(pin)
        })
        .execute()
    )

    if result.data:
        return True, result.data[0]

    return False, "حدث خطأ أثناء إنشاء الحساب."


def login_student(name, pin):
    name_key = normalize_name(name)

    result = (
        supabase.table("students")
        .select("*")
        .eq("name_key", name_key)
        .execute()
    )

    if not result.data:
        return False, "لا يوجد حساب بهذا الاسم."

    student = result.data[0]

    if student["pin_hash"] != hash_pin(pin):
        return False, "الرمز السري غير صحيح."

    return True, student


# =========================
# حسابات الأساتذة
# =========================
def create_teacher(name, pin):
    name = name.strip()
    name_key = normalize_name(name)

    if not name or not pin:
        return False, "اكتب الاسم والرمز السري."

    if len(pin) < 4:
        return False, "الرمز السري يجب أن يحتوي على 4 أحرف أو أرقام على الأقل."

    existing = (
        supabase.table("teachers")
        .select("*")
        .eq("name_key", name_key)
        .execute()
    )

    if existing.data:
        return False, "هذا الأستاذ مسجل من قبل. جرّب تسجيل الدخول."

    result = (
        supabase.table("teachers")
        .insert({
            "name": name,
            "name_key": name_key,
            "pin_hash": hash_pin(pin)
        })
        .execute()
    )

    if result.data:
        return True, result.data[0]

    return False, "حدث خطأ أثناء إنشاء حساب الأستاذ."


def login_teacher(name, pin):
    name_key = normalize_name(name)

    result = (
        supabase.table("teachers")
        .select("*")
        .eq("name_key", name_key)
        .execute()
    )

    if not result.data:
        return False, "لا يوجد حساب أستاذ بهذا الاسم."

    teacher = result.data[0]

    if teacher["pin_hash"] != hash_pin(pin):
        return False, "الرمز السري غير صحيح."

    return True, teacher


# =========================
# السجل الشخصي للتلميذ
# =========================
def save_interaction(student_id, task_type, language, school_cycle, school_level, subject, question, answer):
    supabase.table("study_logs").insert({
        "student_id": student_id,
        "task_type": task_type,
        "language": language,
        "school_cycle": school_cycle,
        "school_level": school_level,
        "subject": subject,
        "level": school_level,
        "question": question,
        "answer": answer
    }).execute()


def get_student_history(student_id, limit=30):
    result = (
        supabase.table("study_logs")
        .select("*")
        .eq("student_id", student_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return result.data or []


def delete_student_history(student_id):
    return (
        supabase.table("study_logs")
        .delete()
        .eq("student_id", student_id)
        .execute()
    )


# =========================
# الأقسام والاختبارات
# =========================
def create_class(teacher_id, class_name, school_cycle, school_level, subject):
    class_code = generate_class_code()

    result = (
        supabase.table("classes")
        .insert({
            "teacher_id": teacher_id,
            "class_name": class_name,
            "class_code": class_code,
            "school_cycle": school_cycle,
            "school_level": school_level,
            "subject": subject
        })
        .execute()
    )

    if result.data:
        return True, result.data[0]

    return False, "حدث خطأ أثناء إنشاء القسم."


def get_teacher_classes(teacher_id):
    result = (
        supabase.table("classes")
        .select("*")
        .eq("teacher_id", teacher_id)
        .order("created_at", desc=True)
        .execute()
    )

    return result.data or []


def class_label(cls):
    context = format_school_context(
        cls.get("school_cycle", "غير محدد"),
        cls.get("school_level", "غير محدد"),
        cls.get("subject", "غير محددة")
    )
    return f'{cls["class_name"]} — {context} — {cls["class_code"]}'


def join_class(student_id, code):
    code = normalize_code(code)

    class_result = (
        supabase.table("classes")
        .select("*")
        .eq("class_code", code)
        .execute()
    )

    if not class_result.data:
        return False, "لم يتم العثور على قسم بهذا الكود."

    class_item = class_result.data[0]

    existing = (
        supabase.table("class_students")
        .select("*")
        .eq("class_id", class_item["id"])
        .eq("student_id", student_id)
        .execute()
    )

    if existing.data:
        return False, "أنت منضم لهذا القسم من قبل."

    supabase.table("class_students").insert({
        "class_id": class_item["id"],
        "student_id": student_id
    }).execute()

    return True, class_item


def get_student_classes(student_id):
    memberships = (
        supabase.table("class_students")
        .select("*")
        .eq("student_id", student_id)
        .execute()
    )

    items = []

    for membership in memberships.data or []:
        class_result = (
            supabase.table("classes")
            .select("*")
            .eq("id", membership["class_id"])
            .execute()
        )

        if class_result.data:
            items.append(class_result.data[0])

    return items


def get_previous_questions_for_class(class_id, topic=None, limit=8):
    query = (
        supabase.table("teacher_quizzes")
        .select("questions_json, topic")
        .eq("class_id", class_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    previous_questions = []

    for item in query.data or []:
        if topic:
            old_topic = item.get("topic", "")
            topic_clean = topic.strip().lower()
            old_topic_clean = old_topic.strip().lower()

            if topic_clean not in old_topic_clean and old_topic_clean not in topic_clean:
                continue

        questions_data = item.get("questions_json", {})

        if isinstance(questions_data, str):
            try:
                questions_data = json.loads(questions_data)
            except Exception:
                questions_data = {}

        for q in questions_data.get("questions", []):
            question_text = q.get("question", "")
            if question_text:
                previous_questions.append(question_text)

    return previous_questions


def create_teacher_quiz(
    teacher_id,
    class_id,
    title,
    topic,
    language,
    school_cycle,
    school_level,
    subject,
    count=None,
    manual_questions=None,
    avoid_repeat=True
):
    if manual_questions:
        quiz_data = {
            "questions": manual_questions
        }
    else:
        previous_questions = []

        if avoid_repeat:
            previous_questions = get_previous_questions_for_class(
                class_id,
                topic=topic,
                limit=8
            )

        prompt = build_quiz_prompt(
            language,
            school_cycle,
            school_level,
            subject,
            topic,
            count,
            previous_questions=previous_questions
        )

        answer_text = generate_with_retry(prompt)
        quiz_data = extract_json(answer_text)

    result = (
        supabase.table("teacher_quizzes")
        .insert({
            "teacher_id": teacher_id,
            "class_id": class_id,
            "title": title,
            "topic": topic,
            "language": language,
            "school_cycle": school_cycle,
            "school_level": school_level,
            "subject": subject,
            "level": school_level,
            "questions_json": quiz_data
        })
        .execute()
    )

    if result.data:
        return True, result.data[0]

    return False, "حدث خطأ أثناء حفظ الاختبار."


def get_teacher_quizzes(teacher_id):
    result = (
        supabase.table("teacher_quizzes")
        .select("*")
        .eq("teacher_id", teacher_id)
        .order("created_at", desc=True)
        .execute()
    )

    return result.data or []


def get_student_teacher_quizzes(student_id):
    memberships = (
        supabase.table("class_students")
        .select("*")
        .eq("student_id", student_id)
        .execute()
    )

    class_ids = [item["class_id"] for item in memberships.data or []]

    if not class_ids:
        return []

    result = (
        supabase.table("teacher_quizzes")
        .select("*")
        .in_("class_id", class_ids)
        .order("created_at", desc=True)
        .execute()
    )

    return result.data or []


def get_submission(quiz_id, student_id):
    result = (
        supabase.table("quiz_submissions")
        .select("*")
        .eq("quiz_id", quiz_id)
        .eq("student_id", student_id)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None


def save_submission(quiz_id, student_id, score, total, answers_json):
    existing = get_submission(quiz_id, student_id)

    payload = {
        "quiz_id": quiz_id,
        "student_id": student_id,
        "score": score,
        "total": total,
        "answers_json": answers_json
    }

    if existing:
        return (
            supabase.table("quiz_submissions")
            .update(payload)
            .eq("id", existing["id"])
            .execute()
        )

    return (
        supabase.table("quiz_submissions")
        .insert(payload)
        .execute()
    )


def get_quiz_submissions(quiz_id):
    result = (
        supabase.table("quiz_submissions")
        .select("*")
        .eq("quiz_id", quiz_id)
        .order("created_at", desc=True)
        .execute()
    )

    submissions = result.data or []

    for item in submissions:
        student_result = (
            supabase.table("students")
            .select("name")
            .eq("id", item["student_id"])
            .execute()
        )

        item["student_name"] = (
            student_result.data[0]["name"]
            if student_result.data
            else "تلميذ غير معروف"
        )

    return submissions


# =========================
# Prompts
# =========================
def build_prompt(task, lang, school_cycle, school_level, subject, text):
    context = f"""
السياق الدراسي:
- السلك الدراسي: {school_cycle}
- المستوى الدراسي: {school_level}
- المادة: {subject}
- البلد: المغرب
- الهدف: الدعم المدرسي وتقوية الفهم
"""

    if task == "شرح درس":
        return f"""
أنت مساعد دعم مدرسي ذكي.

{context}

اشرح الدرس التالي باللغة {lang}.
اجعل الشرح مناسبًا تمامًا لتلميذ في {school_level}، مادة {subject}.
استعمل أسلوبًا بسيطًا، واضحًا، ومنظمًا.

نظم الجواب بهذا الشكل:
1. شرح بسيط وواضح
2. مثال تطبيقي مناسب للمستوى
3. أهم القواعد أو الأفكار التي يجب حفظها
4. تمرين صغير في النهاية
5. نصيحة للمراجعة

الدرس أو السؤال:
{text}
"""

    if task == "تلخيص نص":
        return f"""
أنت مساعد دعم مدرسي ذكي.

{context}

لخص النص التالي باللغة {lang}.
اجعل الملخص مناسبًا لتلميذ في {school_level}، مادة {subject}.

نظم الجواب بهذا الشكل:
1. ملخص قصير
2. أهم الأفكار
3. كلمات مفتاحية
4. أسئلة صغيرة للمراجعة

النص:
{text}
"""

    if task == "إنشاء أسئلة للمراجعة":
        return f"""
أنت مساعد دعم مدرسي ذكي.

{context}

أنشئ أسئلة مراجعة باللغة {lang}.
اجعل الأسئلة مناسبة لتلميذ في {school_level}، مادة {subject}.

نظم الجواب بهذا الشكل:
1. أسئلة مباشرة
2. أسئلة اختيار من متعدد مع الأجوبة
3. أسئلة صح أو خطأ مع التصحيح
4. سؤال تطبيقي
5. الأجوبة النموذجية

الموضوع:
{text}
"""

    if task == "تبسيط مفهوم":
        return f"""
أنت مساعد دعم مدرسي ذكي.

{context}

بسط المفهوم التالي باللغة {lang}.
اجعل الشرح مناسبًا لتلميذ في {school_level}، مادة {subject}.

نظم الجواب بهذا الشكل:
1. تعريف بسيط
2. شرح كأنني مبتدئ
3. مثال من الحياة اليومية
4. مثال دراسي
5. خلاصة قصيرة

المفهوم:
{text}
"""

    if task == "تصحيح جواب":
        return f"""
أنت مساعد دعم مدرسي ذكي.

{context}

صحح جواب الطالب التالي باللغة {lang}.
اجعل التصحيح مناسبًا لتلميذ في {school_level}، مادة {subject}.

نظم الجواب بهذا الشكل:
1. هل الجواب صحيح أم خطأ؟
2. شرح الخطأ إن وجد
3. الجواب الصحيح
4. نصيحة لتحسين الإجابة

جواب الطالب:
{text}
"""

    return f"""
أجب عن السؤال التالي باللغة {lang}
وبطريقة مناسبة لتلميذ في {school_level}، مادة {subject}، ضمن الدعم المدرسي بالمغرب:

{text}
"""


def build_image_question_prompt(lang, school_cycle, school_level, subject, student_question):
    return f"""
أنت مساعد دعم مدرسي ذكي.

السياق الدراسي:
- السلك الدراسي: {school_cycle}
- المستوى الدراسي: {school_level}
- المادة: {subject}
- البلد: المغرب
- الهدف: الدعم المدرسي

الصورة المرفقة قد تحتوي على تمرين، درس، نص، سؤال، جدول، مسألة، أو صفحة من كتاب/دفتر.

مطلوب منك:
1. اقرأ محتوى الصورة بعناية.
2. إذا كانت الصورة غير واضحة، أخبر التلميذ بذلك بلطف واطلب صورة أوضح.
3. أجب عن سؤال التلميذ باللغة {lang}.
4. اجعل الشرح مناسبًا لتلميذ في {school_level}، مادة {subject}.
5. لا تعطِ الجواب فقط، بل اشرح الطريقة خطوة بخطوة.
6. إذا كان تمرينًا، اشرح الحل بطريقة تعليمية.
7. إذا كان نصًا، ساعد في الفهم أو التلخيص أو استخراج الأفكار حسب سؤال التلميذ.

سؤال التلميذ:
{student_question}

نظم الجواب بهذا الشكل:
1. ماذا يوجد في الصورة؟
2. فهم السؤال أو التمرين
3. الشرح خطوة بخطوة
4. الجواب النهائي
5. نصيحة صغيرة للمراجعة
"""


def build_quiz_prompt(lang, school_cycle, school_level, subject, topic, count, previous_questions=None):
    previous_questions = previous_questions or []

    avoid_text = ""

    if previous_questions:
        avoid_text = "\nتجنب تكرار هذه الأسئلة السابقة أو إعادة صياغتها بنفس الفكرة:\n"
        for i, question in enumerate(previous_questions, start=1):
            avoid_text += f"{i}. {question}\n"

    return f"""
أنت مساعد دعم مدرسي ذكي.

أنشئ اختبار Quiz باللغة {lang}.

السياق الدراسي:
- السلك الدراسي: {school_cycle}
- المستوى الدراسي: {school_level}
- المادة: {subject}
- البلد: المغرب
- الهدف: الدعم المدرسي

الموضوع: {topic}
عدد الأسئلة: {count}

يجب أن تكون الأسئلة اختيار من متعدد.
كل سؤال يجب أن يحتوي على 4 اختيارات.
يجب أن يكون هناك جواب صحيح واحد فقط.

مهم جدًا:
- اجعل الأسئلة مناسبة للمستوى: {school_level}.
- اجعل الأسئلة مرتبطة بالمادة: {subject}.
- اجعل الأسئلة مختلفة ومتنوعة.
- لا تكرر نفس السؤال.
- لا تستعمل نفس الفكرة بنفس الطريقة.
- اجعل الاختيارات واضحة وغير مربكة.
{avoid_text}

أرجع النتيجة بصيغة JSON فقط بدون أي شرح خارج JSON.
لا تكتب markdown.
لا تكتب علامات backticks.
لا تكتب وسوم json.

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


# =========================
# دوال عرض آمنة
# =========================
def render_answer_card(title, content):
    with st.container(border=True):
        st.markdown(f"## {title}")
        st.markdown(content)


def render_quiz_question_card(number, question):
    with st.container(border=True):
        st.markdown(f"### السؤال {number}")
        st.markdown(f"**{question}**")


def render_quiz_result_card(number, question, user_answer, correct_answer, explanation, is_correct):
    with st.container(border=True):
        if is_correct:
            st.success(f"السؤال {number}: إجابة صحيحة ✅")
        else:
            st.error(f"السؤال {number}: إجابة خاطئة ❌")

        st.markdown("### السؤال")
        st.write(question)

        st.markdown("### جوابك")
        st.write(user_answer)

        st.markdown("### الجواب الصحيح")
        st.success(correct_answer)

        st.markdown("### الشرح")
        st.info(explanation)


def render_score_card(score, total):
    percentage = int((score / total) * 100)

    if percentage >= 80:
        message = "ممتاز بزاف! مستواك رائع 🇲🇦"
    elif percentage >= 50:
        message = "مزيان، ولكن خاصك تراجع بعض النقاط."
    else:
        message = "خاصك تراجع الدرس مرة أخرى وتحاول من جديد."

    with st.container(border=True):
        st.markdown(f"# 🏆 درجتك: {score} / {total}")
        st.markdown(f"### {message}")


# =========================
# Session State
# =========================
if "account" not in st.session_state:
    st.session_state.account = None

if "account_type" not in st.session_state:
    st.session_state.account_type = None

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_version" not in st.session_state:
    st.session_state.quiz_version = 0


# =========================
# صفحة تسجيل الدخول
# =========================
if st.session_state.account is None:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">👤 الدخول إلى منصة الدعم</div>
            <div class="small-note">
                اختر نوع الحساب: تلميذ أو أستاذ. المنصة موجهة للدعم المدرسي في الابتدائي والإعدادي.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    account_type_choice = st.radio(
        "نوع الحساب:",
        ["تلميذ", "أستاذ"],
        horizontal=True
    )

    mode = st.radio(
        "اختر العملية:",
        ["تسجيل الدخول", "إنشاء حساب جديد"],
        horizontal=True
    )

    user_name = st.text_input("الاسم:")
    user_pin = st.text_input("الرمز السري:", type="password")

    if account_type_choice == "تلميذ":
        if mode == "إنشاء حساب جديد":
            if st.button("🚀 إنشاء حساب تلميذ"):
                try:
                    ok, result = create_student(user_name, user_pin)

                    if ok:
                        st.session_state.account = result
                        st.session_state.account_type = "student"
                        st.success("تم إنشاء حساب التلميذ بنجاح.")
                        st.rerun()
                    else:
                        st.warning(result)

                except Exception as e:
                    st.error("حدث خطأ أثناء إنشاء الحساب.")
                    st.code(str(e))
        else:
            if st.button("🚀 دخول التلميذ"):
                try:
                    ok, result = login_student(user_name, user_pin)

                    if ok:
                        st.session_state.account = result
                        st.session_state.account_type = "student"
                        st.success("تم تسجيل الدخول بنجاح.")
                        st.rerun()
                    else:
                        st.warning(result)

                except Exception as e:
                    st.error("حدث خطأ أثناء تسجيل الدخول.")
                    st.code(str(e))

    else:
        if mode == "إنشاء حساب جديد":
            if st.button("🚀 إنشاء حساب أستاذ"):
                try:
                    ok, result = create_teacher(user_name, user_pin)

                    if ok:
                        st.session_state.account = result
                        st.session_state.account_type = "teacher"
                        st.success("تم إنشاء حساب الأستاذ بنجاح.")
                        st.rerun()
                    else:
                        st.warning(result)

                except Exception as e:
                    st.error("حدث خطأ أثناء إنشاء حساب الأستاذ.")
                    st.code(str(e))
        else:
            if st.button("🚀 دخول الأستاذ"):
                try:
                    ok, result = login_teacher(user_name, user_pin)

                    if ok:
                        st.session_state.account = result
                        st.session_state.account_type = "teacher"
                        st.success("تم تسجيل الدخول بنجاح.")
                        st.rerun()
                    else:
                        st.warning(result)

                except Exception as e:
                    st.error("حدث خطأ أثناء تسجيل دخول الأستاذ.")
                    st.code(str(e))

    st.stop()


account = st.session_state.account
account_type = st.session_state.account_type
name_safe = html.escape(account["name"])


# =========================
# شريط الحساب
# =========================
role_label = "أستاذ" if account_type == "teacher" else "تلميذ"

st.markdown(
    f"""
    <div class="section-card">
        <div class="section-title">مرحبا {name_safe} 👋</div>
        <div class="small-note">
            نوع الحساب: {role_label}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("تسجيل الخروج"):
    st.session_state.account = None
    st.session_state.account_type = None
    st.session_state.quiz_questions = []
    st.rerun()


# =========================
# لوحة الأستاذ
# =========================
if account_type == "teacher":
    st.markdown(
        """
        <div class="teacher-card">
            <div class="teacher-title">🧑‍🏫 لوحة الأستاذ</div>
            <div class="small-note">
                يمكنك إنشاء أقسام للدعم، إرسال Quiz، ومتابعة نتائج تلاميذك.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    teacher_page = st.selectbox(
        "اختر الخدمة:",
        [
            "إنشاء قسم",
            "أقسامي",
            "إنشاء Quiz للقسم",
            "نتائج التلاميذ"
        ]
    )

    if teacher_page == "إنشاء قسم":
        st.markdown("## ➕ إنشاء قسم دعم جديد")

        class_name = st.text_input(
            "اسم القسم:",
            placeholder="مثال: دعم الثانية إعدادي - رياضيات"
        )

        school_cycle, school_level, subject = school_context_selector("teacher_class")

        if st.button("إنشاء القسم"):
            if not class_name.strip():
                st.warning("اكتب اسم القسم أولًا.")
            else:
                try:
                    ok, result = create_class(
                        account["id"],
                        class_name,
                        school_cycle,
                        school_level,
                        subject
                    )

                    if ok:
                        st.success("تم إنشاء القسم بنجاح.")
                        st.markdown("### كود القسم للتلاميذ:")
                        st.markdown(
                            f"""
                            <div class="code-box">{result["class_code"]}</div>
                            """,
                            unsafe_allow_html=True
                        )
                        st.info("أرسل هذا الكود للتلاميذ حتى ينضموا إلى قسم الدعم.")
                    else:
                        st.error(result)

                except Exception as e:
                    st.error("حدث خطأ أثناء إنشاء القسم.")
                    st.code(str(e))

    elif teacher_page == "أقسامي":
        st.markdown("## 📚 أقسامي")

        classes = get_teacher_classes(account["id"])

        if not classes:
            st.info("لم تنشئ أي قسم بعد.")
        else:
            for cls in classes:
                with st.container(border=True):
                    st.markdown(f"### {cls['class_name']}")
                    st.caption(
                        format_school_context(
                            cls.get("school_cycle", "غير محدد"),
                            cls.get("school_level", "غير محدد"),
                            cls.get("subject", "غير محددة")
                        )
                    )
                    st.markdown("**كود القسم:**")
                    st.markdown(
                        f"""
                        <div class="code-box">{cls["class_code"]}</div>
                        """,
                        unsafe_allow_html=True
                    )

    elif teacher_page == "إنشاء Quiz للقسم":
        st.markdown("## 🧠 إنشاء Quiz وإرساله للقسم")

        classes = get_teacher_classes(account["id"])

        if not classes:
            st.warning("يجب إنشاء قسم أولًا قبل إرسال Quiz.")
        else:
            class_labels = {
                class_label(cls): cls
                for cls in classes
            }

            selected_label = st.selectbox("اختر القسم:", list(class_labels.keys()))
            selected_class = class_labels[selected_label]

            school_cycle = selected_class.get("school_cycle", "الإعدادي")
            school_level = selected_class.get("school_level", "الأولى إعدادي")
            subject = selected_class.get("subject", "الرياضيات")

            st.info(f"سياق Quiz: {format_school_context(school_cycle, school_level, subject)}")

            quiz_title = st.text_input(
                "عنوان Quiz:",
                placeholder="مثال: Quiz المعادلات من الدرجة الأولى"
            )

            quiz_topic = st.text_area(
                "موضوع Quiz:",
                placeholder="مثال: المعادلات من الدرجة الأولى",
                height=120
            )

            quiz_language = st.selectbox(
                "لغة Quiz:",
                ["العربية", "الفرنسية", "الإنجليزية", "الدارجة المغربية"]
            )

            question_creation_mode = st.radio(
                "طريقة إنشاء الأسئلة:",
                [
                    "توليد تلقائي بواسطة AI",
                    "كتابة الأسئلة يدويًا"
                ],
                horizontal=True
            )

            manual_questions = None
            quiz_count = None
            avoid_repeat = True

            if question_creation_mode == "توليد تلقائي بواسطة AI":
                quiz_count = st.selectbox("عدد الأسئلة:", [3, 5, 10])

                avoid_repeat = st.checkbox(
                    "تجنّب تكرار أسئلة Quiz السابقة لنفس القسم والموضوع",
                    value=True
                )

                st.info(
                    "عند تفعيل هذا الخيار، سيحاول التطبيق إنشاء أسئلة جديدة مختلفة عن الأسئلة السابقة."
                )

            else:
                st.markdown("## ✍️ كتابة الأسئلة يدويًا")

                manual_count = st.selectbox(
                    "عدد الأسئلة التي تريد كتابتها:",
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                )

                manual_questions = []

                for i in range(manual_count):
                    with st.expander(f"السؤال {i + 1}", expanded=(i == 0)):
                        question_text = st.text_area(
                            f"نص السؤال {i + 1}:",
                            key=f"manual_question_text_{i}"
                        )

                        choice_1 = st.text_input(
                            "الاختيار 1:",
                            key=f"manual_choice_1_{i}"
                        )

                        choice_2 = st.text_input(
                            "الاختيار 2:",
                            key=f"manual_choice_2_{i}"
                        )

                        choice_3 = st.text_input(
                            "الاختيار 3:",
                            key=f"manual_choice_3_{i}"
                        )

                        choice_4 = st.text_input(
                            "الاختيار 4:",
                            key=f"manual_choice_4_{i}"
                        )

                        correct_choice = st.selectbox(
                            "اختر الجواب الصحيح:",
                            ["الاختيار 1", "الاختيار 2", "الاختيار 3", "الاختيار 4"],
                            key=f"manual_correct_choice_{i}"
                        )

                        explanation = st.text_area(
                            "شرح الجواب الصحيح:",
                            key=f"manual_explanation_{i}",
                            placeholder="مثال: لأن هذا الجواب يطبق القاعدة بشكل صحيح..."
                        )

                        answer_index = {
                            "الاختيار 1": 0,
                            "الاختيار 2": 1,
                            "الاختيار 3": 2,
                            "الاختيار 4": 3
                        }[correct_choice]

                        manual_questions.append({
                            "question": question_text,
                            "choices": [
                                choice_1,
                                choice_2,
                                choice_3,
                                choice_4
                            ],
                            "answer_index": answer_index,
                            "explanation": explanation
                        })

            if st.button("✨ إنشاء وإرسال Quiz"):
                if not quiz_title.strip() or not quiz_topic.strip():
                    st.warning("اكتب عنوان Quiz والموضوع أولًا.")
                else:
                    try:
                        if question_creation_mode == "كتابة الأسئلة يدويًا":
                            incomplete = False

                            for q in manual_questions:
                                if not q["question"].strip():
                                    incomplete = True

                                for choice in q["choices"]:
                                    if not choice.strip():
                                        incomplete = True

                                if not q["explanation"].strip():
                                    incomplete = True

                            if incomplete:
                                st.warning("أكمل جميع الأسئلة والاختيارات والشرح قبل الإرسال.")
                                st.stop()

                        with st.spinner("جاري إنشاء Quiz وإرساله للقسم..."):
                            ok, result = create_teacher_quiz(
                                account["id"],
                                selected_class["id"],
                                quiz_title,
                                quiz_topic,
                                quiz_language,
                                school_cycle,
                                school_level,
                                subject,
                                count=quiz_count,
                                manual_questions=manual_questions,
                                avoid_repeat=avoid_repeat
                            )

                            if ok:
                                st.success("تم إنشاء Quiz وإرساله للتلاميذ بنجاح.")
                            else:
                                st.error(result)

                    except Exception as e:
                        st.error("حدث خطأ أثناء إنشاء Quiz.")
                        st.code(str(e))

    elif teacher_page == "نتائج التلاميذ":
        st.markdown("## 📊 نتائج التلاميذ")

        quizzes = get_teacher_quizzes(account["id"])

        if not quizzes:
            st.info("لم تنشئ أي Quiz بعد.")
        else:
            quiz_labels = {
                f'{quiz["title"]} — {quiz["created_at"][:10]}': quiz
                for quiz in quizzes
            }

            selected_quiz_label = st.selectbox("اختر Quiz:", list(quiz_labels.keys()))
            selected_quiz = quiz_labels[selected_quiz_label]

            submissions = get_quiz_submissions(selected_quiz["id"])

            st.markdown(f"### {selected_quiz['title']}")
            st.caption(
                f"{selected_quiz.get('school_cycle', '')} | "
                f"{selected_quiz.get('school_level', '')} | "
                f"{selected_quiz.get('subject', '')}"
            )
            st.caption(f"الموضوع: {selected_quiz['topic']}")

            if not submissions:
                st.info("لا توجد أجوبة من التلاميذ بعد.")
            else:
                for sub in submissions:
                    with st.expander(f'{sub["student_name"]} — {sub["score"]}/{sub["total"]}'):
                        st.markdown(f"**التلميذ:** {sub['student_name']}")
                        st.markdown(f"**الدرجة:** {sub['score']} / {sub['total']}")
                        st.markdown(f"**التاريخ:** {sub['created_at'][:19]}")

                        answers = sub.get("answers_json", [])

                        if isinstance(answers, str):
                            try:
                                answers = json.loads(answers)
                            except Exception:
                                answers = []

                        for idx, item in enumerate(answers):
                            st.markdown("---")
                            st.markdown(f"### السؤال {idx + 1}")
                            st.write(item.get("question", ""))
                            st.markdown("**جواب التلميذ:**")
                            st.write(item.get("student_answer", ""))
                            st.markdown("**الجواب الصحيح:**")
                            st.write(item.get("correct_answer", ""))
                            st.markdown("**النتيجة:**")
                            st.write("صحيح ✅" if item.get("is_correct") else "خطأ ❌")

    st.markdown(
        """
        <div class="footer">
            <div class="footer-icons">🇲🇦 📚 🤖 ✨</div>
            <strong>منصة الدعم الذكي</strong><br>
            لوحة الأستاذ — أقسام الدعم، Quiz، وتتبع نتائج التلاميذ
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# =========================
# لوحة التلميذ
# =========================
st.markdown(
    """
    <div class="section-card">
        <div class="section-title">⚙️ لوحة التلميذ</div>
        <div class="small-note">
            استعمل المساعد الدراسي، ارفع صورة سؤال، حل Quiz، انضم إلى قسم دعم، أو شاهد Quizzes من الأستاذ.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

student_page = st.selectbox(
    "اختر الخدمة:",
    [
        "المساعد الدراسي",
        "سؤال بصورة",
        "Quiz Mode",
        "الانضمام إلى قسم",
        "Quizzes من الأستاذ",
        "سجل أسئلتي"
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

school_cycle, school_level, subject = school_context_selector("student_context")


# =========================
# سجل التلميذ
# =========================
if student_page == "سجل أسئلتي":
    st.markdown("## 📚 سجل أسئلتي")

    st.markdown(
        """
        <div class="danger-card">
            <div class="danger-title">🗑️ حذف السجل</div>
            <div class="small-note">
                يمكنك حذف كل الأسئلة والأجوبة المحفوظة في حسابك. هذه العملية لا يمكن التراجع عنها.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    confirm_delete = st.checkbox("أؤكد أنني أريد حذف سجل أسئلتي بالكامل")

    if st.button("🗑️ حذف سجل أسئلتي"):
        if not confirm_delete:
            st.warning("قبل الحذف، فعّل خانة التأكيد أولًا.")
        else:
            try:
                delete_student_history(account["id"])
                st.success("تم حذف سجل أسئلتك بنجاح.")
                st.rerun()
            except Exception as e:
                st.error("حدث خطأ أثناء حذف السجل.")
                st.code(str(e))

    st.markdown("---")

    try:
        history = get_student_history(account["id"], limit=30)

        if not history:
            st.info("لا توجد أسئلة محفوظة بعد.")
        else:
            for item in history:
                date = item.get("created_at", "")[:10]
                title = f'{item["task_type"]} — {date}'

                with st.expander(title):
                    st.markdown("**السؤال:**")
                    st.write(item["question"])

                    st.markdown("**الجواب:**")
                    st.write(item["answer"])

                    st.caption(
                        f'{item.get("school_cycle", "")} | '
                        f'{item.get("school_level", "")} | '
                        f'{item.get("subject", "")} | '
                        f'اللغة: {item.get("language", "")}'
                    )

    except Exception as e:
        st.error("حدث خطأ أثناء جلب السجل.")
        st.code(str(e))


# =========================
# انضمام التلميذ إلى قسم
# =========================
elif student_page == "الانضمام إلى قسم":
    st.markdown("## 🏫 الانضمام إلى قسم دعم")

    code = st.text_input("اكتب كود القسم الذي أعطاه لك الأستاذ:")

    if st.button("الانضمام إلى القسم"):
        if not code.strip():
            st.warning("اكتب كود القسم أولًا.")
        else:
            try:
                ok, result = join_class(account["id"], code)

                if ok:
                    st.success(f'تم الانضمام إلى القسم: {result["class_name"]}')
                else:
                    st.warning(result)

            except Exception as e:
                st.error("حدث خطأ أثناء الانضمام إلى القسم.")
                st.code(str(e))

    st.markdown("## أقسامي")
    classes = get_student_classes(account["id"])

    if not classes:
        st.info("لم تنضم إلى أي قسم بعد.")
    else:
        for cls in classes:
            with st.container(border=True):
                st.markdown(f"### {cls['class_name']}")
                st.caption(
                    format_school_context(
                        cls.get("school_cycle", "غير محدد"),
                        cls.get("school_level", "غير محدد"),
                        cls.get("subject", "غير محددة")
                    )
                )
                st.caption(f"كود القسم: {cls['class_code']}")


# =========================
# Quizzes من الأستاذ
# =========================
elif student_page == "Quizzes من الأستاذ":
    st.markdown("## 🧑‍🏫 Quizzes من الأستاذ")

    quizzes = get_student_teacher_quizzes(account["id"])

    if not quizzes:
        st.info("لا توجد اختبارات من الأستاذ بعد. تأكد أنك منضم إلى قسم.")
    else:
        quiz_labels = {
            f'{quiz["title"]} — {quiz["created_at"][:10]}': quiz
            for quiz in quizzes
        }

        selected_quiz_label = st.selectbox("اختر Quiz:", list(quiz_labels.keys()))
        selected_quiz = quiz_labels[selected_quiz_label]

        existing_submission = get_submission(selected_quiz["id"], account["id"])

        st.markdown(f"### {selected_quiz['title']}")
        st.caption(
            f"{selected_quiz.get('school_cycle', '')} | "
            f"{selected_quiz.get('school_level', '')} | "
            f"{selected_quiz.get('subject', '')}"
        )
        st.caption(f"الموضوع: {selected_quiz['topic']}")

        if existing_submission:
            st.success(
                f'لقد أجبت على هذا Quiz من قبل. درجتك: {existing_submission["score"]}/{existing_submission["total"]}'
            )

        questions_data = selected_quiz["questions_json"]

        if isinstance(questions_data, str):
            questions_data = json.loads(questions_data)

        questions = questions_data.get("questions", [])

        student_answers = []

        for i, q in enumerate(questions):
            render_quiz_question_card(i + 1, q["question"])

            answer = st.radio(
                "اختر الجواب:",
                q["choices"],
                key=f'teacher_quiz_{selected_quiz["id"]}_{i}'
            )

            selected_index = q["choices"].index(answer)
            student_answers.append(selected_index)

        if st.button("✅ إرسال Quiz للأستاذ"):
            score = 0
            answers_json = []

            st.markdown("## النتيجة")

            for i, q in enumerate(questions):
                correct_index = int(q["answer_index"])
                selected_index = student_answers[i]
                is_correct = selected_index == correct_index

                if is_correct:
                    score += 1

                render_quiz_result_card(
                    i + 1,
                    q["question"],
                    q["choices"][selected_index],
                    q["choices"][correct_index],
                    q["explanation"],
                    is_correct
                )

                answers_json.append({
                    "question": q["question"],
                    "student_answer": q["choices"][selected_index],
                    "correct_answer": q["choices"][correct_index],
                    "is_correct": is_correct,
                    "explanation": q["explanation"]
                })

            total = len(questions)
            render_score_card(score, total)

            try:
                save_submission(
                    selected_quiz["id"],
                    account["id"],
                    score,
                    total,
                    answers_json
                )
                st.success("تم إرسال نتيجتك للأستاذ بنجاح.")
            except Exception as e:
                st.error("حدث خطأ أثناء إرسال النتيجة للأستاذ.")
                st.code(str(e))


# =========================
# سؤال بصورة
# =========================
elif student_page == "سؤال بصورة":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">📷 سؤال بصورة</div>
            <div class="small-note">
                ارفع صورة لتمرين، درس، نص، مسألة، أو صفحة من كتاب/دفتر،
                واكتب سؤالك عنها. سيحاول المساعد قراءة الصورة وشرحها لك.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_image = st.file_uploader(
        "ارفع صورة السؤال أو التمرين:",
        type=["png", "jpg", "jpeg", "webp"]
    )

    if uploaded_image is not None:
        file_size_mb = uploaded_image.size / (1024 * 1024)

        if file_size_mb > 8:
            st.warning("الصورة كبيرة جدًا. حاول رفع صورة أقل من 8MB.")
        else:
            st.image(uploaded_image, caption="الصورة المرفوعة", use_container_width=True)

            image_question = st.text_area(
                "اكتب سؤالك حول الصورة:",
                height=120,
                placeholder="مثال: اشرح لي هذا التمرين خطوة بخطوة، أو ما هو الجواب الصحيح؟"
            )

            if st.button("🔍 حلل الصورة وأجب"):
                if not image_question.strip():
                    st.warning("اكتب سؤالك حول الصورة أولًا.")
                else:
                    with st.spinner("جاري قراءة الصورة وتحليل السؤال..."):
                        try:
                            prompt = build_image_question_prompt(
                                language,
                                school_cycle,
                                school_level,
                                subject,
                                image_question
                            )

                            answer_text = generate_with_retry_image(
                                prompt,
                                uploaded_image
                            )

                            render_answer_card("📷 الجواب عن الصورة", answer_text)

                            save_interaction(
                                account["id"],
                                "سؤال بصورة",
                                language,
                                school_cycle,
                                school_level,
                                subject,
                                f"سؤال حول صورة: {image_question}",
                                answer_text
                            )

                            st.success("تم حفظ السؤال والجواب في سجلك.")

                        except Exception as e:
                            st.error("حدث خطأ أثناء تحليل الصورة. جرّب صورة أوضح أو أعد المحاولة.")
                            st.write("تفاصيل الخطأ:")
                            st.code(str(e))


# =========================
# Quiz Mode الشخصي
# =========================
elif student_page == "Quiz Mode":
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">🧠 Quiz Mode</div>
            <div class="small-note">
                أنشئ اختبارًا شخصيًا حسب السلك، المستوى، والمادة.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    quiz_topic = st.text_area(
        "اكتب موضوع الاختبار:",
        height=120,
        placeholder="مثال: المتطابقات الهامة، الجهاز الهضمي، الظواهر الكهربائية..."
    )

    quiz_count = st.selectbox(
        "اختر عدد الأسئلة:",
        [3, 5, 10]
    )

    if st.button("✨ إنشاء Quiz"):
        if quiz_topic.strip() == "":
            st.warning("اكتب موضوع الاختبار أولًا.")
        else:
            with st.spinner("جاري إنشاء الاختبار..."):
                try:
                    prompt = build_quiz_prompt(
                        language,
                        school_cycle,
                        school_level,
                        subject,
                        quiz_topic,
                        quiz_count
                    )

                    answer_text = generate_with_retry(prompt)
                    quiz_data = extract_json(answer_text)

                    st.session_state.quiz_questions = quiz_data["questions"]
                    st.session_state.quiz_version += 1

                    st.success("تم إنشاء الاختبار بنجاح. أجب عن الأسئلة بالأسفل.")

                except Exception as e:
                    st.error("حدث خطأ أثناء إنشاء الاختبار. جرّب عدد أسئلة أقل أو أعد المحاولة بعد قليل.")
                    st.write("تفاصيل الخطأ:")
                    st.code(str(e))

    if st.session_state.quiz_questions:
        st.markdown("## 📝 الأسئلة")

        user_answers = []

        for i, q in enumerate(st.session_state.quiz_questions):
            render_quiz_question_card(i + 1, q["question"])

            answer = st.radio(
                "اختر الجواب:",
                q["choices"],
                key=f"question_{st.session_state.quiz_version}_{i}"
            )

            selected_index = q["choices"].index(answer)
            user_answers.append(selected_index)

        if st.button("✅ تصحيح Quiz"):
            score = 0
            result_text = ""

            st.markdown("## 🏆 النتيجة")

            for i, q in enumerate(st.session_state.quiz_questions):
                correct_index = int(q["answer_index"])
                selected_index = user_answers[i]
                is_correct = selected_index == correct_index

                if is_correct:
                    score += 1
                    status = "صحيح"
                else:
                    status = "خطأ"

                render_quiz_result_card(
                    i + 1,
                    q["question"],
                    q["choices"][selected_index],
                    q["choices"][correct_index],
                    q["explanation"],
                    is_correct
                )

                result_text += f"""
السؤال {i + 1}: {q["question"]}
جواب الطالب: {q["choices"][selected_index]}
الجواب الصحيح: {q["choices"][correct_index]}
النتيجة: {status}
الشرح: {q["explanation"]}

"""

            total = len(st.session_state.quiz_questions)
            percentage = int((score / total) * 100)

            render_score_card(score, total)

            if percentage >= 80:
                st.balloons()

            try:
                save_interaction(
                    account["id"],
                    "Quiz Mode",
                    language,
                    school_cycle,
                    school_level,
                    subject,
                    quiz_topic,
                    f"الدرجة: {score}/{total}\n\n{result_text}"
                )
                st.success("تم حفظ نتيجة Quiz في سجلك.")
            except Exception as e:
                st.warning("تم التصحيح، لكن لم يتم حفظ النتيجة.")
                st.code(str(e))

    if st.button("🗑️ مسح Quiz"):
        st.session_state.quiz_questions = []
        st.session_state.quiz_version += 1
        st.rerun()


# =========================
# المساعد الدراسي
# =========================
else:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">🌟 المساعد الدراسي</div>
            <div class="small-note">
                اختر نوع الدعم، ثم اكتب الدرس أو السؤال. الجواب سيكون مناسبًا للسلك والمستوى والمادة.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    task_type = st.selectbox(
        "اختر نوع الدعم:",
        [
            "شرح درس",
            "تلخيص نص",
            "إنشاء أسئلة للمراجعة",
            "تبسيط مفهوم",
            "تصحيح جواب"
        ]
    )

    example = st.selectbox(
        "اختر مثالًا أو اكتب سؤالك بنفسك:",
        [
            "",
            "اشرح لي درس المتطابقات الهامة مع أمثلة",
            "لخص لي درس الجهاز الهضمي",
            "أعطني أسئلة مراجعة حول درس الطاقة الكهربائية",
            "اشرح لي المعادلات من الدرجة الأولى",
            "بسط لي مفهوم السلسلة الغذائية"
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
                    prompt = build_prompt(
                        task_type,
                        language,
                        school_cycle,
                        school_level,
                        subject,
                        user_input
                    )

                    answer_text = generate_with_retry(prompt)

                    render_answer_card("📌 الجواب", answer_text)

                    save_interaction(
                        account["id"],
                        task_type,
                        language,
                        school_cycle,
                        school_level,
                        subject,
                        user_input,
                        answer_text
                    )

                    st.success("تم حفظ السؤال والجواب في سجلك.")

                except Exception as e:
                    st.error("حدث خطأ أثناء توليد الجواب أو حفظه. جرّب مرة أخرى بعد قليل.")
                    st.write("تفاصيل الخطأ:")
                    st.code(str(e))


# =========================
# الفوتر
# =========================
st.markdown(
    """
    <div class="footer">
        <div class="footer-icons">🇲🇦 📚 🤖 ✨</div>
        <strong>منصة الدعم الذكي</strong><br>
        دعم مدرسي للابتدائي والإعدادي: سؤال بصورة، أقسام، Quizzes، نتائج، ومساعد دراسي ذكي<br>
        تم إنشاؤه باستعمال Streamlit و Google Gemini API و Supabase<br>
        <small style="opacity: 0.7;">© 2026 - جميع الحقوق محفوظة</small>
    </div>
    """,
    unsafe_allow_html=True
)
