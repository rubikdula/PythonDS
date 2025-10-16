import pandas as pd
import plotly.express as px

df = pd.read_csv("avgIQpercountry.csv")

df["Population - 2023"] = df["Population - 2023"].str.replace(',', '').astype(float)

fig = px.choropleth(df, locations="Country", locationmode="country names", color="Average IQ", hover_name="Country", hover_data=['Literacy Rate', 'Nobel Prices'], color_continuous_scale="agsunset", projection='natural earth', title="Average IQ per country")

fig.show()