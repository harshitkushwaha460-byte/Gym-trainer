import streamlit as st
from sarvamai import SarvamAI

from rag import FitnessRAG

from fitness_utils import *



st.set_page_config(

    page_title="AI Personal Fitness Trainer",

    page_icon="💪",

    layout="wide"

)

client = SarvamAI(
    api_subscription_key=st.secrets["SARVAM_API_KEY"]
)





@st.cache_resource

def load_rag():

    return FitnessRAG()

rag = load_rag()



st.title("💪 Personal Fitness Trainer")

st.write(

    "Hi ,what's in your mind?"

)



st.sidebar.header("User Profile")

age = st.sidebar.slider(

    "Age",

    15,

    80,

    22

)

gender = st.sidebar.selectbox(

    "Gender",

    [

        "Male",

        "Female"

    ]

)

height = st.sidebar.number_input(

    "Height (cm)",

    100,

    250,

    170

)

weight = st.sidebar.number_input(

    "Weight (kg)",

    30,

    200,

    70

)

goal = st.sidebar.selectbox(

    "Goal",

    [

        "Weight Loss",

        "Muscle Gain",

        "Maintain"

    ]

)

experience = st.sidebar.selectbox(

    "Experience",

    [

        "Beginner",

        "Intermediate",

        "Advanced"

    ]

)

activity = st.sidebar.selectbox(

    "Activity Level",

    [

        "Sedentary",

        "Lightly Active",

        "Moderately Active",

        "Very Active",

        "Athlete"

    ]

)

diet = st.sidebar.selectbox(

    "Diet",

    [

        "Veg",

        "Non Veg"

    ]

)


# CALCULATIONS


bmi = calculate_bmi(

    weight,

    height

)

category = bmi_category(

    bmi

)

bmr = calculate_bmr(

    weight,

    height,

    age,

    gender

)

tdee = calculate_tdee(

    bmr,

    activity

)

calories = daily_calories(

    goal,

    tdee

)

protein = protein_requirement(

    weight,

    goal

)

fat = fat_requirement(

    weight

)

carbs = carb_requirement(

    calories,

    protein,

    fat

)

water = water_requirement(

    weight

)



st.sidebar.markdown("---")

st.sidebar.subheader("Health Summary")

st.sidebar.write(f"**BMI:** {bmi}")

st.sidebar.write(f"**Category:** {category}")

st.sidebar.write(f"**BMR:** {bmr} kcal")

st.sidebar.write(f"**TDEE:** {tdee} kcal")

st.sidebar.write(f"**Calories:** {calories} kcal")

st.sidebar.write(f"**Protein:** {protein} g")

st.sidebar.write(f"**Carbs:** {carbs} g")

st.sidebar.write(f"**Fat:** {fat} g")

st.sidebar.write(f"**Water:** {water} L")

# -----------------------------
# CHAT HISTORY
# -----------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])



query = st.chat_input(

    "Ask your fitness question..."

)

# USER PROFILE


profile = f"""
Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
Goal: {goal}
Experience: {experience}
Activity Level: {activity}
Diet: {diet}

Health Summary:
BMI: {bmi} ({category})
BMR: {bmr}
TDEE: {tdee}
Daily Calories: {calories}
Protein: {protein} g
Carbs: {carbs} g
Fat: {fat} g
Water: {water} L
"""



def ask_sarvam(question):

    # Retrieve context from all PDFs
    context = rag.get_context(question)

    # Last few messages for conversation memory
    history = ""

    for msg in st.session_state.messages[-6:]:

        history += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are an expert AI Personal Fitness Trainer.

You help users with:

• Workout Plans
• Exercise Guidance
• Diet Planning
• Nutrition
• Muscle Gain
• Fat Loss
• Supplements
• Injuries
• Cardio
• Recovery
• Motivation
• BMI
• BMR
• Calories
• Protein

==================================

USER PROFILE

{profile}

==================================

FITNESS KNOWLEDGE BASE

{context}

==================================

CHAT HISTORY

{history}

==================================

USER QUESTION

{question}

==================================

RULES

1. First use the knowledge base.
2. If the knowledge base is incomplete, use reliable fitness knowledge.
3. Personalize every answer using the user's profile.
4. Keep answers well formatted.
5. Use headings and bullet points.
6. Recommend diet whenever appropriate.
7. Mention calories/macros if useful.
8. Never make up facts.
9.Give short answer stick to the questions,
10. If the answer isn't in the knowledge base, clearly mention that you're using general fitness knowledge.

Answer:
"""
    response = client.chat.completions(
    model="sarvam-105b",
    messages=[
        {
            "role": "system",
            "content": "You are an expert AI Personal Fitness Trainer."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    return response.choices[0].message.content

# CHAT


if query:

    # Show user message
    st.chat_message("user").markdown(query)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.spinner("Thinking..."):

        try:

            answer = ask_sarvam(query)

        except Exception as e:

            answer = f"Error: {e}"

    st.chat_message("assistant").markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
