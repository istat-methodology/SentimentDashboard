import polars as pl
import json
import streamlit as st
from datequarter import DateQuarter
from modules import params

class Data():
    """
    A class to load JSON files inside the dashboard.
    """
    def __init__(self, path: str):
        with open(path) as f:
            self.data = json.load(f)
    
    def _get_date(self, year: int, quarter: str):
        quarter_int = params.QUARTER_FILTER['MAPPING'][quarter]
        year_int = int(year)
        return {
            'date': DateQuarter(year_int, quarter_int),
            'date_str': f"Q{quarter_int}{year_int}"
        }

    def filter_data(self, year: int, quarter: str, semantic_group: str):
        date_quarter = self._get_date(year, quarter)
        
        semantic_group = semantic_group if semantic_group else '-'

        # TimeSeries
        time_series = pl.from_dict(self.data['time_series'][semantic_group])
        time_series = time_series.with_columns(
            pl.col("DATE").str.strptime(pl.Date, "%Y-%m-%d")
        )
        time_series = time_series.filter(
            (pl.col("DATE") >= date_quarter['date'].start_date()) & (pl.col("DATE") <= date_quarter['date'].end_date())
        )

        # WordFrequencies
        word_freqs = self.data['word_frequencies'][semantic_group][date_quarter['date_str']]

        return {
            'time_series': time_series,
            'word_freqs': word_freqs
        }

def load_data():
    if st.session_state['initialized'] is False:
        with st.spinner("Caricamento dei dati in corso..."):
            st.session_state['data'] = Data(
                path = params.PATHS['JSON_PATH']
            )
            st.session_state['initialized'] = True
            st.toast("Dati caricati con successo!", icon="✅")
