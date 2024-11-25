import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from modules import params

class VolumePlot():
    def __init__(self):
        pass
    
    def _filters(self):
        type, overlay = st.columns(2)

        with type:
            st.selectbox(
                label=params.VOLUME_PLOT['SELECT_BOX']['LABEL'],
                options=params.VOLUME_PLOT['SELECT_BOX']['OPTIONS'].keys(),
                key=params.VOLUME_PLOT['SELECT_BOX']['KEY'],
                help=params.VOLUME_PLOT['SELECT_BOX']['HELPER']
            )
        with overlay:
            st.toggle(
                label=params.VOLUME_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.VOLUME_PLOT['TOGGLE']['KEY'],
                value=params.VOLUME_PLOT['TOGGLE']['VALUE'],
                help=params.VOLUME_PLOT['TOGGLE']['HELPER']
            )
    
    def _plot(self):
        if params.VOLUME_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.VOLUME_PLOT['SELECT_BOX']['KEY']]] == 'absolute_values':
            count = st.session_state['filtered_data']['data']['time_series']['TOTAL_COUNT']
            daily_mean = int(count.mean())
            y_lab = 'Numero di Post'
        else:
            count = st.session_state['filtered_data']['data']['time_series']['TOTAL_COUNT'] / st.session_state['filtered_data']['benchmark']['time_series']['TOTAL_COUNT']
            daily_mean = f"{round(count.mean() * 100, 1)}%"
            y_lab = 'Percentuale di Post'

        chart_data = {
            'Data': st.session_state['filtered_data']['data']['time_series']['DATE'],
            st.session_state[params.SEMANTIC_GROUPS['KEY']]: count
        }

        colors = [params.VOLUME_PLOT['COLOR']['A']]

        if st.session_state['semantic_group'] != "-" and st.session_state[params.VOLUME_PLOT['TOGGLE']['KEY']] and params.VOLUME_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.VOLUME_PLOT['SELECT_BOX']['KEY']]] == 'absolute_values':
            chart_data['Totale'] = st.session_state['filtered_data']['benchmark']['time_series']['TOTAL_COUNT']
            colors.append(params.VOLUME_PLOT['COLOR']['B'])

        plot_col, stats_col = st.columns([3, 1])    
        with plot_col:
            st.line_chart(
                data = chart_data,
                x = 'Data',
                x_label = 'Data',
                y_label = y_lab,
                color=colors
            )
        with stats_col:
            self._metrics(daily_mean)
    
    def _metrics(self, value):
        st.metric(
            label = 'Media giornaliera',
            value = value
        )
    
    def add(self):
        st.subheader('Volumi', help=params.VOLUME_PLOT['HELPER'])
        self._filters()
        self._plot()

class QuantitativePlot():
    def __init__(self):
        pass

    def _filters(self):
        type, overlay = st.columns(2)

        with type:
            st.selectbox(
                label=params.SENTIMENT_PLOT['SELECT_BOX']['LABEL'],
                options=params.SENTIMENT_PLOT['SELECT_BOX']['OPTIONS'].keys(),
                key=params.SENTIMENT_PLOT['SELECT_BOX']['KEY'],
                help=params.SENTIMENT_PLOT['SELECT_BOX']['HELPER']
            )
            st.session_state['quantitative_window'] = params.SENTIMENT_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.SENTIMENT_PLOT['SELECT_BOX']['KEY']]]

        with overlay:
            st.toggle(
                label=params.SENTIMENT_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.SENTIMENT_PLOT['TOGGLE']['KEY'],
                value=params.SENTIMENT_PLOT['TOGGLE']['VALUE'],
                help=params.SENTIMENT_PLOT['TOGGLE']['HELPER']
            )
    
    def _plot(self):
        chart_data = {
            'Data': st.session_state['filtered_data']['data']['time_series']['DATE']
        }
        colors = [params.SENTIMENT_PLOT['COLOR']['A']]

        if st.session_state['quantitative_window']:
            chart_data[st.session_state['semantic_group']] = st.session_state['filtered_data']['data']['time_series']['SENTIMENT_SCORE'].to_pandas().rolling(window=st.session_state['quantitative_window'], center=True).mean()
            if st.session_state[params.SENTIMENT_PLOT['TOGGLE']['KEY']] and st.session_state[params.SEMANTIC_GROUPS['KEY']] != '-':
                chart_data['Totale'] = st.session_state['filtered_data']['benchmark']['time_series']['SENTIMENT_SCORE'].to_pandas().rolling(window=st.session_state['quantitative_window'], center=True).mean()
                colors.append(params.SENTIMENT_PLOT['COLOR']['B'])
        else:
            chart_data[st.session_state['semantic_group']] = st.session_state['filtered_data']['data']['time_series']['SENTIMENT_SCORE']
            if st.session_state[params.SENTIMENT_PLOT['TOGGLE']['KEY']] and st.session_state[params.SEMANTIC_GROUPS['KEY']] != '-':
                chart_data['Totale'] = st.session_state['filtered_data']['benchmark']['time_series']['SENTIMENT_SCORE']
                colors.append(params.SENTIMENT_PLOT['COLOR']['B'])
        
        plot_col, stats_col = st.columns([3, 1])    
        with plot_col:
            st.line_chart(
                data = chart_data,
                x = 'Data',
                x_label = 'Data',
                y_label = 'Sentiment Index',
                color = colors
            )
        with stats_col:
            self._metrics(round(chart_data[st.session_state['semantic_group']].mean(), 3))
    
    def _metrics(self, value):
        st.metric(
            label = 'Media giornaliera',
            value = value
        )
    
    def add(self):
        st.subheader('Sentiment Index', help=params.SENTIMENT_PLOT['HELPER'])
        self._filters()
        self._plot()

class QualitativePlot():
    def __init__(self):
        pass

    def _filters(self):
        type, overlay = st.columns(2)

        with type:
            st.selectbox(
                label=params.QUALITATIVE_PLOT['SELECT_BOX']['LABEL'],
                options=params.QUALITATIVE_PLOT['SELECT_BOX']['OPTIONS'].keys(),
                key=params.QUALITATIVE_PLOT['SELECT_BOX']['KEY'],
                help=params.QUALITATIVE_PLOT['SELECT_BOX']['HELPER']
            )
            st.session_state['qualitative_window'] = params.QUALITATIVE_PLOT['SELECT_BOX']['OPTIONS'][st.session_state[params.QUALITATIVE_PLOT['SELECT_BOX']['KEY']]]

        with overlay:
            st.toggle(
                label=params.QUALITATIVE_PLOT['TOGGLE']['LABEL'],
                disabled=st.session_state['disable_comparison'],
                key=params.QUALITATIVE_PLOT['TOGGLE']['KEY'],
                value=params.QUALITATIVE_PLOT['TOGGLE']['VALUE'],
                help=params.QUALITATIVE_PLOT['TOGGLE']['HELPER']
            )
    
    def _plot(self):
        chart_data = {
            'Data': st.session_state['filtered_data']['data']['time_series']['DATE']
        }
        colors = [params.QUALITATIVE_PLOT['COLOR']['A']]

        if st.session_state['qualitative_window']:
            chart_data[st.session_state['semantic_group']] = st.session_state['filtered_data']['data']['time_series']['QUALITATIVE_SCORE'].to_pandas().rolling(window=st.session_state['qualitative_window'], center=True).mean()
            if st.session_state[params.QUALITATIVE_PLOT['TOGGLE']['KEY']] and st.session_state[params.SEMANTIC_GROUPS['KEY']] != '-':
                chart_data['Totale'] = st.session_state['filtered_data']['benchmark']['time_series']['QUALITATIVE_SCORE'].to_pandas().rolling(window=st.session_state['qualitative_window'], center=True).mean()
                colors.append(params.QUALITATIVE_PLOT['COLOR']['B'])
        else:
            chart_data[st.session_state['semantic_group']] = st.session_state['filtered_data']['data']['time_series']['QUALITATIVE_SCORE']
            if st.session_state[params.QUALITATIVE_PLOT['TOGGLE']['KEY']] and st.session_state[params.SEMANTIC_GROUPS['KEY']] != '-':
                chart_data['Totale'] = st.session_state['filtered_data']['benchmark']['time_series']['QUALITATIVE_SCORE']
                colors.append(params.QUALITATIVE_PLOT['COLOR']['B'])
        
        plot_col, stats_col = st.columns([3, 1])    
        with plot_col:
            st.line_chart(
                data = chart_data,
                x = 'Data',
                x_label = 'Data',
                y_label = 'Qualitative Index',
                color = colors
            )
        with stats_col:
            self._metrics(round(chart_data[st.session_state['semantic_group']].mean(), 3))
        
    def _metrics(self, value):
        st.metric(
            label = 'Media giornaliera',
            value = value
        )
    
    def add(self):
        st.subheader('Indice Qualitativo', help=params.QUALITATIVE_PLOT['HELPER'])
        self._filters()
        self._plot()

class WordFrequencyPlot():
    def __init__(self):
        pass

    def _filters(self):
        sent_class, filter_group = st.columns(2)

        if st.session_state[params.SEMANTIC_GROUPS['KEY']] == '-':
            disable_classes = False
        else:
            disable_classes = True

        with sent_class:
            st.selectbox(
                label=params.WORD_FREQ_PLOT['SELECT_BOX']['LABEL'],
                disabled=disable_classes,
                options=params.SENTIMENT_CLASSES.keys(),
                key=params.WORD_FREQ_PLOT['SELECT_BOX']['KEY'],
                help=params.WORD_FREQ_PLOT['SELECT_BOX']['HELPER']
            )
        with filter_group:
            st.toggle(
                params.WORD_FREQ_PLOT['TOGGLE']['LABEL'],
                value=True,
                disabled=st.session_state['disable_comparison'],
                key=params.WORD_FREQ_PLOT['TOGGLE']['KEY'],
                help=params.WORD_FREQ_PLOT['TOGGLE']['HELPER'],
            )
    
    def _plot(self):

        if st.session_state[params.SEMANTIC_GROUPS['KEY']] == '-':
            class_filter = st.session_state[params.WORD_FREQ_PLOT['SELECT_BOX']['KEY']]
        else:
            class_filter = '-'

        word_freq_data = st.session_state['filtered_data']['data']['word_freqs']
        word_freq_data = {params.SENTIMENT_CLASSES_MAP[key]: value for key, value in word_freq_data.items()}

        chart_data = word_freq_data[class_filter]
        
        if st.session_state[params.WORD_FREQ_PLOT['TOGGLE']['KEY']] and st.session_state['semantic_group'] != '-':
            chart_data = {
                key: value
                for key, value in chart_data.items()
                if params.SEMANTIC_GROUPS['GROUPS'][st.session_state['semantic_group']] not in key
            }
        
        chart_series = pd.Series(chart_data)

        st.bar_chart(
            data = chart_series[0:15],
            horizontal = True,
            x_label='Numero di occorrenze',
            y_label='',
            color=params.SENTIMENT_CLASSES[st.session_state[params.WORD_FREQ_PLOT['SELECT_BOX']['KEY']]]
        )
    
    def add(self):
        st.subheader('Frequenze delle parole', help=params.WORD_FREQ_PLOT['HELPER'])
        self._filters()
        self._plot()

class SentimentClassTS():
    def __init__(self):
        pass

    def _filters(self):
        st.toggle(
            params.SENTIMENT_CLASS_TS['TOGGLE']['LABEL'],
            value=params.SENTIMENT_CLASS_TS['TOGGLE']['VALUE'],
            key=params.SENTIMENT_CLASS_TS['TOGGLE']['KEY'],
            help=params.SENTIMENT_CLASS_TS['TOGGLE']['HELPER']
        )
    
    def _plot(self):
        data = st.session_state['filtered_data']['data']['time_series'].to_dict(as_series = False)
        chart_data = {params.SENTIMENT_CLASSES_MAP[key]: value for key, value in data.items() if key in params.SENTIMENT_CLASSES_MAP.keys()}
        
        if st.session_state[params.SENTIMENT_CLASS_TS['TOGGLE']['KEY']]:
            for key, value in chart_data.items():
                chart_data[key] = pd.Series(value) / pd.Series(data['TOTAL_COUNT'])
        
        chart_data['DATE'] = data['DATE']
        fig = go.Figure()
        sentiment_classes = [sentiment for sentiment in params.SENTIMENT_CLASSES.keys() if sentiment != '-']

        for sentiment in sentiment_classes:
            fig.add_trace(go.Bar(
                x=chart_data['DATE'],
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
        st.subheader('Serie dei sentiment', help=params.SENTIMENT_CLASS_TS['HELPER'])
        self._filters()
        self._plot()

class SentimentPie():
    def __init__(self):
        pass

    def _plot(self):
        data = st.session_state['filtered_data']['data']['time_series'].to_dict(as_series = False)
        data = {params.SENTIMENT_CLASSES_MAP[key]: value for key, value in data.items() if key in params.SENTIMENT_CLASSES_MAP.keys()}

        chart_data = pd.DataFrame(data).mean()
        
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
        st.subheader('Classi di sentiment', help=params.SENTIMENT_CLASS_PIE['HELPER'])
        self._plot()