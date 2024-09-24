from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the grade calculation
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Retrieve the form data from the request
        absences = int(request.form['attendance_absences'])
        quiz = float(request.form['quiz_score'])
        requirements = float(request.form['requirements_grade'])
        recitation = float(request.form['recitation_score'])
        exam = float(request.form['prelim_exam_score'])

        # Define the helper functions for grade calculation
        def calculate_attendance(absences):
            if absences < 0 or absences > 4:
                return None
            if absences >= 4:
                return "FAILED"
            return max(0, 100 - (absences * 10))

        def compute_class_standing(quiz, requirements, recitation):
            return (quiz * 0.40) + (requirements * 0.30) + (recitation * 0.30)

        def compute_prelim_grade(absences, quiz, requirements, recitation, exam):
            attendance_score = calculate_attendance(absences)
            if isinstance(attendance_score, str):
                return attendance_score
            class_standing = compute_class_standing(quiz, requirements, recitation)
            return (exam * 0.60) + (attendance_score * 0.10) + (class_standing * 0.30)

        def grades_needed(prelim_grade, target):
            midterm_needed = (target - (prelim_grade * 0.20)) / 0.80
            final_needed = (target - (prelim_grade * 0.20)) / 0.80
            return midterm_needed, final_needed

        # Calculate the prelim grade
        prelim_grade = compute_prelim_grade(absences, quiz, requirements, recitation, exam)

        # Prepare the output messages
        if isinstance(prelim_grade, str):
            return jsonify({"error": prelim_grade})

        output_message = f"Prelim Grade: {prelim_grade:.2f}"
        pass_midterm, pass_final = grades_needed(prelim_grade, 75)
        dean_midterm, dean_final = grades_needed(prelim_grade, 90)

        output_message += f"\nTo pass with 75%, you need a Midterm grade of {pass_midterm:.2f} and a Final grade of {pass_final:.2f}."
        output_message += f"\nTo achieve 90%, you need a Midterm grade of {dean_midterm:.2f} and a Final grade of {dean_final:.2f}."

        return jsonify({"result": output_message})

    except ValueError as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
