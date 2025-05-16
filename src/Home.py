import os

import streamlit as st

from conf import Settings

env_file = os.getenv("WEIGHTR_FRONTEND_CONF_FILE", "var/conf/weightr-frontend/.env.dev")
settings = Settings(_env_file=env_file, _env_file_encoding="utf-8")


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
    st.markdown(f"[Log in to Withings]({settings.login_url})")
else:
    st.session_state['session_id'] = session_id
