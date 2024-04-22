import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

# Read in clean dataset
skincare_df = pd.read_csv("data.csv")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

all_brands = skincare_df['brand'].unique()
all_categories = skincare_df['primary_category'].unique()

app.layout = dbc.Container([
    # Title and description 
    dbc.Row(
        dbc.Col(html.H1("Skincare Product Analysis", className="text-center text-pink"), width=12),
        className="mb-4",
        style={'background': 'linear-gradient(to right, #ffffff, #dcdcdc)'}
    ),

    # Additional attributes checklist and Brand dropdown
    dbc.Row([
        dbc.Col([
            html.Label('Attributes', style={'color': 'black'}),
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
        ], width=6),

        dbc.Col([
            html.Label('Select Brand(s)', style={'color': 'black'}),
            dcc.Dropdown(
                id='brand-dropdown',
                options=[{'label': 'All Brands', 'value': 'All Brands'}] + [{'label': brand, 'value': brand} for brand in all_brands],
                multi=True,
                value=['All Brands'],
                placeholder="Select Brand(s)",
            ),
        ], width=3),
    ], className="mb-4"),

    # Primary category dropdown and Price range slider
    dbc.Row([
        dbc.Col([
            html.Label('Select Product Type(s)', style={'color': 'black'}),
            dcc.Dropdown(
                id='product-type-dropdown',
                options=[{'label': 'All Product Types', 'value': 'All Product Types'}] + [{'label': category, 'value': category} for category in all_categories],
                multi=True,
                value=['All Product Types'],
                placeholder="Select Product Type(s)",
            ),
        ], width=6),

        dbc.Col([
            html.Label('Choose Price Range (USD)', style={'color': 'black'}),
            dcc.RangeSlider(
                id='price-range-slider',
                min=skincare_df['price_usd'].min(),
                max=skincare_df['price_usd'].max(),
                value=[skincare_df['price_usd'].min(), skincare_df['price_usd'].max()],
                allowCross=False,
                pushable=1,
                tooltip={'always_visible': True},
            ),
            html.Div(id='output-container-range-slider')
        ], width=6),
    ], className="mb-10"),

    # Sunburst Graph and TOP 10 List
    dbc.Row([
        dbc.Col(dcc.Graph(id='sunburst-chart'), width=6),
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
                style_cell={'textAlign': 'left', 'padding': '5px'},
                page_size=10,
                style_as_list_view=True,
                style_header={'backgroundColor': px.colors.qualitative.Pastel1[0], 'fontWeight': 'bold', 'textAlign': 'center'},
                style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {'row_index': 'even'},
                'backgroundColor': 'rgb(220, 220, 220)'
            }
        ]
    ),
], width=6)
    ], className="mb-4"),

    # Radio items for y-axis selection and Second Graph (Scatter Plot)
    dbc.Row([
        dbc.Col([
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
            dcc.Graph(id='scatter-plot')
        ], width=6),
    ], className="mb-4"),

    # Radio items for x-axis selection and Third Graph (Bar Graph)
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                id='x-axis-radio',
                options=[
                    {'label': 'Primary Category', 'value': 'primary_category'},
                    {'label': 'Secondary Category', 'value': 'secondary_category'},
                    {'label': 'Brand', 'value': 'brand'}
                ],
                value='primary_category',
                labelStyle={'display': 'inline-block', 'color': 'black'}
            ),
            dcc.Graph(id='bar-graph')
        ], width=6),
    ], className="mb-4"),

], fluid=True, style={'background': 'linear-gradient(to bottom, rgba(0,0,0,1), rgba(169,169,169,1))'})           

   

# Define the update_output function
def update_output(price_range):
    return f"You have selected price range from {price_range[0]} to {price_range[1]}."

# Callback to update both graphs
@app.callback(
    [Output('sunburst-chart', 'figure'), Output('scatter-plot', 'figure'),  Output('bar-graph', 'figure'), Output('output-container-range-slider', 'children'),
     Output('top-ten-table', 'data')],
    [Input('price-range-slider', 'value'),
     Input('brand-dropdown', 'value'),
     Input('product-type-dropdown', 'value'),
     Input('attribute-checkboxes', 'value'),
     Input('y-axis-radio', 'value'),Input('x-axis-radio', 'value')]
)
def update_graphs(price_range, selected_brands, selected_primary_categories, selected_attributes, y_axis,x_axis):
    # Filter DataFrame based on price range, selected brands, and selected primary categories
    filtered_df = skincare_df[(skincare_df['price_usd'] >= price_range[0]) &
                              (skincare_df['price_usd'] <= price_range[1])]

    if 'All Brands' not in selected_brands:
        filtered_df = filtered_df[filtered_df['brand'].isin(selected_brands)]
    if 'All Categories' not in selected_primary_categories:
        filtered_df = filtered_df[filtered_df['primary_category'].isin(selected_primary_categories)]

    for attr in selected_attributes:
        filtered_df = filtered_df[filtered_df[attr] == True]

    # Group by the selected x-axis criteria and calculate the average rating
    if x_axis == 'brand':
        grouped_df = filtered_df.groupby('brand')[y_axis].mean().reset_index()
        x_label = 'Brand'
    elif x_axis == 'secondary_category':
        grouped_df = filtered_df.groupby('secondary_category')[y_axis].mean().reset_index()
        x_label = 'Secondary Category'
    else:  # Default to primary category
        grouped_df = filtered_df.groupby('primary_category')[y_axis].mean().reset_index()
        x_label = 'Primary Category'

     # Sort DataFrame based on y-axis and select top 10 values

    sorted_df = filtered_df.sort_values(by=y_axis, ascending=False).head(10)
    
    sorted_df['Row Number'] = range(1, min(11, len(sorted_df) + 1))
    # Convert DataFrame to DataTable format
    data = sorted_df.to_dict('records')
    
    # Create bar graph
    bar_fig = px.bar(grouped_df, x=x_axis, y=y_axis, 
                     title='Average Rating by {}'.format(x_label),
                     labels={y_axis: 'Average {}'.format(y_axis)})
    
    bar_fig.update_layout(
        title_font=dict(size=25),
        autosize=True,
        width=800,
        height=600,
        font=dict(color="pink")  # Set text color to pink
    )

  # Create scatter plot
    scatter_fig = px.scatter(filtered_df, x='price_usd', y=y_axis, color=x_axis,
                         title=f'Price vs {y_axis.capitalize()}',
                         hover_data={'product': True, 'primary_category': True})


    # Update layout
    scatter_fig.update_layout(
        title_font=dict(size=25),
        xaxis=dict(title='Price (USD)', title_font=dict(size=20)),
        yaxis=dict(title=y_axis.capitalize(), title_font=dict(size=20)),
        legend=dict(title='Primary Category', title_font=dict(size=20)),
        autosize=True,
        width=800,
        height=600
    )


    # Group by primary and secondary categories and count the occurrences
    category_counts = filtered_df.groupby(['primary_category', 'secondary_category', 'brand']).size().reset_index(
        name='count')

    # Create a sunburst chart
    sunburst_fig = px.sunburst(category_counts,
                                path=['primary_category', 'secondary_category', 'brand'],
                                values='count')

    sunburst_fig.update_layout(
        title='Distribution of Product Types',
        title_font=dict(size=25),
        autosize=True,
        width=800,
        height=600,
        sunburstcolorway=px.colors.qualitative.Pastel1,  # Set sunburst colors to pastel
        font=dict(color="pink")  # Set text color to pink
    )

    # Update the output container with price range information
    output_message = update_output(price_range)

    return sunburst_fig, scatter_fig, bar_fig, output_message,data 




# Run the app
if __name__ == "__main__":
 app.run_server(debug=True)