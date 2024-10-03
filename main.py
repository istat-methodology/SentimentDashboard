import streamlit as st
from modules import bits, tabs, params

bits.set_configs()
bits.set_session_states()
bits.set_header()
bits.load_data()
bits.global_filters()

overview_tab, frequency_tab = st.tabs(['Overview', 'Frequency Analysis'])

if st.session_state['data_ready']:
    with overview_tab:
        tabs.OverviewTab().add()

    with frequency_tab:
        tabs.FrequencyTab().add()
    
    with st.sidebar:
        tabs.Sidebar().add()
else:
    st.warning(params.WARNINGS['no_data'])
