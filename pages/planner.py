import streamlit as st
from datetime import date

from database.database import (
    add_task,
    get_tasks,
    complete_task,
    delete_task
)


def show_planner():

    st.header("📅 Study Planner")

    st.write("Plan your study sessions and track your progress.")

    st.divider()

    st.subheader("➕ Add Study Task")

    with st.form("study_task_form"):

        subject = st.text_input(
            "Subject",
            placeholder="Example: Data Structures"
        )

        topic = st.text_input(
            "Topic",
            placeholder="Example: Binary Trees"
        )

        study_date = st.date_input(
            "Study Date",
            value=date.today()
        )

        duration = st.number_input(
            "Study Duration (minutes)",
            min_value=15,
            max_value=600,
            value=60,
            step=15
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        submitted = st.form_submit_button(
            "Add Task 🚀"
        )

        if submitted:

            if not subject or not topic:
                st.error("Please enter both subject and topic.")

            else:

                add_task(
                    subject,
                    topic,
                    study_date.strftime("%Y-%m-%d"),
                    duration,
                    priority
                )

                st.success("Study task added successfully! 🎉")

                st.rerun()

    st.divider()

    st.subheader("📚 Your Study Plan")

    tasks = get_tasks()

    if not tasks:

        st.info(
            "No study tasks yet. Add your first task above!"
        )

    else:

        for task in tasks:

            task_id = task[0]
            subject = task[1]
            topic = task[2]
            study_date = task[3]
            duration = task[4]
            priority = task[5]
            completed = task[6]

            with st.container(border=True):

                st.markdown(
                    f"### {'✅' if completed else '📖'} "
                    f"{subject} — {topic}"
                )

                st.write(
                    f"📅 {study_date} | "
                    f"⏱️ {duration} minutes | "
                    f"🔥 {priority} priority"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if not completed:

                        if st.button(
                            "Complete",
                            key=f"complete_{task_id}"
                        ):

                            complete_task(task_id)
                            st.rerun()

                    else:

                        st.success("Completed ✅")

                with col2:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_{task_id}"
                    ):

                        delete_task(task_id)
                        st.rerun()