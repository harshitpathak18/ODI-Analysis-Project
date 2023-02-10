import pandas  as pd
import streamlit as st
import plotly.express as px
import helper
from PIL import Image

# read csv file
match_df=pd.read_csv("new_match.csv")
batting_df=pd.read_csv("new_batting.csv")
bowling_df=pd.read_csv("new_bowling.csv")


# sidebar
image = Image.open('logo.png')
st.sidebar.image(image)
st.sidebar.title("ODI-Analysis")
menu=st.sidebar.radio("Select Options",("MATCHES","BATTING","BOWLING","RECORDS"))

# ODI Matches Analysis
if menu=="MATCHES":
    df=match_df
    menu_1=st.sidebar.radio("Select Options",("Overall Analysis","Country-Wise Analysis"))
    

    # Overall Analysis
    if menu_1=="Overall Analysis":
        st.title("ODIs Overall Analysis")
        match_list=helper.match_list(df)
        option=st.selectbox("Select match number",match_list)
        if option=="All":
            st.dataframe(df)
        else:
            st.dataframe(df[(df['Scorecard']==option)])

        st.write("---")
        win_loss_df=helper.win_loss(df)

        # Line chart
        temp_df=helper.country_played_over_years(df,"All")
        fig = px.line(temp_df, x="Year", y="Matches Played")
        st.subheader("Matches played over the years")
        st.plotly_chart(fig)

        # Win & Loss
        st.subheader("Win & Loss by Countries")
        temp=st.selectbox("Select Win or Loss",("Win","Loss"))
        if temp=="Win":
            fig = px.bar(win_loss_df, x='Country', y='Won',color="Won")
            st.plotly_chart(fig)
        if temp=="Loss":
            fig = px.bar(win_loss_df, x='Country', y='Loss',color="Loss")
            st.plotly_chart(fig)

        # Inning wise winner
        st.write("---")
        st.subheader("Winning Team By Innnings")
        fig = px.histogram(df, x="WinInn")
        fig.update_layout(bargap=0.4)
        st.plotly_chart(fig)


    # Counrty wise Analysis
    if menu_1=="Country-Wise Analysis":
        win_loss_df=helper.win_loss(df)
        st.title("ODIs Country Wise Analysis")
        countries_list=helper.country_list(df)
        option1=st.selectbox("Select Country",countries_list)

        win = win_loss_df[win_loss_df["Country"]==option1]["Won"]
        loss = win_loss_df[win_loss_df["Country"]==option1]["Loss"]
        win_ratio = win_loss_df[win_loss_df["Country"]==option1]["Win%"]
        loss_ratio = win_loss_df[win_loss_df["Country"]==option1]["Loss%"]
        total_matches = win_loss_df[win_loss_df["Country"]==option1]["ODI_Played"]
        
        st.write("---")
        st.header(f"{option1} Match Stats")
        st.subheader(f"Total matches:- {int(total_matches)}")
        col1,col2=st.columns(2)
        with col1:
            st.metric(label="Won", value=win)
            st.metric(label="Winning%", value=round(win_ratio,2))
        with col2:
            st.metric(label="Loss", value=loss)
            st.metric(label="Lossing%", value=round(loss_ratio,2))


        st.write("---")
        win_loss_country=helper.win_loss_with_countries(df,option1)
        win_loss_country=win_loss_country.sort_values(by="Total_matches",ascending=False).head(15)

        st.header(f"{option1} against other countries")
        temp=st.selectbox("Select",("Total Matches","Win","Loss"))

        if temp=="Total Matches":
            st.subheader("Matches played against other countries")
            fig = px.bar(win_loss_country, x='Nation', y='Total_matches')
            st.plotly_chart(fig)

        if temp=="Win":
            st.subheader("Wins against other countries")
            fig = px.bar(win_loss_country, x="Nation", y="Win")
            st.plotly_chart(fig)
        
        if temp=="Loss":
            st.subheader("Losses against other countries")
            fig = px.bar(win_loss_country, x="Nation", y="Loss")
            st.plotly_chart(fig)

        temp_df=helper.country_played_over_years(df,option1)
        fig = px.line(temp_df, x="Year", y="Matches Played")
        st.subheader(f" Matches played by {option1} over the years")
        st.plotly_chart(fig)


# ODI Batting Analysis
if menu=="BATTING":
    df=batting_df

    # Known country
    df=df[(df['Nation']=="INDIA") | (df['Nation']=="SL") |(df['Nation']=="AUS") |(df['Nation']=="PAk") |(df['Nation']=="WI") |(df['Nation']=="NZ") |(df['Nation']=="SA") |(df['Nation']=="BDESH") |(df['Nation']=="ZIM") | (df['Nation']=="ENG") | (df['Nation']=="AFG") |(df['Nation']=="SCOT") |(df['Nation']=="HKG")]
    
    st.title("ODI Batting Analysis")

    # Country wise stat
    st.write("---")
    st.header("Overall Batting Stats Nation-Wise")
    Country_Wise=helper.Country_Wise_batting(df)
    choice=st.selectbox("Select Options",("Runs","100s","50s"))
    fig = px.bar(Country_Wise, x='Country', y=choice)
    fig.update_traces(marker_color='blue')
    st.plotly_chart(fig)

    # Player's Batting Stat
    st.write("---")
    st.header("Particular Nation's Players Records")
    nation=list(df["Nation"].unique())
    nation.sort()
    nation.insert(0,"All")
    country=st.selectbox("Select Country",(nation))
    if country!="All":
        st.dataframe(df[df['Nation']==country])
    else:
        st.dataframe(df)


    # Particular Batter's Stats
    st.write("---")
    st.header("Particular Player's Record")
    players=list(df['Player'])
    choice=st.selectbox("Select Player",players)
    Not_out,Span,Matches,Innings,Runs,Highest_Score,Average,Strike_Rate,Hundreds,Fifties,Nation=helper.player_stats_batting(df,choice)

    st.header(f"{choice} Carrier Stats")
    col1,col2=st.columns(2)
    with col1:
        st.write(f"**Nation:** ***{Nation}***")
        st.write(f"**Matches:** *{Matches}*")
        st.write(f"**Innings:** *{Innings}*")
        st.write(f"**Runs:** *{Runs}*")
        st.write(f"**Highest Score:** *{Highest_Score}*")
        st.write(f"**Not Out:** *{Not_out}*")
    with col2:
        st.write(f"**Span:** *{Span}*")
        st.write(f"**100s:** *{Hundreds}*")
        st.write(f"**50s:** *{Fifties}*")
        st.write(f"**Average:** *{Average}*")
        st.write(f"**Strike Rate:** *{Strike_Rate}*")
        

# ODI Bowling
if menu=="BOWLING":
    df=bowling_df

    # Known country
    df=df[(df['Nation']=="INDIA") | (df['Nation']=="SL") |(df['Nation']=="AUS") |(df['Nation']=="PAk") |(df['Nation']=="WI") |(df['Nation']=="NZ") |(df['Nation']=="SA") |(df['Nation']=="BDESH") |(df['Nation']=="ZIM") | (df['Nation']=="ENG") | (df['Nation']=="AFG") |(df['Nation']=="SCOT") |(df['Nation']=="HKG")]
    
    st.title("ODI Bowling Analysis")
    
    # Country wise stat
    st.write("---")
    st.header("Overall Bowling Stats Nation-Wise")
    Country_Wise=helper.Country_Wise_bowling(df)
    choice=st.selectbox("Select Options",("Wickets","4 Wickets","5 Wickets"))
    fig = px.bar(Country_Wise, x='Country', y=choice)
    fig.update_traces(marker_color='blue')
    st.subheader(f"Country-wise Total {choice}")
    st.plotly_chart(fig)

    # Player's Batting Stat
    st.write("---")
    st.header("Particular Nation's Players Records")
    nation=list(df["Nation"].unique())
    nation.sort()
    nation.insert(0,"All")
    country=st.selectbox("Select Country",(nation))
    if country!="All":
        st.dataframe(df[df['Nation']==country])
    else:
        st.dataframe(df)


    # Particular Bowler's Stats
    st.write("---")
    st.header("Particular Player's Record")
    players=list(df['Player'])
    choice=st.selectbox("Select Player",players)
    Span,Matches,Innings,Balls,Runs,Wickets,BBIs,Average,Economy,Strike_Rate,Fours,Fives,Nation=helper.player_stats_bowling(df,choice)
    
    st.subheader(f"{choice} Carrier Stats")
    col1,col2=st.columns(2)
    with col1:
        st.write(f"**Nation:** ***{Nation}***")
        st.write(f"**Matches:** *{Matches}*")
        st.write(f"**Innings:** *{Innings}*")
        st.write(f"**Balls:** *{Balls}*")
        st.write(f"**Runs:** *{Runs}*")
        st.write(f"**BBI** *{BBIs}*")
    with col2:
        st.write(f"**Span:** *{Span}*")
        st.write(f"**Wickets:** *{Wickets}*")
        st.write(f"**Average:** *{Average}*")
        st.write(f"**Economy:** *{Economy}*")
        st.write(f"**4-wickets:** *{Fours}*")
        st.write(f"**5-wickets:** *{Fives}*")

        
# Records
if menu=="RECORDS":
    st.title("ODI RECORDS")
    menu_1=st.selectbox("Select Options",("Batting Records","Bowling Records"))
    
    if menu_1=="Batting Records":
        st.header("ODI Batting Records")
    
        # Top 10 in everything
        df=batting_df        
        feature=st.selectbox("SELECT RECORD",("Most Runs","Most 100s","Most 50s","Best Average","Best Strike Rate"))
        if feature=="Most Runs":
            st.subheader("Most Runs")
            record=helper.sort_record_batting(df,"Runs")
            st.table(record)

        if feature=="Most 100s":
            st.subheader("Most 100s")
            record=helper.sort_record_batting(df,"100s")
            st.table(record)

        if feature=="Most 50s":
            st.subheader("Most 50s")
            record=helper.sort_record_batting(df,"50s")
            st.table(record)

        if feature=='Best Average':
            st.subheader("Best Average")
            record=helper.sort_record_batting(df,"Average")
            st.table(record)

        if feature=="Best Strike Rate":
            st.subheader("Best Strike Rate")
            record=helper.sort_record_batting(df,"Strike Rate")
            st.table(record)
    
    if menu_1=="Bowling Records":
        st.header("ODI Bowling Records")
    
        # Top 10 in everything
        df=bowling_df        
        st.write("---")
        feature=st.selectbox("Select Options",("Most Wickets","Most 4 Wickets","Most 5 Wickets","Best Average","Best Strike Rate","Best Economy"))
        if feature=="Most Wickets":
            st.subheader("Most Wickets")
            record=helper.sort_record_bowling(df,"Wickets")
            st.table(record)

        if feature=="Most 5 Wickets":
            st.subheader("Most 5 Wickets")
            record=helper.sort_record_bowling(df,"5 Wickets")
            st.table(record)

        if feature=="Most 4 Wickets":
            st.subheader("Most 4 Wickets")
            record=helper.sort_record_bowling(df,"4 Wickets")
            st.table(record)

        if feature=='Best Average':
            st.subheader("Best Average")
            record=helper.sort_record_bowling(df,"Average")
            st.table(record)

        if feature=="Best Strike Rate":
            st.subheader("Best Strike Rate")
            record=helper.sort_record_bowling(df,"Strike Rate")
            st.table(record)
        
        if feature=="Best Economy":
            st.subheader("Best Economy")
            record=helper.sort_record_bowling(df,"Economy")
            st.table(record)