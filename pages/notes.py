import streamlit as st

from database.database import (
    add_note,
    get_notes,
    delete_note
)


def show_notes():

    st.header("📝 My Notes")

    st.write(
        "Create, store and review your study notes."
    )

    st.divider()

    # -------------------------
    # ADD NOTE
    # -------------------------

    st.subheader("➕ Create New Note")

    with st.form("note_form"):

        title = st.text_input(
            "Note Title",
            placeholder="Example: Binary Trees"
        )

        subject = st.text_input(
            "Subject",
            placeholder="Example: Data Structures"
        )

        content = st.text_area(
            "Your Notes",
            placeholder="Write your notes here...",
            height=250
        )

        submitted = st.form_submit_button(
            "💾 Save Note"
        )

        if submitted:

            if not title or not subject or not content:

                st.error(
                    "Please fill in all fields."
                )

            else:

                add_note(
                    title,
                    subject,
                    content
                )

                st.success(
                    "Note saved successfully! 🎉"
                )

                st.rerun()

    st.divider()

    # -------------------------
    # DISPLAY NOTES
    # -------------------------

    st.subheader("📚 Saved Notes")

    notes = get_notes()

    if not notes:

        st.info(
            "No notes yet. Create your first note above!"
        )

    else:

        for note in notes:

            note_id = note[0]
            title = note[1]
            subject = note[2]
            content = note[3]
            created_at = note[4]

            with st.expander(
                f"📖 {title} — {subject}"
            ):

                st.caption(
                    f"Created: {created_at}"
                )

                st.write(content)

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_note_{note_id}"
                ):

                    delete_note(note_id)

                    st.success(
                        "Note deleted."
                    )

                    st.rerun()