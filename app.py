import streamlit as st

def calculate_attendance(absences):
    if absences < 0 or absences > 4:
        return None
    return max(0, 100 - (absences * 10))  # Attendance score decreases by 10% for each absence

def compute_class_standing(quiz, requirements, recitation):
    return (quiz * 0.40) + (requirements * 0.30) + (recitation * 0.30)

def compute_prelim_grade(absences, quiz, requirements, recitation, exam):
    attendance_score = calculate_attendance(absences)
    if attendance_score is None:
        return None
    class_standing = compute_class_standing(quiz, requirements, recitation)
    return (exam * 0.60) + (attendance_score * 0.10) + (class_standing * 0.30)

def grades_needed(prelim_grade, target):
    # To calculate required Midterm and Final grades based on the target
    required_midterm = (target - (prelim_grade * 0.20)) / 0.30
    required_final = (target - (prelim_grade * 0.20)) / 0.50
    return required_midterm, required_final

# Streamlit UI
st.title("Preliminary Grade Calculator")

# Input fields
absences = st.number_input("Number of Consecutive Absences:", min_value=0, max_value=4, value=0)
quiz = st.number_input("Quiz Score:", min_value=0, max_value=100, value=0)
requirements = st.number_input("Requirements Grade:", min_value=0, max_value=100, value=0)
recitation = st.number_input("Recitation Score:", min_value=0, max_value=100, value=0)
exam = st.number_input("Prelim Exam Score:", min_value=0, max_value=100, value=0)

if st.button("Calculate Final Grade"):
    prelim_grade = compute_prelim_grade(absences, quiz, requirements, recitation, exam)
    
    if prelim_grade is not None:
        st.write(f"Your Prelim Grade is: {prelim_grade:.2f}")
        
        if prelim_grade < 75:
            midterm_pass, final_pass = grades_needed(prelim_grade, 75)
            midterm_dean, final_dean = grades_needed(prelim_grade, 90)
            st.write(f"To pass with 75%, you need a Midterm grade of {midterm_pass:.2f} and a Final grade of {final_pass:.2f}.")
            st.write(f"To achieve 90%, you need a Midterm grade of {midterm_dean:.2f} and a Final grade of {final_dean:.2f}.")
        else:
            st.write("You've passed! Keep it up!")
            midterm_dean, final_dean = grades_needed(prelim_grade, 90)
            st.write(f"To achieve 90%, you need a Midterm grade of {midterm_dean:.2f} and a Final grade of {final_dean:.2f}.")
    else:
        st.write("Invalid number of absences. Please enter between 0 and 4.")
