import sys
from pathlib import Path
import pandas as pd
import textstat

# Add src to path
project_root = Path(".").resolve()
sys.path.append(str(project_root / "src"))

from analysis.speech_corpus import SpeechCorpus
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('cmudict')
nltk.download('punkt')


def calculate_readability_metrics(text):
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        return {
            "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
            "gunning_fog": textstat.gunning_fog(text),
            "flesch_reading_ease": textstat.flesch_reading_ease(text)
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

print("Loading corpus...")
corpus = SpeechCorpus(data_dir="data")
print(f"Corpus loaded: {corpus}")

print("Merging data...")
df = corpus.speeches.merge(corpus.transcriptions, left_on="id", right_on="speech_id", how="inner")
print(f"Total speeches: {len(df)}")

print("Testing on first 5 speeches...")
subset = df.head(5).copy()
results = subset['text'].apply(calculate_readability_metrics)
print(pd.json_normalize(results))
print("Test complete.")
