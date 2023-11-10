import streamlit as st
from streamlit_ace import st_ace
from streamlit_dynamic_filters import DynamicFilters
import openai
import random
import psycopg2
import pandas as pd
import re
import sqlparse
from st_aggrid import GridOptionsBuilder, AgGrid
import cloudinary
import cloudinary.api
from functions_and_variables import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

#        [data-testid="collapsedControl"] {
#        display: none
#        }
openai.api_key = st.secrets["openai_api_key"]

cloudinary.config( 
  cloud_name = st.secrets["cloudinary_cloud_name"], 
  api_key = st.secrets["cloudinary_api_key"], 
  api_secret = st.secrets["cloudinary_api_secret"]
)

st.markdown(
    """
    <style>

        body {
        margin: 0;
        }
        body h1 {
        padding:0;
        margin-top: 0rem;
        }
        body h3 {
        padding:0;
        margin-top: 1rem;
        margin-bottom: 1rem;
        }
        body img {
        padding: 0 60px;
        }
        .st-emotion-cache-1v0mbdj e115fcil1 {
        padding: 0 40px;
        }
        
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('''
<style>
[data-testid="stHorizontalBlock"]  {
    padding:0;
    gap: 0;
}
div.st-emotion-cache-ocqkz7 e1f1d6gn3 {
    padding:0 140px;
}
div.stButton > button:first-child {
    background-color: white;
    color: #87c0cd;
    border: 1px solid #87c0cd;
    padding: 10px;
}
[data-testid="block-container"] {
    padding: 2rem 1.5rem 2rem;
}
[data-testid="collapsedControl"] {
    display: none
}
</style>
''', unsafe_allow_html=True)



logo = cloudinary.api.resource_by_asset_id("1166fd5abfeb24a93a991cb500f36595")["url"]

col1, col2, col3 = st.columns([5,4,5])
with col1:
    st.write("")
with col2:
    st.image(logo,width=700,use_column_width=True)
with col3:
    st.write("")


col1, col2, col3 = st.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.markdown("<h1 style='padding: 0;text-align: center; color: #113f67;  font-size:2.5rem;'>Daily Dose of <span style=' color:#87c0cd';>PostgreSQL</span></h1><h3 style='text-align: center; color: #113f67; font-size:1.5rem; '>Practice SQL with ChatGPT-Generated Databases, Questions, and Queries.</h3>", unsafe_allow_html=True)
with col3:
    st.write("")

st.title("")
col1, col2, col3, col4, col5 = st.columns([15,15,1,15,15])
with col1:
    st.write("")
with col2:
    switch_to_user = st.button("Practice SQL", use_container_width=True)
    if switch_to_user:
        switch_page("User")
with col3:
    st.markdown("""<p style="color:white">.</p>""", unsafe_allow_html=True)
with col4:
    switch_to_user = st.button("Documentation", use_container_width=True)
    if switch_to_user:
        switch_page("Documentation")
with col5:
    st.write("")

css = '''
<style>
section.main > div:has(~ footer ) {
    padding-bottom: 0px;
}
</style>
'''
st.markdown(css, unsafe_allow_html=True)
