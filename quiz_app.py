
import streamlit as st
import openai
import random

# Set your OpenAI API key
openai.api_key = st.secrets["api_secret"]


def generate_question(subject):
    # this function uses OpenAI API to generate a question based on the user's subject
    prompt = f"Generate a multiple-choice question for {subject} with 4 options."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
    )
    return response['choices'][0]['text']


def generate_quiz(subject, num_questions):
    # this function generates a quiz with a specified number of question that the user inters
    quiz = []
    for _ in range(num_questions):
        question = generate_question(subject)
        quiz.append({"question": question, "options": ["Option A", "Option B", "Option C", "Option D"]})
    return quiz


def main():

    # ----TITTLE----
    st.set_page_config(page_title="MCQ", page_icon="⁉", layout="wide")

    # ----HEADER SECTION----
    with st.container():
        st.subheader("TEST YOUR KNOWLEDGE WITH THE AI QUIZ 📖")
        st.title("AI MCQ Quiz")
        st.write("To start, click on the side bar and insert the subject of your liking and the number of questions")

    # ---SIDE BAR SECTION---
    with st.sidebar:
        # Allow the user to input their own subject and the number of questions
        user_subject = st.text_input("Enter a Subject:")
        num_questions = st.number_input("Enter the Number of Questions:", min_value=4, step=1, value=4)
        generate_button = st.button("Generate Quiz")

    # Initialize session state if not initialized
    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
        st.session_state.current_question_index = 0
        st.session_state.correct_answers_count = 0
        st.session_state.user_answer = None  # Initialize user_answer

    # Check if the user has entered a subject and clicked the generate button
    if user_subject and generate_button:
        # Generate a quiz based on the user-provided subject and number of questions
        st.session_state.quiz = generate_quiz(user_subject, num_questions)

    # Check if a quiz is generated and display questions
    if st.session_state.quiz:
        current_question_data = st.session_state.quiz[st.session_state.current_question_index]

        # Display the current question to the user
        st.write(f"Question {st.session_state.current_question_index + 1}: {current_question_data['question']}")

        # randomly chooses an option and asign it as the correct answer
        correct_answer_index = random.randint(0, 3)
        correct_answer = current_question_data['options'][correct_answer_index]

        # Display buttons with the correct answer in a random position
        random.shuffle(current_question_data['options'])

        # creating four buttons and dynamically labeled ,used a unique key for each button to avoid DuplicateWidgetID
        # error
        option_a = st.button(f"{current_question_data['options'][0]}##{st.session_state.current_question_index}")
        option_b = st.button(f"{current_question_data['options'][1]}##{st.session_state.current_question_index}")
        option_c = st.button(f"{current_question_data['options'][2]}##{st.session_state.current_question_index}")
        option_d = st.button(f"{current_question_data['options'][3]}##{st.session_state.current_question_index}")

        # Check if the user clicked any option and update the score
        if option_a or option_b or option_c or option_d:
            selected_answer = None
            if option_a and len(current_question_data['options']) > 0:
                selected_answer = current_question_data['options'][0]
            elif option_b and len(current_question_data['options']) > 1:
                selected_answer = current_question_data['options'][1]
            elif option_c and len(current_question_data['options']) > 2:
                selected_answer = current_question_data['options'][2]
            elif option_d and len(current_question_data['options']) > 3:
                selected_answer = current_question_data['options'][3]

            # Move to the next question
            st.session_state.current_question_index += 1

            # Check if the selected answer is correct and update the score
            if selected_answer == correct_answer:
                st.session_state.correct_answers_count += 1


if __name__ == "__main__":
    main()
