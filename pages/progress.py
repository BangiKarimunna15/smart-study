import streamlit as st
import pandas as pd

from database.database import (
    get_total_study_minutes,
    get_total_sessions,
    get_completed_tasks,
    get_total_tasks,
    get_daily_study_data,
    get_quiz_results
)


def show_progress():

    st.header("📊 Study Progress")

    st.write(
        "See how consistently you are studying and improving."
    )

    st.divider()

    # -------------------------
    # GET DATA
    # -------------------------

    total_minutes = get_total_study_minutes()
    total_sessions = get_total_sessions()
    completed_tasks = get_completed_tasks()
    total_tasks = get_total_tasks()

    # -------------------------
    # METRICS
    # -------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "⏱️ Study Time",
            f"{total_minutes // 60}h {total_minutes % 60}m"
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

        if total_tasks > 0:

            completion = (
                completed_tasks / total_tasks
            ) * 100

        else:

            completion = 0

        st.metric(
            "📈 Task Completion",
            f"{completion:.0f}%"
        )

    st.divider()

    # -------------------------
    # STUDY ACTIVITY
    # -------------------------

    st.subheader("📈 Daily Study Activity")

    daily_data = get_daily_study_data()

    if daily_data:

        df = pd.DataFrame(
            daily_data,
            columns=[
                "Date",
                "Study Minutes"
            ]
        )

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        df = df.set_index("Date")

        st.line_chart(
            df["Study Minutes"]
        )

    else:

        st.info(
            "Complete some Pomodoro sessions "
            "to see your study activity here."
        )

    st.divider()

    # -------------------------
    # QUIZ PERFORMANCE
    # -------------------------

    st.subheader("🧠 Quiz Performance")

    quiz_results = get_quiz_results()

    if quiz_results:

        quiz_data = []

        for result in quiz_results:

            subject = result[0]
            score = result[1]
            total = result[2]
            completed_at = result[3]

            percentage = (
                score / total
            ) * 100

            quiz_data.append({
                "Subject": subject,
                "Score": f"{score}/{total}",
                "Percentage": f"{percentage:.0f}%",
                "Date": completed_at
            })

        quiz_df = pd.DataFrame(
            quiz_data
        )

        st.dataframe(
            quiz_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Take a quiz to see your performance."
        )