import streamlit as st

from database.database import (
    save_quiz_result,
    get_quiz_results
)


QUESTIONS = [
    {
        "question": "Which data structure follows LIFO?",
        "options": [
            "Queue",
            "Stack",
            "Linked List",
            "Array"
        ],
        "answer": "Stack"
    },
    {
        "question": "What is the time complexity of binary search?",
        "options": [
            "O(n)",
            "O(n²)",
            "O(log n)",
            "O(1)"
        ],
        "answer": "O(log n)"
    },
    {
        "question": "Which language is primarily used for styling web pages?",
        "options": [
            "Python",
            "Java",
            "CSS",
            "SQL"
        ],
        "answer": "CSS"
    },
    {
        "question": "Which SQL command is used to retrieve data?",
        "options": [
            "INSERT",
            "SELECT",
            "DELETE",
            "UPDATE"
        ],
        "answer": "SELECT"
    },
    {
        "question": "Which OOP concept allows a class to acquire properties of another class?",
        "options": [
            "Encapsulation",
            "Polymorphism",
            "Inheritance",
            "Abstraction"
        ],
        "answer": "Inheritance"
    }
]


def show_quiz():

    st.header("🧠 Quiz Center")

    st.write(
        "Test your knowledge and track your scores."
    )

    st.divider()

    subject = st.selectbox(
        "Choose a subject",
        [
            "Data Structures",
            "Programming",
            "Database Management",
            "Web Development",
            "Computer Science"
        ]
    )

    st.divider()

    st.subheader("📝 Quiz")

    with st.form("quiz_form"):

        answers = []

        for i, question in enumerate(QUESTIONS):

            st.write(
                f"### Question {i + 1}"
            )

            st.write(
                question["question"]
            )

            answer = st.radio(
                "Choose your answer:",
                question["options"],
                key=f"question_{i}"
            )

            answers.append(answer)

        submitted = st.form_submit_button(
            "🎯 Submit Quiz"
        )

    if submitted:

        score = 0

        for i, question in enumerate(QUESTIONS):

            if answers[i] == question["answer"]:
                score += 1

        total = len(QUESTIONS)

        save_quiz_result(
            subject,
            score,
            total
        )

        percentage = (score / total) * 100

        st.divider()

        if percentage >= 80:

            st.success(
                f"🎉 Excellent! You scored "
                f"{score}/{total} ({percentage:.0f}%)"
            )

        elif percentage >= 50:

            st.warning(
                f"👍 Good effort! You scored "
                f"{score}/{total} ({percentage:.0f}%)"
            )

        else:

            st.error(
                f"📚 Keep practicing! You scored "
                f"{score}/{total} ({percentage:.0f}%)"
            )

    st.divider()

    st.subheader("📊 Previous Quiz Results")

    results = get_quiz_results()

    if not results:

        st.info(
            "No quiz attempts yet."
        )

    else:

        for result in results:

            subject = result[0]
            score = result[1]
            total = result[2]
            completed_at = result[3]

            st.write(
                f"📚 **{subject}** — "
                f"{score}/{total} "
                f"({(score / total) * 100:.0f}%)"
            )

            st.caption(
                f"Completed: {completed_at}"
            )