import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# load dataset

bike_df = pd.read_csv("https://github.com/rnsmall/submission/raw/main/Dashboard/main_data.csv")
bike_df.head()

bike_df['dteday'] =  pd.to_datetime(bike_df['dteday'])
bike_df['month'] =  bike_df['dteday'].dt.strftime('%B')
bike_df['year'] = bike_df.dteday.dt.year
bike_df['month_num'] = bike_df['dteday'].dt.month
bike_df['total riders'] = bike_df['casual'] + bike_df['registered']
#st.set_page_config(page_title="Capital Bikeshare: Bike-sharing Dashboard",
               #    page_icon="bar_chart:",
                 #  layout="wide")
st.header('Dicoding Collection Dashboard :sparkles:')
# membuat helper

def create_monthly_users_df(df):
    monthly_df = bike_df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_df.index = monthly_df.index.strftime('%b-%y')
    monthly_df = monthly_df.reset_index()
    monthly_df.rename(columns={
        "dteday": "yearmonth",
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    return monthly_df

def create_seasonly_df(df):
    seasonly_df = bike_df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    seasonly_df = seasonly_df.reset_index()
    seasonly_df.rename(columns={
        "cnt": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    
    seasonly_df = pd.melt(seasonly_df,
                                      id_vars=['season'],
                                      value_vars=['casual_rides', 'registered_rides'],
                                      var_name='type_of_rides',
                                      value_name='count_rides')
    
    seasonly_df['season'] = pd.Categorical(seasonly_df['season'],
                                             categories=['Spring', 'Summer', 'Fall', 'Winter'])
    
    seasonly_df = seasonly_df.sort_values('season')
    
    return seasonly_df


min_date = bike_df["dteday"].min()
max_date = bike_df["dteday"].max()


# ----- SIDEBAR -----

with st.sidebar:
    
    st.sidebar.header("Filter:")

    # mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )


main_df = bike_df[
    (bike_df["dteday"] >= str(start_date)) &
    (bike_df["dteday"] <= str(end_date))
]


monthly_df = create_monthly_df(main_df)
seasonly_df = create_seasonly_df(main_df)

# ----- MAINPAGE -----
st.title(":bar_chart: Capital Bikeshare: Bike-Sharing Dashboard")
st.markdown("##")

col1, col2, col3 = st.columns(3)

with col1:
    total_all_rides = main_df['cnt'].sum()
    st.metric("Total Rides", value=total_all_rides)
with col2:
    total_casual_rides = main_df['casual'].sum()
    st.metric("Total Casual Rides", value=total_casual_rides)
with col3:
    total_registered_rides = main_df['registered'].sum()
    st.metric("Total Registered Rides", value=total_registered_rides)

st.markdown("---")
# ----- CHART -----
fig = px.line(monthly_df,
              x='yearmonth',
              y=['casual_rides', 'registered_rides', 'total_rides'],
              color_discrete_sequence=["skyblue", "orange", "red"],
              markers=True,
              title="Monthly Count of Bikeshare Rides").update_layout(xaxis_title='', yaxis_title='Total Rides')

st.plotly_chart(fig, use_container_width=True)

fig1 = px.bar(seasonly_df,
              x='season',
              y=['count_rides'],
              color='type_of_rides',
              color_discrete_sequence=["skyblue", "orange", "red"],
              title='Count of bikeshare rides by season').update_layout(xaxis_title='', yaxis_title='Total Rides')

#st.plotly_chart(fig, use_container_width=True)


# ----- HIDE STREAMLIT STYLE -----
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
