import sqlite3
from flask import Flask, request, jsonify


# --- Flask App ---
app = Flask(__name__)

# --- API Endpoints ---
@app.route('/')
def hello_world():
    return 'The High Score Server is alive!'

# Endpoint to GET the top 10 scores
@app.route('/scores', methods=['GET'])
def get_scores():
    conn = sqlite3.connect('./data/highscores.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, score FROM scores ORDER BY score DESC LIMIT 10')
    scores = cursor.fetchall()
    conn.close()
    # Convert list of tuples to list of dictionaries for JSON
    scores_list = [{'name': name, 'score': score} for name, score in scores]
    return jsonify(scores_list)

# Endpoint to POST a new score
@app.route('/scores', methods=['POST'])
def add_score():
    data = request.get_json()
    name = data['name']
    score = data['score']
    
    conn = sqlite3.connect('./data/highscores.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Score added successfully!'}), 201

# --- Main Execution ---
if __name__ == '__main__':
    init_db() # Ensure the database and table exist when the server starts
    app.run(debug=True)