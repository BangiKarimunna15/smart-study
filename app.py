import streamlit as st
from database.database import (
    create_tables,
    get_total_study_minutes,
    get_total_sessions,
    get_completed_tasks,
    get_total_tasks,
    get_upcoming_tasks
)

st.set_page_config(
    page_title="Smart Study Companion",
    page_icon="📚",
    layout="wide"
)

create_tables()

st.title("📚 Smart Study Companion")
st.write("Your personal AI-powered study companion.")

st.sidebar.title("📚 Smart Study Companion")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📅 Study Planner",
        "📝 Notes",
        "⏱️ Pomodoro",
        "🧠 Quiz",
        "📊 Progress",
        "🤖 AI Assistant"
    ]
)

if page == "🏠 Dashboard":

    st.header("🏠 Dashboard")

    st.write(
        "Welcome back! Here's your study overview."
    )

    st.divider()

    # -------------------------
    # GET REAL DATA
    # -------------------------

    total_minutes = get_total_study_minutes()
    total_sessions = get_total_sessions()
    completed_tasks = get_completed_tasks()
    total_tasks = get_total_tasks()

    # -------------------------
    # CALCULATE PROGRESS
    # -------------------------

    if total_tasks > 0:

        completion_percentage = (
            completed_tasks / total_tasks
        ) * 100

    else:

        completion_percentage = 0

    # -------------------------
    # DASHBOARD METRICS
    # -------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "⏱️ Study Time",
            f"{total_minutes // 60}h "
            f"{total_minutes % 60}m"
        )

    with col2:

        st.metric(
            "📚 Study Sessions",
            total_sessions
        )

    with col3:

        st.metric(
            "✅ Completed Tasks",
            completed_tasks
        )

    with col4:

        st.metric(
            "📈 Completion",
            f"{completion_percentage:.0f}%"
        )

    st.divider()

    # -------------------------
    # PROGRESS BAR
    # -------------------------

    st.subheader("🎯 Overall Task Progress")

    st.progress(
        completion_percentage / 100
    )

    st.write(
        f"{completed_tasks} of "
        f"{total_tasks} tasks completed"
    )

    st.divider()

    # -------------------------
    # UPCOMING TASKS
    # -------------------------

    st.subheader("📅 Upcoming Study Tasks")

    upcoming_tasks = get_upcoming_tasks()

    if upcoming_tasks:

        for task in upcoming_tasks:

            subject = task[0]
            topic = task[1]
            study_date = task[2]
            duration = task[3]
            priority = task[4]

            with st.container(border=True):

                st.markdown(
                    f"### 📖 {subject} — {topic}"
                )

                st.write(
                    f"📅 {study_date}  |  "
                    f"⏱️ {duration} minutes  |  "
                    f"🔥 {priority} priority"
                )

    else:

        st.info(
            "No upcoming study tasks. "
            "Go to Study Planner and add one!"
        )

    st.divider()

    # -------------------------
    # MOTIVATION
    # -------------------------

    st.subheader("💡 Keep Going!")

    if completion_percentage == 100 and total_tasks > 0:

        st.success(
            "🎉 Amazing! You've completed "
            "all your study tasks!"
        )

    elif completion_percentage >= 75:

        st.success(
            "🔥 You're doing great! "
            "You're almost there!"
        )

    elif completion_percentage >= 50:

        st.info(
            "💪 You're halfway there. "
            "Keep pushing!"
        )

    else:

        st.info(
            "🌱 Every study session counts. "
            "Start small and stay consistent!"
        )
    


elif page == "📅 Study Planner":
    from pages.planner import show_planner
    show_planner()


elif page == "📝 Notes":
    from pages.notes import show_notes
    show_notes()
    


elif page == "⏱️ Pomodoro":
    from pages.pomodoro import show_pomodoro
    show_pomodoro()
    


elif page == "🧠 Quiz":
    from pages.quiz import show_quiz
    show_quiz()
    


elif page == "📊 Progress":
    from pages.progress import show_progress
    show_progress()
    


elif page == "🤖 AI Assistant":
    from pages.ai_assistant import show_ai_assistant
    show_ai_assistant()