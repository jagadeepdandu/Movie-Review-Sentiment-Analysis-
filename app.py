from flask import Flask, request, jsonify, render_template
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os

app = Flask(__name__)

# Load the tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

# Load your trained weights with robust error handling
MODEL_PATH = "distilbert_imdb.pth"  
model_loaded = False

try:
    # Print current directory and check if file exists
    print(f"Current directory: {os.getcwd()}")
    print(f"Model file exists: {os.path.exists(MODEL_PATH)}")
    
    # Try different loading approaches
    if os.path.exists(MODEL_PATH):
        try:
            # Standard approach
            model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
            model_loaded = True
            print("Model loaded successfully!")
        except Exception as e1:
            print(f"Standard loading failed: {e1}")
            try:
                
                full_model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
                if isinstance(full_model, dict) and "state_dict" in full_model:
                    model.load_state_dict(full_model["state_dict"])
                else:
                    model = full_model
                model_loaded = True
                print("Model loaded with alternative method!")
            except Exception as e2:
                print(f"Alternative loading failed: {e2}")
    else:
        print(f"Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error during model loading: {e}")

model.eval()

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
    app.run(debug=True, host='0.0.0.0')