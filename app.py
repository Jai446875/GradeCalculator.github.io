import streamlit as st

def calculate_attendance(absences):
    if absences < 0 or absences > 4:
        return None
    return max(0, 100 - (absences * 10))  # Attendance score calculation

def compute_class_standing(quiz, requirements, recitation):
    return (quiz * 0.40) + (requirements * 0.30) + (recitation * 0.30)

def compute_prelim_grade(absences, quiz, requirements, recitation, exam):
    attendance_score = calculate_attendance(absences)
    if attendance_score is None:
        return None
    class_standing = compute_class_standing(quiz, requirements, recitation)
    return (exam * 0.60) + (attendance_score * 0.10) + (class_standing * 0.30)

def grades_needed(prelim_grade, target):
    midterm_needed = (target - (prelim_grade * 0.20)) / 0.80
    final_needed = (target - (prelim_grade * 0.20)) / 0.80
    return midterm_needed, final_needed

def calculate_grades(prelim_grade):
    # Constants
    max_score = 100.0

    # Initialize variables
    req_midterm = 0.0
    req_final = 0.0
    dean_midterm = 0.0
    dean_finals = 0.0
    pass_message = False
    difficult_message = False
    dean_message = False

    if prelim_grade >= 0 and prelim_grade <= 100:
        try:
            temp_prelim = round(prelim_grade * 0.20, 2)

            counter = 0
            while counter == 0:  # Using brute force to find midterm and finals
                temp_midterm = round(max_score * 0.30, 2)
                temp_final = round(max_score * 0.50, 2)

                temp_grade = round(temp_midterm + temp_final + temp_prelim, 2)

                if temp_grade >= 75.0:
                    req_midterm = round(temp_midterm / 0.30, 2)
                    req_final = round(temp_final / 0.50, 2)
                    counter = 1
                elif temp_grade < 75.0:
                    req_midterm = round(temp_midterm / 0.30, 2)
                    req_final = round(temp_final / 0.50, 2)
                    counter = 1
                elif temp_grade >= 90.0:
                    req_midterm = round(temp_midterm / 0.30, 2)
                    req_final = round(temp_final / 0.50, 2)
                    dean_midterm = req_midterm
                    dean_finals = req_final

                    max_score -= 0.01
                    continue
                else:
                    max_score -= 0.01

            if req_midterm <= 75 and req_final <= 75:
                pass_message = True
                difficult_message = False
                dean_message = True
            else:
                difficult_message = True
                pass_message = False
                dean_message = True

        except ValueError:
            st.error("Please enter a valid number.")
    else:
        st.warning("Please enter a number between 0 and 100.")

    return req_midterm, req_final, dean_midterm, dean_finals, pass_message, difficult_message, dean_message


# Streamlit UI
st.title("Prelim Grade Calculator")

# User Input
absences = st.number_input("Number of Consecutive Absences (0-4):", min_value=0, max_value=4, value=0)
quiz = st.number_input("Quiz Score (0-100):", min_value=0, max_value=100, value=0)
requirements = st.number_input("Requirements Grade (0-100):", min_value=0, max_value=100, value=0)
recitation = st.number_input("Recitation Score (0-100):", min_value=0, max_value=100, value=0)
exam = st.number_input("Prelim Exam Score (0-100):", min_value=0, max_value=100, value=0)

if st.button("Calculate Final Grade"):
    prelim_grade = compute_prelim_grade(absences, quiz, requirements, recitation, exam)
    
    if prelim_grade is not None:
        st.write(f"Your Prelim Grade is: {prelim_grade:.2f}")
        if prelim_grade < 75:
            midterm, final = grades_needed(prelim_grade, 75)
            st.write(f"To pass with 75%, you need a Midterm grade of {midterm:.2f} and a Final grade of {final:.2f}.")
            midterm_dean, final_dean = grades_needed(prelim_grade, 90)
            st.write(f"To achieve 90%, you need a Midterm grade of {midterm_dean:.2f} and a Final grade of {final_dean:.2f}.")
        else:
            st.write("You've passed! Keep it up!")
    else:
        st.write("Invalid number of absences.")

