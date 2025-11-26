import sys
from pathlib import Path
import pandas as pd

# Add src to sys.path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

from src.analysis.speech_corpus import SpeechCorpus

def test_speech_corpus():
    print("Initializing SpeechCorpus...")
    corpus = SpeechCorpus(data_dir="data")
    print(f"Total speeches: {len(corpus.speeches)}")
    print(f"Total transcriptions: {len(corpus.transcriptions)}")
    
    print("\n--- Testing Campaign Filter ---")
    campaign_2016 = corpus.get_campaign("2016")
    print(f"2016 Campaign speeches: {len(campaign_2016.speeches)}")
    
    campaign_2024 = corpus.get_campaign("2024")
    print(f"2024 Campaign speeches: {len(campaign_2024.speeches)}")
    
    print("\n--- Testing Rally Filter ---")
    rallies = corpus.get_rallies(is_rally=True)
    print(f"Rally speeches: {len(rallies.speeches)}")
    
    non_rallies = corpus.get_rallies(is_rally=False)
    print(f"Non-Rally speeches: {len(non_rallies.speeches)}")
    
    print("\n--- Testing Campaign Rallies Filter ---")
    rallies_2016 = corpus.get_campaign_rallies("2016")
    print(f"2016 Campaign Rallies: {len(rallies_2016.speeches)}")
    
    print("\n--- Testing Location Filter ---")
    pa_speeches = corpus.get_by_location("Pennsylvania")
    print(f"Speeches in Pennsylvania: {len(pa_speeches.speeches)}")
    
    print("\n--- Testing Category Filter ---")
    # Assuming 'Economy' is a category based on user prompt
    economy_speeches = corpus.get_by_category("Economy")
    print(f"Speeches with 'Economy' category: {len(economy_speeches.speeches)}")
    
    print("\n--- Testing Multiple Filters ---")
    filters = {
        'campaign': '2024',
        'is_rally': True,
        'location': 'Pennsylvania'
    }
    filtered = corpus.filter(filters)
    print(f"2024 Rallies in Pennsylvania: {len(filtered.speeches)}")
    
    print("\n--- Testing Cleaned Transcriptions ---")
    try:
        cleaned_corpus = SpeechCorpus(data_dir="data", transcription_file="transcriptions_cleaned.parquet")
        print(f"Cleaned corpus initialized. Transcriptions: {len(cleaned_corpus.transcriptions)}")
    except FileNotFoundError:
        print("transcriptions_cleaned.parquet not found.")

if __name__ == "__main__":
    test_speech_corpus()
