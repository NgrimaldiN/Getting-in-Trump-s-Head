import spacy
import simplemma
import pandas as pd
from pathlib import Path
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

def apply_cleaning_to_parquet(
    parquet_path: str,
    output_column: str,
    remove_stopwords: bool = True,
    remove_punctuation: bool = True,
    lemmatize: bool = True,
    overwrite: bool = False
):
    """
    Applies text cleaning to the 'text' column of a parquet file and saves the result
    to a new column in the same file.
    
    Args:
        parquet_path (str): Path to the parquet file.
        output_column (str): Name of the new column to store cleaned text.
        remove_stopwords (bool): Whether to remove stopwords.
        remove_punctuation (bool): Whether to remove punctuation.
        lemmatize (bool): Whether to lemmatize words.
        overwrite (bool): Whether to overwrite the column if it already exists.
    """
    path = Path(parquet_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
        
    df = pd.read_parquet(path)
    
    if 'text' not in df.columns:
        raise ValueError("Parquet file must contain a 'text' column")
        
    if output_column in df.columns and not overwrite:
        print(f"Column '{output_column}' already exists. Skipping. Set overwrite=True to force update.")
        return
        
    print(f"Cleaning text for column '{output_column}'...")
    # Use clean_docs for batch processing
    cleaned_texts = clean_docs(
        df['text'].fillna("").tolist(),
        remove_stopwords=remove_stopwords,
        remove_punctuation=remove_punctuation,
        lemmatize=lemmatize
    )
    
    df[output_column] = cleaned_texts
    
    df.to_parquet(path, index=False)
    print(f"Saved updated parquet to {path}")

