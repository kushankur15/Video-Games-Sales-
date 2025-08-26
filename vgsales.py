import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

filename  = "vgsales.csv"
df = pd.read_csv(filename)

st.set_page_config(page_title='Video Game Sales Dashboard', layout='wide')

df_dataframe = pd.DataFrame(df)

# Sidebars
st.sidebar.title("Filter")
platform = st.sidebar.multiselect("Select Platform", df_dataframe["Platform"].unique(), default=df_dataframe["Platform"].unique())
genres = st.sidebar.multiselect("Select Genre", df_dataframe["Genre"].unique(), default=df_dataframe["Genre"].unique())
year = st.sidebar.slider("Select Year", min_value=int(df_dataframe["Year"].min()), max_value=int(df_dataframe["Year"].max()), value=(int(df_dataframe["Year"].min()), int(df_dataframe["Year"].max())))

filtered_data = df_dataframe[
    (df_dataframe["Platform"].isin(platform)) &
    (df_dataframe["Genre"].isin(genres)) &
    (df_dataframe["Year"].between(year[0], year[1]))
]

#11 columns
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11 = st.columns(11)
col1.metric("Rank", df_dataframe["Rank"].iloc[0])
col2.metric("Name", df_dataframe["Name"].iloc[0])
col3.metric("Platform", filtered_data["Platform"].iloc[0])
col4.metric("Year", filtered_data["Year"].iloc[0])
col5.metric("Genre", filtered_data["Genre"].iloc[0])
col6.metric("Publisher", filtered_data["Publisher"].iloc[0])
col7.metric("NA_Sales", filtered_data["NA_Sales"].iloc[0])
col8.metric("EU_Sales", filtered_data["EU_Sales"].iloc[0])
col9.metric("JP_Sales", filtered_data["JP_Sales"].iloc[0])
col10.metric("Other_Sales", filtered_data["Other_Sales"].iloc[0])
col11.metric("Global_Sales", filtered_data["Global_Sales"].iloc[0])

# plots

#plot1: global sales of all games from 1980 to 2020
yearly_sales = df.groupby('Year')['Global_Sales'].sum()
fig1 = px.line(yearly_sales, x=yearly_sales.index, y=yearly_sales.values, title="Global Sales of Video Games (1980-2020)")
st.plotly_chart(fig1)

#plot 2: global sales by genre
genres = df.groupby(['Genre','Year'])['Global_Sales'].sum()
data = {
    "Genre": [],
    "Year": [],
    "Global_Sales": []
}

for index, value in genres.items():
    data['Genre'].append(index[0])
    data['Year'].append(index[1])
    data['Global_Sales'].append(value)

data_2 = pd.DataFrame(data)
fig2 = px.bar(data_2, x="Year", y="Global_Sales", color="Genre", title="Global Sales by Genre and Year", color_discrete_sequence=px.colors.diverging.Tealrose)
st.plotly_chart(fig2)

#plot 3: genre count
genres_count = df['Genre'].value_counts()
fig3 = px.bar(genres_count, x=genres_count.index, y=genres_count.values, title="Video Game Sales by Genre")
st.plotly_chart(fig3)

#plot 4: na_sales, eu_sales, jp_sales, other_sales by genre
sales_by_genre = df.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
fig4 = px.bar(sales_by_genre, x=sales_by_genre.index, y=sales_by_genre.columns, color_discrete_sequence=px.colors.sequential.RdPu,title="Sales by Genre", barmode='group')
st.plotly_chart(fig4)

#plot5: pie chart of the publishers count with count > 200
publishers = df['Publisher'].value_counts()
filtered_publishers = publishers[publishers > 200]
fig5 = px.pie(names=filtered_publishers.index, values=filtered_publishers.values, title="Video Game Publishers with More Than 200 Games", color_discrete_sequence=px.colors.sequential.Turbo_r)
st.plotly_chart(fig5)

#plot6: global sales by platform
platform_sales = df.groupby('Platform')['Global_Sales'].sum()
fig6 = px.bar(platform_sales, x=platform_sales.index, y=platform_sales.values, title="Global Sales by Platform", color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig6)

#plot7: global sales by publishers with count more than 200
filtered_publishers_sales = df[df['Publisher'].isin(filtered_publishers.index)]
fig7 = px.bar(filtered_publishers_sales, x='Publisher', y='Global_Sales', title="Global Sales by Publishers with More Than 200 Games")
st.plotly_chart(fig7)

st.subheader("Video Game Sales Data")
st.dataframe(filtered_data)
