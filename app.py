
#trying 

import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

# Read in clean dataset
skincare_df = pd.read_csv("data.csv")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

all_brands = skincare_df['brand'].unique()
all_categories = skincare_df['product type'].unique()

app.layout = dbc.Container([
  dbc.Row(
    [
        dbc.Col(html.Img(src="/Users/selahmitchell/Desktop/DS interactive app/plotly-dash", height="100px",alt="sephora logo"), width=2),  # Adjust width as needed
        dbc.Col(html.H1("Sephora Skincare Product Analysis", style={'color': 'pink'}), width=10),  # Adjust width as needed
    ],
    className="mb-4",
    style={'background': 'black'}
),

    # Attributes and Sunburst Graph
    dbc.Row([
        dbc.Col([
            html.Label('Attributes', style={'color': 'pink'}),
            dcc.Checklist(
                id='attribute-checkboxes-row-one',
                options=[
                    {'label': 'Online Only', 'value': 'online_only'},
                    {'label': 'Sephora Exclusive', 'value': 'sephora_exclusive'},
                    {'label': 'Dark Circles', 'value': 'Dark Circles'},
                    {'label': 'Pores', 'value': 'Pores'},
                    {'label': 'Loss of Firmness', 'value': 'Loss of firmness'},
                ],
                value=[]
            ),
            html.Label('Attributes', style={'color': 'pink'}),
            dcc.Checklist(
                id='attribute-checkboxes-row-two',
                options=[
                    {'label': 'Dullness/Uneven Texture', 'value': 'Dullness/Uneven Texture'},
                    {'label': 'Dark Spots', 'value': 'Dark spots'},
                    {'label': 'Acne/Blemishes', 'value': 'Acne/Blemishes'},
                    {'label': 'Anti-Aging', 'value': 'Anti-Aging'},
                    {'label': 'Dryness', 'value': 'Dryness'},
                    {'label': 'Damage', 'value': 'Damage'}
                ],
                value=[]
            ),
               html.Label('Select Brand(s)', style={'color': 'pink'}),
            dcc.Dropdown(
                id='brand-dropdown',
                options=[{'label': 'All Brands', 'value': 'All Brands'}] + [{'label': brand, 'value': brand} for brand in all_brands],
                multi=True,
                value=['All Brands'],
                placeholder="Select Brand(s)",
            ),
            html.Label('Select Product Type(s)', style={'color': 'pink'}),
            dcc.Dropdown(
                id='product-type-dropdown',
                options=[{'label': 'All Product Types', 'value': 'All Product Types'}] + [{'label': category, 'value': category} for category in all_categories],
                multi=True,
                value=['All Product Types'],
                placeholder="Select Product Type(s)",
            ),
             html.Label('Choose Price Range (USD)', style={'color': 'pink'}),
            dcc.RangeSlider(
                id='price-range-slider',
                min=skincare_df['price_usd'].min(),
                max=skincare_df['price_usd'].max(),
                value=[skincare_df['price_usd'].min(), skincare_df['price_usd'].max()],
                allowCross=False,
                pushable=1,
                tooltip={'always_visible': True},
            ),

              html.Div(id='output-container-range-slider'),
            html.Label('Ranking and Comparison Options', style={'color': 'pink'}),
            html.Div([
                html.P("Choose the data to rank or compare:"),
                dcc.RadioItems(
                    id='y-axis-radio',
                    options=[
                        {'label': 'Reviews', 'value': 'reviews'},
                        {'label': 'Love Count', 'value': 'loves_count'},
                        {'label': 'Rating', 'value': 'rating'}
                    ],
                    value='reviews',
                    labelStyle={'display': 'inline-block', 'color': 'black'}
                ),

             html.Label('Pick a category to compare', style={'color': 'pink'}),  # Add a label and description
            dcc.RadioItems(
                id='x-axis-radio',
                options=[
                    {'label': 'Product Type', 'value': 'product type'},
                    {'label': 'Subtype', 'value': 'Subtype'},
                    {'label': 'Brand', 'value': 'brand'}
                ],
                value='product type',
                labelStyle={'display': 'inline-block', 'color': 'black'}
            ),
            ])

        ], width=4),
        dbc.Col([
            dcc.Graph(id='sunburst-chart')
        ], width=8),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='scatter-plot'),
        ], width=4),
         dbc.Col([
        ], width=4),
        dbc.Col([
            dcc.Graph(id='bar-graph')
        ], width=4),
    ], className="mb-2"),

    # Data Table
    dbc.Row([
        dbc.Col([
            html.Label('TOP 10 List', style={'color': 'pink'}),
            dash_table.DataTable(
                id='top-ten-table',
                columns=[
                    {'name': 'Rank', 'id': 'Row Number'},
                    {'name': 'Price', 'id': 'price_usd'},
                    {'name': 'Size', 'id': 'size_ml'},
                    {'name': 'Product Name', 'id': 'product'},
                    {'name': 'Brand', 'id': 'brand'},
                    {'name': 'Average Rating', 'id': 'rating'},
                    {'name': 'Love Count', 'id': 'loves_count'},
                    {'name': 'Reviews', 'id': 'reviews'},
                ],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left','padding-top': '10px', 'padding-bottom': '20px', 'padding-left': '30px', 'padding-right': '40px'},
                page_size=10,
                style_as_list_view=True,
                style_header={'backgroundColor': px.colors.qualitative.Pastel1[0], 'fontWeight': 'bold', 'textAlign': 'center'},
                style_data_conditional=[
                    {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
                    {'if': {'row_index': 'even'}, 'backgroundColor': 'rgb(220, 220, 220)'}
                ]
            ),
        ], width=12)
    ], className="mb-2")
], fluid=True,style={'background': 'linear-gradient(to left, rgba(0,0,0,1), rgba(169,169,169,1))'})


# Define the update_output function
def update_output(price_range):
    return f"${price_range[0]} to ${price_range[1]}."

# Callback to update all graphs and tables
@app.callback(
    [Output('sunburst-chart', 'figure'), Output('scatter-plot', 'figure'),  Output('bar-graph', 'figure'), Output('output-container-range-slider', 'children'),
     Output('top-ten-table', 'data')],
    [Input('price-range-slider', 'value'),
     Input('brand-dropdown', 'value'),
     Input('product-type-dropdown', 'value'),
     Input('attribute-checkboxes-row-one', 'value'),
     Input('attribute-checkboxes-row-two', 'value'),
     Input('y-axis-radio', 'value'),
     Input('x-axis-radio', 'value')]
)
def update_graphs(price_range, selected_brands, selected_primary_categories, selected_attributes_one, selected_attributes_two, y_axis, x_axis):
    # Filter DataFrame based on price range, selected brands, and selected primary categories
    filtered_df = skincare_df[(skincare_df['price_usd'] >= price_range[0]) &
                              (skincare_df['price_usd'] <= price_range[1])]

    if 'All Brands' not in selected_brands:
        filtered_df = filtered_df[filtered_df['brand'].isin(selected_brands)]
    if 'All Product Types' not in selected_primary_categories:
        filtered_df = filtered_df[filtered_df['product type'].isin(selected_primary_categories)]

    # Combine selected attributes from both rows
    selected_attributes = selected_attributes_one + selected_attributes_two

    # Filter DataFrame based on selected attributes
    for attr in selected_attributes:
        filtered_df = filtered_df[filtered_df[attr] == True]
    
  # Determine the label for the x-axis and the color parameter
    if x_axis == 'brand':
        x_label = 'product type'
        color_param = 'product type' 
        barmode_param = 'stack'
        
    elif x_axis == 'Subtype':
        x_label = 'Subtype'
        color_param = 'product type' 
        
    else:  # Default to primary category
        x_label = 'Product Type'
        color_param = 'Subtype'
        barmode_param = 'stack'
        
 

# Group by the selected x-axis criteria and calculate the average rating
    if x_axis == 'brand':
        grouped_df = filtered_df.groupby(['brand',color_param])[y_axis].mean().reset_index()
    else:
        grouped_df = filtered_df.groupby([x_axis, color_param])[y_axis].mean().reset_index()

    # Create bar graph
    bar_fig = px.bar(grouped_df, x=x_axis, y=y_axis, 
                 title=f'Average {y_axis} by {x_label}',
                 labels={y_axis: f'Average {y_axis}' },
                 color_discrete_sequence=px.colors.qualitative.Pastel1,
                 color=color_param,
                 barmode=barmode_param
                 ) 
    
   
    bar_fig.update_layout(
        title_font=dict(size=25),
        autosize=True,
        width=800,
        height=500,
        font=dict(color="pink"),  # Set text color to pink
        plot_bgcolor='rgb(220, 220, 220)'
    )

    # Create scatter plot
    scatter_fig = px.scatter(filtered_df, x='price_usd', y=y_axis, color=x_axis,
                             title=f'Price vs {y_axis.capitalize()}',
                             color_discrete_sequence=px.colors.qualitative.Pastel1,
                             hover_data={'product': True, 'product type': True})

    # Update scatter plot layout 
    scatter_fig.update_layout(
        title_font=dict(size=25),
        xaxis=dict(title='Price (USD)', title_font=dict(size=20)),
        yaxis=dict(title=y_axis.capitalize(), title_font=dict(size=20)),
        legend=dict(title=f'{y_axis.capitalize()}', title_font=dict(size=20)),
        autosize=True,
        width=800,
        height=500
    )

     # Sort DataFrame based on y-axis and select top 10 values
    sorted_df = filtered_df.sort_values(by=y_axis, ascending=False).head(10)
    sorted_df['Row Number'] = range(1, min(11, len(sorted_df) + 1))
    # Convert DataFrame to DataTable format
    data = sorted_df.to_dict('records')

    # Create sunburst chart
    sunburst_fig = px.sunburst(filtered_df, path=['product type', 'Subtype', 'brand'],
                                title='Distribution of Product Types',
                                color='product type',
                                color_discrete_sequence=px.colors.qualitative.Pastel1)

    sunburst_fig.update_layout(
        title_font=dict(size=25),
        autosize=False,
        width=500,
        height=500,
        font=dict(color="pink"), # Set text color to pink
        plot_bgcolor='rgba(0,0,0,0)'
    )

    # Update the output container with price range information
    output_message = update_output(price_range)

    return sunburst_fig, scatter_fig, bar_fig, output_message, data


# Run the app
if __name__ == "__main__":
 app.run_server(debug=True)


