import polars as pl
import datetime
from typing import Tuple, List
from modules import params

class Corpus():
    """
    A class to represent and analyze a corpus of text data with sentiment information.
    """
    def __init__(
            self,
            path: str,
            sep: str = ";",
            date_column: str = 'DATE',
            sentiment_column: str = 'SENTIMENT_SCORE',
            class_column: str = 'SENTIMENT_CLASS',
            text_column: str = 'TEXT',
            encoding: str = 'latin1'
        ):
        self.df = pl.read_csv(path, separator=sep, try_parse_dates=True, encoding=encoding)
        self.date_col = date_column
        self.sent_col = sentiment_column
        self.class_col = class_column
        self.text_col = text_column

    def filter_data(
            self,
            start_date: datetime.date,
            end_date: datetime.date,
            word_filter: str = None
        ) -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
        
        daily_stats = {}
        daily_stats['full'] = self._get_daily_stats(self.df)

        if start_date and end_date:
            filtered_df = self._apply_date_filter(self.df, start_date, end_date)

        daily_stats['date_filtered'] = self._get_daily_stats(filtered_df)

        if word_filter:
            filtered_df = self._apply_word_filter(filtered_df, word_filter)
        self.filtered_df = filtered_df

        daily_stats['word_filtered'] = self._get_daily_stats(filtered_df)
        self.daily_stats = daily_stats

        return daily_stats
    
    def extract_top_words(self, class_filter: str, top_n: int = 100) -> pl.DataFrame:
        df = self.filtered_df.with_columns(
            pl.col(self.class_col).replace(params.SENTIMENT_CLASSES_MAP)
        )
        filtered_df = self._apply_class_filter(df, class_filter)

        word_freqs = filtered_df.select([
            pl.col(self.date_col),
            pl.col(self.text_col).str.to_lowercase().str.extract_all(r'\w+').alias('word')
        ]).explode(columns='word')

        return word_freqs['word'].value_counts().sort('count', descending=True)[0:top_n]

    def extract_classes_ts(self, normalize: bool, classes_columns: List[str]) -> pl.DataFrame:
        df = self.daily_stats['word_filtered'].with_columns(
            pl.sum_horizontal(classes_columns).alias("Total"),
        )
        if normalize:
            cols = [
                (pl.col(col) / pl.col("Total")).alias(params.SENTIMENT_CLASSES_MAP[col])
                for col in classes_columns
            ]
        else:
            cols = [
                (pl.col(col)).alias(params.SENTIMENT_CLASSES_MAP[col])
                for col in classes_columns
            ]
        cols.append(params.LOADING_PARAMS['date_column'])
        df = df.with_columns(cols).select(cols)
        return df

    def _apply_class_filter(self, df: pl.DataFrame, class_filter: str) -> pl.DataFrame:
        if class_filter != '-':
            return df.filter(pl.col(self.class_col) == class_filter)
        else:
            return df

    def _apply_date_filter(self, df: pl.DataFrame, start_date: datetime.date, end_date: datetime.date) -> pl.DataFrame:
        s_year, s_month, s_day = start_date.year, start_date.month, start_date.day
        e_year, e_month, e_day = end_date.year, end_date.month, end_date.day
        return df.filter(
            pl.col(self.date_col) <= pl.datetime(e_year, e_month, e_day),
            pl.col(self.date_col) >= pl.datetime(s_year, s_month, s_day)
        )
    
    def _apply_word_filter(self, df: pl.DataFrame, word_filter: str) -> pl.DataFrame:
        return df.filter(pl.col(self.text_col).str.contains(word_filter))
    
    def _get_daily_stats(self, df: pl.DataFrame) -> pl.DataFrame:
        grouped_df = df.group_by(self.date_col)
        counts = grouped_df.len('Count')
        sentiment_score = grouped_df.agg(pl.col(self.sent_col).mean().alias('Sentiment'))
        sentiment_classes = df.pivot(
            on=self.class_col,
            index=self.date_col,
            values=self.class_col,
            aggregate_function=pl.element().count()
        )
        daily_stats = counts.join(sentiment_score, on=self.date_col).join(sentiment_classes, on=self.date_col)
        daily_stats = self._get_qualitative_index(daily_stats)
        return daily_stats
    
    def _get_word_freqs(self, df: pl.DataFrame, top_n: int = 100) -> pl.DataFrame:
        word_freqs = df.select([
            pl.col(self.date_col),
            pl.col(self.text_col).str.to_lowercase().str.extract_all(r'\w+').alias('word')
        ]).explode(columns='word')
        most_frequent = word_freqs['word'].value_counts().sort('count', descending=True)[0:top_n]
        return most_frequent

    def _get_qualitative_index(self, df: pl.DataFrame) -> pl.DataFrame:
        return (
            df.with_columns([
                (pl.col('Strongly Positive') + pl.col('Positive')).alias('POS'),
                (pl.col('Strongly Negative') + pl.col('Negative')).alias('NEG'),
                pl.col('Count').alias('TOT')
            ])
            .with_columns([
                pl.col('POS').cast(pl.Int64),
                pl.col('NEG').cast(pl.Int64),
                pl.col('TOT').cast(pl.Int64),
            ])
            .with_columns([
                (((pl.col('POS') - pl.col('NEG')).cast(pl.Float64) / pl.col('TOT').cast(pl.Float64))).alias('Qualitative Index')
            ])
            .sort('DATE')
        )
    