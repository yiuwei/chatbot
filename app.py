# Import required modules
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from flask import Flask, request, jsonify, render_template

# Download nltk resources
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Setup flask application
app = Flask(__name__)

# Initialize the NLTK tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load the training data from text.txt
with open('text.txt', 'r') as file:
    train_data = file.read().split('\n')

# Filter the text input with NLTK tools
def filtering(text):
    tokenize = word_tokenize(text.lower())
    filtered = [lemmatizer.lemmatize(letter) for letter in tokenize if letter.isalnum() and letter not in stop_words]
    return filtered

# Generate response by filtering sentences
def responses(input):
    user_tokens = filtering(input)
    word_overlap = 0
    gets_replies = []
    
    for obj, line in enumerate(train_data):
        if line.startswith("User: "):
            pattern = filtering(line[6:])
            overlap = len(set(user_tokens) & set(pattern))

            if overlap > word_overlap:
                word_overlap = overlap
                gets_replies = [train_data[obj + 1][5:]] if obj + 1 < len(train_data) and train_data[obj + 1].startswith("Bot: ") else []
            elif overlap == word_overlap and overlap > 0:
                if obj + 1 < len(train_data) and train_data[obj + 1].startswith("Bot: "):
                    gets_replies.append(train_data[obj + 1][5:])
   
    return gets_replies

# Display responses to queries 
def display_replies(responses):
    if len(responses) == 1:
        return responses[0]
    elif len(responses) > 1:
        join_responses = ' '.join(responses)
        return join_responses
    return "Please enter another query"

# Get route and return template 
@app.route('/')
def index():
    return render_template('index.html')

# Get route and post response
@app.route('/query', methods=['POST'])
def ask():
    user_input = request.form['message']
    gets_replies = responses(user_input)
    response = display_replies(gets_replies)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
