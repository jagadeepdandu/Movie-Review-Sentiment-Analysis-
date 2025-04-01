document.addEventListener('DOMContentLoaded', function() {
    const reviewInput = document.getElementById('review');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultDiv = document.getElementById('result');
    const positiveExampleBtn = document.getElementById('positive-example');
    const negativeExampleBtn = document.getElementById('negative-example');
    
    // Initialize
    displayReviewHistory();
    
    // Analyze button click
    analyzeBtn.addEventListener('click', analyzeSentiment);
    
    // Keyboard shortcuts
    reviewInput.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            analyzeSentiment();
        }
        
        if (e.key === 'Escape') {
            e.preventDefault();
            reviewInput.value = '';
        }
    });
    
    // Example buttons
    positiveExampleBtn.addEventListener('click', function() {
        reviewInput.value = "This movie was absolutely brilliant! The acting was superb, especially the lead performance. The cinematography was breathtaking and the story kept me engaged from beginning to end.";
    });
    
    negativeExampleBtn.addEventListener('click', function() {
        reviewInput.value = "I was extremely disappointed with this film. The plot made no sense and had major holes throughout. The acting felt forced and wooden, especially from the lead who seemed completely disinterested.";
    });
    
    // Clear history button
    document.getElementById('clear-history').addEventListener('click', function(e) {
        e.stopPropagation();
        if (confirm('Are you sure you want to clear your review history?')) {
            localStorage.removeItem('reviewHistory');
            displayReviewHistory();
        }
    });
    
    // Export buttons
    document.getElementById('export-image').addEventListener('click', function() {
        alert('To implement this feature, you would need to include the html2canvas library.');
    });
    
    document.getElementById('export-pdf').addEventListener('click', function() {
        alert('To implement this feature, you would need to include the jsPDF library.');
    });
    
    document.getElementById('share-result').addEventListener('click', function() {
        if (navigator.share) {
            navigator.share({
                title: 'Movie Review Sentiment Analysis',
                text: `Analysis of review: "${document.getElementById('review-text').textContent}" - Result: ${document.getElementById('sentiment-text').textContent}`,
            })
            .catch(err => console.error('Error sharing:', err));
        } else {
            alert('Copy this link to share your result.');
        }
    });
});

// Main analysis function
function analyzeSentiment() {
    const review = document.getElementById('review').value.trim();
    
    if (!review) {
        alert('Please enter a movie review to analyze.');
        return;
    }
    
    // Show loading state
    const analyzeBtn = document.getElementById('analyze-btn');
    analyzeBtn.innerHTML = 'Analyzing... <span class="loading-spinner"></span>';
    analyzeBtn.disabled = true;
    
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ review: review })
    })
    .then(response => response.json())
    .then(data => {
        // Update result
        renderHighlightedReview(data.review);
        
        const sentiment = data.sentiment;
        const confidence = data.confidence;
        const confidencePercent = (confidence * 100).toFixed(2);
        
        // Add icon based on sentiment
        const sentimentIcon = sentiment === 'positive' ? '😊' : '😞';
        document.getElementById('sentiment-text').innerHTML = 
            `<span class="sentiment-icon">${sentimentIcon}</span> Sentiment: ${sentiment}`;
        document.getElementById('sentiment-text').className = `sentiment ${sentiment.toLowerCase()}`;
        
        // Prepare progress bar for animation
        const confidenceBar = document.getElementById('confidence-bar');
        confidenceBar.style.width = '0';
        confidenceBar.className = `progress-bar ${sentiment.toLowerCase()}-bar`;
        
        // Set the final width as a CSS variable for the animation
        document.documentElement.style.setProperty('--final-width', `${confidencePercent}%`);
        
        // Update sentiment scale
        updateSentimentScale(data.confidence, data.sentiment);
        
        // Show result div
        document.getElementById('result').style.display = 'block';
        
        // Trigger animation after a small delay
        setTimeout(() => {
            confidenceBar.classList.add('animate-bar');
            document.getElementById('confidence-text').textContent = `Confidence: ${confidencePercent}%`;
        }, 100);
        
        // Save to history
        saveReviewToHistory(data.review, data.sentiment, data.confidence);
        
        // Scroll to result
        document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while analyzing the review.');
    })
    .finally(() => {
        // Reset button
        analyzeBtn.innerHTML = 'Analyze Sentiment';
        analyzeBtn.disabled = false;
    });
}

// Word highlighting function
function renderHighlightedReview(reviewText) {
    const words = reviewText.split(/\s+/);
    const reviewTextElement = document.getElementById('review-text');
    reviewTextElement.innerHTML = '';
    reviewTextElement.className = 'highlighted-text';
    
    words.forEach(word => {
        const sentiment = getWordSentiment(word);
        const span = document.createElement('span');
        span.textContent = word + ' ';
        span.className = `${sentiment}-word`;
        reviewTextElement.appendChild(span);
    });
}

// Simple word sentiment detector
function getWordSentiment(word) {
    const positiveWords = ['good', 'great', 'excellent', 'amazing', 'love', 'brilliant', 'enjoyed', 'best', 'happy', 'wonderful', 'beautiful', 'fantastic', 'perfect', 'impressive'];
    const negativeWords = ['bad', 'terrible', 'awful', 'disappointing', 'hate', 'waste', 'boring', 'worst', 'poor', 'horrible', 'stupid', 'ridiculous', 'annoying', 'pathetic'];
    
    const normalizedWord = word.toLowerCase().replace(/[.,!?;:'"]/g, '');
    
    if (positiveWords.includes(normalizedWord)) return 'positive';
    if (negativeWords.includes(normalizedWord)) return 'negative';
    return 'neutral';
}

// Sentiment scale function
function updateSentimentScale(confidence, sentiment) {
    const marker = document.getElementById('sentiment-marker');
    
    let position;
    if (sentiment === 'negative') {
        // For negative, position between 0% and 40% based on confidence
        position = 40 - (confidence * 40);
    } else {
        // For positive, position between 60% and 100% based on confidence
        position = 60 + (confidence * 40);
    }
    
    marker.style.left = `${position}%`;
}

// History functions
function saveReviewToHistory(review, sentiment, confidence) {
    let history = JSON.parse(localStorage.getItem('reviewHistory') || '[]');
    
    // Add new review at the beginning
    history.unshift({
        review: review,
        sentiment: sentiment,
        confidence: confidence,
        timestamp: new Date().toISOString()
    });
    
    // Keep only the last 10 reviews
    history = history.slice(0, 10);
    
    localStorage.setItem('reviewHistory', JSON.stringify(history));
    displayReviewHistory();
}

function displayReviewHistory() {
    const historyContainer = document.getElementById('history-items');
    const history = JSON.parse(localStorage.getItem('reviewHistory') || '[]');
    
    historyContainer.innerHTML = '';
    
    if (history.length === 0) {
        historyContainer.innerHTML = '<p>No review history yet.</p>';
        return;
    }
    
    history.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        // Format the review text (truncate if too long)
        const shortReview = item.review.length > 50 
            ? item.review.substring(0, 50) + '...' 
            : item.review;
        
        historyItem.innerHTML = `
            <span class="sentiment-badge ${item.sentiment}">${item.sentiment}</span>
            <span class="history-review">${shortReview}</span>
            <span class="history-confidence">(${(item.confidence * 100).toFixed(1)}%)</span>
        `;
        
        // Click to restore this review
        historyItem.addEventListener('click', () => {
            document.getElementById('review').value = item.review;
            analyzeSentiment();
        });
        
        historyContainer.appendChild(historyItem);
    });
}

// Debounce function for real-time analysis
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}