import os
import json
import time
import html
import hashlib
import streamlit as st
from google import genai
from supabase import create_client


# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="AI Study Assistant Morocco",
    page_icon="🇲🇦",
    layout="centered"
)


# =========================
# تصميم مغربي محسن
# =========================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&family=Tajawal:wght@300;400;500;700;800&display=swap');

    :root {
        --morocco-red: #b11226;
        --morocco-green: #006233;
        --gold: #d4af37;
        --gold-light: #ffe9a6;
        --cream: #fff8ef;
        --cream-dark: #f7efe3;
        --text-dark: #2d1810;
        --text-medium: #5d4037;
        --shadow-soft: rgba(93, 64, 55, 0.10);
        --shadow-medium: rgba(0, 0, 0, 0.15);
        --shadow-strong: rgba(177, 18, 38, 0.25);
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
            linear-gradient(135deg, #fff8ef 0%, #fef5eb 30%, #fffaf5 70%, #fff8ef 100%);
        color: var(--text-dark);
    }

    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            radial-gradient(circle at 20% 50%, rgba(212, 175, 55, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(0, 98, 51, 0.06) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    .block-container {
        max-width: 960px;
        padding-top: 2rem;
        padding-bottom: 2rem;
        position: relative;
        z-index: 1;
    }

    .moroccan-hero {
        background: linear-gradient(135deg, var(--morocco-red) 0%, #c41230 25%, var(--morocco-green) 75%, #007a3f 100%);
        color: white;
        padding: 3rem 2.5rem;
        border-radius: 32px;
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.25),
            0 0 0 3px var(--gold),
            inset 0 2px 0 rgba(255, 255, 255, 0.2);
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        animation: heroFloat 6s ease-in-out infinite;
    }

    @keyframes heroFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .moroccan-hero::before {
        content: "✦ ✧ ✦ ✧ ✦ ✧ ✦";
        position: absolute;
        top: 16px;
        left: 24px;
        font-size: 24px;
        color: rgba(255, 215, 0, 0.5);
        letter-spacing: 10px;
        animation: sparkle 3s ease-in-out infinite;
    }

    @keyframes sparkle {
        0%, 100% { opacity: 0.5; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.08); }
    }

    .moroccan-hero::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 215, 0, 0.10) 0%, transparent 60%);
        animation: rotateGlow 20s linear infinite;
    }

    @keyframes rotateGlow {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .moroccan-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(10px);
        color: var(--gold-light);
        padding: 10px 20px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 14px;
        margin-bottom: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        position: relative;
        z-index: 1;
        animation: badgePulse 2s ease-in-out infinite;
    }

    @keyframes badgePulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.4); }
        50% { box-shadow: 0 0 20px 5px rgba(212, 175, 55, 0.2); }
    }

    .moroccan-hero h1 {
        font-size: clamp(32px, 6vw, 52px);
        font-weight: 900;
        line-height: 1.2;
        margin-bottom: 16px;
        position: relative;
        z-index: 1;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        color: #ffffff;
    }

    .moroccan-hero p {
        font-size: clamp(16px, 2.5vw, 19px);
        line-height: 1.9;
        color: #fff7df;
        max-width: 700px;
        position: relative;
        z-index: 1;
        margin: 0;
    }

    .section-card {
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(212, 175, 55, 0.35);
        border-radius: 28px;
        padding: 28px;
        margin: 24px 0;
        box-shadow:
            0 12px 36px var(--shadow-soft),
            0 4px 12px rgba(212, 175, 55, 0.08);
        transition: all 0.35s ease;
        position: relative;
        overflow: hidden;
    }

    .section-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--morocco-red), var(--gold), var(--morocco-green));
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .section-card:hover {
        transform: translateY(-5px);
        box-shadow:
            0 20px 48px var(--shadow-medium),
            0 8px 24px rgba(212, 175, 55, 0.15);
        border-color: rgba(212, 175, 55, 0.55);
    }

    .section-card:hover::before {
        opacity: 1;
    }

    .section-title {
        color: var(--morocco-red);
        font-size: clamp(22px, 4vw, 28px);
        font-weight: 900;
        margin-bottom: 12px;
    }

    .small-note {
        color: var(--text-medium);
        font-size: 16px;
        line-height: 1.85;
        font-weight: 400;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stRadio"] label {
        color: #5a1f1f !important;
        font-weight: 800 !important;
        font-size: 17px !important;
    }

    textarea,
    input,
    div[data-baseweb="select"] > div {
        background: linear-gradient(135deg, #ffffff 0%, #fffdf7 100%) !important;
        border-radius: 18px !important;
        border-color: rgba(212, 175, 55, 0.35) !important;
        color: var(--text-dark) !important;
    }

    textarea:focus,
    input:focus {
        border-color: var(--morocco-green) !important;
        box-shadow:
            0 0 0 4px rgba(0, 98, 51, 0.12),
            0 8px 24px rgba(0, 98, 51, 0.15) !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--morocco-red) 0%, var(--morocco-green) 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.85rem 1.5rem;
        font-size: 18px;
        font-weight: 800;
        box-shadow:
            0 10px 28px var(--shadow-strong),
            inset 0 2px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.35s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow:
            0 16px 36px rgba(177, 18, 38, 0.35),
            inset 0 2px 0 rgba(255, 255, 255, 0.3);
        color: #fff7d6;
    }

    .stButton > button:active {
        transform: translateY(-2px) scale(0.98);
    }

    div[data-testid="stAlert"] {
        border-radius: 18px;
        border: 1px solid rgba(212, 175, 55, 0.25);
    }

    div[data-testid="stExpander"] {
        background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
        border: 2px solid rgba(212, 175, 55, 0.25);
        border-radius: 18px;
        overflow: hidden;
        margin: 12px 0;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
    }

    div[data-testid="stExpander"]:hover {
        border-color: rgba(212, 175, 55, 0.45);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
    }

    div[role="radiogroup"] {
        gap: 12px;
    }

    div[role="radiogroup"] label {
        background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
        border: 2px solid rgba(212, 175, 55, 0.3);
        border-radius: 16px;
        padding: 10px 14px;
        transition: all 0.3s ease;
        margin-bottom: 10px;
    }

    div[role="radiogroup"] label:hover {
        transform: translateY(-2px);
        border-color: var(--gold);
    }

    .answer-card {
        background: linear-gradient(135deg, #ffffff 0%, #fffdf7 100%);
        border-radius: 28px;
        padding: 26px;
        margin: 24px 0;
        border: 2px solid rgba(212, 175, 55, 0.35);
        border-right: 7px solid var(--morocco-green);
        border-left: 7px solid var(--morocco-red);
        box-shadow:
            0 14px 34px rgba(0, 0, 0, 0.08),
            inset 0 2px 0 rgba(255, 255, 255, 0.9);
        animation: slideUp 0.45s ease-out;
    }

    .answer-card-title {
        color: var(--morocco-green);
        font-size: 26px;
        font-weight: 900;
        margin-bottom: 18px;
    }

    .answer-card-content {
        background: rgba(255, 248, 239, 0.75);
        border-radius: 20px;
        padding: 22px;
        color: var(--text-dark);
        font-size: 18px;
        line-height: 2;
        border: 1px solid rgba(212, 175, 55, 0.25);
    }

    .quiz-question-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 253, 247, 0.95));
        border: 2px solid rgba(212, 175, 55, 0.35);
        border-radius: 26px;
        padding: 24px;
        margin: 26px 0 14px 0;
        box-shadow: 0 10px 28px rgba(93, 64, 55, 0.10);
        position: relative;
        overflow: hidden;
    }

    .quiz-question-card::before {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 8px;
        height: 100%;
        background: linear-gradient(180deg, var(--morocco-red), var(--morocco-green));
    }

    .quiz-number {
        display: inline-block;
        background: linear-gradient(135deg, var(--morocco-red), var(--morocco-green));
        color: white;
        padding: 8px 18px;
        border-radius: 999px;
        font-weight: 900;
        font-size: 17px;
        margin-bottom: 14px;
        box-shadow: 0 8px 20px rgba(177, 18, 38, 0.22);
    }

    .quiz-question-text {
        color: var(--text-dark);
        font-size: 22px;
        font-weight: 800;
        line-height: 1.8;
        margin-top: 10px;
    }

    .quiz-result-card {
        background: linear-gradient(135deg, #ffffff 0%, #fffdf7 100%);
        border-radius: 26px;
        padding: 24px;
        margin: 24px 0;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
        border: 2px solid rgba(212, 175, 55, 0.35);
    }

    .quiz-result-card.correct {
        border-right: 8px solid #0f8a4c;
    }

    .quiz-result-card.wrong {
        border-right: 8px solid #b11226;
    }

    .quiz-status {
        font-size: 22px;
        font-weight: 900;
        margin-bottom: 16px;
    }

    .quiz-status.correct-text {
        color: #0f8a4c;
    }

    .quiz-status.wrong-text {
        color: #b11226;
    }

    .answer-line {
        background: rgba(255, 248, 239, 0.75);
        padding: 14px 18px;
        border-radius: 16px;
        margin: 12px 0;
        border: 1px solid rgba(212, 175, 55, 0.25);
        font-size: 17px;
        line-height: 1.8;
    }

    .answer-line strong {
        color: var(--morocco-red);
    }

    .correct-answer-box {
        background: rgba(0, 98, 51, 0.08);
        border: 1px solid rgba(0, 98, 51, 0.25);
    }

    .explanation-box {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.16), rgba(255, 233, 166, 0.18));
        border: 1px solid rgba(212, 175, 55, 0.45);
    }

    .score-card {
        background: linear-gradient(135deg, var(--morocco-red), var(--morocco-green));
        color: white;
        padding: 28px;
        border-radius: 28px;
        margin: 28px 0;
        text-align: center;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.18);
        border: 3px solid var(--gold);
    }

    .score-card h2 {
        margin: 0;
        font-size: 34px;
        font-weight: 900;
        color: white;
    }

    .score-card p {
        margin-top: 12px;
        font-size: 18px;
        color: #fff7df;
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    hr {
        border: none;
        height: 3px;
        background: linear-gradient(
            90deg,
            transparent 0%,
            var(--gold) 20%,
            var(--morocco-red) 50%,
            var(--morocco-green) 80%,
            transparent 100%
        );
        margin: 36px 0;
        border-radius: 2px;
    }

    .footer {
        text-align: center;
        color: #7a5b2e;
        font-size: 14px;
        margin-top: 40px;
        padding: 24px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.6) 0%, rgba(255, 248, 239, 0.8) 100%);
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        backdrop-filter: blur(10px);
        line-height: 1.9;
    }

    .footer-icons {
        font-size: 24px;
        margin-bottom: 10px;
        letter-spacing: 8px;
    }

    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--morocco-red), var(--morocco-green));
        border-radius: 10px;
    }

    ::selection {
        background: rgba(212, 175, 55, 0.3);
        color: var(--text-dark);
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .moroccan-hero {
            padding: 2rem 1.5rem;
            border-radius: 24px;
        }

        .section-card {
            padding: 20px;
            border-radius: 22px;
        }

        .stButton > button {
            padding: 0.75rem 1.2rem;
            font-size: 16px;
        }

        .answer-card {
            padding: 18px;
            border-radius: 22px;
        }

        .answer-card-content {
            font-size: 16px;
            padding: 16px;
        }

        .quiz-question-text {
            font-size: 18px;
        }

        .score-card h2 {
            font-size: 26px;
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
        <div class="moroccan-badge">🇲🇦 Moroccan Study Assistant</div>
        <h1>📚 AI Study Assistant</h1>
        <p>
            مساعد دراسي ذكي بطابع مغربي يساعدك على شرح الدروس، تلخيص النصوص،
            إنشاء أسئلة للمراجعة، وحفظ أسئلة كل تلميذ في حسابه الخاص.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


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


# =========================
# إنشاء العملاء
# =========================
client = genai.Client(api_key=GEMINI_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# =========================
# توليد جواب Gemini مع إعادة المحاولة
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
# أدوات الحساب
# =========================
def normalize_name(name):
    return " ".join(name.strip().lower().split())


def hash_pin(pin):
    raw = f"{APP_SECRET}:{pin}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


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


def save_interaction(student_id, task_type, language, level, question, answer):
    supabase.table("study_logs").insert({
        "student_id": student_id,
        "task_type": task_type,
        "language": language,
        "level": level,
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


# =========================
# Session State
# =========================
if "student" not in st.session_state:
    st.session_state.student = None

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_version" not in st.session_state:
    st.session_state.quiz_version = 0


# =========================
# تسجيل الدخول / إنشاء حساب
# =========================
if st.session_state.student is None:
    st.markdown(
        """
        <div class="section-card">
            <div class="section-title">👤 دخول التلميذ</div>
            <div class="small-note">
                أنشئ حسابًا باسمك ورمز سري، وبعدها ستبقى أسئلتك محفوظة في حسابك.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    mode = st.radio(
        "اختر العملية:",
        ["تسجيل الدخول", "إنشاء حساب جديد"],
        horizontal=True
    )

    student_name = st.text_input("اسم التلميذ:")
    student_pin = st.text_input("الرمز السري:", type="password")

    if mode == "إنشاء حساب جديد":
        if st.button("🚀 إنشاء الحساب"):
            try:
                ok, result = create_student(student_name, student_pin)

                if ok:
                    st.session_state.student = result
                    st.success("تم إنشاء الحساب بنجاح.")
                    st.rerun()
                else:
                    st.warning(result)

            except Exception as e:
                st.error("حدث خطأ أثناء إنشاء الحساب.")
                st.code(str(e))

    else:
        if st.button("🚀 تسجيل الدخول"):
            try:
                ok, result = login_student(student_name, student_pin)

                if ok:
                    st.session_state.student = result
                    st.success("تم تسجيل الدخول بنجاح.")
                    st.rerun()
                else:
                    st.warning(result)

            except Exception as e:
                st.error("حدث خطأ أثناء تسجيل الدخول.")
                st.code(str(e))

    st.stop()


student = st.session_state.student


# =========================
# ترحيب الطالب
# =========================
st.markdown(
    f"""
    <div class="section-card">
        <div class="section-title">مرحبا {html.escape(student["name"])} 👋</div>
        <div class="small-note">
            أنت الآن داخل حسابك. كل سؤال وجواب سيتم حفظه في سجلك الدراسي.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("تسجيل الخروج"):
    st.session_state.student = None
    st.session_state.quiz_questions = []
    st.rerun()


# =========================
# إعدادات المساعدة
# =========================
st.markdown(
    """
    <div class="section-card">
        <div class="section-title">⚙️ إعدادات المساعدة</div>
        <div class="small-note">
            اختر نوع المساعدة، اللغة، والمستوى الدراسي.
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
        "Quiz Mode",
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

level = st.selectbox(
    "اختر المستوى الدراسي:",
    [
        "ابتدائي",
        "إعدادي",
        "ثانوي",
        "جامعي"
    ]
)


# =========================
# Prompts
# =========================
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


def extract_json(text):
    text = text.strip()
    text = text.replace("```json", "")
    text = text.replace("```", "")

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:
        text = text[start:end + 1]

    return json.loads(text)


# =========================
# دوال العرض الجمالي
# =========================
def safe_html(text):
    return html.escape(str(text)).replace("\n", "<br>")


def render_answer_card(title, content):
    st.markdown(
        f"""
        <div class="answer-card">
            <div class="answer-card-title">{title}</div>
            <div class="answer-card-content">
                {safe_html(content)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_quiz_question_card(number, question):
    st.markdown(
        f"""
        <div class="quiz-question-card">
            <div class="quiz-number">السؤال {number}</div>
            <div class="quiz-question-text">{safe_html(question)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_quiz_result_card(number, question, user_answer, correct_answer, explanation, is_correct):
    card_class = "correct" if is_correct else "wrong"
    status_class = "correct-text" if is_correct else "wrong-text"
    status_text = "إجابة صحيحة ✅" if is_correct else "إجابة خاطئة ❌"

    st.markdown(
        f"""
        <div class="quiz-result-card {card_class}">
            <div class="quiz-status {status_class}">
                السؤال {number}: {status_text}
            </div>

            <div class="answer-line">
                <strong>السؤال:</strong><br>
                {safe_html(question)}
            </div>

            <div class="answer-line">
                <strong>جوابك:</strong><br>
                {safe_html(user_answer)}
            </div>

            <div class="answer-line correct-answer-box">
                <strong>الجواب الصحيح:</strong><br>
                {safe_html(correct_answer)}
            </div>

            <div class="answer-line explanation-box">
                <strong>الشرح:</strong><br>
                {safe_html(explanation)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_score_card(score, total):
    percentage = int((score / total) * 100)

    if percentage >= 80:
        message = "ممتاز بزاف! مستواك رائع 🇲🇦"
    elif percentage >= 50:
        message = "مزيان، ولكن خاصك تراجع بعض النقاط."
    else:
        message = "خاصك تراجع الدرس مرة أخرى وتحاول من جديد."

    st.markdown(
        f"""
        <div class="score-card">
            <h2>🏆 درجتك: {score} / {total}</h2>
            <p>{message}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# سجل الأسئلة
# =========================
if task_type == "سجل أسئلتي":
    st.markdown("## 📚 سجل أسئلتي")

    try:
        history = get_student_history(student["id"], limit=30)

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
                        f'اللغة: {item.get("language", "")} | المستوى: {item.get("level", "")}'
                    )

    except Exception as e:
        st.error("حدث خطأ أثناء جلب السجل.")
        st.code(str(e))


# =========================
# Quiz Mode
# =========================
elif task_type == "Quiz Mode":
    st.markdown(
        """
        <div class="section-card">
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

    if st.button("✨ إنشاء Quiz"):
        if quiz_topic.strip() == "":
            st.warning("اكتب موضوع الاختبار أولًا.")
        else:
            with st.spinner("جاري إنشاء الاختبار... إذا كان هناك ضغط على الخادم سيحاول التطبيق تلقائيًا مرة أخرى."):
                try:
                    prompt = build_quiz_prompt(
                        language,
                        level,
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
                    student["id"],
                    "Quiz Mode",
                    language,
                    level,
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
# باقي المهام
# =========================
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
            with st.spinner("جاري توليد الجواب... إذا كان هناك ضغط على الخادم سيحاول التطبيق تلقائيًا مرة أخرى."):
                try:
                    prompt = build_prompt(task_type, language, level, user_input)

                    answer_text = generate_with_retry(prompt)

                    render_answer_card("📌 الجواب", answer_text)

                    save_interaction(
                        student["id"],
                        task_type,
                        language,
                        level,
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
        <strong>AI Study Assistant Morocco</strong><br>
        تصميم مستوحى من الألوان المغربية والزليج التقليدي<br>
        تم إنشاؤه باستعمال Streamlit و Google Gemini API و Supabase<br>
        <small style="opacity: 0.7;">© 2026 - جميع الحقوق محفوظة</small>
    </div>
    """,
    unsafe_allow_html=True
)
