import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import gaussian_kde
import numpy as np
from util import load_weight_data


st.set_page_config(page_title="Distributions", page_icon="📊")
st.title("Distributions")
st.sidebar.header("Distributions")
st.markdown("Here is the distribution of your weight.")

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

weights = df["Weight (lb)"]

# KDE using scipy
kde = gaussian_kde(weights)
x_vals = np.linspace(weights.min(), weights.max(), 200)
kde_vals = kde(x_vals)

# Create the histogram
hist = go.Histogram(
    x=weights,
    nbinsx=30,
    histnorm='probability density',
    name='Histogram',
    opacity=0.6
)

# Create the KDE line
kde_line = go.Scatter(
    x=x_vals,
    y=kde_vals,
    mode='lines',
    name='Distribution',
    line=dict(width=2)
)

# Combine and plot
fig = go.Figure(data=[hist, kde_line])
fig.update_layout(
    title='Weight Distribution',
    xaxis_title='Weight (lb)',
    yaxis_title='Density',
    bargap=0.2
)

# Display in Streamlit
st.plotly_chart(fig)
