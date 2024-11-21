import streamlit as st
from modules import utils
from modules.utils import Corpus
from modules import params

def set_configs():
    st.set_page_config(page_title=params.PAGE_CONFIGS['TITLE'], layout=params.PAGE_CONFIGS['LAYOUT'], initial_sidebar_state=params.PAGE_CONFIGS['SIDEBAR'])

def set_session_states():
    for state, default in params.SESSION_STATES.items():
        if state not in st.session_state:
            st.session_state[state] = default

def set_header():
    st.title(params.HEADER['TITLE'])
    st.markdown(params.HEADER['SUBTITLE'])

def global_filters():  
    year, quarter, group, _ = st.columns([1, 1, 2, 4])
    with year:
        st.selectbox(
            'Seleziona Anno',
            options=params.YEAR_FILTER['YEAR'],
            key=params.YEAR_FILTER['KEY'],
            help=params.YEAR_FILTER['HELPER']
        )
    with quarter:
        st.selectbox(
            'Seleziona Trimestre',
            options=params.QUARTER_FILTER['QUARTER'][st.session_state[params.YEAR_FILTER['KEY']]],
            key=params.QUARTER_FILTER['KEY'],
            help=params.QUARTER_FILTER['HELPER']
        )
    with group:
        st.selectbox(
            'Seleziona gruppo semantico',
            options=params.SEMANTIC_GROUPS['GROUPS'].keys(),
            key='semantic_group_tmp',
            help=params.SEMANTIC_GROUPS['HELPER']
        )
    
    date_filter = utils.get_date(st.session_state[params.YEAR_FILTER['KEY']], st.session_state[params.QUARTER_FILTER['KEY']], params.QUARTER_FILTER['MAPPING'])

    def update_data():
        st.session_state['daily_stats'] = st.session_state['full_df'].filter_data(
            start_date=date_filter.start_date(),
            end_date=date_filter.end_date(),
            word_filter=params.SEMANTIC_GROUPS['GROUPS'][st.session_state['semantic_group_tmp']]
        )
        if st.session_state['semantic_group_tmp'] == '-':
            st.session_state['disable_comparison'] = True
        else:
            st.session_state['disable_comparison'] = False
        st.session_state['data_ready'] = True
        st.session_state['semantic_group'] = st.session_state['semantic_group_tmp']

    st.button("Filtra", on_click=update_data)

def load_data():
    if st.session_state['initialized'] is False:
        with st.spinner("Caricamento dei dati in corso..."):
            st.session_state['full_df'] = Corpus(
                path=params.LOADING_PARAMS['data_path'],
                date_column=params.LOADING_PARAMS['date_column'],
                sentiment_column=params.LOADING_PARAMS['sentiment_column'],
                class_column=params.LOADING_PARAMS['class_column'],
                text_column=params.LOADING_PARAMS['text_column']
            )
            st.session_state['initialized'] = True
            st.toast("Dati caricati con successo!", icon="✅")

