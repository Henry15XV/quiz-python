from flask import Flask, request, render_template_string

app = Flask(name)

QUESTIONS = {
    "What is the capital of France?": "Paris",
    "What is 2 + 2?": "4",
    "Which planet is known as the Red Planet?": "Mars"
}

# (templates unchanged...)

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
