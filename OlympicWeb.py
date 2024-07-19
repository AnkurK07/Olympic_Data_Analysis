import streamlit as st
import pandas as pd
import preprocessor , helper
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set the background image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images2.alphacoders.com/120/1202991.jpg");
background-size: 100%;
}}
</style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(page_bg_img, unsafe_allow_html=True)


df = pd.read_csv("athlete_events.csv")
r_df = pd.read_csv("noc_regions.csv")

df = preprocessor.preprocess(df,r_df)


st.sidebar.title('Olympics Analysis')
import streamlit as st

# Display image in the sidebar
st.sidebar.image('https://trademarklawyermagazine.com/wp-content/uploads/2022/02/sochi-2014-g8880ee89a_640-e1645698211307.jpg')

user_menu=st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall analysis','Country Wise Analysis','Athlete Wise Analysis')
)


if user_menu == 'Medal Tally' :
   
   st.header('Medal Tally')
   st.sidebar.title('Medal Tally')
   st.image("https://grizzenergygum.com/media/responsive/fill/2352/80/1440/503/header.jpeg")
   years , country = helper.country_year_list(df)

   selected_year=st.sidebar.selectbox('Select Year',years)
   selected_country=st.sidebar.selectbox('Select Country',country)

   medal_tally= helper.fetch_medal_tally(df,selected_year,selected_country)

   if selected_year == 'Overall' and selected_country == 'Overall':
      st.title('Overall Tally')
   if selected_year != 'Overall' and selected_country == 'Overall':
      st.title('Medal Tally in '+ str(selected_year))
   if selected_year == 'Overall' and selected_country != 'Overall':
      st.title('Medal Tally in '+ str(selected_country))
   if selected_year != 'Overall' and selected_country != 'Overall':
      st.title('Medal Tally in  '+ str(selected_year ) +','+ str(selected_country))


   st.table(medal_tally)

# Some Overall Analysis of Olympics Game

if user_menu == 'Overall analysis':
   editions = df['Year'].unique().shape[0]-1
   cities = df['City'].unique().shape[0]
   sports = df['Sport'].unique().shape[0]
   events = df['Event'].unique().shape[0]
   athletes = df['Name'].unique().shape[0]
   nations = df['region'].unique().shape[0]


   st.title('Top Statistics')
   st.image("https://visme.co/blog/wp-content/uploads/2021/06/data-visualization-techniques-header-wide.png")
   col1,col2,col3 = st.columns(3)
   with col1:
      st.header('Editions')
      st.title(editions)
   with col2:
      st.header('Hosts')
      st.title(cities)
   with col3:
      st.header('Sports')
      st.title(sports)

   col1,col2,col3 = st.columns(3)
   with col1:
      st.header('Events')
      st.title(events)
   with col2:
      st.header('Nations')
      st.title(nations)
   with col3:
      st.header('Athletes')
      st.title(athletes)

   # Nations Over Time
   NOT =  helper.participating_nations_over_time(df)
   #fig = px.line(NOT,x='Editions',y='No of countries',title='No of participating nations over time')
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=NOT['Editions'],y=NOT['No of countries'],mode='lines+markers',line=dict(color='firebrick',width=3,dash='dashdot')))
   fig.update_layout(xaxis_title='Editions',yaxis_title='No of countries')
   fig.update_layout(
    
   # Updating X axis features
   xaxis=dict(
   showline=True,
   showgrid=True,
   showticklabels=True,
   linecolor='rgb(204,204,204)',
   linewidth=2,
   ticks='outside',
   tickfont=dict(family='Arial',size=12,color='rgb(82,82,82)')),

   #Updating The Y-Axis Features
   yaxis=dict(
   showgrid=True,
   zeroline=True,
   showline=False,
   showticklabels=True),
   template='plotly_dark')

   st.title('Participating Nations Over The Time ')
   st.plotly_chart(fig)
  
   # Events Over the time 
   EOT =  helper.events_over_time(df)
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=EOT['Editions'],y=EOT['Event'],mode='lines+markers',line=dict(color='orange',width=3,dash='dashdot')))
   fig.update_layout(xaxis_title='Editions',yaxis_title='Event')
   fig.update_layout(
    
   #Updating The Y-Axis Features
   yaxis=dict(
   showgrid=True,
   zeroline=True,
   showline=False,
   showticklabels=True),
   template='plotly_dark')

   st.title('Events Over The Year')
   st.plotly_chart(fig)


   # No of Atheletes Over time 
   AOT = helper.ath_over_time(df)
   fig = go.Figure()
   fig.add_trace(go.Scatter(x=AOT['Editions'],y=AOT['No Of Atheletes'],mode='lines+markers',line=dict(color='palegreen',width=3,dash='solid')))
   fig.update_layout(xaxis_title='Editions',yaxis_title='No Of Atheletes')
   fig.update_layout(
    
   # Updating X axis features
   xaxis=dict(
   showline=True,
   showgrid=True,
   showticklabels=True,
   linecolor='rgb(204,204,204)',
   linewidth=2,
   ticks='outside',
   tickfont=dict(family='Arial',size=12,color='rgb(82,82,82)')),

   #Updating The Y-Axis Features
   yaxis=dict(
   showgrid=True,
   zeroline=True,
   showline=False,
   showticklabels=True),
   template='plotly_dark')

   st.title('No Of Atheletes Over The Year')
   st.plotly_chart(fig)


   # Heatmap of Sports over Yer
   st.title('Every Sport Played Per year')
   fig,ax = plt.subplots(figsize=(20,20))
   H = df.drop_duplicates(['Year','Sport','Event'])
   ax = sns.heatmap(H.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
   st.pyplot(fig)

   # Most successful Athletes Overall Sports
   st.title('Most successful Athletes')
   sport_list = df['Sport'].unique().tolist()
   sport_list.sort()
   sport_list.insert(0,'Overall')

   selected_sport = st.selectbox('Select a Sport',sport_list)
   x = helper.most_successful(df,selected_sport)
   st.table(x)
  
# Country wise Analysis
if user_menu == 'Country Wise Analysis':
    st.title("Country Wise Analysis")
    st.image("https://s.france24.com/media/display/d812d2d4-6d49-11ec-b015-005056a90284/w:980/p:16x9/2022-01-04T021438Z_1739487563_RC2SOR9WYABL_RTRMADP_3_OLYMPICS-2022-VENUES.JPG")

    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=country_df['Year'],y=country_df['Medal'],mode='lines+markers',line=dict(color='mediumorchid',width=3,dash='solid')))
    fig.update_layout(xaxis_title='Year',yaxis_title='Medals')
    fig.update_layout(
    
    # Updating X axis features
    xaxis=dict(
    showline=True,
    showgrid=True,
    showticklabels=True,
    linecolor='rgb(204,204,204)',
    linewidth=2,
    ticks='outside',
    tickfont=dict(family='Arial',size=12,color='rgb(82,82,82)')),

    #Updating The Y-Axis Features
    yaxis=dict(
    showgrid=True,
    zeroline=True,
    showline=False,
    showticklabels=True),
    template='plotly_dark')

    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country +" "+"Sports Wise Performence")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    # Most successful athletes in the country
    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_in_Country(df,selected_country)
    st.table(top10_df)

# Athlete Wise Analysis
if user_menu == 'Athlete Wise Analysis':
    st.title("Athelete Analysis")
    st.image("https://theshakerbison.com/wp-content/uploads/2021/02/sports-marketing-1-900x345.jpg")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    # Distribution of Age wrt Sports
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    # Height Vs Weight Graph

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    sns.set_style('darkgrid')
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', s=60, data=temp_df)
    st.pyplot(fig)

    # Men Vs Women Participation
    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
