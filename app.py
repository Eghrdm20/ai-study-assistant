<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Study Assistant Morocco - Enhanced UI</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800;900&family=Tajawal:wght@300;400;500;700;800&display=swap" rel="stylesheet">
    
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

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

        body {
            font-family: 'Cairo', 'Tajawal', sans-serif;
            background: 
                radial-gradient(circle at top left, rgba(0, 98, 51, 0.12), transparent 35%),
                radial-gradient(circle at bottom right, rgba(177, 18, 38, 0.14), transparent 35%),
                linear-gradient(135deg, #fff8ef 0%, #fef5eb 30%, #fffaf5 70%, #fff8ef 100%);
            min-height: 100vh;
            color: var(--text-dark);
            line-height: 1.7;
            overflow-x: hidden;
            position: relative;
        }

        /* Animated Background Pattern */
        body::before {
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

        .container {
            max-width: 960px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
            position: relative;
            z-index: 1;
        }

        /* ===== HERO SECTION - Enhanced ===== */
        .hero {
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
            transform-style: preserve-3d;
        }

        @keyframes heroFloat {
            0%, 100% { transform: translateY(0px) rotateX(0deg); }
            50% { transform: translateY(-8px) rotateX(1deg); }
        }

        .hero::before {
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
            50% { opacity: 1; transform: scale(1.1); }
        }

        .hero::after {
            content: "";
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255, 215, 0, 0.1) 0%, transparent 60%);
            animation: rotate 20s linear infinite;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .badge {
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
            letter-spacing: 0.5px;
            position: relative;
            z-index: 1;
            animation: badgePulse 2s ease-in-out infinite;
        }

        @keyframes badgePulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(212, 175, 55, 0.4); }
            50% { box-shadow: 0 0 20px 5px rgba(212, 175, 55, 0.2); }
        }

        .hero h1 {
            font-size: clamp(32px, 6vw, 52px);
            font-weight: 900;
            line-height: 1.2;
            margin-bottom: 16px;
            position: relative;
            z-index: 1;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            background: linear-gradient(to bottom, #ffffff 0%, #fff7df 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .hero p {
            font-size: clamp(16px, 2.5vw, 19px);
            line-height: 1.9;
            color: #fff7df;
            max-width: 650px;
            position: relative;
            z-index: 1;
            font-weight: 400;
        }

        /* ===== SECTION CARDS - Glassmorphism ===== */
        .card {
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 2px solid rgba(212, 175, 55, 0.35);
            border-radius: 28px;
            padding: 28px;
            margin: 24px 0;
            box-shadow: 
                0 12px 36px var(--shadow-soft),
                0 4px 12px rgba(212, 175, 55, 0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }

        .card::before {
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

        .card:hover {
            transform: translateY(-6px) scale(1.01);
            box-shadow: 
                0 20px 48px var(--shadow-medium),
                0 8px 24px rgba(212, 175, 55, 0.15);
            border-color: rgba(212, 175, 55, 0.55);
        }

        .card:hover::before {
            opacity: 1;
        }

        .section-title {
            color: var(--morocco-red);
            font-size: clamp(22px, 4vw, 28px);
            font-weight: 900;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            background: linear-gradient(135deg, var(--morocco-red), #c41230);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .section-desc {
            color: var(--text-medium);
            font-size: 16px;
            line-height: 1.85;
            font-weight: 400;
        }

        /* ===== FORM ELEMENTS - Modern ===== */
        .form-group {
            margin: 20px 0;
        }

        .form-label {
            display: block;
            color: #5a1f1f;
            font-weight: 800;
            font-size: 17px;
            margin-bottom: 10px;
            font-family: 'Cairo', sans-serif;
        }

        .form-input,
        .form-select,
        .form-textarea {
            width: 100%;
            background: linear-gradient(135deg, #ffffff 0%, #fffdf7 100%);
            border: 2px solid rgba(212, 175, 55, 0.3);
            border-radius: 18px;
            padding: 14px 18px;
            font-size: 16px;
            font-family: 'Cairo', sans-serif;
            transition: all 0.3s ease;
            direction: rtl;
            text-align: right;
            color: var(--text-dark);
        }

        .form-input:focus,
        .form-select:focus,
        .form-textarea:focus {
            outline: none;
            border-color: var(--morocco-green);
            box-shadow: 
                0 0 0 4px rgba(0, 98, 51, 0.12),
                0 8px 24px rgba(0, 98, 51, 0.15);
            transform: translateY(-2px);
        }

        .form-textarea {
            min-height: 140px;
            resize: vertical;
        }

        /* ===== BUTTONS - Premium ===== */
        .btn-primary {
            background: linear-gradient(135deg, var(--morocco-red) 0%, var(--morocco-green) 100%);
            color: white;
            border: none;
            border-radius: 20px;
            padding: 16px 32px;
            font-size: 18px;
            font-weight: 800;
            font-family: 'Cairo', sans-serif;
            cursor: pointer;
            box-shadow: 
                0 10px 28px var(--shadow-strong),
                inset 0 2px 0 rgba(255, 255, 255, 0.2);
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
            margin-top: 12px;
        }

        .btn-primary::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            background: rgba(255, 255, 255, 0.25);
            border-radius: 50%;
            transform: translate(-50%, -50%);
            transition: width 0.6s ease, height 0.6s ease;
        }

        .btn-primary:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 
                0 16px 36px rgba(177, 18, 38, 0.35),
                inset 0 2px 0 rgba(255, 255, 255, 0.3);
            color: #fff7d6;
        }

        .btn-primary:hover::before {
            width: 350px;
            height: 350px;
        }

        .btn-primary:active {
            transform: translateY(-2px) scale(0.98);
        }

        .btn-secondary {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            color: var(--text-dark);
            border: 2px solid rgba(212, 175, 55, 0.4);
            border-radius: 18px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Cairo', sans-serif;
        }

        .btn-secondary:hover {
            background: linear-gradient(135deg, #fff 0%, #f8f9fa 100%);
            border-color: var(--gold);
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
        }

        /* ===== RESULT BOX - Enhanced ===== */
        .result-box {
            background: linear-gradient(135deg, #ffffff 0%, #fffdf7 100%);
            border-right: 6px solid var(--morocco-green);
            border-left: 6px solid var(--morocco-red);
            border-radius: 26px;
            padding: 28px;
            margin-top: 24px;
            box-shadow: 
                0 12px 32px rgba(0, 0, 0, 0.09),
                inset 0 2px 0 rgba(255, 255, 255, 0.8);
            position: relative;
            overflow: hidden;
            animation: slideUp 0.5s ease-out;
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

        .result-box h2 {
            color: var(--morocco-green);
            font-size: 24px;
            font-weight: 900;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* ===== WELCOME BAR ===== */
        .welcome-bar {
            background: linear-gradient(135deg, rgba(0, 98, 51, 0.08) 0%, rgba(177, 18, 38, 0.06) 100%);
            border: 2px solid rgba(212, 175, 55, 0.3);
            border-radius: 24px;
            padding: 24px 28px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }

        .welcome-info h3 {
            color: var(--morocco-green);
            font-size: 22px;
            font-weight: 800;
            margin-bottom: 6px;
        }

        .welcome-info p {
            color: var(--text-medium);
            font-size: 15px;
        }

        /* ===== RADIO GROUP - Custom ===== */
        .radio-group {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin: 16px 0;
        }

        .radio-option {
            flex: 1;
            min-width: 150px;
        }

        .radio-option label {
            display: block;
            padding: 14px 20px;
            background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
            border: 2px solid rgba(212, 175, 55, 0.3);
            border-radius: 16px;
            cursor: pointer;
            text-align: center;
            font-weight: 700;
            font-size: 15px;
            transition: all 0.3s ease;
            font-family: 'Cairo', sans-serif;
        }

        .radio-option input[type="radio"] {
            display: none;
        }

        .radio-option input[type="radio"]:checked + label {
            background: linear-gradient(135deg, var(--morocco-green) 0%, #007a3f 100%);
            color: white;
            border-color: var(--morocco-green);
            box-shadow: 0 6px 20px rgba(0, 98, 51, 0.25);
            transform: translateY(-2px);
        }

        /* ===== LOADING SPINNER ===== */
        .loading-container {
            text-align: center;
            padding: 40px 20px;
        }

        .spinner {
            width: 56px;
            height: 56px;
            border: 5px solid rgba(212, 175, 55, 0.2);
            border-top: 5px solid var(--morocco-green);
            border-right: 5px solid var(--morocco-red);
            border-radius: 50%;
            animation: spin 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading-text {
            color: var(--text-medium);
            font-size: 17px;
            font-weight: 600;
            animation: pulse 1.5s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }

        /* ===== FOOTER - Premium ===== */
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
        }

        .footer-icons {
            font-size: 24px;
            margin-bottom: 10px;
            letter-spacing: 8px;
        }

        /* ===== DIVIDER ===== */
        .divider {
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
            position: relative;
            overflow: hidden;
        }

        .divider::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 50%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            to { left: 150%; }
        }

        /* ===== ALERT BOXES ===== */
        .alert {
            padding: 18px 24px;
            border-radius: 18px;
            margin: 16px 0;
            font-weight: 600;
            font-size: 15px;
            display: flex;
            align-items: center;
            gap: 12px;
            animation: slideDown 0.4s ease-out;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .alert-success {
            background: linear-gradient(135deg, rgba(0, 98, 51, 0.12) 0%, rgba(0, 122, 63, 0.08) 100%);
            color: #006233;
            border: 2px solid rgba(0, 98, 51, 0.3);
        }

        .alert-warning {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(255, 217, 102, 0.1) 100%);
            color: #856404;
            border: 2px solid rgba(212, 175, 55, 0.4);
        }

        .alert-error {
            background: linear-gradient(135deg, rgba(177, 18, 38, 0.12) 0%, rgba(196, 18, 48, 0.08) 100%);
            color: var(--morocco-red);
            border: 2px solid rgba(177, 18, 38, 0.3);
        }

        .alert-info {
            background: linear-gradient(135deg, rgba(0, 98, 51, 0.08) 0%, rgba(0, 122, 63, 0.05) 100%);
            color: var(--morocco-green);
            border: 2px solid rgba(0, 98, 51, 0.25);
        }

        /* ===== EXPANDER/ACCORDION ===== */
        .expander {
            background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);
            border: 2px solid rgba(212, 175, 55, 0.25);
            border-radius: 18px;
            margin: 12px 0;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .expander:hover {
            border-color: rgba(212, 175, 55, 0.45);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.07);
        }

        .expander-header {
            padding: 18px 22px;
            cursor: pointer;
            font-weight: 800;
            color: var(--morocco-red);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.05) 0%, transparent 100%);
            transition: all 0.3s ease;
        }

        .expander-header:hover {
            background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(212, 175, 55, 0.03) 100%);
        }

        .expander-content {
            padding: 0 22px 22px;
            color: var(--text-medium);
            line-height: 1.8;
        }

        /* ===== RESPONSIVE DESIGN ===== */
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            .hero {
                padding: 2rem 1.5rem;
                border-radius: 24px;
            }

            .card {
                padding: 20px;
                border-radius: 22px;
            }

            .welcome-bar {
                flex-direction: column;
                text-align: center;
            }

            .radio-group {
                flex-direction: column;
            }

            .btn-primary {
                padding: 14px 24px;
                font-size: 16px;
            }
        }

        /* ===== UTILITY CLASSES ===== */
        .text-center { text-align: center; }
        .mt-2 { margin-top: 16px; }
        .mt-3 { margin-top: 24px; }
        .mb-2 { margin-bottom: 16px; }
        .mb-3 { margin-bottom: 24px; }

        /* ===== SCROLLBAR CUSTOMIZATION ===== */
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

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #c41230, #007a3f);
        }

        /* ===== SELECTION COLOR ===== */
        ::selection {
            background: rgba(212, 175, 55, 0.3);
            color: var(--text-dark);
        }
    </style>
</head>
<body>
    <div class="container">
        
        <!-- Hero Section -->
        <div class="hero">
            <div class="badge">🇲🇦 Moroccan Study Assistant</div>
            <h1>📚 AI Study Assistant</h1>
            <p>
                مساعد دراسي ذكي بطابع مغربي يساعدك على شرح الدروس، تلخيص النصوص،
                إنشاء أسئلة للمراجعة، وحفظ أسئلة كل تلميذ في حسابه الخاص.
            </p>
        </div>

        <!-- Login Section -->
        <div class="card">
            <h2 class="section-title">👤 دخول التلميذ</h2>
            <p class="section-desc">
                أنشئ حسابًا باسمك ورمز سري، وبعدها ستبقى أسئلتك محفوظة في حسابك.
            </p>

            <hr class="divider">

            <div class="form-group">
                <label class="form-label">اختر العملية:</label>
                <div class="radio-group">
                    <div class="radio-option">
                        <input type="radio" id="login" name="mode" checked>
                        <label for="login">تسجيل الدخول</label>
                    </div>
                    <div class="radio-option">
                        <input type="radio" id="register" name="mode">
                        <label for="register">إنشاء حساب جديد</label>
                    </div>
                </div>
            </div>

            <div class="form-group">
                <label class="form-label" for="name">اسم التلميذ:</label>
                <input type="text" id="name" class="form-input" placeholder="اكتب اسمك هنا...">
            </div>

            <div class="form-group">
                <label class="form-label" for="pin">الرمز السري:</label>
                <input type="password" id="pin" class="form-input" placeholder="اكتب الرمز السري...">
            </div>

            <button class="btn-primary" onclick="handleAuth()">
                <span>🚀</span>
                <span>دخول / إنشاء حساب</span>
            </button>
        </div>

        <!-- Welcome Bar (Hidden by default) -->
        <div class="welcome-bar" id="welcomeBar" style="display: none;">
            <div class="welcome-info">
                <h3>مرحبا <span id="studentName">---</span> 👋</h3>
                <p>أنت الآن داخل حسابك. كل سؤال وجواب سيتم حفظه في سجلك الدراسي.</p>
            </div>
            <button class="btn-secondary" onclick="logout()">تسجيل الخروج</button>
        </div>

        <!-- Settings Section -->
        <div class="card">
            <h2 class="section-title">⚙️ إعدادات المساعدة</h2>
            <p class="section-desc">اختر نوع المساعدة، اللغة، والمستوى الدراسي.</p>

            <hr class="divider">

            <div class="form-group">
                <label class="form-label" for="taskType">اختر نوع المساعدة:</label>
                <select id="taskType" class="form-select">
                    <option value="explain">شرح درس</option>
                    <option value="summarize">تلخيص نص</option>
                    <option value="questions">إنشاء أسئلة للمراجعة</option>
                    <option value="simplify">تبسيط مفهوم</option>
                    <option value="correct">تصحيح جواب</option>
                    <option value="quiz">Quiz Mode</option>
                    <option value="history">سجل أسئلتي</option>
                </select>
            </div>

            <div class="form-group">
                <label class="form-label" for="language">اختر اللغة:</label>
                <select id="language" class="form-select">
                    <option value="ar">العربية</option>
                    <option value="fr">الفرنسية</option>
                    <option value="en">الإنجليزية</option>
                    <option value="ma">الدارجة المغربية</option>
                </select>
            </div>

            <div class="form-group">
                <label class="form-label" for="level">اختر المستوى الدراسي:</label>
                <select id="level" class="form-select">
                    <option value="primary">ابتدائي</option>
                    <option value="middle">إعدادي</option>
                    <option value="secondary">ثانوي</option>
                    <option value="university">جامعي</option>
                </select>
            </div>
        </div>

        <!-- Input Section -->
        <div class="card">
            <h2 class="section-title">🌟 أمثلة يمكنك تجربتها</h2>
            <p class="section-desc">اختر مثالًا جاهزًا أو اكتب سؤالك بنفسك في المربع.</p>

            <hr class="divider">

            <div class="form-group">
                <label class="form-label" for="example">اختر مثالًا:</label>
                <select id="example" class="form-select" onchange="setExample()">
                    <option value="">اكتب سؤالك بنفسك</option>
                    <option value="اشرح لي درس المتطابقات الهامة مع أمثلة">اشرح لي درس المتطابقات الهامة مع أمثلة</option>
                    <option value="لخص لي درس الجهاز الهضمي">لخص لي درس الجهاز الهضمي</option>
                    <option value="أعطني 10 أسئلة حول درس الحرب العالمية الثانية">أعطني 10 أسئلة حول درس الحرب العالمية الثانية</option>
                    <option value="اشرح لي المعادلات من الدرجة الأولى">اشرح لي المعادلات من الدرجة الأولى</option>
                    <option value="بسط لي مفهوم الطاقة الكهربائية">بسط لي مفهوم الطاقة الكهربائية</option>
                </select>
            </div>

            <div class="form-group">
                <label class="form-label" for="userInput">اكتب الدرس أو النص أو السؤال هنا:</label>
                <textarea id="userInput" class="form-textarea" placeholder="اكتب سؤالك أو النص هنا..."></textarea>
            </div>

            <button class="btn-primary" onclick="submitQuery()">
                <span>🚀</span>
                <span>إرسال</span>
            </button>
        </div>

        <!-- Loading State (Hidden by default) -->
        <div class="loading-container" id="loadingState" style="display: none;">
            <div class="spinner"></div>
            <p class="loading-text">جاري توليد الجواب... ⏳</p>
        </div>

        <!-- Result Box (Hidden by default) -->
        <div class="result-box" id="resultBox" style="display: none;">
            <h2>📌 الجواب</h2>
            <div id="resultContent"></div>
        </div>

        <!-- Success Alert Example -->
        <div class="alert alert-success mt-3" style="display: none;" id="successAlert">
            <span>✅</span>
            <span>تم حفظ السؤال والجواب في سجلك!</span>
        </div>

        <!-- Footer -->
        <div class="footer">
            <div class="footer-icons">🇲🇦 📚 🤖 ✨</div>
            <strong>AI Study Assistant Morocco</strong><br>
            تصميم مستوحى من الألوان المغربية والزليج التقليدي<br>
            تم إنشاؤه باستخدام Streamlit و Google Gemini API و Supabase<br>
            <small style="opacity: 0.7; margin-top: 8px; display: inline-block;">© 2024 - جميع الحقوق محفوظة</small>
        </div>

    </div>

    <script>
        // Set example in textarea
        function setExample() {
            const select = document.getElementById('example');
            const textarea = document.getElementById('userInput');
            textarea.value = select.value;
        }

        // Handle authentication (demo)
        function handleAuth() {
            const name = document.getElementById('name').value;
            const pin = document.getElementById('pin').value;

            if (!name || !pin) {
                showAlert('warning', 'يرجى كتابة الاسم والرمز السري.');
                return;
            }

            if (pin.length < 4) {
                showAlert('warning', 'الرمز السري يجب أن يحتوي على 4 أحرف أو أرقام على الأقل.');
                return;
            }

            // Simulate login success
            document.getElementById('studentName').textContent = name;
            document.getElementById('welcomeBar').style.display = 'flex';
            showAlert('success', `مرحباً ${name}! تم تسجيل الدخول بنجاح.`);
            
            // Scroll to welcome bar
            document.getElementById('welcomeBar').scrollIntoView({ behavior: 'smooth' });
        }

        // Logout function
        function logout() {
            document.getElementById('welcomeBar').style.display = 'none';
            document.getElementById('name').value = '';
            document.getElementById('pin').value = '';
            showAlert('info', 'تم تسجيل الخروج بنجاح.');
        }

        // Submit query (demo)
        function submitQuery() {
            const input = document.getElementById('userInput').value;

            if (!input.trim()) {
                showAlert('warning', 'اكتب شيئًا أولًا.');
                return;
            }

            // Show loading
            document.getElementById('loadingState').style.display = 'block';
            document.getElementById('resultBox').style.display = 'none';

            // Scroll to loading
            document.getElementById('loadingState').scrollIntoView({ behavior: 'smooth' });

            // Simulate API call
            setTimeout(() => {
                document.getElementById('loadingState').style.display = 'none';
                
                // Show result
                const resultBox = document.getElementById('resultBox');
                const resultContent = document.getElementById('resultContent');
                
                resultContent.innerHTML = `
                    <p style="line-height: 1.9; color: #5d4037;">
                        <strong style="color: #006233;">💡 هذا عرض توضيحي للنتيجة:</strong><br><br>
                        بناءً على سؤالك: "<em>${input}</em>"<br><br>
                        سيتم هنا عرض الإجابة من الذكاء الاصطناعي بعد ربط التطبيق بالـ API الفعلي.
                        <br><br>
                        <span style="color: #b11226; font-weight: 700;">✨ النتيجة ستظهر هنا بشكل منظم وجميل!</span>
                    </p>
                `;
                
                resultBox.style.display = 'block';
                document.getElementById('successAlert').style.display = 'flex';
                
                // Scroll to result
                resultBox.scrollIntoView({ behavior: 'smooth' });
                
            }, 2500);
        }

        // Show alert function
        function showAlert(type, message) {
            // Remove existing alerts
            const existingAlerts = document.querySelectorAll('.alert-toast');
            existingAlerts.forEach(alert => alert.remove());

            // Create new alert
            const alert = document.createElement('div');
            alert.className = `alert alert-${type} alert-toast`;
            alert.style.position = 'fixed';
            alert.style.top = '20px';
            alert.style.left = '50%';
            alert.style.transform = 'translateX(-50%)';
            alert.style.zIndex = '9999';
            alert.style.maxWidth = '90%';
            alert.style.width = '500px';
            alert.style.boxShadow = '0 10px 40px rgba(0,0,0,0.2)';

            const icons = {
                success: '✅',
                warning: '⚠️',
                error: '❌',
                info: 'ℹ️'
            };

            alert.innerHTML = `<span>${icons[type]}</span><span>${message}</span>`;
            document.body.appendChild(alert);

            // Auto remove after 4 seconds
            setTimeout(() => {
                alert.style.animation = 'slideDown 0.3s ease-out reverse';
                setTimeout(() => alert.remove(), 300);
            }, 4000);
        }

        // Add smooth scroll behavior
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
    </script>
</body>
</html>
