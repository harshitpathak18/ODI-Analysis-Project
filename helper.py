import pandas as pd


# Matches-------------------------------------------
def match_list(df):
    match_list=list(df['Scorecard'])
    match_list.sort()
    match_list.insert(0,"All")
    return match_list

def country_list(df):
    countries_list=list(df['Team 1'].unique())
    countries_list.sort()
    return countries_list

def country_played_over_years(df,country):
    if country=="All":
        Yf=df["Year"].value_counts().reset_index()
    else:
        Yf=df[(df['Team 1']==country) | (df['Team 2']==country)]['Year'].value_counts().reset_index()
    Yf=Yf.rename(columns={"index":"Year","Year":"Matches Played"})
    Yf=Yf.sort_values(by=["Year"])
    return Yf

def win_loss(df):
    new_df=df['Winner'].value_counts().reset_index()
    new_df=new_df.rename(columns={"index":"Country","Winner":"Won"})
    new_df=new_df.sort_values(by="Country")
    
    l=country_list(df)
    List=[]
    x=df
    for i in range(22):
        x=df[((df['Team 1']==l[i]) | (df['Team 2']==l[i])) & (df['Winner']!=l[i])]['Winner'].count()
        List.append(x)
    List[20]=0
    List[21]=351
    List.append(345)
    new_df['Loss']=List
    new_df["ODI_Played"]=new_df['Won']+new_df['Loss']

    new_df["Win%"]=(new_df["Won"]/new_df["ODI_Played"])*100
    new_df["Loss%"]=(new_df["Loss"]/new_df["ODI_Played"])*100

    return new_df

def opp_matches(df,country):
    Ind=df[(df['Team 1']==country) | (df['Team 2']==country)]
    x1=Ind[df['Team 1']!=country]["Team 1"].value_counts()
    x2=Ind[df['Team 2']!=country]["Team 2"].value_counts()
    z=x1.append(x2).reset_index()
    l=list(z["index"].unique())
    team=[]
    matches=[]
    for i in range(len(l)):
        m=z[z["index"]==l[i]].sum()[0]
        team.append(l[i])
        matches.append(m)
    data=pd.DataFrame()
    data["Opponent"]=team
    data["Matches"]=matches
    return data

def win_loss_with_countries(df,country):
    Opponent=[]
    t_win=[]
    op_win=[]
    Country_list= country_list(df)
    for i in range(len(Country_list)):
        opp=Country_list[i]
        if opp!=country:
            x1=df[(df['Team 1']==country) & (df["Team 2"]==opp)]['Winner'].value_counts().reset_index()
            x2=df[(df['Team 2']==country) & (df["Team 1"]==opp)]['Winner'].value_counts().reset_index()
            z=x1.append(x2)
            team=z[z['index']==country].sum()["Winner"]
            opp_win=z[z['index']==opp].sum()["Winner"]
            Opponent.append(opp)
            op_win.append(opp_win)
            t_win.append(team)
    data=pd.DataFrame()
    data['Nation']=Opponent
    data["Loss"]=op_win
    data["Win"]=t_win

    data["Loss"]=data["Loss"].astype('int')
    data["Win"]=data["Win"].astype('int')
    data["Total_matches"]=data["Loss"]+data["Win"]
    return data



# Battings
def Country_Wise_batting(df):
    country=[]
    runs=[]
    fifty=[]
    hundered=[]
    nation=df['Nation'].unique()
    nation.sort()
    data=pd.DataFrame()
    for i in nation:
        x=df[df['Nation']==i]['Runs'].sum()
        y=df[df['Nation']==i]['100'].sum()
        z=df[df['Nation']==i]['50'].sum()
        country.append(i)
        runs.append(x)
        hundered.append(y)
        fifty.append(z)
        
    data['Country']=country
    data['Runs']=runs
    data['100s']=hundered
    data['50s']=fifty
    return data

def sort_record_batting(df,feature):
    df=df.rename(columns={"Player":"Name","HS":"Highest Score","Ave":"Average","SR":"Strike Rate","100":"100s","50":"50s"})
    top_10=df.sort_values(by=feature,ascending=False)
    top_10=top_10[top_10['Mat']>=20]
    top_10=top_10.head(15)
    return top_10[['Name',feature,'Nation']]

def player_stats_batting(df,name):
    x=df[df['Player']==name]
    Span=x['Span'].values[0]
    Matches=x['Mat'].values[0]
    Innings=x['Inns'].values[0]
    Runs=x['Runs'].values[0]
    Highest_Score=x['HS'].values[0]
    Average=x['Ave'].values[0]
    Strike_Rate=x['SR'].values[0]
    Hundreds=x['100'].values[0]
    Fifties=x['50'].values[0]
    Nation=x['Nation'].values[0]
    Not_out=x['NO'].values[0]
    return Not_out,Span,Matches,Innings,Runs,Highest_Score,Average,Strike_Rate,Hundreds,Fifties,Nation


# Bowling
def Country_Wise_bowling(df):
    country=[]
    Wickets=[]
    fours=[]
    fives=[]
    nation=df['Nation'].unique()
    nation.sort()
    data=pd.DataFrame()
    for i in nation:
        x=df[df['Nation']==i]['Wkts'].sum()
        y=df[df['Nation']==i]['4'].sum()
        z=df[df['Nation']==i]['5'].sum()
        country.append(i)
        Wickets.append(x)
        fours.append(y)
        fives.append(z)
        
    data['Country']=country
    data['Wickets']=Wickets
    data['4 Wickets']=fours
    data['5 Wickets']=fives
    return data

def sort_record_bowling(df,feature):
    df=df.rename(columns={"Player":"Name","Wkts":"Wickets","Ave":"Average","SR":"Strike Rate","4":"4 Wickets","5":"5 Wickets","Econ":"Economy"})
    
    if (feature=="Average") | (feature=="Strike Rate") | (feature=="Economy"):
        top_10=df.sort_values(by=feature)   
    else:
        top_10=df.sort_values(by=feature,ascending=False)
    top_10=top_10[top_10['Mat']>=20]
    top_10=top_10.head(15)
    return top_10[['Name',feature,'Nation']]


def player_stats_bowling(df,name):
    x=df[df['Player']==name]
    Span=x['Span'].values[0]
    Matches=x['Mat'].values[0]
    Innings=x['Inns'].values[0]
    Balls=x['Balls'].values[0]
    Runs=x['Runs'].values[0]
    Wickets=x['Wkts'].values[0]
    BBI=x['BBI'].values[0]
    Average=x['Ave'].values[0]
    Economy=x['Econ'].values[0]
    Strike_Rate=x['SR'].values[0]
    Fours=x['4'].values[0]
    Fives=x['5'].values[0]
    Nation=x['Nation'].values[0]
    return Span,Matches,Innings,Balls,Runs,Wickets,BBI,Average,Economy,Strike_Rate,Fours,Fives,Nation