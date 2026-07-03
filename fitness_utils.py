import random


# -----------------------------
# BMI
# -----------------------------
def calculate_bmi(weight, height_cm):

    height = height_cm / 100

    bmi = weight / (height ** 2)

    return round(bmi, 2)


def bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


# -----------------------------
# BMR
# -----------------------------
def calculate_bmr(weight, height, age, gender):

    if gender.lower() == "male":

        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )

    else:

        bmr = (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

    return round(bmr)


# -----------------------------
# TDEE
# -----------------------------
def calculate_tdee(bmr, activity):

    factors = {

        "Sedentary": 1.2,

        "Lightly Active": 1.375,

        "Moderately Active": 1.55,

        "Very Active": 1.725,

        "Athlete": 1.9

    }

    return round(
        bmr * factors.get(activity, 1.2)
    )


# -----------------------------
# Calories
# -----------------------------
def daily_calories(goal, tdee):

    goal = goal.lower()

    if goal == "weight loss":

        return tdee - 500

    elif goal == "muscle gain":

        return tdee + 300

    else:

        return tdee


# -----------------------------
# Protein
# -----------------------------
def protein_requirement(weight, goal):

    goal = goal.lower()

    if goal == "muscle gain":

        return round(weight * 2.2)

    elif goal == "weight loss":

        return round(weight * 2)

    else:

        return round(weight * 1.6)


# -----------------------------
# Fat
# -----------------------------
def fat_requirement(weight):

    return round(weight * 0.8)


# -----------------------------
# Carbs
# -----------------------------
def carb_requirement(calories, protein, fat):

    protein_cal = protein * 4

    fat_cal = fat * 9

    carbs = (
        calories
        - protein_cal
        - fat_cal
    ) / 4

    return round(carbs)


# -----------------------------
# Water
# -----------------------------
def water_requirement(weight):

    return round(weight * 0.035, 1)


# -----------------------------
# Workout Recommendation
# -----------------------------
def workout_plan(goal, experience):

    goal = goal.lower()

    experience = experience.lower()

    if goal == "weight loss":

        if experience == "beginner":

            return """
• 4 Days Full Body
• 30 min Cardio
• 10k Steps
"""

        elif experience == "intermediate":

            return """
• Push Pull Legs
• HIIT 20 min
• Core Training
"""

        else:

            return """
• 6 Day Split
• HIIT
• Strength + Cardio
"""

    elif goal == "muscle gain":

        if experience == "beginner":

            return """
• Full Body
• Progressive Overload
• Compound Exercises
"""

        elif experience == "intermediate":

            return """
• Push Pull Legs
• Heavy Compound Lifts
"""

        else:

            return """
• Advanced PPL
• High Volume
• Strength Focus
"""

    return """
• 3 Day Workout
• Walking
• Mobility
"""


# -----------------------------
# Diet Suggestion
# -----------------------------
def diet_plan(goal, diet):

    diet = diet.lower()

    if diet == "veg":

        if goal.lower() == "muscle gain":

            return """
Breakfast:
Paneer + Oats

Lunch:
Rice + Dal + Paneer

Snack:
Protein Shake

Dinner:
Chapati + Soybean
"""

        else:

            return """
Breakfast:
Oats

Lunch:
Dal + Rice

Snack:
Fruit

Dinner:
Vegetables + Roti
"""

    else:

        if goal.lower() == "muscle gain":

            return """
Breakfast:
Eggs

Lunch:
Chicken + Rice

Snack:
Whey

Dinner:
Fish + Chapati
"""

        else:

            return """
Breakfast:
Egg Whites

Lunch:
Chicken Salad

Snack:
Fruit

Dinner:
Grilled Fish
"""


# -----------------------------
# Motivation
# -----------------------------
def motivation():

    quotes = [

        "Discipline beats motivation.",

        "One workout at a time.",

        "Progress, not perfection.",

        "Consistency creates results.",

        "Future you will thank you.",

        "Every rep makes you stronger.",

        "Your only competition is yourself.",

        "Train hard. Stay humble.",

        "Small steps every day.",

        "Never skip two workouts in a row."

    ]

    return random.choice(quotes)