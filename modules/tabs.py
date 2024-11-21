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
                key=params.VOLUME_PLOT['SELECT_BOX']['KEY'],
                help=params.VOLUME_PLOT['SELECT_BOX']['HELPER']
            )
        with col2:
            st.toggle(
                label=params.VOLUME_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.VOLUME_PLOT['TOGGLE']['KEY'],
                value=params.VOLUME_PLOT['TOGGLE']['VALUE'],
                help=params.VOLUME_PLOT['TOGGLE']['HELPER']
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
                key=params.SENTIMENT_PLOT['SELECT_BOX']['KEY'],
                help=params.SENTIMENT_PLOT['SELECT_BOX']['HELPER']
            )
            window = params.SENTIMENT_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.SENTIMENT_PLOT['SELECT_BOX']['KEY']]]
        with col2:
            st.toggle(
                label=params.SENTIMENT_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.SENTIMENT_PLOT['TOGGLE']['KEY'],
                value=params.SENTIMENT_PLOT['TOGGLE']['VALUE'],
                help=params.SENTIMENT_PLOT['TOGGLE']['HELPER']
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
    

    def add(self):
        counts, quant = st.columns(2)

        with counts:
            graph, stats = st.columns([4, 1])
            if st.session_state['data_ready']:
                with graph:
                    st.subheader('Volumi', help=params.VOLUME_PLOT['HELPER'])
                    self._plot_volumes()
                with stats:
                    avg_volume = st.session_state['daily_stats']['word_filtered']['Count'].mean()
                    st.metric('Volume medio', int(avg_volume))
        
        with quant:
            graph, stats = st.columns([4, 1])
            if st.session_state['data_ready']:
                with graph:
                    st.subheader('Sentiment Quantitativo', help=params.SENTIMENT_PLOT['HELPER'])
                    self._plot_quantitative()
                with stats:
                    avg_sentiment_quant = st.session_state['daily_stats']['word_filtered']['Sentiment'].mean()
                    st.metric('Sentiment medio', round(avg_sentiment_quant, 4))
                

class FrequencyTab():
    def __init__(self):
        pass

    def _plot_qualitative(self):
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox(
                label=params.QUALITATIVE_PLOT['SELECT_BOX']['LABEL'],
                options=params.QUALITATIVE_PLOT['SELECT_BOX']['OPTIONS'].keys(),
                disabled=False,
                key=params.QUALITATIVE_PLOT['SELECT_BOX']['KEY'],
                help=params.QUALITATIVE_PLOT['SELECT_BOX']['HELPER']
            )
            window = params.QUALITATIVE_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.QUALITATIVE_PLOT['SELECT_BOX']['KEY']]]
        with col2:
            st.toggle(
                label=params.QUALITATIVE_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.QUALITATIVE_PLOT['TOGGLE']['KEY'],
                value=params.QUALITATIVE_PLOT['TOGGLE']['VALUE'],
                help=params.QUALITATIVE_PLOT['TOGGLE']['HELPER']
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

    def _plot_word_freqs(self):
        col1, col2 = st.columns(2)
        if st.session_state['semantic_group'] == '-':
            disable_classes = False
        else:
            disable_classes = True
        with col1:
            st.selectbox(
                label=params.WORD_FREQ_PLOT['SELECT_BOX']['LABEL'],
                disabled=disable_classes,
                options=params.SENTIMENT_CLASSES.keys(),
                key=params.WORD_FREQ_PLOT['SELECT_BOX']['KEY'],
                help=params.WORD_FREQ_PLOT['SELECT_BOX']['HELPER']
            )
        with col2:
            st.toggle(
                params.WORD_FREQ_PLOT['TOGGLE']['LABEL'],
                value=True,
                disabled=st.session_state['disable_comparison'],
                key=params.WORD_FREQ_PLOT['TOGGLE']['KEY'],
                help=params.WORD_FREQ_PLOT['TOGGLE']['HELPER'],
            )
        chart_data = st.session_state['full_df'].extract_top_words(class_filter=st.session_state[params.WORD_FREQ_PLOT['SELECT_BOX']['KEY']], top_n=100)
        
        if st.session_state[params.WORD_FREQ_PLOT['TOGGLE']['KEY']] and st.session_state['semantic_group'] != '-':
            chart_data = chart_data.filter(
                ~pl.col('word').str.contains(params.SEMANTIC_GROUPS['GROUPS'][st.session_state['semantic_group']],literal=True)
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
        st.toggle(
            params.SENTIMENT_CLASS_TS['TOGGLE']['LABEL'],
            value=params.SENTIMENT_CLASS_TS['TOGGLE']['VALUE'],
            key=params.SENTIMENT_CLASS_TS['TOGGLE']['KEY'],
            help=params.SENTIMENT_CLASS_TS['TOGGLE']['HELPER']
        )
        
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
    
    def _plot_classes_pie(self):
        chart_data = st.session_state['full_df'].extract_classes_ts(
            normalize=st.session_state[params.SENTIMENT_CLASS_TS['TOGGLE']['KEY']],
            classes_columns=params.SENTIMENT_CLASSES_MAP.keys()
        ).drop('DATE').to_pandas().mean()

        colors = [params.SENTIMENT_CLASSES[label] for label in chart_data.index]

        fig = go.Figure(
            data=[go.Pie(
                labels=chart_data.index,
                values=chart_data.values, 
                hoverinfo='label+percent', 
                textinfo='percent',
                marker=dict(colors=colors)
            )]
        )
        fig.update_layout(
            template='plotly_dark',
            bargap=0.0,
            bargroupgap=0.0,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=120
            ),
        )
        st.plotly_chart(fig)
        
    def add(self):
        qual, bars = st.columns(2)

        with qual:
            graph, stats = st.columns([4, 1])
            if st.session_state['data_ready']:
                with graph:
                    st.subheader('Sentiment Qualitativo', help=params.QUALITATIVE_PLOT['HELPER'])
                    self._plot_qualitative()
                with stats:
                    avg_sentiment_qual = st.session_state['daily_stats']['word_filtered']['Qualitative Index'].mean()
                    st.metric('Indice medio', round(avg_sentiment_qual, 3))

        
        with bars:
            if st.session_state['data_ready']:
                st.subheader("Frequenze Sentiment", help=params.SENTIMENT_CLASS_TS['HELPER'])
                self._plot_classes()

        freqs, _, pie, _ = st.columns([2, 1, 2, 1])

        with freqs:
            if st.session_state['data_ready']:
                st.subheader("Frequenze Parole", help=params.WORD_FREQ_PLOT['HELPER'])
                self._plot_word_freqs()
        
        with pie:
            if st.session_state['data_ready']:
                st.subheader("Frequenze Sentiment Medie", help=params.SENTIMENT_CLASS_PIE['HELPER'])
                self._plot_classes_pie()


class Sidebar():

    def __init__(self):
        pass

    def add(self):
        st.subheader('Info')
        st.metric("Gruppo semantico selezionato", value=st.session_state['semantic_group'])
        st.selectbox(
            label=params.SIDEBAR['SELECT_BOX']['LABEL'],
            options=params.SIDEBAR['SELECT_BOX']['OPTIONS'],
            key=params.SIDEBAR['SELECT_BOX']['KEY'],
            disabled=not st.session_state['data_ready'],
            help=params.SIDEBAR['SELECT_BOX']['HELPER']
        )
        if st.session_state['data_ready']:
            if st.session_state['comparison_term'] == 'Totale periodo (stesso gruppo)':
                volume_comparison = int(st.session_state['daily_stats']['word_filtered_full']['Count'].mean())
                sentiment_comparison = st.session_state['daily_stats']['word_filtered_full']['Sentiment'].mean()
                delta_num_volume = round((int(st.session_state['daily_stats']['word_filtered']['Count'].mean()) - volume_comparison)*100 / volume_comparison, 2)
                delta_sign_volume = '+' if delta_num_volume >= 0 else ''
                delta_volume = f"{delta_sign_volume}{delta_num_volume}%"
                delta_color_volume = "normal"

                delta_num_sentiment = round((st.session_state['daily_stats']['date_filtered']['Sentiment'].mean() - sentiment_comparison)*100 / sentiment_comparison, 2)
                delta_sign_sentiment = '+' if delta_num_sentiment >= 0 else ''
                delta_sentiment = f"{delta_sign_sentiment}{delta_num_sentiment}%"

            elif st.session_state['comparison_term'] == 'Totale gruppi (stesso periodo)':
                volume_comparison = int(st.session_state['daily_stats']['date_filtered']['Count'].mean())
                sentiment_comparison = st.session_state['daily_stats']['date_filtered']['Sentiment'].mean()
                delta_volume = f"{round(st.session_state['daily_stats']['word_filtered']['Count'].mean()*100 / volume_comparison, 2)}% dei Tweet"
                delta_color_volume = "off"
                delta_num_sentiment = -round((st.session_state['daily_stats']['word_filtered']['Sentiment'].mean() - sentiment_comparison)*100 / sentiment_comparison, 2)
                delta_sign_sentiment = '+' if delta_num_sentiment >= 0 else ''
                delta_sentiment = f"{delta_sign_sentiment}{delta_num_sentiment}%"
            
            st.write(
                """
                <style>
                [data-testid="stMetricDelta"] svg {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            
            if st.session_state['semantic_group'] == '-':
                st.metric("Volume giornaliero medio", int(st.session_state['daily_stats']['word_filtered']['Count'].mean()))
                st.metric("Sentiment quantitativo medio", round(st.session_state['daily_stats']['word_filtered']['Sentiment'].mean(), 4))
            else:
                st.metric(
                    f"Volume giornaliero medio ({st.session_state['semantic_group']})",
                    int(st.session_state['daily_stats']['word_filtered']['Count'].mean()),
                    delta=delta_volume,
                    delta_color=delta_color_volume
                )
                st.metric(
                    f"Sentiment quantitativo medio ({st.session_state['semantic_group']})",
                    round(st.session_state['daily_stats']['word_filtered']['Sentiment'].mean(), 4),
                    delta=delta_sentiment
                )