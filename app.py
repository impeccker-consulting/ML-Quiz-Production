from quiz.visuals import render_visual
import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from quiz.access import verify_access_code
from quiz.engine import (
    load_bank,
    create_attempt,
    save_attempt,
    load_attempt,
    submit_attempt,
    is_expired,
    parse_iso,
)

BASE = Path(__file__).resolve().parent
QUIZ_DIR = BASE / "quiz"
QUIZ_CONFIG_FILE = QUIZ_DIR / "config.json"
QUESTION_BANK_FILE = QUIZ_DIR / "question_bank.json"
ATTEMPTS_DIR = BASE / "attempts"

st.set_page_config(page_title="ML Quiz", page_icon="📝", layout="centered")

with open(QUIZ_CONFIG_FILE, encoding="utf-8") as f:
    CONFIG = json.load(f)

QUESTION_BANK = load_bank(QUESTION_BANK_FILE)

QUIZ_ID = CONFIG["Quiz_ID"]
QUIZ_TITLE = CONFIG["Quiz_Title"]
DURATION_MINUTES = int(CONFIG["Duration_Minutes"])
TOTAL_MARKS = int(CONFIG.get("Total_Marks", 20))
QUESTION_COUNT = int(CONFIG.get("Question_Count", 20))

for key, value in {
    "authenticated": False,
    "sap_id": None,
    "attempt": None,
    "current_question": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

if not st.session_state.authenticated:
    st.title("📝 ML Quiz")
    st.subheader(QUIZ_TITLE)
    st.info(
        f"Total Questions: {QUESTION_COUNT}  \n"
        f"Total Marks: {TOTAL_MARKS}  \n"
        f"Duration: {DURATION_MINUTES} minutes"
    )

    sap_id = st.text_input("SAP ID", placeholder="Enter your SAP ID")
    access_code = st.text_input(
        "Quiz Access Code",
        type="password",
        placeholder="Enter your quiz access code",
    )

    if st.button("Start Quiz", type="primary"):
        sap_id = sap_id.strip().upper()
        access_code = access_code.strip().upper()

        if not sap_id:
            st.error("Please enter your SAP ID.")
            st.stop()
        if not access_code:
            st.error("Please enter your quiz access code.")
            st.stop()

        faculty_key = st.secrets["FACULTY_KEY"]

        if not verify_access_code(sap_id, QUIZ_ID, access_code, faculty_key):
            st.error("Invalid SAP ID or quiz access code.")
            st.stop()

        attempt = load_attempt(BASE, QUIZ_ID, sap_id)

        if attempt is None:
            try:
                attempt = create_attempt(BASE, QUESTION_BANK, CONFIG, sap_id)
            except ValueError as exc:
                st.error(str(exc))
                st.stop()

        st.session_state.authenticated = True
        st.session_state.sap_id = sap_id
        st.session_state.attempt = attempt
        st.rerun()

    st.stop()

sap_id = st.session_state.sap_id
attempt = load_attempt(BASE, QUIZ_ID, sap_id)

if attempt is None:
    st.session_state.authenticated = False
    st.session_state.attempt = None
    st.error("Your quiz attempt could not be recovered. Please contact the faculty administrator.")
    st.stop()

st.session_state.attempt = attempt

if attempt.get("Submitted"):
    st.title("📝 ML Quiz")
    st.success("Your quiz has been submitted successfully.")
    if attempt.get("Auto_Submitted"):
        st.warning("Time is up. Your quiz was submitted automatically.")
    st.info("Your response has been recorded. You may close this page.")
    st.stop()

if is_expired(attempt):
    submit_attempt(BASE, attempt, auto=True)
    st.session_state.attempt = attempt
    st.rerun()

deadline = parse_iso(attempt["Deadline_Timestamp"])

@st.fragment(run_every="1s")
def render_timer():
    remaining = max(
        0,
        int((deadline - datetime.now(timezone.utc)).total_seconds()),
    )

    minutes, seconds = divmod(remaining, 60)

    st.markdown(
        f"""
        <div style="
            position:fixed;
            top:0;
            left:50%;
            transform:translateX(-50%);
            width:min(700px, calc(100vw - 24px));
            z-index:999999;
            background:white;
            padding:10px;
            border-radius:8px;
            border:2px solid #ccc;
            text-align:center;
            font-size:26px;
            font-weight:bold;
            box-sizing:border-box;">
            TIME REMAINING<br>{minutes:02d}:{seconds:02d}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if remaining <= 0:
        fresh = load_attempt(BASE, QUIZ_ID, sap_id)

        if fresh is not None and not fresh.get("Submitted"):
            submit_attempt(BASE, fresh, auto=True)

        st.session_state.attempt = fresh

        st.rerun(scope="app")

render_timer()

st.title("📝 ML Quiz")
st.caption(
    f"SAP ID: {sap_id}  |  Questions: {QUESTION_COUNT}  |  "
    f"Duration: {DURATION_MINUTES} minutes"
)
st.divider()

questions = attempt["Questions"]
current = max(0, min(attempt.get("Current_Question", 0), len(questions) - 1))
q = questions[current]

if q.get("Shown_Timestamp") is None:
    q["Shown_Timestamp"] = datetime.now(timezone.utc).isoformat()
    save_attempt(BASE, attempt)

st.subheader(f"Question {current + 1} of {len(questions)}")
st.caption(
    "Select all options that apply."
    if q.get("Response_Type") == "Multi"
    else "Select one option."
)
st.markdown(q["Question_Text"])

visual_html = render_visual(q)

if visual_html:
    st.iframe(visual_html, height=300)

option_labels = {
    option["Option_ID"]: option.get(
        "Option_Text",
        option.get("Text", option["Option_ID"])
    )
    for option in q["Options"]
}

option_ids = list(option_labels.keys())

# Display full option text to the student, but keep Option_ID
# internally for Final_Response, scoring, and reporting.
display_to_id = {
    option_labels[option_id]: option_id
    for option_id in option_ids
}

existing = q.get("Final_Response")
if isinstance(existing, str):
    existing = [existing]
elif existing is None:
    existing = []

existing_display = [
    option_labels[x]
    for x in existing
    if x in option_labels
]

display_options = [
    option_labels[option_id]
    for option_id in option_ids
]

if q.get("Response_Type") == "Multi":
    selected_display = st.multiselect(
        "Your answer",
        display_options,
        default=[
            x for x in existing_display
            if x in display_options
        ],
        key=f"answer_multi_{q['Question_ID']}",
    )

    selected = [
        display_to_id[x]
        for x in selected_display
    ]

else:
    default_index = (
        display_options.index(existing_display[0])
        if existing_display and existing_display[0] in display_options
        else None
    )

    selected_display = st.radio(
        "Your answer",
        display_options,
        index=default_index,
        key=f"answer_single_{q['Question_ID']}",
    )

    selected = (
        []
        if selected_display is None
        else [display_to_id[selected_display]]
    )

old_response = q.get("Final_Response")
old_ids = (
    old_response
    if isinstance(old_response, list)
    else ([old_response] if old_response else [])
)

if list(selected) != old_ids:
    now = datetime.now(timezone.utc).isoformat()
    if not q.get("First_Response_Timestamp"):
        q["First_Response_Timestamp"] = now
    if old_ids:
        q["Answer_Changed"] = True
    q["Final_Response_Timestamp"] = now
    q["Final_Response"] = list(selected)
    q["Answered"] = bool(selected)
    save_attempt(BASE, attempt)

st.divider()
answered = sum(bool(x.get("Final_Response")) for x in questions)
st.write(f"**Answered: {answered} / {len(questions)}**")

col1, col2, col3 = st.columns(3)

with col1:
    if current > 0 and st.button("← Previous"):
        attempt["Current_Question"] = current - 1
        save_attempt(BASE, attempt)
        st.rerun()

with col2:
    if current < len(questions) - 1 and st.button("Next →"):
        attempt["Current_Question"] = current + 1
        save_attempt(BASE, attempt)
        st.rerun()

with col3:
    if st.button("Submit Quiz", type="primary"):
        fresh = load_attempt(BASE, QUIZ_ID, sap_id)
        if fresh is None:
            st.error("Quiz attempt could not be found.")
            st.stop()
        submit_attempt(BASE, fresh, auto=is_expired(fresh))
        st.session_state.attempt = fresh
        st.rerun()
