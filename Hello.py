# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
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
    
            .container {
            position: fixed;
            top:0;
            left:0;
            width: 100%;
            height: 100%;
            display: grid;
            }
    
            .square {
            position: absolute;
            bottom: -100px;
            animation: boxes 2s infinite ease-out;
            }
    
            .square:nth-child(1) {
            width: 4.7rem;
            height: 4.7rem;
            left: 7%;
            animation-duration: 6800ms;
            }
            .square:nth-child(2) {
            width: 5.1rem;
            height: 5.1rem;
            left: 22%;
            animation-delay: 280ms;
            animation-duration: 9.8s;
            }
    
            .square:nth-child(3) {
            width: 6.25rem;
            height: 6.25rem;
            left: 39%;
            animation-delay: 405ms;
            animation-duration: 11s;
            }
            .square:nth-child(4) {
            width: 3rem;
            height: 3rem;
            left: 49%;
            animation-delay: 855ms;
            animation-duration: 15s;
            }
    
            .square:nth-child(5) {
            width: 6rem;
            height: 6rem;
            left: 59%;
            animation-delay: 803ms;
            animation-duration: 7654ms;
            }
            .square:nth-child(6) {
            width: 3.3rem;
            height: 3.3rem;
            left: 68%;
            animation-delay: 1203ms;
            animation-duration: 9999ms;
            }
            .square:nth-child(7) {
            width: 3.8rem;
            height: 3.8rem;
            left: 79%;
            animation-delay: 103ms;
            animation-duration: 7600ms;
            }
            .square:nth-child(8) {
            width: 4.2rem;
            height: 4.2rem;
            left: 73%;
            animation-delay: 143ms;
            animation-duration: 12500ms;
            }
    
            .square:nth-child(9) {
            width: 3.5rem;
            height: 3.5rem;
            left: 92%;
            animation-delay: 1105ms;
            animation-duration: 10050ms;
            }
    
            .square:nth-child(10) {
            width: 7rem;
            height: 7rem;
            left: 11%;
            animation-delay: 925ms;
            animation-duration: 15000ms;
            }
    
            .square:nth-child(11) {
            width: 3rem;
            height: 3rem;
            left: 18%;
            animation-delay: 1300ms;
            animation-duration: 9000ms;
            }
    
            .square:nth-child(12) {
            width: 2.5rem;
            height: 2.5rem;
            left: 29%;
            animation-delay: 600ms;
            animation-duration: 16000ms;
            }
    
            .square:nth-child(13) {
            width: 5rem;
            height: 5rem;
            left: 3%;
            animation-delay: 1400ms;
            animation-duration: 7000ms;
            }
    
            .square:nth-child(14) {
            width: 6rem;
            height: 6rem;
            left: 55%;
            animation-delay: 925ms;
            animation-duration: 5000ms;
            }
    
            .square:nth-child(15) {
            width: 2rem;
            height: 2rem;
            left: 84%;
            animation-delay: 525ms;
            animation-duration: 11000ms;
            }
    
            @keyframes boxes {
            0% {
                top: 110vh;
                opacity: 0.35;
            }
            100% {
                top: -15vh;
                transform: rotate(200deg);
                opacity: 0.35;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown('''
    <style>
    [data-testid="stHorizontalBlock"]  {
        padding:0 40px;
    }
    div.stButton > button:first-child {
        background-color: white;
        color: #87c0cd;
        border: 1px solid #87c0cd;
        padding: 10px;
    }
    [data-testid="collapsedControl"] {
        display: none
    }
    </style>
    ''', unsafe_allow_html=True)
    
    html_string = """
    <div class="container">
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697376224/dailysql/xtehaheljgssameikri5.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697430070/dailysql/kh6vc5tk6abmtnraqyuh.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697376224/dailysql/xtehaheljgssameikri5.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697430070/dailysql/kh6vc5tk6abmtnraqyuh.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697376224/dailysql/xtehaheljgssameikri5.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697430070/dailysql/kh6vc5tk6abmtnraqyuh.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697376224/dailysql/xtehaheljgssameikri5.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697430070/dailysql/kh6vc5tk6abmtnraqyuh.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697376224/dailysql/xtehaheljgssameikri5.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697430070/dailysql/kh6vc5tk6abmtnraqyuh.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697376224/dailysql/xtehaheljgssameikri5.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697430070/dailysql/kh6vc5tk6abmtnraqyuh.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697376224/dailysql/xtehaheljgssameikri5.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697430070/dailysql/kh6vc5tk6abmtnraqyuh.png"/>
        <img class="square" src="https://res.cloudinary.com/drwsupfyj/image/upload/v1697376224/dailysql/xtehaheljgssameikri5.png"/>
    </div>
    """
    st.markdown(html_string, unsafe_allow_html=True)
    
    logo = cloudinary.api.resource_by_asset_id("1166fd5abfeb24a93a991cb500f36595")["url"]
    
    col1, col2, col3 = st.columns([5,3,5])
    with col1:
        st.write("")
    with col2:
        st.image(logo,width=700,use_column_width=True)
    with col3:
        st.write("")
    
    
    col1, col2, col3 = st.columns([1,6,1])
    with col1:
        st.write("")
    with col2:
        st.markdown("<h1 style='text-align: center; color: #113f67;  font-size:2.5rem;'>Daily Dose of <span style=' color:#87c0cd';>PostgreSQL</span></h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #113f67; font-size:1.5rem; '>Practice SQL with ChatGPT-Generated Databases, Questions, and Queries.</h1>", unsafe_allow_html=True)
    with col3:
        st.write("")
    
    st.title("")
    col1, col2, col3, col4 = st.columns([4,4,4,4])
    with col1:
        st.write("")
    with col2:
        switch_to_user = st.button("Practice SQL", use_container_width=True)
        if switch_to_user:
            switch_page("User")
    with col3:
        switch_to_user = st.button("Documentation", use_container_width=True)
        if switch_to_user:
            switch_page("Documentation")
    with col4:
        st.write("")
    
    



if __name__ == "__main__":
    run()
