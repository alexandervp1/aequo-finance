import streamlit as st
import plotly.express as px
import pandas as pd
import numpy
import warnings
warnings.filterwarnings('ignore')

 
df_db = pd.read_csv("../../data/ps_data.csv", comment="#", 
                    usecols=["hostname", "sy_snum", "sy_pnum", "st_teff", "st_rad", "st_mass", "st_logg",
                             "sy_dist"])

df_db = df_db.head(100)

fig = px.scatter(
    df_db,
    x="st_mass",
    y="st_rad",
    color="sy_dist",
    hover_data="hostname"
    )

st.plotly_chart(fig)

st.write("This is a message")