import plotly.express as px
import streamlit as st

from util import load_weight_data

st.set_page_config(page_title="Overview", page_icon="📈")
st.title("Overview")
st.sidebar.header("Overview")
st.markdown("Here is your historical weight data.")

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
    fig = px.line(df, x=df.index, y='Weight (lb)', title='Weight by Date')
    st.plotly_chart(fig)

    # TODO show stats: min, max, avg.  Maybe show markers on graph

    if st.checkbox('Show raw data'):
        st.write(df)
