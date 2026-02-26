import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st

st.sidebar.checkbox("Show raw data", key="show_data")


st.sidebar.radio("Select a plot type", (
    "Medal Distribution", "Age Distribution", "Height vs Weight"
    ), key="plot_type")