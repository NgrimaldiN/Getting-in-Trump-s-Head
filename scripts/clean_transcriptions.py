import sys
import pandas as pd
from pathlib import Path
import logging

# Add src to python path to import text_cleaning
# Assuming script is run from root or scripts dir, we need to find src
# Get the project root directory
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from src.text_cleaning.cleaner import clean_docs

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    data_dir = project_root / 'data'
    input_file = data_dir / 'transcriptions.parquet'
    output_file = data_dir / 'transcriptions_cleaned.parquet'

    if not input_file.exists():
        logging.error(f"Input file not found: {input_file}")
        sys.exit(1)

    logging.info(f"Reading transcriptions from {input_file}")
    df = pd.read_parquet(input_file)

    if 'text' not in df.columns:
        logging.error("Column 'text' not found in parquet file")
        # Check if it's named differently, e.g. 'text'
        logging.info(f"Available columns: {df.columns.tolist()}")
        sys.exit(1)

    logging.info("Cleaning transcriptions...")
    # Convert to list for processing
    texts = df['text'].fillna("").astype(str).tolist()
    
    # Process
    cleaned_texts = clean_docs(texts, n_process=4)
    
    # Add to dataframe
    df['cleaned_transcription'] = cleaned_texts
    
    # Save to new parquet
    logging.info(f"Saving cleaned transcriptions to {output_file}")
    df.to_parquet(output_file)
    logging.info("Done.")

if __name__ == "__main__":
    main()
