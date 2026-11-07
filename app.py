"""
Gulzar-AI — Streamlit interface
Run with: streamlit run app.py

Keep app.py, engine.py, knowledge_base.py and treatments.py in the same folder.
"""

import streamlit as st

from engine import diagnose
from knowledge_base import (
    CHOICES,
    EXTRA_CONDITIONS,
    PLANTS,
    SYMPTOM_GROUPS,
    kb_stats,
)
from treatments import get_treatment


st.set_page_config(
    page_title="Gulzar-AI | Plant Doctor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

    :root {
        --green: #246b49;
        --green-dark: #174b35;
        --green-pale: #e8f3eb;
        --ink: #193126;
        --muted: #52665a;
        --line: #dce7df;
        --surface: #ffffff;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 8% 2%, rgba(205, 235, 211, .68), transparent 34rem),
            #f5f8f4;
        color: #193126 !important;
        font-family: 'DM Sans', sans-serif;
    }
    .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 4rem; }
    h1, h2, h3, h4, h5, h6 { font-family: 'Manrope', sans-serif !important; color: #193126 !important; }
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stCaption, [data-testid="stCaptionContainer"] {
        color: #344b3d;
    }
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stForm"] label,
    [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {
        color: #263d30 !important;
    }
    [data-testid="stWidgetLabel"] p { font-weight: 600; }
    [data-testid="stCaptionContainer"] p,
    .stCaption { color: #52665a !important; }
    .hero {
        background: linear-gradient(120deg, #173f30 0%, #246b49 62%, #438259 100%);
        border-radius: 24px;
        color: white;
        padding: 2.2rem 2.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 16px 38px rgba(29, 73, 49, .15);
        position: relative;
        overflow: hidden;
        animation: hero-arrive .75s cubic-bezier(.2,.8,.2,1) both;
    }
    .hero:after {
        content: '🌿';
        position: absolute;
        right: 5%;
        top: 5%;
        font-size: 7rem;
        opacity: .14;
        transform: rotate(-18deg);
        animation: leaf-float 5s ease-in-out infinite;
        pointer-events: none;
    }
    .hero h1 { color: white; margin: .15rem 0 .45rem; font-size: 2.5rem; }
    .hero p { color: rgba(255,255,255,.86); max-width: 700px; margin: 0; font-size: 1.05rem; }
    .eyebrow {
        text-transform: uppercase;
        letter-spacing: .14em;
        font-size: .73rem;
        font-weight: 700;
        color: #d2ead7;
    }
    .section-intro { color: #52665a !important; margin-top: -.5rem; margin-bottom: 1.25rem; }
    .panel-title {
        border-bottom: 1px solid var(--line);
        padding-bottom: .6rem;
        margin: 1.2rem 0 .9rem;
    }
    .panel-title h4 { color: #214532 !important; margin: 0; }
    div[data-testid="stForm"] {
        background: rgba(255,255,255,.96);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1.35rem 1.5rem 1.5rem;
        box-shadow: 0 8px 26px rgba(28, 57, 39, .045);
    }
    div[data-testid="stForm"] [data-baseweb="select"] > div,
    div[data-testid="stForm"] [data-baseweb="input"] > div,
    div[data-testid="stForm"] [data-baseweb="textarea"] > div {
        background: #ffffff !important;
        border-color: #b9cbbf !important;
        color: #193126 !important;
        transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease;
    }
    div[data-testid="stForm"] [data-baseweb="select"] > div:hover,
    div[data-testid="stForm"] [data-baseweb="input"] > div:hover {
        border-color: #57916d !important;
    }
    div[data-testid="stForm"] input,
    div[data-testid="stForm"] textarea,
    div[data-testid="stForm"] [data-baseweb="select"] *,
    div[data-testid="stForm"] [data-baseweb="tag"] {
        color: #193126 !important;
        -webkit-text-fill-color: #193126;
    }
    div[data-testid="stForm"] input::placeholder,
    div[data-testid="stForm"] textarea::placeholder {
        color: #66796d !important;
        -webkit-text-fill-color: #66796d;
        opacity: 1;
    }
    div[data-testid="stForm"] [data-baseweb="tag"] {
        background: #e8f3eb !important;
        border: 1px solid #c9dfcf !important;
        border-radius: 8px !important;
    }
    [data-baseweb="popover"] [role="option"],
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="menu"] [role="option"] {
        color: #193126 !important;
        background-color: #ffffff !important;
    }
    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="menu"] [role="option"]:hover {
        background-color: #e8f3eb !important;
    }
    div[data-testid="stForm"] [data-baseweb="select"]:focus-within > div,
    div[data-testid="stForm"] [data-baseweb="input"]:focus-within > div {
        border-color: #246b49 !important;
        box-shadow: 0 0 0 3px rgba(36, 107, 73, .16) !important;
    }
    [data-testid="stSlider"] [role="slider"] { box-shadow: 0 0 0 4px rgba(36,107,73,.12); }
    div[data-testid="stFormSubmitButton"] button {
        min-height: 3.2rem;
        border-radius: 11px;
        background: var(--green);
        border-color: var(--green);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 6px 14px rgba(38, 115, 77, .18);
        transition: transform .2s ease, box-shadow .2s ease, background .2s ease;
    }
    div[data-testid="stFormSubmitButton"] button:hover {
        background: var(--green-dark);
        border-color: var(--green-dark);
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(23, 75, 53, .24);
    }
    div[data-testid="stFormSubmitButton"] button:focus-visible {
        outline: 3px solid #83b993;
        outline-offset: 3px;
    }
    .result-card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 1.2rem 1.35rem;
        margin: .65rem 0;
        box-shadow: 0 5px 18px rgba(28, 57, 39, .04);
        animation: card-arrive .5s ease both;
        transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
    }
    .result-card:hover {
        transform: translateY(-3px);
        border-color: #b6d2be;
        box-shadow: 0 12px 26px rgba(28, 57, 39, .09);
    }
    .result-meta { color: #52665a !important; font-size: .9rem; }
    .result-heading { color: #193126 !important; font-size: 1.2rem; font-weight: 700; }
    .confidence {
        display: inline-block;
        color: #174b35 !important;
        background: var(--green-pale);
        padding: .3rem .65rem;
        border-radius: 999px;
        font-size: .83rem;
        font-weight: 700;
        white-space: nowrap;
    }
    .footer-note { color: #52665a !important; font-size: .85rem; }
    [data-testid="stSidebar"] { background: #edf4ee; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] { color: #344b3d !important; }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] { color: #193126 !important; }
    [data-testid="stProgressBar"] > div > div { background-color: #246b49; }
    @keyframes hero-arrive {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes card-arrive {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes leaf-float {
        0%, 100% { transform: translateY(0) rotate(-18deg); }
        50% { transform: translateY(-9px) rotate(-12deg); }
    }
    @media (max-width: 640px) {
        .block-container { padding: 1rem 1rem 3rem; }
        .hero { border-radius: 18px; padding: 1.6rem 1.3rem; }
        .hero h1 { font-size: 2rem; }
        .hero:after { right: 0; top: 20%; font-size: 5rem; }
        div[data-testid="stForm"] { padding: 1rem; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: .01ms !important;
            animation-iteration-count: 1 !important;
            scroll-behavior: auto !important;
            transition-duration: .01ms !important;
        }
    }

    /* Keep every surface mint and all ordinary text high-contrast. */
    :root {
        --green: #2f7955;
        --green-dark: #1d593c;
        --green-pale: #dcefe1;
        --ink: #173a29;
        --muted: #365744;
        --line: #b8d5c0;
        --surface: #e8f4ea;
    }
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: #eaf4ec !important;
        color: #173a29 !important;
    }
    .stApp {
        background: #eaf4ec !important;
        color: #173a29 !important;
    }
    .stApp p, .stApp li, .stApp strong, .stApp em,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stWidgetLabel"],
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stMetricValue"],
    .stApp [data-testid="stAlert"] p,
    .stApp [data-testid="stExpander"] summary,
    .stApp [data-testid="stRadio"] label,
    .stApp [data-testid="stCheckbox"] label {
        color: #173a29 !important;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #173a29 !important;
    }
    .stApp [data-testid="stCaptionContainer"] p,
    .stApp .stCaption,
    .section-intro, .result-meta, .footer-note {
        color: #365744 !important;
    }
    .hero {
        background: linear-gradient(120deg, #2f7955 0%, #3b8b61 58%, #58a174 100%) !important;
    }
    .hero h1, .hero p, .hero .eyebrow {
        color: #ffffff !important;
    }
    .hero .eyebrow { color: #e3f5e8 !important; }
    div[data-testid="stForm"] {
        background: #e2f0e5 !important;
        border-color: #b8d5c0 !important;
    }
    div[data-testid="stForm"] [data-baseweb="select"] > div,
    div[data-testid="stForm"] [data-baseweb="input"] > div,
    div[data-testid="stForm"] [data-baseweb="textarea"] > div {
        background: #f2f8f3 !important;
        border-color: #9fbea8 !important;
    }
    div[data-testid="stForm"] input,
    div[data-testid="stForm"] textarea,
    div[data-testid="stForm"] [data-baseweb="select"] *,
    div[data-testid="stForm"] [data-baseweb="tag"],
    div[data-testid="stForm"] label {
        color: #173a29 !important;
        -webkit-text-fill-color: #173a29 !important;
    }
    div[data-testid="stForm"] input::placeholder,
    div[data-testid="stForm"] textarea::placeholder {
        color: #526e5c !important;
        -webkit-text-fill-color: #526e5c !important;
        opacity: 1 !important;
    }
    [data-baseweb="popover"], [data-baseweb="menu"],
    [data-baseweb="popover"] ul, [data-baseweb="popover"] li {
        background: #edf6ef !important;
        color: #173a29 !important;
    }
    [data-baseweb="popover"] [role="option"],
    [data-baseweb="menu"] [role="option"] {
        background: #edf6ef !important;
        color: #173a29 !important;
    }
    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="menu"] [role="option"]:hover {
        background: #d5eadb !important;
        color: #173a29 !important;
    }
    .result-card {
        background: #e4f1e7 !important;
        border-color: #b8d5c0 !important;
    }
    .result-heading, .confidence { color: #173a29 !important; }
    .confidence { background: #cfe7d5 !important; }
    [data-testid="stSidebar"] {
        background: #dcefe1 !important;
    }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMetricLabel"],
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #173a29 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: #eaf4ec;
        border: 1px solid #b8d5c0;
        border-radius: 12px;
        padding: .6rem .8rem;
    }
    [data-testid="stFormSubmitButton"] button {
        background: #2f7955 !important;
        border-color: #2f7955 !important;
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🌱 About Gulzar-AI")
    st.write(
        "A plant-care decision-support tool that uses forward chaining and "
        "Certainty Factors to connect your observations with possible causes."
    )
    stats = kb_stats()
    st.metric("Supported plants", stats["plants"])
    st.metric("Knowledge-base rules", stats["total_rules"])
    st.caption(
        "For education only—not a laboratory diagnosis. For serious or spreading "
        "problems, consult a local agricultural expert."
    )
    st.divider()
    st.caption("Made for Pakistani home gardens 🌿")


st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Your garden, in good hands</div>
      <h1>Gulzar-AI Plant Doctor</h1>
      <p>Tell us what you’re seeing. Get likely causes and practical next steps
      tailored to your plant and growing conditions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


def choice_widget(label, options, key):
    """Return the selected internal ID, or None when the user skips it."""
    labels = ["Not sure / skip"] + list(options.values())
    selected_label = st.selectbox(label, labels, key=key)
    if selected_label == "Not sure / skip":
        return None
    return next(
        option_id
        for option_id, option_label in options.items()
        if option_label == selected_label
    )


st.header("Let’s learn about your plant")
st.markdown(
    '<p class="section-intro">Share what you know—every detail is optional except the plant type.</p>',
    unsafe_allow_html=True,
)

with st.form("plant_diagnosis_form"):
    st.markdown("#### 🌼 Plant and location")
    plant_col, location_col, setting_col = st.columns(3)
    with plant_col:
        plant_id = st.selectbox(
            "Which plant is affected? *",
            options=list(PLANTS.keys()),
            format_func=lambda value: PLANTS[value],
        )
    with location_col:
        location_id = choice_widget("Where is it planted?", CHOICES["location"], "location_choice")
    with setting_col:
        setting_id = choice_widget("Where is it kept?", CHOICES["setting"], "setting_choice")

    st.markdown('<div class="panel-title"><h4>🍃 What symptoms do you notice?</h4></div>', unsafe_allow_html=True)
    symptom_columns = st.columns(2)
    symptoms = []
    for index, (group, options) in enumerate(SYMPTOM_GROUPS.items()):
        with symptom_columns[index % 2]:
            selected = st.multiselect(
                group,
                options=list(options.keys()),
                format_func=lambda value, labels=options: labels[value],
                key=f"symptoms_{index}",
                placeholder="Choose any that apply",
            )
            symptoms.extend(selected)

    st.markdown('<div class="panel-title"><h4>🪴 Care and environment</h4></div>', unsafe_allow_html=True)
    care_columns = st.columns(3)
    with care_columns[0]:
        watering = choice_widget("How often do you water?", CHOICES["watering"], "watering_choice")
        drainage = choice_widget("How is the drainage?", CHOICES["drainage"], "drainage_choice")
        soil_feel = choice_widget("How does the soil feel?", CHOICES["soil_feel"], "soil_choice")
        fertilizer = choice_widget("When was it last fertilized?", CHOICES["fertilizer"], "fertilizer_choice")
    with care_columns[1]:
        pot_size = choice_widget("Is the pot the right size?", CHOICES["pot_size"], "pot_size_choice")
        season = choice_widget("Current season", CHOICES["season"], "season_choice")
        humidity = choice_widget("Humidity", CHOICES["humidity"], "humidity_choice")
        airflow = choice_widget("Air circulation", CHOICES["airflow"], "airflow_choice")
    with care_columns[2]:
        water_source = choice_widget("Main water source", CHOICES["water_source"], "water_source_choice")
        sun_hours = st.slider("Approx. hours of direct sun", 0, 12, 4, help="Move this if you know the plant’s daily sun exposure.")
        temperature = st.slider("Approx. daytime temperature (°C)", 0, 50, 25, help="Move this if you know the recent daytime temperature.")

    st.markdown('<div class="panel-title"><h4>🔎 A few extra details</h4></div>', unsafe_allow_html=True)
    extra_columns = st.columns(3)
    extras = []
    for index, (group, options) in enumerate(EXTRA_CONDITIONS.items()):
        with extra_columns[index % 3]:
            selected = st.multiselect(
                group,
                options=list(options.keys()),
                format_func=lambda value, labels=options: labels[value],
                key=f"extras_{index}",
                placeholder="Choose any that apply",
            )
            extras.extend(selected)

    st.caption("* Required. Select “Not sure / skip” whenever you’re uncertain.")
    submitted = st.form_submit_button(
        "🌿  Get my plant diagnosis",
        type="primary",
        use_container_width=True,
    )

if submitted:
    form_data = {
        "plant": plant_id,
        "location": location_id,
        "setting": setting_id,
        "symptoms": symptoms,
        "extras": extras,
        "watering": watering,
        "drainage": drainage,
        "soil_feel": soil_feel,
        "fertilizer": fertilizer,
        "pot_size": pot_size,
        "season": season,
        "humidity": humidity,
        "airflow": airflow,
        "water_source": water_source,
        "sun_hours": sun_hours,
        "temperature": temperature,
    }
    st.session_state["diagnosis_result"] = diagnose(form_data)
    st.session_state["diagnosis_plant"] = PLANTS[plant_id]

result = st.session_state.get("diagnosis_result")
if result is not None:
    st.divider()
    st.header(f"Your plant health report")
    st.markdown(
        f'<p class="section-intro">Findings for <strong>{st.session_state["diagnosis_plant"]}</strong>, ranked by certainty.</p>',
        unsafe_allow_html=True,
    )

    if not result.diagnoses:
        st.info(
            "There isn’t enough matching evidence for a specific diagnosis yet. "
            "Try selecting the symptoms you can see, then submit again."
        )
    else:
        for rank, diagnosis in enumerate(result.diagnoses[:5], start=1):
            treatment = get_treatment(diagnosis.id)
            st.markdown(
                f"""
                <div class="result-card">
                  <div style="display:flex;justify-content:space-between;gap:1rem;align-items:flex-start;flex-wrap:wrap">
                    <div>
                      <div class="result-heading">{rank}. {diagnosis.name}</div>
                      <div class="result-meta">{diagnosis.category} · {diagnosis.level}</div>
                    </div>
                    <span class="confidence">{diagnosis.percent}% match</span>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(diagnosis.percent / 100)
            st.write(treatment["summary"])
            if treatment["treatment"]:
                st.markdown("**What to do**")
                for step in treatment["treatment"]:
                    st.markdown(f"- {step}")
            if treatment["prevention"]:
                st.markdown(f"**Prevention:** {treatment['prevention']}")
            st.caption(f"Urgency: {treatment['urgency']}")

        with st.expander("How did Gulzar-AI reach this result?"):
            st.write(
                f"The expert system completed {result.cycles} inference "
                f"cycle(s) and matched {len(result.trace)} rule(s)."
            )
            for diagnosis in result.diagnoses[:5]:
                st.markdown(f"**{diagnosis.name} — supporting evidence**")
                if diagnosis.evidence:
                    for evidence in diagnosis.evidence:
                        st.markdown(f"- {evidence.description} *(CF {evidence.cf:.2f})*")
                else:
                    st.write("No individual rule evidence was recorded.")

    st.markdown(
        '<p class="footer-note">These are possible causes, not a confirmed diagnosis. '
        'Use treatments cautiously and seek local expert advice if the plant continues to decline.</p>',
        unsafe_allow_html=True,
    )
