import streamlit as st
import time

from database.database import add_study_session


def show_pomodoro():

    st.header("⏱️ Pomodoro Timer")

    st.write(
        "Focus deeply, take breaks, and track your study time."
    )

    st.divider()

    # -------------------------
    # SESSION SETTINGS
    # -------------------------

    col1, col2 = st.columns(2)

    with col1:

        study_minutes = st.number_input(
            "Study Duration (minutes)",
            min_value=1,
            max_value=120,
            value=25
        )

    with col2:

        break_minutes = st.number_input(
            "Break Duration (minutes)",
            min_value=1,
            max_value=30,
            value=5
        )

    st.divider()

    # -------------------------
    # SESSION STATE
    # -------------------------

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False

    if "timer_type" not in st.session_state:
        st.session_state.timer_type = "Study"

    if "remaining_seconds" not in st.session_state:
        st.session_state.remaining_seconds = study_minutes * 60

    # -------------------------
    # TIMER
    # -------------------------

    if st.session_state.timer_type == "Study":

        st.subheader("📚 Study Session")

    else:

        st.subheader("☕ Break Time")

    minutes = st.session_state.remaining_seconds // 60
    seconds = st.session_state.remaining_seconds % 60

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:70px;
            font-weight:bold;
            padding:30px;
        ">
        {minutes:02d}:{seconds:02d}
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # BUTTONS
    # -------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        if not st.session_state.timer_running:

            if st.button(
                "▶️ Start",
                use_container_width=True
            ):

                st.session_state.timer_running = True
                st.rerun()

    with col2:

        if st.button(
            "🔄 Reset",
            use_container_width=True
        ):

            st.session_state.timer_running = False
            st.session_state.timer_type = "Study"
            st.session_state.remaining_seconds = (
                study_minutes * 60
            )

            st.rerun()

    with col3:

        if st.button(
            "⏭️ Skip",
            use_container_width=True
        ):

            if st.session_state.timer_type == "Study":

                st.session_state.timer_type = "Break"
                st.session_state.remaining_seconds = (
                    break_minutes * 60
                )

            else:

                st.session_state.timer_type = "Study"
                st.session_state.remaining_seconds = (
                    study_minutes * 60
                )

            st.session_state.timer_running = False

            st.rerun()

    # -------------------------
    # RUN TIMER
    # -------------------------

    if st.session_state.timer_running:

        if st.session_state.remaining_seconds > 0:

            time.sleep(1)

            st.session_state.remaining_seconds -= 1

            st.rerun()

        else:

            st.session_state.timer_running = False

            if st.session_state.timer_type == "Study":

                add_study_session(
                    study_minutes
                )

                st.success(
                    "🎉 Study session completed!"
                )

                st.session_state.timer_type = "Break"

                st.session_state.remaining_seconds = (
                    break_minutes * 60
                )

            else:

                st.success(
                    "☕ Break finished! Time to study!"
                )

                st.session_state.timer_type = "Study"

                st.session_state.remaining_seconds = (
                    study_minutes * 60
                )

            st.rerun()