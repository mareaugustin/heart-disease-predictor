# ============================================================
# FICHIER DE STYLE GLOBAL — Partagé entre toutes les pages
# ============================================================

def get_css():
    return """
    <!-- Font Awesome pour les icônes -->
    <link rel="stylesheet" 
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" 
          rel="stylesheet">

    <style>
    /* ========== FONT GLOBALE ========== */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ========== SIDEBAR ========== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-right: none;
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] p {
        color: #b0b8c1 !important;
    }
    /* Liens de navigation sidebar */
    [data-testid="stSidebarNavLink"] {
        border-radius: 10px !important;
        margin: 3px 8px !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
        color: #b0b8c1 !important;
    }
    [data-testid="stSidebarNavLink"]:hover {
        background-color: rgba(255,255,255,0.1) !important;
        color: #ffffff !important;
        transform: translateX(5px);
    }
    [data-testid="stSidebarNavLink"][aria-selected="true"] {
        background: linear-gradient(90deg, #e74c3c, #c0392b) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* ========== PAGE PRINCIPALE ========== */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    /* ========== CARTES / CARDS ========== */
    .card {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }

    /* ========== TITRE PRINCIPAL ========== */
    .main-title {
        font-size: 2.8em;
        font-weight: 700;
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 5px;
        line-height: 1.2;
    }
    .sub-title {
        font-size: 1.1em;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 30px;
        font-weight: 400;
    }

    /* ========== BADGES ========== */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: 600;
        margin: 3px;
    }
    .badge-red   { background: #fde8e8; color: #e74c3c; }
    .badge-green { background: #e8f8f0; color: #27ae60; }
    .badge-blue  { background: #e8f0fe; color: #2980b9; }
    .badge-orange{ background: #fef3e8; color: #e67e22; }
    .badge-purple{ background: #f3e8fe; color: #8e44ad; }

    /* ========== BOÎTES INFO ========== */
    .info-box {
        background: linear-gradient(135deg, #f8f9ff, #eef2ff);
        border-left: 5px solid #3498db;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .success-box {
        background: linear-gradient(135deg, #f0fff4, #e8f8f0);
        border-left: 5px solid #2ecc71;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #fffbf0, #fef9e7);
        border-left: 5px solid #f39c12;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .danger-box {
        background: linear-gradient(135deg, #fff5f5, #fde8e8);
        border-left: 5px solid #e74c3c;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
    }
    .question-box {
        background: linear-gradient(135deg, #eaf4fb, #d6eaf8);
        border-left: 5px solid #2980b9;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
        font-weight: 600;
        font-size: 1.05em;
    }
    .answer-box {
        background: linear-gradient(135deg, #f0fff4, #e8f8f0);
        border-left: 5px solid #27ae60;
        border-radius: 0 12px 12px 0;
        padding: 16px 20px;
        margin: 12px 0;
        line-height: 1.7;
    }

    /* ========== METRIC CARDS ========== */
    .metric-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 15px rgba(0,0,0,0.07);
        border: 1px solid #f0f0f0;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-value {
        font-size: 2em;
        font-weight: 700;
        color: #2c3e50;
    }
    .metric-label {
        font-size: 0.9em;
        color: #7f8c8d;
        margin-top: 5px;
        font-weight: 500;
    }
    .metric-icon {
        font-size: 1.8em;
        margin-bottom: 8px;
    }

    /* ========== ALGO CARDS ========== */
    .algo-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        height: 140px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .algo-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: linear-gradient(180deg, #e74c3c, #c0392b);
    }
    .algo-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(231,76,60,0.15);
    }
    .algo-number {
        font-size: 1.8em;
        font-weight: 700;
        color: #e74c3c;
    }
    .algo-name {
        font-size: 1em;
        font-weight: 600;
        color: #2c3e50;
        margin: 5px 0;
    }
    .algo-desc {
        font-size: 0.82em;
        color: #7f8c8d;
        line-height: 1.4;
    }

    /* ========== SECTION HEADERS ========== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f0f0;
    }
    .section-header i {
        font-size: 1.4em;
        color: #e74c3c;
    }
    .section-header h2 {
        font-size: 1.5em;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }

    /* ========== DIVIDER ========== */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #e74c3c, #3498db, #2ecc71);
        border: none;
        border-radius: 3px;
        margin: 30px 0;
    }

    /* ========== FOOTER ========== */
    .footer {
        text-align: center;
        color: #95a5a6;
        font-size: 0.85em;
        margin-top: 60px;
        padding: 20px;
        border-top: 1px solid #ecf0f1;
        background: #fafafa;
        border-radius: 12px;
    }

    /* ========== STREAMLIT NATIFS - OVERRIDE ========== */
    .stButton > button {
        background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 1em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(231,76,60,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(231,76,60,0.4) !important;
    }
    div[data-testid="metric-container"] {
        background: #ffffff;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border: 1px solid #f0f0f0;
    }

    /* ========== DATAFRAME ========== */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ========== SIDEBAR LOGO/TITLE ========== */
    .sidebar-logo {
        text-align: center;
        padding: 20px 10px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
    }
    .sidebar-logo .logo-icon {
        font-size: 3em;
        display: block;
        margin-bottom: 8px;
    }
    .sidebar-logo .logo-title {
        font-size: 1.1em;
        font-weight: 700;
        color: #ffffff !important;
    }
    .sidebar-logo .logo-sub {
        font-size: 0.8em;
        color: #b0b8c1 !important;
    }
    </style>
    """


def inject_css(st):
    """Injecte le CSS dans la page Streamlit"""
    st.markdown(get_css(), unsafe_allow_html=True)


def footer(st):
    """Affiche le footer"""
    st.markdown("""
    <div class="footer">
        <b>Heart Disease Predictor</b> — IFOAD Intelligence Artificielle<br>
        <span>MILLOGO Maré Augustin & OUEDRAOGO Abdoul Koudous &nbsp;|&nbsp; 
        Dataset: UCI Heart Disease (ID=45) &nbsp;|&nbsp;
        <i class="fa-solid fa-code"></i> Machine Learning</span>
    </div>
    """, unsafe_allow_html=True)


def section_header(st, icon_class, title):
    """Affiche un header de section avec icône Font Awesome"""
    st.markdown(f"""
    <div class="section-header">
        <i class="{icon_class}"></i>
        <h2>{title}</h2>
    </div>
    """, unsafe_allow_html=True)


def divider(st):
    """Affiche un divider coloré"""
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
