import pandas as pd



def preprocess(df,r_df):
    #filtering Summer Olympics
    df = df[df['Season']== 'Summer']
    #Merge With r_df
    df=df.merge(r_df,on='NOC',how='left')
    #Droping Duplicates
    df.drop_duplicates(inplace=True)
    # One Hot Encoading
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return df 