import datetime as dt, pickle, time
import os,re,pandas as pd
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px, plotly.graph_objects as go
import matplotlib.pyplot as plt, matplotlib.colors as mtpcl
from pylab import cm
from dorianUtils.dccExtendedD import DccExtended
from dorianUtils.utilsD import Utils
import smallPowerDash.configFilesSmallPower as cfs

class SmallPowerTab():
    ''' computation tab '''

    def __init__(self,app,baseId):
        self.baseId=baseId
        self.app = app
        self.utils = Utils()
        self.dccE = DccExtended()
    # ==========================================================================
    #                           SHARED FUNCTIONS CALLBACKS
    # ==========================================================================
    def buildLayoutLocal(self,dicWidgets,baseId,widthG=80,nbGraphs=1,nbCaches=0):
        widgetLayout,dicLayouts = [],{}
        for wid_key,wid_val in dicWidgets.items():
            if 'dd_computation' in wid_key:
                widgetObj = self.dccE.dropDownFromList(baseId+wid_key,self.computationGraphs,
                                                        'what should be computed ?',value = wid_val)
            elif 'dd_cmap' in wid_key:
                widgetObj = self.dccE.dropDownFromList(baseId+wid_key,self.utils.cmapNames[0],
                                                'select the colormap : ',value=wid_val)

            elif 'dd_resampleMethod' in wid_key:
                widgetObj = self.dccE.dropDownFromList(baseId+wid_key,['mean','max','min','median'],
                'Select the resampling method: ',value=wid_val,multi=False)

            elif 'dd_style' in wid_key:
                widgetObj = self.dccE.dropDownFromList(baseId+wid_key,self.spd.graphStyles,'Select the style : ',value = wid_val)

            elif 'dd_expand' in wid_key:
                widgetObj = self.dccE.dropDownFromList(baseId+wid_key,['groups','tags'],'Select the option : ',value = wid_val)

            elif 'btn_export' in wid_key:
                widgetObj = [html.Button('export .txt',id=baseId+wid_key, n_clicks=wid_val)]


            elif 'in_timeRes' in wid_key:
                widgetObj = [html.P('time resolution : '),
                dcc.Input(id=baseId+wid_key,placeholder='time resolution : ',type='text',value=wid_val)]

            elif 'pdr_time' in wid_key :
                tmax=wid_val
                # if not tmax : tmax = dt.datetime.now()
                if not tmax :
                    tmax = self.utils.findDateInFilename(self.cfg.listFilesPkl[-1])
                t1 = tmax - dt.timedelta(hours=tmax.hour+1)
                t0 = t1 - dt.timedelta(days=2)

                widgetObj = [
                html.Div([
                    dbc.Row([dbc.Col(html.P('select start and end time : ')),
                        dbc.Col(html.Button(id  = baseId + wid_key + 'Btn',children='update Time'))]),

                    dbc.Row([dbc.Col(dcc.DatePickerRange( id = baseId + wid_key + 'Pdr',
                                max_date_allowed = tmax, initial_visible_month = t0.date(),
                                display_format = 'MMM D, YY',minimum_nights=0,
                                start_date = t0.date(), end_date   = t1.date()))]),

                    dbc.Row([dbc.Col(dcc.Input(id = baseId + wid_key + 'Start',type='text',value = '07:00',size='13',style={'font-size' : 13})),
                            dbc.Col(dcc.Input(id = baseId + wid_key + 'End',type='text',value = '21:00',size='13',style={'font-size' : 13}))])
                ])]

            for widObj in widgetObj:widgetLayout.append(widObj)

        dicLayouts['widgetLayout'] = html.Div(widgetLayout,
                                    style={"width": str(100-widthG) + "%", "float": "left"})

        dicLayouts['graphLayout']= html.Div([dcc.Graph(id=baseId+'graph' + str(k)) for k in range(1,nbGraphs+1)],
                                    style={"width": str(widthG) + "%", "display": "inline-block"})

        layout = html.Div(list(dicLayouts.values()))
        return layout

    def addWidgets(self,dicWidgets,baseId):
        widgetLayout,dicLayouts = [],{}
        for wid_key,wid_val in dicWidgets.items():
            if 'dd_computation' in wid_key:
                widgetObj = self.dccE.dropDownFromList(baseId+wid_key,self.computationGraphs,
                                                        'what should be computed ?',value = wid_val)
            elif 'dd_expand' in wid_key:
                widgetObj = self.dccE.dropDownFromList(baseId+wid_key,['groups','tags'],'Select the option : ',value = wid_val)

            elif 'dd_modules' in wid_key:
                widgetObj = self.dccE.dropDownFromList(baseId+wid_key,list(self.cfg.modules.keys()),'Select your module: ',value = wid_val)

            for widObj in widgetObj:widgetLayout.append(widObj)

        return widgetLayout

class ComputationTab(SmallPowerTab):
    def __init__(self,folderPkl,app,baseId='ct0_'):
        super().__init__(app,baseId)
        self.cfg = cfs.ConfigFilesSmallPower(folderPkl)
        self.computationGraphs=['power repartition']
        self.tabLayout = self._buildComputeLayout()
        self.tabname = 'computation'
        self._define_callbacks()

    def _define_callbacks(self):
        listInputsGraph = {
            'dd_computation':'value',
            'pdr_timeBtn':'n_clicks',
            'dd_resampleMethod' : 'value',
            'dd_expand' : 'value',
            'dd_cmap':'value',
            'dd_style':'value'
            }
        listStatesGraph = {
            'graph':'figure',
            'in_timeRes' : 'value',
            'pdr_timeStart' : 'value',
            'pdr_timeEnd':'value',
            'pdr_timePdr':'start_date',
                            }

        @self.app.callback(
        Output(self.baseId + 'graph', 'figure'),
        Output(self.baseId + 'pdr_timeBtn', 'n_clicks'),
        [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
        [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
        State(self.baseId+'pdr_timePdr','end_date'))
        def updateGraph(computation,timeBtn,rsmethod,expand,colmap,style,fig,rs,date0,date1,t0,t1):
            ctx = dash.callback_context
            trigId = ctx.triggered[0]['prop_id'].split('.')[0]
            # to ensure that action on graphs only without computation do not
            # trigger computing the dataframe again
            if not timeBtn or trigId in [self.baseId+k for k in ['dd_computation','pdr_timeBtn','dd_typeGraph','dd_expand','dd_resampleMethod']] :
                if not timeBtn : timeBtn=1 # to initialize the first graph
                timeRange = [date0+' '+t0,date1+' '+t1]
                params,params['rs'],params['method'],params['expand']={},rs,rsmethod,expand
                fig   = self.plotGraphComputation(timeRange,computation,params)
                timeBtn = max(timeBtn,1) # to close the initialisation
            else :fig = go.Figure(fig)
            fig = self.utils.updateStyleGraph(fig,style,colmap)
            return fig,timeBtn

        @self.app.callback(Output(self.baseId + 'btn_export','children'),
        Input(self.baseId + 'btn_export', 'n_clicks'),
        State(self.baseId + 'graph','figure'))
        def exportClick(btn,fig):
            fig = go.Figure(fig)
            if btn>0:self.utils.exportDataOnClick(fig,baseName='proof')
            return 'export Data'

    def plotGraphComputation(self,timeRange,computation,params):
        start     = time.time()
        if computation == 'power repartition' :
            fig = self.cfg.plotGraphPowerArea(timeRange,rs=params['rs'],applyMethod=params['method'],expand=params['expand'])
            fig.update_layout(yaxis_title='power in W')
        self.utils.printCTime(start,'computation time : ')
        return fig

    def _buildComputeLayout(self,widthG=80):
        dicWidgets = {'pdr_time' : None,'in_timeRes':str(60*10)+'s','dd_resampleMethod':'mean',
                    'dd_style':'lines+markers','dd_cmap':'jet','btn_export':0}
        basicWidgets = self.dccE.basicComponents(self.cfg,dicWidgets,self.baseId)
        specialWidgets = self.addWidgets({'dd_computation':'power repartition','dd_expand':'groups'},self.baseId)
        # reodrer widgets
        widgetLayout = basicWidgets + specialWidgets
        return self.dccE.buildGraphLayout(widgetLayout,self.baseId,widthG=widthG)

class ModuleTab(SmallPowerTab):
    def __init__(self,folderPkl,app,baseId='mt0_'):
        super().__init__(app,baseId)
        self.cfg = cfs.AnalysisPerModule(folderPkl)
        self.tabLayout = self._buildModuleLayout()
        self.tabname = 'modules'
        self._define_callbacks()

    def _buildModuleLayout(self,widthG=85):
        dicWidgets = {'pdr_time' : None,'in_timeRes':str(60*10)+'s','dd_resampleMethod':'mean',
        'dd_style':'lines','dd_cmap':'prism','in_heightGraph':900,'btn_export':0}
        basicWidgets = self.dccE.basicComponents(self.cfg,dicWidgets,self.baseId)
        specialWidgets = self.addWidgets({'dd_modules':'GV'},self.baseId)
        # reodrer widgets
        widgetLayout = basicWidgets + specialWidgets
        return self.dccE.buildGraphLayout(widgetLayout,self.baseId,widthG=widthG)

    def _define_callbacks(self):
        listInputsGraph = {
            'dd_modules':'value',
            'pdr_timeBtn':'n_clicks',
            'dd_resampleMethod' : 'value',
            'dd_cmap':'value',
            'dd_style':'value',
            'in_heightGraph':'value',
            }
        listStatesGraph = {
            'graph':'figure',
            'in_timeRes' : 'value',
            'pdr_timeStart' : 'value',
            'pdr_timeEnd':'value',
            'pdr_timePdr':'start_date',
        }
        @self.app.callback(
        Output(self.baseId + 'graph', 'figure'),
        Output(self.baseId + 'pdr_timeBtn', 'n_clicks'),
        [Input(self.baseId + k,v) for k,v in listInputsGraph.items()],
        [State(self.baseId + k,v) for k,v in listStatesGraph.items()],
        State(self.baseId+'pdr_timePdr','end_date'))
        def updateGraph(module,timeBtn,rsmethod,colmap,style,hg,fig,rs,date0,date1,t0,t1):
            ctx = dash.callback_context
            trigId = ctx.triggered[0]['prop_id'].split('.')[0]
            # to ensure that action on graphs only without computation do not
            # trigger computing the dataframe again
            if not timeBtn or trigId in [self.baseId+k for k in ['dd_modules','pdr_timeBtn','dd_resampleMethod']] :
                # print('===============here===============')
                if not timeBtn : timeBtn=1 # to initialize the first graph
                timeRange = [date0+' '+t0,date1+' '+t1]
                fig = self.cfg.figureModuleUnits(module,timeRange,rs=rs,applyMethod=rsmethod)
                timeBtn = max(timeBtn,1) # to close the initialisation
            else :fig = go.Figure(fig)
            fig = self.utils.updateStyleGraph(fig,style,colmap,heightGraph=hg)
            return fig,timeBtn

        @self.app.callback(
        Output(self.baseId + 'btn_export','children'),
        Input(self.baseId + 'btn_export', 'n_clicks'),
        State(self.baseId + 'graph','figure'))
        def exportClick(btn,fig):
            fig = go.Figure(fig)
            if btn>0:self.utils.exportDataOnClick(fig,baseName='proof')
            return 'export Data'
