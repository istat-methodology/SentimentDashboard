import json
import polars as pl
import logging
from modules import params

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class BatchProcessing():

    def __init__(self):
        self.dfs = {}
        self.output = {}
    
    def _load_data(self, path):
        logging.info(f"[LOAD PARQUET] Loading Parquet file from \"{path}\"")
        self.dfs['-'] = pl.read_parquet(path)
        logging.info("[LOAD PARQUET] Parquet file loaded succesfully!")
    
    def _classify_sentiment(self, score):
        if score == None:
            return None
        if score <= params.SENTIMENT_THRESHOLDS['t1']:
            sentiment = 'Strongly Negative'
            return sentiment
        elif score > params.SENTIMENT_THRESHOLDS['t1'] and score <= params.SENTIMENT_THRESHOLDS['t2']:
            sentiment = 'Negative'
            return sentiment
        elif score > params.SENTIMENT_THRESHOLDS['t2'] and score <= params.SENTIMENT_THRESHOLDS['t3']:
            sentiment = 'Neutral'
            return sentiment
        elif score > params.SENTIMENT_THRESHOLDS['t3'] and score <= params.SENTIMENT_THRESHOLDS['t4']:
            sentiment = 'Positive'
            return sentiment
        else:
            sentiment = 'Strongly Positive'
        return sentiment
    
    def _add_sentiment_class(self):
        logging.info('[SENTIMENT_CLASS] Extracting sentiment classes...')
        self.dfs['-'] = self.dfs['-'].with_columns(
            pl.col('SENTIMENT_SCORE').map_elements(
                self._classify_sentiment, return_dtype=pl.String
            ).alias('SENTIMENT_CLASS')
        )
        logging.info('[SENTIMENT CLASS] Sentiment classes extracted succesfully!')
    
    def _get_subsets(self):
        logging.info(f"[WORD LIST TO STRING] Converting word lists to strings...")
        self.dfs['-'] = self.dfs['-'].with_columns(
            pl.col("WORD_LIST").cast(pl.List(pl.String)).list.join(", ").alias("TEXT_STR")
        )
        for group in params.SEMANTIC_GROUPS['GROUPS'].values():
            if group:
                logging.info(f"[DATA FILTERING] Filtering series by group \"{group}\"...")
                self.dfs[group] = self.dfs['-'].filter(pl.col('TEXT_STR').str.contains(group))

    def _aggregate_series(self):
        self.aggregate_dfs = {}
        for group, df in self.dfs.items():
            logging.info(f"[SERIES AGGREGATION] Aggregating series for group \"{group}\"...")
            grouped_df = df.group_by('DATE', maintain_order=True).agg([
                pl.col('SENTIMENT_SCORE').mean(),
                pl.col('SENTIMENT_CLASS').value_counts(),
                pl.col('TEXT_STR').len().alias('TOTAL_COUNT')
            ])
            sentiment_exploded = grouped_df.explode('SENTIMENT_CLASS').unnest('SENTIMENT_CLASS')
            sentiment_pivot = sentiment_exploded.pivot(
                values="count", 
                index="DATE", 
                on=["SENTIMENT_CLASS"], 
                aggregate_function="sum"
            )
            sentiment_pivot = sentiment_pivot.with_columns(
                [pl.col(col).cast(pl.Int64).alias(col) for col in df['SENTIMENT_CLASS'].unique()]
            )
            self.aggregate_dfs[group] = sentiment_pivot.with_columns(
                grouped_df["SENTIMENT_SCORE"],
                (((sentiment_pivot["Positive"] + sentiment_pivot["Strongly Positive"]) - 
                (sentiment_pivot["Negative"] + sentiment_pivot["Strongly Negative"])) / 
                grouped_df["TOTAL_COUNT"]).alias('QUALITATIVE_SCORE'),
                grouped_df["TOTAL_COUNT"].cast(pl.Int64)
            )
    
    def _get_quarters(self):
        logging.info("[EXTRACT QUARTERS] Extracting quarters...")
        self.freq_dfs = {}
        for group, df in self.dfs.items():
            self.freq_dfs[group] = {}
            df = df.select(['DATE', 'SENTIMENT_CLASS', 'WORD_LIST'])
            df = df.with_columns(pl.col("DATE").str.strptime(pl.Date, "%Y-%m-%d"))
            self.freq_dfs[group] = df.with_columns(("Q" + pl.col("DATE").dt.quarter().cast(pl.Utf8) + pl.col("DATE").dt.year().cast(pl.Utf8)).alias("QUARTER"))
    
    def _word_frequencies(self, n_top_words):
        logging.info('[WORD FREQUENCY] Starting word frequency procedure.')
        self.word_freqs = {}

        for group, df in self.freq_dfs.items():
            self.word_freqs[group] = {}

            if group == '-':
                classes = list(df['SENTIMENT_CLASS'].unique()) + ['Total']
            else:
                classes = ['Total']

            for sent_class in classes:
                self.word_freqs[group][sent_class] = {}

                for quarter in df["QUARTER"].unique():
                    logging.info(f'[WORD FREQUENCY] Processing "{sent_class} | {quarter}" for group "{group}"...')
                    self.word_freqs[group][sent_class][quarter] = {}
                    quarter_df = df.filter(pl.col("QUARTER") == quarter)

                    # explode the word_list column
                    quarter_df = quarter_df.explode("WORD_LIST").rename({"WORD_LIST": "WORD"})

                    # count the word frequencies
                    word_counts = quarter_df.group_by(['QUARTER', 'WORD']).len().rename({'len': 'FREQUENCY'})

                    # extract the top 30 words
                    top_words = (
                        word_counts
                        .sort(["QUARTER", "FREQUENCY"], descending=[False, True])
                        .group_by("QUARTER")
                        .head(n_top_words)
                    )

                    # create a dictionary where "key" = word, and "value" = count
                    df_temp = top_words.select('WORD', 'FREQUENCY').to_dict(as_series=False)
                    self.word_freqs[group][sent_class][quarter] = dict(zip(df_temp['WORD'], df_temp['FREQUENCY']))
    
    def _export(self, output_dir: str):
        logging.info(f'[EXPORT] Exporting data to \"{output_dir}\"...')
        time_series = {}

        for group, df in self.aggregate_dfs.items():
            time_series[group] = df.sort('DATE').to_dict(as_series=False)

        self.output['time_series'] = time_series
        self.output['word_frequencies'] = self.word_freqs

        with open(output_dir + 'dashboard_data.json', 'w') as fp:
            json.dump(self.output, fp)
    
    def run(self, path_to_file: str, n_top_words: int = 30, output_dir: str = 'data/'):
        self._load_data(path_to_file)
        self._add_sentiment_class()
        self._get_subsets()
        self._aggregate_series()
        self._get_quarters()
        self._word_frequencies(n_top_words)
        self._export(output_dir)
        logging.info("[COMPLETED] Batch procedure completed succesfully!")


if __name__ == "__main__":
    path_to_file = "data/full_polars_df.parquet"
    output_dir = "data/"
    n_top_words = 30

    processor = BatchProcessing()
    processor.run(path_to_file, n_top_words=n_top_words, output_dir=output_dir)
