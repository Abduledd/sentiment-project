import pickle
import numpy as np
from flask import Flask, request, jsonify
from keras.preprocessing.sequence import pad_sequences
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained LSTM model and Tokenizer
with open(r'C:\Users\User\Desktop\projects\Sentiment project\backend\lstm_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open(r'C:\Users\User\Desktop\projects\Sentiment project\backend\tokenizer.pkl', 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

# Preprocessing
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    tokens = word_tokenize(text.lower())  # Tokenize and lowercase
    tokens = [t for t in tokens if t.isalpha()]  # Remove non-alphabetic tokens
    tokens = [t for t in tokens if t not in stop_words]  # Remove stopwords
    return ' '.join(tokens)

@app.route('/api', methods=['POST'])
def predict_sentiment():
    try:
        # Get the phrase from the request
        data = request.get_json(force=True)
        phrase = data['phrase']

        # Preprocess the phrase
        processed_phrase = preprocess_text(phrase)

        # Tokenize and pad the input for the LSTM model
        sequence = tokenizer.texts_to_sequences([processed_phrase])
        input_data = pad_sequences(sequence, maxlen=28)  # Adjust maxlen as needed

        # Predict using the loaded model
        predicted_probabilities = loaded_model.predict(input_data)
        predicted_class = np.argmax(predicted_probabilities, axis=1)[0]

        # Return the predicted sentiment
        sentiment_mapping = {
            0: 'negative',
            1: 'somewhat negative',
            2: 'neutral',
            3: 'somewhat positive',
            4: 'positive'
        }
        predicted_sentiment = sentiment_mapping[predicted_class]

        return jsonify({'sentiment': predicted_sentiment})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
