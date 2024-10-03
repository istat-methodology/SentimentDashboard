import streamlit as st
import polars as pl
import plotly.graph_objects as go
from modules import params

class OverviewTab():
    def __init__(self):
        pass

    def _plot_volumes(self):
        col1, col2 = st.columns(2)

        with col1:
            st.selectbox(
                label=params.VOLUME_PLOT['SELECT_BOX']['LABEL'],
                options=params.VOLUME_PLOT['SELECT_BOX']['OPTIONS'].keys(),
                disabled=st.session_state['disable_comparison'],
                key=params.VOLUME_PLOT['SELECT_BOX']['KEY']
            )
        with col2:
            st.toggle(
                label=params.VOLUME_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.VOLUME_PLOT['TOGGLE']['KEY']
            )
        
        if params.VOLUME_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.VOLUME_PLOT['SELECT_BOX']['KEY']]] == 'absolute_values':
            counts = st.session_state['daily_stats']['word_filtered']['Count']
        else:
            counts = st.session_state['daily_stats']['word_filtered']['Count'] / st.session_state['daily_stats']['date_filtered']['Count']

        chart_data = {}
        chart_data['Date'] = st.session_state['daily_stats']['word_filtered']['DATE']
        chart_data[st.session_state['semantic_group']] = counts
        colors = [params.VOLUME_PLOT['COLOR']['A']]

        if st.session_state['semantic_group'] != "-" and st.session_state[params.VOLUME_PLOT['TOGGLE']['KEY']] and params.VOLUME_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.VOLUME_PLOT['SELECT_BOX']['KEY']]] == 'absolute_values':
            chart_data['Totale'] = st.session_state['daily_stats']['date_filtered']['Count']
            colors.append(params.VOLUME_PLOT['COLOR']['B'])

        st.line_chart(chart_data, x='Date', color=colors, x_label='Data', y_label='Numero di Tweet')
    
    def _plot_quantitative(self):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                label=params.SENTIMENT_PLOT['SELECT_BOX']['LABEL'],
                options=params.SENTIMENT_PLOT['SELECT_BOX']['OPTIONS'].keys(),
                disabled=False,
                key=params.SENTIMENT_PLOT['SELECT_BOX']['KEY']
            )
            window = params.SENTIMENT_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.SENTIMENT_PLOT['SELECT_BOX']['KEY']]]
        with col2:
            st.toggle(
                label=params.SENTIMENT_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.SENTIMENT_PLOT['TOGGLE']['KEY']
            )
        chart_data = {}
        chart_data['Date'] = st.session_state['daily_stats']['word_filtered']['DATE']
        if window:
            chart_data[st.session_state['semantic_group']] = st.session_state['daily_stats']['word_filtered']['Sentiment'].to_pandas().rolling(window=window, center=True).mean()
        else:
            chart_data[st.session_state['semantic_group']] = st.session_state['daily_stats']['word_filtered']['Sentiment']

        colors = [params.SENTIMENT_PLOT['COLOR']['A']]
        
        if st.session_state['semantic_group'] != "-" and st.session_state[params.SENTIMENT_PLOT['TOGGLE']['KEY']]:
            if window:
                chart_data['Totale'] = st.session_state['daily_stats']['date_filtered']['Sentiment'].to_pandas().rolling(window=window, center=True).mean()
            else:
                chart_data['Totale'] = st.session_state['daily_stats']['date_filtered']['Sentiment']
            colors.append(params.SENTIMENT_PLOT['COLOR']['B'])

        st.line_chart(chart_data, x='Date', color=colors, x_label='Data', y_label='Score')
    
    def _plot_qualitative(self):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                label=params.QUALITATIVE_PLOT['SELECT_BOX']['LABEL'],
                options=params.QUALITATIVE_PLOT['SELECT_BOX']['OPTIONS'].keys(),
                disabled=False,
                key=params.QUALITATIVE_PLOT['SELECT_BOX']['KEY']
            )
            window = params.QUALITATIVE_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.QUALITATIVE_PLOT['SELECT_BOX']['KEY']]]
        with col2:
            st.toggle(
                label=params.QUALITATIVE_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.QUALITATIVE_PLOT['TOGGLE']['KEY']
            )
        chart_data = {}
        chart_data['Date'] = st.session_state['daily_stats']['word_filtered']['DATE']
        if window:
            chart_data[st.session_state['semantic_group']] = st.session_state['daily_stats']['word_filtered']['Qualitative Index'].to_pandas().rolling(window=window, center=True).mean()
        else:
            chart_data[st.session_state['semantic_group']] = st.session_state['daily_stats']['word_filtered']['Qualitative Index']
        colors = [params.QUALITATIVE_PLOT['COLOR']['A']]

        if st.session_state['semantic_group'] != "-" and st.session_state[params.QUALITATIVE_PLOT['TOGGLE']['KEY']]:
            if window:
                chart_data['Totale'] = st.session_state['daily_stats']['date_filtered']['Qualitative Index'].to_pandas().rolling(window=window, center=True).mean()
            else:
                chart_data['Totale'] = st.session_state['daily_stats']['date_filtered']['Qualitative Index']
            colors.append(params.QUALITATIVE_PLOT['COLOR']['B'])

        st.line_chart(chart_data, x='Date', color=colors, x_label='Data', y_label='Score')

    def add(self):
        counts, quant, qual = st.columns(3)

        with counts:
            if st.session_state['data_ready']:
                st.subheader('Volumi')
                self._plot_volumes()
        
        with quant:
            if st.session_state['data_ready']:
                st.subheader('Sentiment Quantitativo')
                self._plot_quantitative()
        
        with qual:
            if st.session_state['data_ready']:
                st.subheader('Sentiment Qualitativo')
                self._plot_qualitative()
                

class FrequencyTab():
    def __init__(self):
        pass

    def _plot_word_freqs(self):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                label=params.WORD_FREQ_PLOT['SELECT_BOX']['LABEL'],
                options=params.SENTIMENT_CLASSES.keys(),
                key=params.WORD_FREQ_PLOT['SELECT_BOX']['KEY']
            )
        with col2:
            st.toggle(
                params.WORD_FREQ_PLOT['TOGGLE']['LABEL'],
                value=True,
                disabled=st.session_state['disable_comparison'],
                key=params.WORD_FREQ_PLOT['TOGGLE']['KEY']
            )
        chart_data = st.session_state['full_df'].extract_top_words(class_filter=st.session_state[params.WORD_FREQ_PLOT['SELECT_BOX']['KEY']], top_n=100)
        
        if st.session_state[params.WORD_FREQ_PLOT['TOGGLE']['KEY']] and st.session_state['semantic_group'] != '-':
            chart_data = chart_data.filter(
                ~pl.col('word').str.contains(params.SEMANTIC_GROUPS[st.session_state['semantic_group']],literal=True)
            )

        st.bar_chart(
            data=chart_data[0:15],
            x='word',
            y='count',
            x_label='Occorrenze',
            y_label='',
            horizontal=True,
            color=params.SENTIMENT_CLASSES[st.session_state[params.WORD_FREQ_PLOT['SELECT_BOX']['KEY']]]
        )
    
    def _plot_classes(self):
        st.toggle(params.SENTIMENT_CLASS_TS['TOGGLE']['LABEL'], value=params.SENTIMENT_CLASS_TS['TOGGLE']['VALUE'], key=params.SENTIMENT_CLASS_TS['TOGGLE']['KEY'])
        
        chart_data = st.session_state['full_df'].extract_classes_ts(
            normalize=st.session_state[params.SENTIMENT_CLASS_TS['TOGGLE']['KEY']],
            classes_columns=params.SENTIMENT_CLASSES_MAP.keys()
        )
        fig = go.Figure()
        sentiment_classes = [sentiment for sentiment in params.SENTIMENT_CLASSES.keys() if sentiment != '-']
        for sentiment in sentiment_classes:
            fig.add_trace(go.Bar(
                x=chart_data[params.LOADING_PARAMS['date_column']],
                y=chart_data[sentiment],
                name=sentiment,
                marker_color=params.SENTIMENT_CLASSES[sentiment]
            ))
        fig.update_layout(
            barmode='stack',
            xaxis_tickformat="%Y-%m-%d",
            template="simple_white",
            bargap=0.0,
            bargroupgap=0.0,
            margin=dict(
                l=20,
                r=20,
                t=0,
                b=120
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        st.plotly_chart(fig)
        
    def add(self):
        freqs, bars = st.columns([1,2])

        with freqs:
            if st.session_state['data_ready']:
                st.subheader("Frequenze Parole")
                self._plot_word_freqs()
        
        with bars:
            if st.session_state['data_ready']:
                st.subheader("Frequenze Sentiment")
                self._plot_classes()

class Sidebar():

    def __init__(self):
        pass

    def add(self):
        st.subheader('Info')
        st.selectbox(
            label=params.SIDEBAR['SELECT_BOX']['LABEL'],
            options=params.SIDEBAR['SELECT_BOX']['OPTIONS'],
            key=params.SIDEBAR['SELECT_BOX']['KEY'],
            disabled=not st.session_state['data_ready']
        )
        if st.session_state['data_ready']:
            if st.session_state['comparison_term'] == 'Totale periodo (stesso gruppo)':
                volume_comparison = int(st.session_state['daily_stats']['full']['Count'].mean())
                sentiment_comparison = st.session_state['daily_stats']['full']['Sentiment'].mean()

            elif st.session_state['comparison_term'] == 'Totale gruppi (stesso periodo)':
                volume_comparison = int(st.session_state['daily_stats']['date_filtered']['Count'].mean())
                sentiment_comparison = st.session_state['daily_stats']['date_filtered']['Sentiment'].mean()
            
            if st.session_state['semantic_group'] == '-':
                st.metric("Volume giornaliero medio", int(st.session_state['daily_stats']['word_filtered']['Count'].mean()))
                st.metric("Sentiment quantitativo medio", round(st.session_state['daily_stats']['word_filtered']['Sentiment'].mean(), 4))
            else:
                st.metric(
                    f"Volume giornaliero medio ({st.session_state['semantic_group']})",
                    int(st.session_state['daily_stats']['word_filtered']['Count'].mean()),
                    delta=int(st.session_state['daily_stats']['word_filtered']['Count'].mean()) - volume_comparison
                )
                st.metric(
                    f"Sentiment quantitativo medio ({st.session_state['semantic_group']})",
                    round(st.session_state['daily_stats']['word_filtered']['Sentiment'].mean(), 4),
                    delta=round(st.session_state['daily_stats']['word_filtered']['Sentiment'].mean() - sentiment_comparison, 4)
                )