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
