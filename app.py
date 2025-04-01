from flask import Flask, request, jsonify, render_template
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os
import gc  # Garbage collector

# Create the Flask application instance with name 'app'
app = Flask(__name__)

# Initialize with None to load on first request
tokenizer = None
model = None
model_loaded = False

def load_model():
    global tokenizer, model, model_loaded
    
    # Only load if not already loaded
    if not model_loaded:
        try:
            print("Loading your custom IMDB model...")
            
            # Use your specific model
            model_name = "jagadeepdandu/distilbert-imdb-sentiment"
            
            # Load tokenizer and model
            tokenizer = DistilBertTokenizer.from_pretrained(model_name)
            model = DistilBertForSequenceClassification.from_pretrained(model_name)
            
            model.eval()
            model_loaded = True
            print("Custom model loaded successfully!")
            
            gc.collect()
            
        except Exception as e:
            print(f"Error loading custom model: {e}")
            # Fallback to the public model if yours fails
            try:
                print("Attempting to load fallback model...")
                fallback_model = "distilbert-base-uncased-finetuned-sst-2-english"
                tokenizer = DistilBertTokenizer.from_pretrained(fallback_model)
                model = DistilBertForSequenceClassification.from_pretrained(fallback_model)
                model.eval()
                model_loaded = True
                print("Fallback model loaded successfully")
                gc.collect()
            except Exception as e2:
                print(f"Critical error loading fallback model: {e2}")
                return False
    
    return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Load model on first prediction
    if not load_model():
        return jsonify({
            'error': 'Failed to load model',
            'modelLoaded': model_loaded
        }), 500
    
    data = request.json
    review = data.get('review', '')
    
    # Define words to highlight
    positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'brilliant', 'enjoyed',
                     'best', 'happy', 'wonderful', 'beautiful', 'fantastic', 'perfect', 'impressive']
    negative_words = ['bad', 'terrible', 'awful', 'disappointing', 'hate', 'waste', 'boring',
                     'worst', 'poor', 'horrible', 'stupid', 'ridiculous', 'annoying', 'pathetic']
    
    # Tokenize with reduced max length
    inputs = tokenizer(review, return_tensors="pt", truncation=True, padding=True, max_length=256)
    
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
    
    # Clear memory after prediction
    gc.collect()
    
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
