<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <title>Grade Calculator</title>
</head>

<body>
    <div class="container">
        <h1>Grade Calculator</h1>

  <form action="/" method="POST">
            <label for="txtPrelim">Enter Prelim Grade:</label>
            <input type="number" id="txtPrelim" name="txtPrelim" placeholder="0-100" min="0" max="100" required>
            <button type="submit" id="calculate">Calculate</button>
        </form>

  <div id="results">
            <p>Prelim Grade: <span id="displayPrelim">{{ prelim_grade }}</span></p>
            <p>Required Midterm Grade: <span id="reqMidterm">{{ req_midterm }}</span></p>
            <p>Required Final Grade: <span id="reqFinal">{{ req_final }}</span></p>
            <p id="passMessage" style="display: {{ 'block' if pass_message else 'none' }}">You have a chance to pass!</p>
            <p id="difficultMessage" style="display: {{ 'block' if difficult_message else 'none' }}">It is difficult to pass.</p>
            <p id="deanListersInfo" style="display: {{ 'block' if dean_message else 'none' }}">To be a Dean’s Lister, aim for <span id="deanMidterm">{{ dean_midterm }}</span> (midterm) and <span id="deanFinal">{{ dean_final }}</span> (finals).</p>
            <p id="invalidNumber" style="display: {{ 'block' if invalid_number else 'none' }}">Please input a valid number! Enter a value between 0 and 100.</p>
        </div>
    </div>
</body>
</html>


