Movie Review Sentiment Analysis
Overview
This web application analyzes movie reviews to determine if the sentiment is positive or negative using a fine-tuned DistilBERT model. The application provides an interactive UI with word highlighting to help users understand which words contributed to the sentiment classification.
Features

Real-time sentiment analysis of movie reviews
Highlighting of positive and negative impact words
Confidence score visualization
Sentiment scale from Very Negative to Very Positive
Example reviews for quick testing
Mobile-friendly responsive design

Tech Stack

Frontend: HTML, CSS, JavaScript
Backend: Flask (Python)
Machine Learning: DistilBERT (Hugging Face Transformers)
Model Training: Fine-tuned on IMDB Movie Reviews dataset
Installation and Setup
Prerequisites

Python 3.8+
pip package manager

Installation

Clone the repository:
Copygit clone https://github.com/jagadeepdandu/movie-review-.git
cd movie-review-

Install dependencies:
Copypip install -r requirements.txt

Run the application:
Copypython app.py

Open your browser and navigate to http://localhost:5000

Usage

Enter a movie review in the text area
Click "Analyze Sentiment"
View the results showing sentiment (positive/negative), confidence score, and highlighted impact words

Model Information

Base Model: DistilBERT (distilbert-base-uncased)
Fine-tuning: Trained on IMDB movie reviews dataset
Performance: ~95% accuracy on test set
Model Size: 225 MB
