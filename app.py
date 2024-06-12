'''
COMMENTS
A python virtual environment was created called - shinyTest
    conda create --name shinyTest python=3.9.13

The environment was activated
    conda activate shinyTest
    
The following libraries were then installed
    conda install pandas plotly numpy matplotlib ipywidgets
    conda install -c conda-forge r-shiny
    pip install shinywidgets
    conda install -c conda-forge rsconnect-python
    
Please find all the dependencies for this project in the requirements.txt file

To run this webapp 
shiny run  --reload app.py

'''

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, register_widget, render_widget
import matplotlib.pyplot as plt
import plotly.express as px

# myUtils.py contains two functions that I wrote
# from myUtils_Copy import prepData, createMap

# read in the cleaned dataset
df = pd.read_csv('quakes-cleaned.csv', index_col=0)

# spliting the values in the state_country column
df['country'] = df['state_country'].apply(lambda x: x.split(',')[-1].strip() if ',' in x else x.strip())

'''
The Shiny app
working from examples here https://shinylive.io/py/examples/
'''

app_ui = ui.page_fluid(

    # title
    ui.h1("SIESMIC EVENT ANALYSIS"),
    ui.p("The plots below shows the distributions of Siesmic Events between September 1st, 2023 and November 15th, 2023.", style="max-width:1000px"),
    

    # UI
    ui.panel_main(
        ui.output_text_verbatim("etext1"),
        output_widget("ebar", width=900, height= 500),
        ui.output_text_verbatim("etext2"),
        output_widget("ebox", width=900, height= 700),
        ui.output_text_verbatim("etext3"),
        output_widget("ehist", width=900, height= 700),
        ui.output_text_verbatim("etext4"),
        output_widget("epie", width=900, height= 700),
        ui.output_text_verbatim("etext5"),
        output_widget("emap", width='Auto', height= 'Auto'),))
    

def server(input, output, session):
    
    @output
    @render.text
    def etext1():
        return "1) A Plot of Event Distribution by Event Type."
    

    @output
    @render_widget
    def ebar():
        # Get the value counts for the 'type' column
        type_counts = df['type'].value_counts().reset_index()
        type_counts.columns = ['type', 'count']

        # Plotting the bar chart using Plotly Express
        fig = px.bar(type_counts, x='type', y='count', 
                     labels={'type': 'Event Type', 'count': 'Event Frequency'},
                    color ='type')

        # Return the plotly figure
        return go.FigureWidget(fig)
    
    
    
    
    @output
    @render.text
    def etext2():
        return "2) A Plot of the Distribution of Seismic Event Magnitudes."
    
    
    @output
    @render_widget
    def ebox():
        # Plotting the box plot for the 'mag' column
        fig = px.box(df, y='mag', 
             labels={'mag': 'Magnitude'})

        # Adjust the height and width of the plot
        fig.update_layout(
            height=600,  
            width=800 
        )
        
        # Return the plotly figure
        return go.FigureWidget(fig)
    
    
    
    
    @output
    @render.text
    def etext3():
        return "3) A Plot of the Distribution of Seismic Event Depths."
    
    @output
    @render_widget
    def ehist():
        # Plotting the box plot for the 'mag' column
        # Plotting the histogram for the depth column
        fig = px.histogram(df, x='depth', 
                           labels={'depth': 'Depth'},
                           color ='type',
                           opacity=0.7,
                           )

        # Adjust the height and width of the plot
        fig.update_layout(
            xaxis_title='Depth',  
            yaxis_title='Frequency',
            height=600, 
            width=800    
        )

        # Return the plotly figure
        return go.FigureWidget(fig)
    
    
    
    
    @output
    @render.text
    def etext4():
        return "4) A Plot of the Distribution of Seismic Event Status."
    
    @output
    @render_widget
    def epie():
        # Plotting the box plot for the 'mag' column
        # Plotting the histogram for the depth column
        fig = px.pie(df, names='status', 
             labels={'status': 'Status'}, color_discrete_sequence=px.colors.sequential.RdBu)

        # Return the plotly figure
        return go.FigureWidget(fig)
    
    
    
    
    @output
    @render.text
    def etext5():
        return "5) A Plot of Seismic Event Distribution by Geographical Location."
    
    @output
    @render_widget
    def emap():
        # Plotting the box plot for the 'mag' column
        # Plotting the histogram for the depth column
        fig = px.scatter_geo(
            scope="world",
            data_frame=df,
            lon=df.longitude,
            lat=df.latitude,
            hover_data=df,
            color=df.country,
            basemap_visible=True,
            color_discrete_sequence=px.colors.qualitative.Set1  # Use a qualitative color scale
        )

        fig.update_geos(
            resolution=50,
            lonaxis={"range": [-180, 180]},
            lataxis={"range": [67, -4]}
        )

        fig.update_layout(
            height=800,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )


        # Return the plotly figure
        return go.FigureWidget(fig)


app = App(app_ui, server)
