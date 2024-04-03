from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import json
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import subprocess

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the intents data
with open("intents.json", "r") as file:
    intents = json.load(file)

# Preprocess the data
lemmatizer = WordNetLemmatizer()
stop_words = set(nltk.corpus.stopwords.words("english"))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum() and token not in stop_words]
    return " ".join(tokens)

patterns = []
responses = []
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(preprocess_text(pattern))
        responses.append(intent["responses"])

# Vectorize the patterns
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(patterns)

# Run the chatbot
def get_response(user_input):
    preprocessed_input = preprocess_text(user_input)

    # Check spelling and suggest correction
    corrected_input = str(TextBlob(preprocessed_input).correct())

    # Vectorize corrected user input
    X_user = vectorizer.transform([corrected_input])

    # Calculate similarity scores
    similarity_scores = cosine_similarity(X_user, X).flatten()

    # Find the most similar intent
    max_score_index = similarity_scores.argmax()

    # Check if similarity score is above a certain threshold
    if similarity_scores[max_score_index] > 0.5:
        response_options = responses[max_score_index]
        return random.choice(response_options)
    return "I do not understand... <br><br> Please select from following keywords:<br> - Gen Garage <br> - Leads <br> - Mission <br> - Achievements <br> - Gen Z <br> - Projects <br> - Notebook"

# Run Gunicorn server using subprocess
def run_gunicorn():
    command = [
        "gunicorn",            # Gunicorn command
        "-b", "0.0.0.0:8000",  # Bind address and port
        "app:app"             # Name of your Flask app object
    ]
    subprocess.run(command)

# Define Flask routes
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.json.get('message')
    elif request.method == 'GET':
        user_input = request.args.get('message')
    else:
        return "Method not allowed", 405

    if not user_input:
        return "No message provided", 400

    response = get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    run_gunicorn()
