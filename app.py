from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
    


def index():
    # Initialize variables
    prelim_grade = 0.00
    req_midterm = 0.00
    req_final = 0.00
    temp_prelim = 0.00
    dean_midterm = 0.00
    dean_finals = 0.00
    max = 100.0

    temp_grade2 = 0.00
    temp_midtermLower = 0.00
    temp_finalLower = 0.00

    pass_message = False
    difficult_message = False
    dean_message = False
    invalid_number = False

    
    

    if request.method == 'POST':

        # Get the prelim grade from the form
        prelim_grade = request.form.get('txtPrelim')
        


        if prelim_grade.isdigit():

            prelim_grade = float(prelim_grade) 

            if prelim_grade >= 0 and prelim_grade <= 100:    

                try:

                    temp_prelim = round(prelim_grade * 0.20,2)


                    counter = 0
                        
                    while counter == 0: #using brute force to find midterm and finals based on grade composition midterm: 30% and finals: 50%
                        temp_midterm = round(max * 0.30,2)
                        temp_final = round(max * 0.50,2)

                        temp_grade = round(temp_midterm + temp_final,2)
                        temp_grade = round(temp_grade + temp_prelim,2)

                        if temp_grade == 75.0 and max >= 0:
                            req_midterm = round(temp_midterm / 0.30,2)
                            req_final = round(temp_final / 0.50, 2)
                                
                            counter = 1  
                        elif temp_grade < 75.0 and max >= 0:
                            #print(temp_grade2)

                            #print(temp_midterm)
                            #print(temp_midtermLower)
                            req_midterm = round(temp_midtermLower / 0.30,2)
                            req_final = round(temp_finalLower / 0.50, 2)

                            counter = 1  
                        elif temp_grade >= 90.0 and max >= 0:
                            req_midterm = round(temp_midterm / 0.30,2)
                            req_final = round(temp_final / 0.50, 2)
                            
                            dean_midterm = req_midterm
                            dean_finals = req_midterm

                            max = max - 0.01

                            continue 

                        else:
                            max = max - 0.01
                            
                        #this is to get the value before < 75
                        temp_grade2 = temp_grade 
                        temp_midtermLower = temp_midterm
                        temp_finalLower = temp_final
                        #-----------------------------------

                        if req_midterm <= 75 and req_final <= 75:
                            pass_message = True 
                            difficult_message = False 
                            dean_message = True
                        else:
                            difficult_message = True  
                            pass_message = False
                            dean_message = True
                        
                except ValueError:
                    return "Please enter a valid number."
            else:
               invalid_number = True     
        else:
            invalid_number = True

    return render_template('index.html', prelim_grade=prelim_grade, req_midterm=req_midterm, req_final=req_final,dean_midterm=dean_midterm,dean_finals=dean_finals,pass_message=pass_message, difficult_message=difficult_message, dean_message = dean_message,invalid_number=invalid_number)
    
if __name__ == "__main__":
    app.run(debug=True)