import streamlit as st
import random

# Custom CSS for UX/colors
st.markdown("""
<style>
.main {
    background-color: #f7fbff;
    padding: 20px;
    border-radius: 10px;
}
.stButton>button {
    background-color: #3e7cb1;
    color: white;
    font-weight: 600;
    border-radius: 10px;
    margin-top: 12px;
    padding: 8px 24px;
}
.stRadio [role="radiogroup"] > label {
    background: #e8f0fe;
    margin-bottom: 8px;
    padding: 5px 12px 7px 10px;
    border-radius: 8px;
    border: 1.5px solid #b2dafa;
    transition: background .2s;
}
.stRadio [role="radiogroup"] > label[data-selected="true"] {
    background: #3e7cb1;
    color: #fff;
    border: 1.5px solid #32618a;
}
</style>
""", unsafe_allow_html=True)


# 20+ Science invention questions
ALL_QUESTIONS = [
    {"question": "Who invented the light bulb?", "options": ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "James Watt"], "answer": "Thomas Edison"},
    {"question": "Who invented the telephone?", "options": ["Michael Faraday", "Guglielmo Marconi", "Alexander Graham Bell", "Tim Berners-Lee"], "answer": "Alexander Graham Bell"},
    {"question": "Who is credited with inventing the World Wide Web?", "options": ["Bill Gates", "Steve Jobs", "Tim Berners-Lee", "Larry Page"], "answer": "Tim Berners-Lee"},
    {"question": "Who developed the theory of relativity?", "options": ["Isaac Newton", "Albert Einstein", "Max Planck", "Marie Curie"], "answer": "Albert Einstein"},
    {"question": "Who invented the first practical telephone?", "options": ["Alexander Graham Bell", "Elisha Gray", "Charles Babbage", "James Watt"], "answer": "Alexander Graham Bell"},
    {"question": "Who invented the radio?", "options": ["Guglielmo Marconi", "Alexander Graham Bell", "Nikola Tesla", "Thomas Edison"], "answer": "Guglielmo Marconi"},
    {"question": "Who invented the airplane?", "options": ["Wright Brothers", "Louis Pasteur", "Alexander Graham Bell", "Nikola Tesla"], "answer": "Wright Brothers"},
    {"question": "Who invented the printing press?", "options": ["Johannes Gutenberg", "Alexander Graham Bell", "Thomas Edison", "James Watt"], "answer": "Johannes Gutenberg"},
    {"question": "Who invented the steam engine?", "options": ["James Watt", "Isaac Newton", "Nikola Tesla", "Thomas Edison"], "answer": "James Watt"},
    {"question": "Who invented the polio vaccine?", "options": ["Jonas Salk", "Louis Pasteur", "Alexander Fleming", "Edward Jenner"], "answer": "Jonas Salk"},
    {"question": "Who invented the gasoline-powered car?", "options": ["Karl Benz", "Henry Ford", "Nikola Tesla", "James Watt"], "answer": "Karl Benz"},
    {"question": "Who invented the dynamo?", "options": ["Michael Faraday", "Nikola Tesla", "Thomas Edison", "James Watt"], "answer": "Michael Faraday"},
    {"question": "Who invented the first programmable computer?", "options": ["Alan Turing", "Charles Babbage", "John von Neumann", "Konrad Zuse"], "answer": "Konrad Zuse"},
    {"question": "Who invented the laser?", "options": ["Theodore Maiman", "Albert Einstein", "Nikola Tesla", "Isaac Newton"], "answer": "Theodore Maiman"},
    {"question": "Who invented the thermometer?", "options": ["Galileo Galilei", "Isaac Newton", "Benjamin Franklin", "Anders Celsius"], "answer": "Galileo Galilei"},
    {"question": "Who invented the telescope?", "options": ["Galileo Galilei", "Isaac Newton", "Hans Lippershey", "Nicolaus Copernicus"], "answer": "Hans Lippershey"},
    {"question": "Who invented the refrigerator?", "options": ["Carl von Linde", "Thomas Edison", "Alexander Graham Bell", "James Watt"], "answer": "Carl von Linde"},
    {"question": "Who invented the satellite?", "options": ["Konstantin Tsiolkovsky", "Nikola Tesla", "Robert Goddard", "Wernher von Braun"], "answer": "Konstantin Tsiolkovsky"},
    {"question": "Who invented the first digital camera?", "options": ["Steven Sasson", "Kodak", "Thomas Edison", "Nikola Tesla"], "answer": "Steven Sasson"},
    {"question": "Who invented penicillin?", "options": ["Alexander Fleming", "Louis Pasteur", "Marie Curie", "Edward Jenner"], "answer": "Alexander Fleming"},
]

NUM_QUESTIONS_PER_QUIZ = 10

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "show_score" not in st.session_state:
    st.session_state.show_score = False
if "selected_questions" not in st.session_state:
    # Randomly pick 10 questions on start/new session
    st.session_state.selected_questions = random.sample(ALL_QUESTIONS, NUM_QUESTIONS_PER_QUIZ)


def show_question():
    qn = st.session_state.selected_questions[st.session_state.current_index]
    st.subheader(f"Question {st.session_state.current_index + 1} of {NUM_QUESTIONS_PER_QUIZ}")
    st.write(qn["question"])

    selected = st.radio(
        "Select your answer below:",
        qn["options"],
        key=f"radio_{st.session_state.current_index}",
    )
    if st.button("Submit", key=f"submit_{st.session_state.current_index}"):
        if selected == qn["answer"]:
            st.session_state.score += 1
            st.success("Correct! 🎉")
        else:
            st.error(f"Wrong! The correct answer was: {qn['answer']}")

        if st.session_state.current_index + 1 < NUM_QUESTIONS_PER_QUIZ:
            st.session_state.current_index += 1
            st.rerun()
        else:
            st.session_state.show_score = True
            st.rerun()


def show_final_score():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Quiz Completed! 🏆")
    st.write(f"Your final score is: {st.session_state.score} out of {NUM_QUESTIONS_PER_QUIZ}")
    if st.session_state.score == NUM_QUESTIONS_PER_QUIZ:
        st.balloons()
        st.success("🎉 Congratulations on a perfect score! 🎉")
    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.current_index = 0
        st.session_state.show_score = False
        st.session_state.selected_questions = random.sample(ALL_QUESTIONS, NUM_QUESTIONS_PER_QUIZ)
        st.rerun()


st.title("🔬 Science Inventions Quiz")
st.markdown("<div class='main'>", unsafe_allow_html=True)

if not st.session_state.show_score:
    show_question()
else:
    show_final_score()

st.markdown("</div>", unsafe_allow_html=True)
