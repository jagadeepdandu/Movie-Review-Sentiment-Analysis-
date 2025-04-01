Movie Review Sentiment Analysis

Overview

This web application analyzes movie reviews to determine whether the sentiment is positive or negative using a fine-tuned DistilBERT model. The application provides an interactive UI with word highlighting to help users understand which words contributed to the sentiment classification.

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

Model Training: Fine-tuned on the IMDB Movie Reviews dataset

Project Structure

movie-review-sentiment-analysis/
├── app.py                  # Main Flask application
├── distilbert_imdb.pth     # Fine-tuned DistilBERT model
├── requirements.txt        # Python dependencies
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # Styling
│   └── js/
│       └── script.js       # Frontend functionality
└── templates/
    └── index.html          # Main HTML template

Installation and Setup

Prerequisites

Python 3.8+

pip package manager

Installation

Clone the repository:

git clone https://github.com/jagadeepdandu/movie-review-.git

Change into the project directory:

cd movie-review-

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Open your browser and navigate to http://localhost:5000

Usage

Enter a movie review in the text area.

Click "Analyze Sentiment".

View the results showing sentiment (positive/negative), confidence score, and highlighted impact words.

Model Information

Base Model: DistilBERT (distilbert-base-uncased)

Fine-tuning: Trained on IMDB movie reviews dataset

Performance: ~95% accuracy on the test set

Model Size: 225 MB

Deployment

This application can be deployed to cloud platforms such as:

Render

Heroku

AWS

Google Cloud

Follow the platform-specific instructions for deploying a Flask application.

License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

Acknowledgments

Hugging Face for the Transformers library

IMDB for the movie reviews dataset used in training

Flask team for the web framework
