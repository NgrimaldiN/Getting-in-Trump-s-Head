import spacy
import simplemma
from typing import List, Optional

# Load spacy model globally to avoid reloading it multiple times
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading 'en_core_web_sm' model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load('en_core_web_sm')

def clean_text(
    text: str,
    remove_stopwords: bool = True,
    remove_punctuation: bool = True,
    lemmatize: bool = True
) -> str:
    """
    Cleans a single text string by tokenizing, optionally removing stopwords/punctuation,
    and lemmatizing with simplemma.
    """
    if not text:
        return ""

    # Tokenize with spacy (disable unnecessary components for speed)
    doc = nlp(text, disable=['parser', 'ner', 'textcat'])
    
    stopwords = nlp.Defaults.stop_words
    
    tokens = []
    for token in doc:
        # Skip punctuation if requested
        if remove_punctuation and token.is_punct:
            continue
            
        # Skip stopwords if requested
        if remove_stopwords and token.text.lower() in stopwords:
            continue
            
        # Skip whitespace
        if token.is_space:
            continue
            
        word = token.text.lower()
        
        # Lemmatize if requested
        if lemmatize:
            # simplemma.lemmatize returns the lemma
            lemma = simplemma.lemmatize(word, lang='en')
            tokens.append(lemma)
        else:
            tokens.append(word)
            
    return " ".join(tokens)

def clean_docs(
    texts: List[str],
    remove_stopwords: bool = True,
    remove_punctuation: bool = True,
    lemmatize: bool = True,
    n_process: int = 1,
    batch_size: int = 100
) -> List[str]:
    """
    Cleans a list of documents.
    """
    # For simplemma, we might just iterate. Spacy pipe is good for tokenization.
    # But since we want to use simplemma for lemmatization, we can mix them.
    # However, simplemma works on words. Spacy gives us tokens.
    
    cleaned_texts = []
    # We can use nlp.pipe for faster tokenization if we have many docs
    # But we need to handle the custom logic inside.
    
    # If n_process > 1, we should be careful with simplemma inside the loop if it's not picklable or efficient.
    # For simplicity and safety with simplemma, let's stick to a simple loop or use spacy's pipe for tokenization only.
    
    # Let's use nlp.pipe to get docs, then process them.
    docs = nlp.pipe(texts, n_process=n_process, batch_size=batch_size, disable=['parser', 'ner', 'textcat'])
    
    stopwords = nlp.Defaults.stop_words
    
    for doc in docs:
        tokens = []
        for token in doc:
            if remove_punctuation and token.is_punct:
                continue
            if remove_stopwords and token.text.lower() in stopwords:
                continue
            if token.is_space:
                continue
                
            word = token.text.lower()
            if lemmatize:
                tokens.append(simplemma.lemmatize(word, lang='en'))
            else:
                tokens.append(word)
        cleaned_texts.append(" ".join(tokens))
        
    return cleaned_texts
