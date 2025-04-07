import pandas as pd
import plotly.express as px
import streamlit as st

from util import load_weight_data

st.set_page_config(page_title="Weight Loss", page_icon="📉")
st.title("Weight Loss")
st.sidebar.header("Weight Loss")
st.markdown("Here is some data about your weight loss attempts.")

session_id = None
if 'session_id' in st.session_state:
    session_id = st.session_state['session_id']

if not session_id:
    st.write("Please log in with withings on the Home page to view your weight data.")
    st.markdown("[Home](/)")  # TODO this link opens a new browser tab.  Make it open to the same tab
else:
    st.session_state['session_id'] = session_id
    with st.spinner("Fetching weight data..."):
        df = load_weight_data(session_id)

    curr_year = int(df.iloc[0]['Year'])
    prev_year = curr_year - 1
    df_curr = df[df['Year'] == curr_year].copy()
    df_prev = df[df['Year'] == prev_year].copy()
    combined_df = pd.concat(([df_prev, df_curr]))
    fig = px.line(combined_df, x='Day of Year', y='Weight (lb)', color='Year', title='Weight This Year vs Last Year')

    st.plotly_chart(fig)



