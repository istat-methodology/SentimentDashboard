import streamlit as st
from modules.utils import Data
from modules import params

def set_configs():
    st.set_page_config(page_title=params.PAGE_CONFIGS['TITLE'], layout=params.PAGE_CONFIGS['LAYOUT'], initial_sidebar_state=params.PAGE_CONFIGS['SIDEBAR'])

def load_data():
    if st.session_state['initialized'] is False:
        with st.spinner("Caricamento dei dati in corso..."):
            st.session_state['data'] = Data(
                path = params.PATHS['JSON_PATH']
            )
            st.session_state['initialized'] = True
            st.toast("Dati caricati con successo!", icon="✅")

def set_session_states():
    for state, default in params.SESSION_STATES.items():
        if state not in st.session_state:
            st.session_state[state] = default

def set_header():
    st.title(params.HEADER['TITLE'])
    st.markdown(params.HEADER['SUBTITLE'])

def global_filters():
    year, quarter, group, _ = st.columns([2, 2, 3, 7])
    with year:
        st.selectbox(
            label = params.YEAR_FILTER['LABEL'],
            options = params.YEAR_FILTER['YEAR'],
            key = params.YEAR_FILTER['KEY'],
            help = params.YEAR_FILTER['HELPER']
        )
    with quarter:
        st.selectbox(
            label = params.QUARTER_FILTER['LABEL'],
            options = params.QUARTER_FILTER['QUARTER'][st.session_state[params.YEAR_FILTER['KEY']]],
            key = params.QUARTER_FILTER['KEY'],
            help = params.QUARTER_FILTER['HELPER']
        )
    with group:
        st.selectbox(
            label = params.SEMANTIC_GROUPS['LABEL'],
            options=params.SEMANTIC_GROUPS['GROUPS'].keys(),
            key=params.SEMANTIC_GROUPS['KEY'],
            help=params.SEMANTIC_GROUPS['HELPER']
        )

def get_filtered_data():
    filtered_data = st.session_state['data'].filter_data(
        year = st.session_state[params.YEAR_FILTER['KEY']],
        quarter = st.session_state[params.QUARTER_FILTER['KEY']],
        semantic_group = params.SEMANTIC_GROUPS['GROUPS'][st.session_state[params.SEMANTIC_GROUPS['KEY']]]
    )
    benchmark_data = st.session_state['data'].filter_data(
        year = st.session_state[params.YEAR_FILTER['KEY']],
        quarter = st.session_state[params.QUARTER_FILTER['KEY']],
        semantic_group = '-'
    )
    if st.session_state['semantic_group'] == '-':
        st.session_state['disable_comparison'] = True
    else:
        st.session_state['disable_comparison'] = False

    st.session_state['filtered_data'] = {
        'data': filtered_data,
        'benchmark': benchmark_data
    }
