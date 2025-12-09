
import sys
import os
sys.path.append(os.path.abspath("src"))

from filtering_corpus.speech_corpus import SpeechCorpus
# from filtering_corpus.other_candidates import OtherCandidatesCorpus

def verify_speech_corpus():
    print("Verifying SpeechCorpus...")
    corpus = SpeechCorpus()
    
    # Check default columns
    try:
        df = corpus.get_full_speeches(text_columns=['text'])
        print(f"Success: retrieved 'text'. Shape: {df.shape}")
    except Exception as e:
        print(f"Failed to retrieve 'text': {e}")
        
    # Check specific cleaned column (should exist from previous step, e.g. clean_v1)
    # We'll check column names first to pick one that exists
    existing_cols = corpus.transcriptions.columns.tolist()
    print(f"Existing columns: {existing_cols}")
    
    test_col = 'clean_v1' if 'clean_v1' in existing_cols else 'cleaned_transcription'
    if test_col in existing_cols:
        try:
            df = corpus.get_full_speeches(text_columns=[test_col])
            print(f"Success: retrieved '{test_col}'. First few chars: {df[test_col].iloc[0][:20]}...")
        except Exception as e:
            print(f"Failed to retrieve '{test_col}': {e}")
            
    # Check failure on missing column
    try:
        corpus.get_full_speeches(text_columns=['NON_EXISTENT_COLUMN'])
        print("Error: Should have failed for non-existent column but didn't.")
    except ValueError as e:
        print(f"Success: Caught expected error for missing column: {e}")

if __name__ == "__main__":
    verify_speech_corpus()
