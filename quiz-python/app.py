from flask import Flask, request, render_template_string
import os

app = Flask(name)

QUESTIONS = {
    "What is the capital of France?": "Paris",
    "What is 2 + 2?": "4",
    "Which planet is known as the Red Planet?": "Mars"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>CBT Quiz</title></head>
<body>
    <h1>Simple CBT Quiz</h1>
    <form action="/submit" method="POST">
        {% for question in questions %}
        <p>{{ loop.index }}. {{ question }}</p>
        <input type="text" name="q{{ loop.index }}" placeholder="Your answer" required><br>
        {% endfor %}
        <br><input type="submit" value="Submit">
    </form>
</body>
</html>
"""

RESULTS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Your Results</title></head>
<body>
    <h2>Your Results</h2>
    {% for result in results %}
    <p>{{ result }}</p>
    {% endfor %}
    <h3>Score: {{ score }} / {{ total }}</h3>
    <a href="/">Try Again</a>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, questions=QUESTIONS.keys())

@app.route('/submit', methods=['POST'])
def submit():
    score = 0
    results = []
    for i, (question, correct_answer) in enumerate(QUESTIONS.items(), start=1):
        user_answer = request.form.get(f'q{i}', '').strip()
        is_correct = user_answer.lower() == correct_answer.lower()
        if is_correct:
            score += 1
        results.append(f"Q{i}: {'✅ Correct' if is_correct else '❌ Wrong (Correct: ' + correct_answer + ')'}")
    
    return render_template_string(RESULTS_TEMPLATE, results=results, score=score, total=len(QUESTIONS))

if name == 'main':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
