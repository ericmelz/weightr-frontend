import plotly.express as px
import streamlit as st

from util import load_weight_data

st.title("My Withings Weight Tracker")

# Get session_id from URL
query_params = st._get_query_params()
session_id = query_params.get("session_id", [None])[0]

if not session_id:
    st.write("Please log in to view your weight data.")
    st.markdown("[Log in with Withings](http://localhost/withings-login)")
else:
    st.success("Authenticated!")
    with st.spinner("Fetching weight data..."):
        df = load_weight_data(session_id)
    st.dataframe(df)
    fig = px.line(df, x=df.index, y='weight', title='Weight')
    st.plotly_chart(fig)
