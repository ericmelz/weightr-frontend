import plotly.express as px
import streamlit as st

from util import load_weight_data

DEVELOPMENT_ENV = 'dev.docker'
DEVELOPMENT_ENV_TO_LOGIN_URL = {
    'dev': 'http://localhost/local-withings-login',
    'dev.docker': 'http://localhost/k3d-withings-login'
}
LOGIN_URL = DEVELOPMENT_ENV_TO_LOGIN_URL.get(DEVELOPMENT_ENV, 'http://localhost/local-withings-login')

st.set_page_config(
    page_title="Weightr.ai",
    page_icon="📉"
)

st.title("Weightr.ai")

session_id = None
if 'session_id' in st.session_state:
    session_id = st.session_state['session_id']

st.markdown(
    """
    This site shows some fun facts about your weight.  You need to have a Withings smart scale 
    along with a Withings account. 
    * **📈 Overview** - shows historic weight
    * **📉 Weight Loss** - shows visualizations of attempted weight loss episodes 
    * **📊 Distribution** - shows some interactive weight distribution visualizations

    Questions? Contact <eric@emelz.com>

    Enjoy!
    """
)

# Get session_id from URL
query_params = st._get_query_params()
session_id = None
if 'session_id' in st.session_state:
    session_id = st.session_state['session_id']

# Query params session overrides cached session
session_id_from_query_params = query_params.get("session_id", [None])[0]
if session_id_from_query_params:
    session_id = session_id_from_query_params

if not session_id:
    st.markdown('---')
    st.write("Please log in to view your weight data.")
    st.markdown(f"[Log in to Withings]({LOGIN_URL})")
else:
    st.session_state['session_id'] = session_id
