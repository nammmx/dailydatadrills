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


st.set_page_config(layout="wide")

openai.api_key = st.secrets["openai_api_key"]

cloudinary.config( 
  cloud_name = st.secrets["cloudinary_cloud_name"], 
  api_key = st.secrets["cloudinary_api_key"], 
  api_secret = st.secrets["cloudinary_api_secret"]
)
add_logo()

#add_css_and_animations()
add_css()

create_sidebar()

st.sidebar.header("")
######################################################################################## generate chatgpt output on button click

st.title("ChatGPT-4")


if st.button('Generate New Topic'):
    try:
        results_to_variable = generate_chatgpt_results()
        message_history = results_to_variable[0]
        create_tables = results_to_variable[1]
        insert_data = results_to_variable[2]
        display_tables = results_to_variable[3]
        questions = results_to_variable[4]
        hints = results_to_variable[5]
        solution_code = results_to_variable[6]
        solution_code2 = results_to_variable[7]
        solution_explanation = results_to_variable[8]
        solution_explanation2 = results_to_variable[9]
        daily_db_topic = results_to_variable[10]
        daily_sql_topics = results_to_variable[11]


        # convert daily_sql_topics into a string for IN operator in sql query
        string_daily_sql_topics = """"""
        for i in daily_sql_topics:
            string_daily_sql_topics+= f"""\'{i}\',"""
        string_daily_sql_topics = string_daily_sql_topics.rstrip(",")
        query_daily_sql_topics_id_junction = f"""select daily_sql_topics_id from daily_sql_topics where sql_topic IN ({string_daily_sql_topics});"""

        # daily_tables
        populate_daily_tables_arguments = []
        populate_daily_tables_arguments.append((daily_db_topic, create_tables, insert_data, display_tables, questions, hints, solution_code, solution_code2, solution_explanation, solution_explanation2))
        execute_query(query = populate_daily_tables, query_arguments = populate_daily_tables_arguments, role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin)
        daily_tables_id_for_junction_table = execute_query(query = query_daily_tables_id_junction, role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin)
        daily_tables_id_for_junction_table = daily_tables_id_for_junction_table[0][0]

        # daily_sql_topics
        list_of_results = execute_query(query = query_daily_sql_topics_id_junction, role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin)
        daily_sql_topics_id_junction = []
        for i in list_of_results:
            daily_sql_topics_id_junction.append(i[0])
        populate_daily_sql_topics_arguments = []
        for i in range(0, len(daily_sql_topics_id_junction)):
            populate_daily_sql_topics_arguments.append((daily_tables_id_for_junction_table,daily_sql_topics_id_junction[i]))
        execute_query(query = populate_dailytables_dailysqltopics, query_arguments = populate_daily_sql_topics_arguments, len_query_list = len(daily_sql_topics_id_junction), role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin)

        st.write("New topic generated and added to topic database!")
    except Exception as error:
        st.write(error)

######################################################################################## display topic database

try:
    options = execute_query("SELECT a.daily_tables_id AS ID, a.date_created AS Date, b.sql_topic AS SQL_Topic, a.daily_db_topic AS DB_Topic, a.question FROM daily_tables AS a INNER JOIN dailytables_dailysqltopics AS c ON a.daily_tables_id = c.daily_tables_id INNER JOIN daily_sql_topics AS b ON b.daily_sql_topics_id = c.daily_sql_topics_id;",role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin)
    options_sql = []
    for i in range(0,len(options)):
        options_sql.append(options[i][2])
        
    options_db = []
    for i in range(0,len(options)):
        options_db.append(options[i][3])

    options_id = []
    for i in range(0,len(options)):
        options_id.append(options[i][0])
        
    options_question = []
    for i in range(0,len(options)):
        options_question.append(options[i][4])
        
    options_date = []
    for i in range(0,len(options)):
        options_date.append(options[i][1].strftime('%Y-%m-%d'))

    df = pd.DataFrame(list(zip(options_id, options_date, options_sql, options_db, options_question)),
            columns =['ID', 'Date', 'SQL Topics', 'DB Topics', 'Question'])
    df = df.sort_values(["Date","ID"], ascending=[False,False])
except Exception as error:
    st.write(error)


gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_grid_options(domLayout='normal')
gb.configure_default_column(**defaultColDef)
gb.configure_side_bar()
gb.configure_selection(use_checkbox=True)
gridOptions = gb.build()

st.title("Topic Database")
st.write("Note: Select a topic by checking the box in the ID column. De-select current selection before making a new selection.")
display_options = AgGrid(df, theme="alpine", enable_quicksearch=True, gridOptions=gridOptions, data_return_mode="FILTERED", columns_auto_size_mode="FIT_CONTENTS")
st.divider()

######################################################################################## generate editors and queries 
create_editor(display_options=display_options, selected_id=selected_id, step_editor_empty=create_tables_query_empty, ace_key=key_create_tables,ace_key2=key_create_tables_2, step_query=step_query_create_tables, step_editor=step_editor_create_tables,header=header_create_table,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin,aggrid_key=aggrid_key_create_tables)
create_editor(display_options=display_options, selected_id=selected_id, step_editor_empty=insert_data_query_empty, ace_key=key_insert_data,ace_key2=key_insert_data_2, step_query=step_query_insert_data, step_editor=step_editor_insert_data,header=header_insert_data,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin,aggrid_key=aggrid_key_insert_data)
create_editor(display_options=display_options, selected_id=selected_id, step_editor_empty=display_tables_query_empty, ace_key=key_display_tables,ace_key2=key_display_tables_2, step_query=step_query_display_tables, step_editor=step_editor_display_tables,header=header_display_tables,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin,aggrid_key=aggrid_key_display_tables, image="yes", erd_url=erd_url)
create_texts(display_options=display_options, selected_id=selected_id, step_query=step_query_questions,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin, header=header_question)
on_hints = st.toggle('Show Hints')
if on_hints:
    create_texts(display_options=display_options, selected_id=selected_id, step_query=step_query_hints,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin, header=header_hints)
solve_empty = st_ace(key = "key_solve", language="sql", placeholder="Write your query here", min_lines=20, keybinding="vscode", theme="sqlserver", wrap="true",font_size=14)
if solve_empty:
    execute_query_2(query=solve_empty,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin)
st.header('Solutions')
on_solutions = st.toggle('Show Solutions')
if on_solutions:
    create_texts(display_options=display_options, selected_id=selected_id, step_query=step_query_solution_1_explanation,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin, header=header_solution_1_explanation)
    create_editor(display_options=display_options, selected_id=selected_id, step_editor_empty=solution_1_query_empty, ace_key=key_solution_1,ace_key2=key_solution_1_2, step_query=step_query_solution_1, step_editor=step_editor_solution_1,header=header_solution_1,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin,aggrid_key=aggrid_key_solution_1)
    create_texts(display_options=display_options, selected_id=selected_id, step_query=step_query_solution_2_explanation,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin, header=header_solution_2_explanation)
    create_editor(display_options=display_options, selected_id=selected_id, step_editor_empty=solution_2_query_empty, ace_key=key_solution_2,ace_key2=key_solution_2_2, step_query=step_query_solution_2, step_editor=step_editor_solution_2,header=header_solution_2,role_hostname=hostname_admin, role_database=database_admin, role_username=username_admin, role_port_id=port_id_admin, role_pwd=pwd_admin,aggrid_key=aggrid_key_solution_2)






