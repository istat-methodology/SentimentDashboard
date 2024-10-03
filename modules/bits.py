import streamlit as st
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
    col1, col2, col3, _ = st.columns([1, 1, 2, 4])
    with col1:
        st.date_input('Da', params.GLOBAL_FILTERS['default_start_date'], min_value=params.GLOBAL_FILTERS['min_start_date'], max_value=st.session_state['end_date'], key='start_date')
    with col2:
        st.date_input('A', min_value=st.session_state['start_date'], max_value=params.GLOBAL_FILTERS['max_end_date'], key='end_date')
    with col3:
        st.selectbox('Gruppo semantico', options=params.SEMANTIC_GROUPS.keys(), key='semantic_group_tmp')

    def update_data():
        st.session_state['daily_stats'] = st.session_state['full_df'].filter_data(
            start_date=st.session_state['start_date'],
            end_date=st.session_state['end_date'],
            word_filter=params.SEMANTIC_GROUPS[st.session_state['semantic_group_tmp']]
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

