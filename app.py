from flask import Flask, request, jsonify, render_template
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os

app = Flask(__name__)

# Initialize model info
MODEL_ID = "jagadeepdandu/distilbert-imdb-sentiment"
model_loaded = False

# Load the tokenizer and model from Hugging Face directly
try:
    print(f"Loading model from Hugging Face: {MODEL_ID}")
    tokenizer = DistilBertTokenizer.from_pretrained(MODEL_ID)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_ID)
    model.eval()
    model_loaded = True
    print("Model loaded successfully from Hugging Face!")
except Exception as e:
    print(f"Error loading model from Hugging Face: {e}")
    # Fallback to base model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
    print("Loaded base model as fallback")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    review = data.get('review', '')
    
    # Define words to highlight
    positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'brilliant', 'enjoyed',
                     'best', 'happy', 'wonderful', 'beautiful', 'fantastic', 'perfect', 'impressive']
    negative_words = ['bad', 'terrible', 'awful', 'disappointing', 'hate', 'waste', 'boring',
                     'worst', 'poor', 'horrible', 'stupid', 'ridiculous', 'annoying', 'pathetic']
    
    # Tokenize and make prediction
    inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiment = "positive" if prediction[0][1] > prediction[0][0] else "negative"
        confidence = float(prediction[0][1] if sentiment == "positive" else prediction[0][0])
    
    # Process review for highlighting
    highlighted_review = ""
    for word in review.split():
        clean_word = word.lower().strip(".,!?;:'\"")
        word_class = ""
        
        if clean_word in positive_words:
            word_class = "positive-word"
        elif clean_word in negative_words:
            word_class = "negative-word"
        
        if word_class:
            highlighted_review += f'<span class="{word_class}">{word}</span> '
        else:
            highlighted_review += word + " "
    
    return jsonify({
        'review': review,
        'highlightedReview': highlighted_review,
        'sentiment': sentiment,
        'confidence': confidence,
        'modelLoaded': model_loaded
    })

if __name__ == '__main__':
    # Use PORT environment variable for compatibility with Render
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)