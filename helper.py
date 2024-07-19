import numpy as np


'''Medal for a particular country or Year'''

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year=='Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
        
        flag =1
        
    if year != 'Overall' and country == 'Overall':
         temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
         temp_df = medal_df[(medal_df['region']== country) & (medal_df['Year']== int(year))]
            
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    x['Total']= x['Gold'] +  x['Silver'] +  x['Bronze']   

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')


    return(x)

def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally =medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] +  medal_tally['Silver'] +  medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally

def country_year_list(df):
    years=df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years , country

#Participating Nations Over Time
def participating_nations_over_time(df):
    XO = df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index()
    XO =XO.rename(columns={'Year':'Editions' ,'count':'No of countries'})
    XO = XO.sort_values('Editions')
    return XO

# Events Over the time 
def events_over_time(df):
    EO = df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index()
    EO = EO.rename(columns={'Year':'Editions' ,'count':'Event'})
    EO = EO.sort_values('Editions')
    return EO

# No Of Atheletes Over the Year 
def ath_over_time(df):
    AO = df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index()
    AO = AO.rename(columns={'Year':'Editions' ,'count':'No Of Atheletes'})
    AO = AO.sort_values('Editions')
    return AO

# Most Successful Atheletes
def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={ 'count': 'Medals','region':'Region'}, inplace=True)
    return x

# Country Wise  Analysis
def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

# Country wise Sports Analysis
def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

# Top 10 Athletes of the country
def most_successful_in_Country(df,Country):
    temp_df = df.dropna(subset=['Medal'])

    
    temp_df = temp_df[temp_df['region'] == Country]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='Name', right_on='Name', how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={ 'count': 'Medals',}, inplace=True)
    return x


# Athletes wise analysis
def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    
# Men Vs Women 
    
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final