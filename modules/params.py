from datetime import date
import os

PAGE_CONFIGS = {
    'TITLE': f'Dashboard (V.{os.getenv("APP_VERSION")})',
    'LAYOUT': 'wide',
    'SIDEBAR': 'expanded'
}

HEADER = {
    'TITLE': 'Dashboard Demo',
    'SUBTITLE': 'Statistica sperimentale: dashboard per il monitoraggio del sentiment social (X) verso i migranti.'
}

GLOBAL_FILTERS = {
    'default_start_date': date(2020, 2, 1),
    'min_start_date': date(2020, 1, 1),
    'max_end_date': date(2020, 12, 31),
    'default_semantic_group': '-'
}

WARNINGS = {
    'no_data': 'Per favore, applica un filtro per iniziare a visualizzare i dati.'
}

LOADING_PARAMS = {
    'data_path': 'data/demo_2020.csv',
    'date_column': 'DATE',
    'sentiment_column': 'SENTIMENT_SCORE',
    'class_column': 'SENTIMENT_CLASS',
    'text_column': 'TEXT'
}

SESSION_STATES = {
    'full_df': None,
    'daily_stats': None,
    'word_freq': None,
    'end_date': date(2020, 4, 30),
    'initialized': False,
    'data_ready': False
}

SEMANTIC_GROUPS = {
    '-': None,
    'Migranti': 'migrant',
    'Immigrati': 'immigra',
    'Clandestini': 'clandestin',
    'Stranieri': 'stranier',
    'Cinesi': 'cines',
    'Italiani': 'italian'
}

SENTIMENT_CLASSES = {
    '-': '#72BF78',
    'Molto Positivi': '#003049',
    'Positivi': '#669bbc',
    'Neutri': '#fdf0d5',
    'Negativi': '#c1121f',
    'Molto Negativi': '#780000'
}

SENTIMENT_CLASSES_MAP = {
    'Strongly Positive': 'Molto Positivi',
    'Positive': 'Positivi',
    'Neutral': 'Neutri',
    'Negative': 'Negativi',
    'Strongly Negative': 'Molto Negativi'
}

TABS = [
    'Overview',
    'Frequency Analysis',
    'Sentiment Analysis',
    'ℹ️ Info'
]

ROLLING_MEAN = {
    "-": None,
    "7 Giorni": 7,
    "30 Giorni": 30
}

VOLUME_PLOT = {
    'SELECT_BOX': {
        'LABEL': 'Seleziona serie',
        'OPTIONS': {
            'Valori assoluti': 'absolute_values',
            'Percentuali': 'percentage'
        },
        'KEY': 'series_type_volumes'
    },
    'TOGGLE': {
        'LABEL': 'Aggiungi totale',
        'VALUE': False,
        'KEY': 'overlay_volume'
    },
    'COLOR': {
        'A': '#0077b6',
        'B': '#00b4d8'
    }
}

SENTIMENT_PLOT = {
    'SELECT_BOX': {
        'LABEL': 'Media mobile',
        'OPTIONS': ROLLING_MEAN,
        'KEY': 'ma_sentiment'
    },
    'TOGGLE': {
        'LABEL': 'Aggiungi totale',
        'VALUE': False,
        'KEY': 'overlay_sentiment'
    },
    'COLOR': {
        'A': '#2b9348',
        'B': '#80b918'
    }
}

QUALITATIVE_PLOT = {
    'SELECT_BOX': {
        'LABEL': 'Media mobile',
        'OPTIONS': ROLLING_MEAN,
        'KEY': 'ma_qualitative'
    },
    'TOGGLE': {
        'LABEL': 'Aggiungi totale',
        'VALUE': False,
        'KEY': 'overlay_qualitative'
    },
    'COLOR': {
        'A': '#921A40',
        'B': '#C75B7A'
    }
}

SIDEBAR = {
    'SELECT_BOX': {
        'LABEL': 'Rispetto a',
        'OPTIONS': ['Totale periodo (stesso gruppo)', 'Totale gruppi (stesso periodo)'],
        'KEY': 'comparison_term'
    }
}

WORD_FREQ_PLOT = {
    'SELECT_BOX': {
        'LABEL': 'Seleziona classe',
        'OPTIONS': SENTIMENT_CLASSES.keys(),
        'KEY': 'sentiment_class_wf'
    },
    'TOGGLE': {
        'LABEL': 'Filtra',
        'VALUE': False,
        'KEY': 'filter_wf'
    },
}

SENTIMENT_CLASS_TS = {
    'TOGGLE': {
        'LABEL': 'Normalizza',
        'VALUE': True,
        'KEY': 'normalize_sentiment_class'
    },
}
