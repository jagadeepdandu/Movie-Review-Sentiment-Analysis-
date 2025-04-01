from flask import Flask, request, jsonify, render_template
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os
import gc  # Garbage collector

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
            print("Loading model from Hugging Face")
            # Use the public distilbert-base-uncased-finetuned-sst-2-english model instead
            # This is a sentiment analysis model that's publicly available
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            
            tokenizer = DistilBertTokenizer.from_pretrained(
                model_name,
                local_files_only=False
            )
            
            model = DistilBertForSequenceClassification.from_pretrained(
                model_name,
                local_files_only=False,
                torchscript=True,  # Optimize with TorchScript
                low_cpu_mem_usage=True  # Use lower memory
            )
            
            model.eval()  # Set to evaluation mode
            model_loaded = True
            print("Model loaded successfully!")
            
            # Force garbage collection
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
        except Exception as e:
            print(f"Error loading model: {e}")
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
    
    # Tokenize with max length reduced to save memory
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
