# Movie Review Sentiment Analysis

## Overview

This web application analyzes movie reviews to determine whether the sentiment is positive or negative using a fine-tuned DistilBERT model. The application provides an interactive UI with word highlighting to help users understand which words contributed to the sentiment classification.

## Features

- **Real-time sentiment analysis of movie reviews**
- **Highlighting of positive and negative impact words**
- **Confidence score visualization**
- **Sentiment scale from Very Negative to Very Positive**
- **Example reviews for quick testing**

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask (Python)
- **Machine Learning:** DistilBERT (Hugging Face Transformers)
- **Model Training:** Fine-tuned on the IMDB Movie Reviews dataset

## Installation and Setup

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/jagadeepdandu/movie-review-.git
    ```

2.  Change into the project directory:

    ```bash
    cd movie-review-
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Run the application:

    ```bash
    python app.py
    ```

5.  Open your browser and navigate to `http://localhost:5000`

## Usage

1.  Enter a movie review in the text area.
2.  Click "Analyze Sentiment".
3.  View the results showing sentiment (positive/negative), confidence score, and highlighted impact words.

## Model Information

- **Base Model:** DistilBERT (distilbert-base-uncased)
- **Fine-tuning:** Trained on IMDB movie reviews dataset
- **Performance:** ~95% accuracy on the test set
- **Model Size:** 225 MB

## Deployment

This application can be deployed to cloud platforms such as:

- Render

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for the Transformers library
- [IMDB](https://www.imdb.com/) for the movie reviews dataset used in training
