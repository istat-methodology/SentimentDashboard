import streamlit as st
import streamlit_nested_layout
from modules import bits, plots

bits.set_configs()
bits.set_header()
bits.set_session_states()
bits.load_data()
bits.global_filters()
#bits.get_filtered_data()

overview_tab, frequency_tab, debug = st.tabs(['Overview', 'Frequency Analysis', 'Debug'])

#with overview_tab:
#    col1, col2 = st.columns(2)
#    with col1:
#        plots.VolumePlot().add()
#    with col2:
#        plots.QuantitativePlot().add()
#
#with frequency_tab:
#    col1, col2 = st.columns(2)
#    with col1:
#        plots.QualitativePlot().add()
#    with col2:
#        plots.SentimentClassTS().add()
#    
#    col3, col4 = st.columns(2)
#    with col3:
#        plots.WordFrequencyPlot().add()
#    with col4:
#        plots.SentimentPie().add()

with debug:
    st.json(st.session_state['data'].data)