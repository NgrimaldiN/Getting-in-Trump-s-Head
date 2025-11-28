import pandas as pd
from pathlib import Path

file_path = Path('data/transcriptions_cleaned.parquet')
if file_path.exists():
    df = pd.read_parquet(file_path)
    print(f"File exists. Shape: {df.shape}")
    print("Columns:", df.columns)
    print("\nSample cleaned text:")
    print(df[['text', 'cleaned_transcription']].head(3).to_string())
else:
    print("File does not exist.")
