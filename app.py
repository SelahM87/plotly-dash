import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc


stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # load the CSS stylesheet
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=stylesheets)

server = app.server

all_brands = skincare_df['brand'].unique()
all_categories = skincare_df['primary_category'].unique()

# Define the layout of the app
# Define the layout of the app
app.layout = html.Div([
    # Title and description
    html.H1("Skincare Product Analysis"),
   
    # Additional attributes checklist
    html.Div([
        html.Label('Attributes'),
        dcc.Checklist(
            id='attribute-checkboxes',
            options=[
                {'label': 'Online Only', 'value': 'online_only'},
                {'label': 'Sephora Exclusive', 'value': 'sephora_exclusive'},
                {'label': 'Dark Circles', 'value': 'Dark Circles'},
                {'label': 'Pores', 'value': 'Pores'},
                {'label': 'Loss of Firmness', 'value': 'Loss of firmness'},
                {'label': 'Dullness/Uneven Texture', 'value': 'Dullness/Uneven Texture'},
                {'label': 'Dark Spots', 'value': 'Dark spots'},
                {'label': 'Acne/Blemishes', 'value': 'Acne/Blemishes'},
                {'label': 'Anti-Aging', 'value': 'Anti-Aging'},
                {'label': 'Dryness', 'value': 'Dryness'},
                {'label': 'Damage', 'value': 'Damage'}
            ],
            value=[]
        ),
    ]),
    
    # Brand dropdown and primary category dropdown
    html.Div([
        # Brand dropdown
        dcc.Dropdown(
            id='brand-dropdown',
            options=[{'label': 'All Brands', 'value': 'All Brands'}] + [{'label': brand, 'value': brand} for brand in all_brands],
            multi=True,
            value=['All Brands'],
            placeholder="Select Brand(s)",
            className="  two   columns"
        ),
        
        # Primary category dropdown
        dcc.Dropdown(
            id='primary-category-dropdown',
            options=[{'label': 'All Categories', 'value': 'All Categories'}] + [{'label': category, 'value': category} for category in all_categories],
            multi=True,
            value=['All Categories'],
            placeholder="Select Primary Category(s)",
            className=" two columns"
        ),
    ], className="row"),
    
    # Price range slider and graph
    html.Div([
         html.Label('Choose your price range'),
        # Price range slider
        html.Div([
            dcc.RangeSlider(
                id='price-range-slider',
                min=skincare_df['price_usd'].min(),
                max=skincare_df['price_usd'].max(),
                marks=None,
                value=[skincare_df['price_usd'].min(), skincare_df['price_usd'].max()],
                allowCross=False,
                pushable=1,
                tooltip={'always_visible': True}
            ),
        ], className=' four  columns'),
        
        # Graph
        html.Div([
            dcc.Graph(id='sunburst-chart', className='six columns')
        ], className=' three columns'),
    ], className='row'),
])



# Define callback to update the sunburst chart based on user input
@app.callback(
    Output('sunburst-chart', 'figure'),
    [Input('price-range-slider', 'value'),
     Input('brand-dropdown', 'value'),
     Input('primary-category-dropdown', 'value'),
     Input('attribute-checkboxes', 'value')]
)
def update_sunburst_chart(price_range, selected_brands, selected_primary_categories, selected_attributes):
    filtered_df = skincare_df[(skincare_df['price_usd'] >= price_range[0]) & 
                              (skincare_df['price_usd'] <= price_range[1])]
    if 'All Brands' not in selected_brands:
        filtered_df = filtered_df[filtered_df['brand'].isin(selected_brands)]
    if 'All Categories' not in selected_primary_categories:
        filtered_df = filtered_df[filtered_df['primary_category'].isin(selected_primary_categories)]
    
    for attr in selected_attributes:
        filtered_df = filtered_df[filtered_df[attr] == True]
    
    # Group by primary and secondary categories and count the occurrences
    category_counts = filtered_df.groupby(['primary_category', 'secondary_category','brand']).size().reset_index(name='count')
    
    # Create a sunburst chart
    fig = px.sunburst(category_counts, path=['primary_category', 'secondary_category','brand'], values='count')
    
    fig.update_layout(
        title='Distribution of Product Types',
        title_font=dict(size=25),
        autosize=False,
        width=800,
        height=600,
        sunburstcolorway=px.colors.qualitative.Pastel1,  # Set sunburst colors to pink
        font=dict(color="pink")  # Set text color to pink
    )
    
    return fig

# Run the app
if __name__ == "__main__":
 app.run_server(debug=True)