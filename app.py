from flask import Flask, request, render_template

app = Flask(__name__)

# Simple question structure for MBTI dimensions
questions = [
    {"text": "Do you prefer spending time alone rather than with groups?", "dimension": "I-E"},
    {"text": "Do you rely more on facts than intuition?", "dimension": "S-N"},
    {"text": "Do you make decisions based on logic rather than emotions?", "dimension": "T-F"},
    {"text": "Do you prefer structured plans over spontaneity?", "dimension": "J-P"}
]

@app.route('/')
def home():
    return render_template('index.html', questions=questions)

@app.route('/result', methods=['POST'])
def result():
    responses = request.form
    personality_scores = {"I": 0, "E": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    # Analyze user responses and score dimensions
    for i, question in enumerate(questions):
        dimension = question["dimension"]

        # Ensure dimension is valid (e.g., "I-E")
        if len(dimension) == 3 and '-' in dimension:
            choice = responses.get(f"q{i}")
            if choice == "Yes":
                personality_scores[dimension[0]] += 1
            else:
                personality_scores[dimension[2]] += 1

    # Determine MBTI type based on scores
    mbti_type = (
        "I" if personality_scores["I"] >= personality_scores["E"] else "E"
    ) + (
        "S" if personality_scores["S"] >= personality_scores["N"] else "N"
    ) + (
        "T" if personality_scores["T"] >= personality_scores["F"] else "F"
    ) + (
        "J" if personality_scores["J"] >= personality_scores["P"] else "P"
    )

    return render_template('result.html', mbti_type=mbti_type)

if __name__ == "__main__":
    app.run(debug=True)
