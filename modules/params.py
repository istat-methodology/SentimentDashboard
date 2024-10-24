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
    'GROUPS': {
        '-': None,
        'Migranti': 'migrant',
        'Immigrati': 'immigra',
        'Clandestini': 'clandestin',
        'Stranieri': 'stranier',
        'Cinesi': 'cines',
        'Italiani': 'italian'
    },
    'HELPER': """Questa selezione permette di filtrare i Tweet che contengono parole relative a uno specifico gruppo semantico. Ad esempio, se si seleziona 'Stranieri', si otterranno tutti i Tweet contenenti le parole 'straniera', 'straniero', 'straniere', 'stranieri'."""
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
        'KEY': 'series_type_volumes',
        'HELPER': """**Valori assoluti**: numero effettivo di Tweet in un giorno.\n\n**Percentuali**: rapporto tra il numero effettivo di Tweet in un giorno per il gruppo semantico selezionato e il numero totale di Tweet nello stesso giorno."""
    },
    'TOGGLE': {
        'LABEL': 'Aggiungi totale',
        'VALUE': True,
        'KEY': 'overlay_volume',
        'HELPER': """Aggiungi alla visualizzazione dei volumi i Tweet non filtrati per gruppo semantico."""
    },
    'COLOR': {
        'A': '#0077b6',
        'B': '#00b4d8'
    },
    'HELPER': 'Questa serie indica la quantità giornaliera di Tweet nel dataset.'
}

SENTIMENT_PLOT = {
    'SELECT_BOX': {
        'LABEL': 'Media mobile',
        'OPTIONS': ROLLING_MEAN,
        'KEY': 'ma_sentiment'
    },
    'TOGGLE': {
        'LABEL': 'Aggiungi totale',
        'VALUE': True,
        'KEY': 'overlay_sentiment',
        'HELPER': """Aggiungi alla visualizzazione dell'indice di sentiment quantitativo i Tweet non filtrati per gruppo semantico."""
    },
    'COLOR': {
        'A': '#2b9348',
        'B': '#80b918'
    },
    'HELPER': """L'indice di sentiment quantitativo viene calcolato tramite l'utilizzo di coordinate polari. Il valore giornaliero dell'indice è ottenuto come media pesata delle polarità."""
}

QUALITATIVE_PLOT = {
    'SELECT_BOX': {
        'LABEL': 'Media mobile',
        'OPTIONS': ROLLING_MEAN,
        'KEY': 'ma_qualitative'
    },
    'TOGGLE': {
        'LABEL': 'Aggiungi totale',
        'VALUE': True,
        'KEY': 'overlay_qualitative',
        'HELPER': """Aggiungi alla visualizzazione dell'indice di sentiment qualitativo i Tweet non filtrati per gruppo semantico."""
    },
    'COLOR': {
        'A': '#921A40',
        'B': '#C75B7A'
    },
    'HELPER': """L'indice di sentiment qualitativo è ottenuto a partire dall'indice di sentiment quantitativo. Si tratta di una classificazione a 5 classi ('Molto Positivo', 'Positivo', 'Neutro', 'Negativo', 'Molto Negativo') che viene effettuata per ogni Tweet in base alle polarità positive e negative. L'indice giornaliero è ottenuto come differenza tra i Tweet classificati come positivi (o molto positivi) e i Tweet classificati come negativi (o molto negativi) sul totale di Tweet giornalieri."""
}

SIDEBAR = {
    'SELECT_BOX': {
        'LABEL': 'Rispetto a',
        'OPTIONS': ['Totale periodo (stesso gruppo)', 'Totale gruppi (stesso periodo)'],
        'KEY': 'comparison_term',
        'HELPER': """**Totale periodo (stesso gruppo)**: Confronto tra Tweet contenenti parole del gruppo semantico selezionato nel periodo selezionato e Tweet contenenti parole del gruppo semantico selezionato nel periodo totale.\n\n**Totale gruppi (stesso periodo)**: Confronto tra Tweet contenenti parole del gruppo semantico selezionato nel periodo selezionato e Tweet non filtrati per gruppo semantico nel periodo selezionato."""
    }
}

WORD_FREQ_PLOT = {
    'SELECT_BOX': {
        'LABEL': 'Seleziona classe',
        'OPTIONS': SENTIMENT_CLASSES.keys(),
        'KEY': 'sentiment_class_wf',
        'HELPER': """Filtra i Tweet per classe di sentiment. Le frequenze delle parole saranno calcolate solamente sui Tweet filtrati. Ad esempio, se viene selezionata la classe 'Negativi', il bar plot mostrerà le frequenze delle parole solamente nei Tweet classificati come negativi."""
    },
    'TOGGLE': {
        'LABEL': 'Filtra',
        'VALUE': False,
        'KEY': 'filter_wf',
        'HELPER': """Nel caso in cui venga selezionato un gruppo semantico, questo switch permette di nascondere le parole appartenenti al gruppo semantico dalla visualizzazione."""
    },
    'HELPER': """Questa visualizzazione mostra le parole più frequenti nel periodo selezionato."""
}

SENTIMENT_CLASS_TS = {
    'TOGGLE': {
        'LABEL': 'Normalizza',
        'VALUE': True,
        'KEY': 'normalize_sentiment_class',
        'HELPER': """Questo switch permette di normalizzare le barre tra 0 e 1. Ogni gruppo di barre corrisponde a un giorno. Se disattivato, l'altezza di ogni gruppo di barre rappresenterà il numero totale di Tweet presenti nel giorno."""
    },
    'HELPER': """Questa visualizzazione mostra la ripartizione giornaliera tra Tweet classificati come 'Molto Positivi', 'Positivi', 'Neutri', 'Negativi' e 'Molto Negativi'."""
}
