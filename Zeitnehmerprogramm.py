import streamlit as st
import time

# Seitenkonfiguration für das Tablet
st.set_page_config(page_title="Zeitnehmer-App", layout="wide")

# ==========================================
# SESSION STATE INITIALISIERUNG (Zustand speichern)
# ==========================================
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.game_started = False
    st.session_state.score_home = 0
    st.session_state.score_guest = 0
    st.session_state.remaining_seconds = 12 * 60
    st.session_state.elapsed_seconds = 0
    st.session_state.running = False
    st.session_state.name_home = "HEIM"
    st.session_state.name_guest = "GAST"
    st.session_state.period_type = "Halbzeit"
    st.session_state.current_period = 1
    st.session_state.max_periods = 6

# ==========================================
# 1. SETUP-BILDSCHIRM (Konfiguration vor Spielstart)
# ==========================================
if not st.session_state.game_started:
    st.title("⏱️ Zeitnehmer-App - Konfiguration")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.name_home = st.text_input("Name Heim-Team", st.session_state.name_home)
    with col2:
        st.session_state.name_guest = st.text_input("Name Gast-Team", st.session_state.name_guest)

    st.subheader("Spielzeit wählen (Minuten)")
    time_col1, time_col2, time_col3, time_col4 = st.columns(4)
    
    selected_minutes = st.session_state.remaining_seconds // 60
    if time_col1.button("12 min", use_container_width=True):
        selected_minutes = 12
    if time_col2.button("15 min", use_container_width=True):
        selected_minutes = 15
    if time_col3.button("20 min", use_container_width=True):
        selected_minutes = 20
        
    custom_min = time_col4.number_input("Oder eigene Min:", min_value=1, max_value=90, value=selected_minutes)
    st.session_state.remaining_seconds = custom_min * 60

    st.subheader("Spielabschnitt")
    p_type = st.radio("Modus auswählen:", ["Halbzeit", "Drittel"], horizontal=True)
    st.session_state.period_type = p_type
    st.session_state.max_periods = 6 if p_type == "Halbzeit" else 3

    st.write("")
    if st.button("🚀 Spiel starten", type="primary", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# ==========================================
# 2. HAUPTSPIEL-BILDSCHIRM (Das Bedienfeld)
# ==========================================
else:
    # Zurück-Button oben links
    if st.button("← Zurück zur Konfiguration"):
        st.session_state.game_started = False
        st.rerun()

    st.markdown("---")

    # Layout: Heim | Uhr / Steuerung | Gast
    col_home, col_center, col_guest = st.columns([1, 1.5, 1])

    # --- HEIM TEAM ---
    with col_home:
        st.markdown(f"### 🏠 {st.session_state.name_home}")
        st.markdown(f"<h1 style='font-size: 80px; text-align: center; color: #00FF00;'>{st.session_state.score_home}</h1>", unsafe_allow_html=True)
        
        h_col1, h_col2 = st.columns(2)
        if h_col1.button("Tor +1 (Heim)", use_container_width=True):
            st.session_state.score_home += 1
            st.rerun()
        if h_col2.button("Tor -1 (Heim)", use_container_width=True):
            st.session_state.score_home = max(0, st.session_state.score_home - 1)
            st.rerun()

    # --- MITTE (UHR & STEUERUNG) ---
    with col_center:
        period_text = f"{st.session_state.current_period}. Halbzeit" if st.session_state.period_type == "Halbzeit" else f"{st.session_state.current_period}. Drittel"
        st.markdown(f"<h3 style='text-align: center; color: #00E5FF;'>{period_text}</h3>", unsafe_allow_html=True)

        # Zeit formatieren (MM:SS)
        mins = st.session_state.remaining_seconds // 60
        secs = st.session_state.remaining_seconds % 60
        time_display = f"{mins:02d}:{secs:02d}"
        
        st.markdown(f"<h1 style='font-size: 90px; text-align: center; color: #FFCC00;'>{time_display}</h1>", unsafe_allow_html=True)

        # Start / Stopp Buttons
        c_btn1, c_btn2 = st.columns(2)
        if not st.session_state.running:
            if c_btn1.button("▶️ START", use_container_width=True, type="primary"):
                st.session_state.running = True
                st.rerun()
        else:
            if c_btn1.button("⏸️ STOPP", use_container_width=True):
                st.session_state.running = False
                st.rerun()

        if c_btn2.button("🔄 Reset Zeit", use_container_width=True):
            st.session_state.running = False
            st.session_state.remaining_seconds = (st.session_state.remaining_seconds + st.session_state.elapsed_seconds)
            st.session_state.elapsed_seconds = 0
            st.rerun()

    # --- GAST TEAM ---
    with col_guest:
        st.markdown(f"### ✈️ {st.session_state.name_guest}")
        st.markdown(f"<h1 style='font-size: 80px; text-align: center; color: #00FF00;'>{st.session_state.score_guest}</h1>", unsafe_allow_html=True)
        
        g_col1, g_col2 = st.columns(2)
        if g_col1.button("Tor +1 (Gast)", use_container_width=True):
            st.session_state.score_guest += 1
            st.rerun()
        if g_col2.button("Tor -1 (Gast)", use_container_width=True):
            st.session_state.score_guest = max(0, st.session_state.score_guest - 1)
            st.rerun()

    # Timer-Logik im Hintergrund, wenn aktiv
    if st.session_state.running:
        if st.session_state.remaining_seconds > 0:
            time.sleep(1)
            st.session_state.remaining_seconds -= 1
            st.session_state.elapsed_seconds += 1
            st.rerun()
        else:
            st.session_state.running = False
            st.warning("⏰ Zeit abgelaufen!")