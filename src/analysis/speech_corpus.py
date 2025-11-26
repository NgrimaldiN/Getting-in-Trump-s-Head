import pandas as pd
from pathlib import Path
import re
import datetime

class SpeechCorpus:
    def __init__(self, data_dir="data", transcription_file="transcriptions.parquet"):
        """
        Initialize the SpeechCorpus.
        
        Args:
            data_dir (str): Directory containing the parquet files.
            transcription_file (str): Name of the transcription file to load.
        """
        self.data_dir = Path(data_dir)
        self.speeches_path = self.data_dir / "speeches.parquet"
        self.transcriptions_path = self.data_dir / transcription_file
        
        if not self.speeches_path.exists():
            raise FileNotFoundError(f"Speeches file not found at {self.speeches_path}")
        
        if not self.transcriptions_path.exists():
            raise FileNotFoundError(f"Transcriptions file not found at {self.transcriptions_path}")
            
        self.speeches = pd.read_parquet(self.speeches_path)
        self.transcriptions = pd.read_parquet(self.transcriptions_path)
        
        self._preprocess()
        
    def _preprocess(self):
        """
        Preprocess the speeches dataframe to add useful columns for filtering.
        """
        # Convert date to datetime
        self.speeches['date'] = pd.to_datetime(self.speeches['date'], errors='coerce')
        self.speeches['year'] = self.speeches['date'].dt.year
        
        # Determine is_rally
        self.speeches['is_rally'] = self.speeches['title'].apply(
            lambda x: bool(re.search(r"Rally|Campaign", str(x), re.IGNORECASE))
        )
        
        # Extract location
        # Pattern looks for " in " followed by text until " - " or end of string
        def extract_location(title):
            if not isinstance(title, str):
                return None
            match = re.search(r" in (.*?)(?: -|$)", title)
            if match:
                return match.group(1).strip()
            return None
            
        self.speeches['location'] = self.speeches['title'].apply(extract_location)
        
        # Assign campaign
        def get_campaign(date):
            if pd.isna(date):
                return None
            year = date.year
            if year in [2015, 2016]:
                return "2016"
            elif year in [2019, 2020]:
                return "2020"
            elif year in [2023, 2024, 2025]:
                return "2024"
            return "Other"
            
        self.speeches['campaign'] = self.speeches['date'].apply(get_campaign)

    def get_campaign(self, campaign_cycle):
        """
        Filter speeches by campaign cycle.
        
        Args:
            campaign_cycle (str): The campaign cycle to filter by (e.g., "2016", "2020", "2024").
            
        Returns:
            SpeechCorpus: A new SpeechCorpus instance with the filtered data.
        """
        filtered_speeches = self.speeches[self.speeches['campaign'] == str(campaign_cycle)].copy()
        return self._create_filtered_corpus(filtered_speeches)

    def get_rallies(self, is_rally=True):
        """
        Filter speeches by rally status.
        
        Args:
            is_rally (bool): Whether to include only rallies (True) or non-rallies (False).
            
        Returns:
            SpeechCorpus: A new SpeechCorpus instance with the filtered data.
        """
        filtered_speeches = self.speeches[self.speeches['is_rally'] == is_rally].copy()
        return self._create_filtered_corpus(filtered_speeches)

    def get_campaign_rallies(self, campaign_cycle):
        """
        Filter for speeches that are both in the specified campaign and are rallies.
        
        Args:
            campaign_cycle (str): The campaign cycle to filter by.
            
        Returns:
            SpeechCorpus: A new SpeechCorpus instance with the filtered data.
        """
        filtered_speeches = self.speeches[
            (self.speeches['campaign'] == str(campaign_cycle)) & 
            (self.speeches['is_rally'] == True)
        ].copy()
        return self._create_filtered_corpus(filtered_speeches)

    def get_by_location(self, location):
        """
        Filter speeches by location (partial match).
        
        Args:
            location (str): The location string to search for.
            
        Returns:
            SpeechCorpus: A new SpeechCorpus instance with the filtered data.
        """
        filtered_speeches = self.speeches[
            self.speeches['location'].str.contains(location, case=False, na=False)
        ].copy()
        return self._create_filtered_corpus(filtered_speeches)

    def get_by_category(self, category):
        """
        Filter speeches by category (partial match).
        
        Args:
            category (str): The category to search for.
            
        Returns:
            SpeechCorpus: A new SpeechCorpus instance with the filtered data.
        """
        filtered_speeches = self.speeches[
            self.speeches['categories'].str.contains(category, case=False, na=False)
        ].copy()
        return self._create_filtered_corpus(filtered_speeches)

    def filter(self, filters):
        """
        Apply multiple filters.
        
        Args:
            filters (dict): Dictionary of filters to apply. 
                            Keys can be 'campaign', 'is_rally', 'location', 'category'.
        
        Returns:
            SpeechCorpus: A new SpeechCorpus instance with the filtered data.
        """
        filtered_speeches = self.speeches.copy()
        
        if 'campaign' in filters:
            filtered_speeches = filtered_speeches[filtered_speeches['campaign'] == str(filters['campaign'])]
            
        if 'is_rally' in filters:
            filtered_speeches = filtered_speeches[filtered_speeches['is_rally'] == filters['is_rally']]
            
        if 'location' in filters:
            filtered_speeches = filtered_speeches[
                filtered_speeches['location'].str.contains(filters['location'], case=False, na=False)
            ]
            
        if 'category' in filters:
            filtered_speeches = filtered_speeches[
                filtered_speeches['categories'].str.contains(filters['category'], case=False, na=False)
            ]
            
        return self._create_filtered_corpus(filtered_speeches)

    def _create_filtered_corpus(self, filtered_speeches):
        """
        Helper to create a new SpeechCorpus instance from filtered speeches.
        """
        new_corpus = SpeechCorpus.__new__(SpeechCorpus)
        new_corpus.data_dir = self.data_dir
        new_corpus.speeches_path = self.speeches_path
        new_corpus.transcriptions_path = self.transcriptions_path
        
        new_corpus.speeches = filtered_speeches
        # Filter transcriptions to match speeches
        speech_ids = filtered_speeches['id'].unique()
        new_corpus.transcriptions = self.transcriptions[self.transcriptions['speech_id'].isin(speech_ids)].copy()
        
        return new_corpus

    def save_sub_db(self, output_dir_name):
        """
        Save the filtered corpus to a new directory.
        
        Args:
            output_dir_name (str): Name of the subdirectory in the data directory to save to.
        """
        output_path = self.data_dir / output_dir_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        self.speeches.to_parquet(output_path / "speeches.parquet", index=False)
        self.transcriptions.to_parquet(output_path / "transcriptions.parquet", index=False)
        print(f"Saved sub-database to {output_path}")

    def __repr__(self):
        return f"<SpeechCorpus: {len(self.speeches)} speeches, {len(self.transcriptions)} transcriptions>"
