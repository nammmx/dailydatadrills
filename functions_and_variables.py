import streamlit as st
from streamlit_ace import st_ace
import openai
import random
import psycopg2
import pandas as pd
import re
import sqlparse
import cloudinary
import cloudinary.api
import hmac
from st_aggrid import GridOptionsBuilder, AgGrid

hostname_user = st.secrets["hostname_user"]
database_user = st.secrets["database_user"]
username_user = st.secrets["username_user"]
port_id_user = st.secrets["port_id_user"]
pwd_user = st.secrets["pwd_user"]

hostname_admin = st.secrets["hostname_admin"]
database_admin = st.secrets["database_admin"]
username_admin = st.secrets["username_admin"]
port_id_admin = st.secrets["port_id_admin"]
pwd_admin = st.secrets["pwd_admin"]

custom_css = {
    ".ag-row-hover": {"background-color": "#87c0cd !important"},
    ".ag-header-cell-text": {"color": "#113f67 !important;"},
    ".ag-theme-streamlit .ag-cell": {"color": "#113f67 !important;"},
    ".ag-side-button-label": {"color": "#113f67 !important;"},
    ".ag-icon ag-icon-columns": {"color": "#113f67 !important;"},
    ".ag-side-buttons": {"background-color": "rgb(222, 225, 230,0.25) !important;"},
    ".ag-header-viewport ": {"background-color": "rgb(222, 225, 230,0.25) !important;"},
}
#################################################################################################### Functions


def create_sidebar():
    st.sidebar.divider()
    st.sidebar.write("")
    st.sidebar.subheader("Quick Queries")
    st.sidebar.write("")
    st.sidebar.write("Data Query (DQL)")
    quick_queries_data_query = st.sidebar.selectbox(label='Data Query',label_visibility="collapsed",options=('Email', 'Home phone', 'Mobile phone'), index=None, placeholder="Select Task")
    st.sidebar.code(quick_queries_data_query, language="sql")
    st.sidebar.write("")
    st.sidebar.write("Data Definition (DDL)")
    quick_queries_data_definition = st.sidebar.selectbox(label='Data Definition',label_visibility="collapsed",options=('Email', 'Home phone', 'Mobile phone'), index=None, placeholder="Select Task")
    st.sidebar.code(quick_queries_data_definition, language="sql")
    st.sidebar.write("")
    st.sidebar.write("Data Manipulation (DML)")
    quick_queries_data_manipulation = st.sidebar.selectbox(label='Data Manipulation',label_visibility="collapsed",options=('Email', 'Home phone', 'Mobile phone'), index=None, placeholder="Select Task")
    st.sidebar.code(quick_queries_data_manipulation, language="sql")
    st.sidebar.write("")
    st.sidebar.write("Data Control (DCL)")
    quick_queries_data_control = st.sidebar.selectbox(label='Data Control',label_visibility="collapsed",options=('Email', 'Home phone', 'Mobile phone'), index=None, placeholder="Select Task")
    st.sidebar.code(quick_queries_data_control, language="sql")

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://res.cloudinary.com/drwsupfyj/image/upload/v1697339563/dailysql/usi1lgghqk7jrrxthpcf.png);
                background-size:260px;
                background-repeat: no-repeat;
                padding-top: 130px;
                background-position: 5px -15px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
def add_css():
    st.markdown(
            """
            <style>
                [data-testid="block-container"] {
                    padding:1rem 1.5rem 2rem;
                }
                section[data-testid="stSidebar"] {
                    width: 275px !important; 
                }
                section[data-testid="stSidebar"] .st-emotion-cache-1kfofzc {
                    display: none; 
                }
                div[data-testid="stSidebarNav"] {
                    padding-bottom: 7px !important;
                }
                div[data-baseweb="select"] > div {
                    font-size:13px;
                    background:rgb(248, 249, 251);
                    border-color:rgb(248, 249, 251);
                }    
                div[data-baseweb="popover"] > div *{
                    font-size:13px !important; 
                }      
                div[data-testid="stCodeBlock"]  *{
                font-size: 12px !important;
                padding: 0.3rem !important;
                }
                section[data-testid="stSidebar"] *{
                }
                div[data-testid="stSidebarUserContent"] {
                    padding: 1rem 1.75rem 6rem !important;
                }

                div.stButton > button:first-child {
                    background-color: white;
                    border: 1px solid #113f67;
                }
            </style>
            """,
    unsafe_allow_html=True,
    )

def add_css_and_animations():
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 275px !important;
            }

            div[data-baseweb="select"] > div {
                font-size:13px;
                background:rgb(248, 249, 251);
                border-color:rgb(248, 249, 251);
            }    
            div[data-baseweb="popover"] > div *{
                font-size:13px !important; 
            }      
            div[data-testid="stCodeBlock"]  *{
            font-size: 12px !important;
            padding: 0.3rem !important;
            }
            section[data-testid="stSidebar"] *{
            }
            div[data-testid="stSidebarUserContent"] {
                padding: 1rem 1.75rem 6rem !important;
            }

            div.stButton > button:first-child {
                background-color: white;
                border: 1px solid #113f67;
            }

            body {
            margin: 0;
            }

            .container {
            position: absolute;
            top:0;
            width: 100%;
            height: 100vh;
            display: grid;
            }

            .square {
            position: absolute;
            bottom: -100px;
            animation: boxes 8s infinite ease-out;
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
            width: 6rem;
            height: 6rem;
            left: 11%;
            animation-delay: 925ms;
            animation-duration: 15000ms;
            }

            @keyframes boxes {
            0% {
                top: 70px;
            }
            100% {
                top: -25vh;
                transform: rotate(200deg);
                opacity: 0.5;
            }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

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
    </div>
    """
    st.markdown(html_string, unsafe_allow_html=True)


def generate_chatgpt_results():
    db_topics = ["Biology", "Physics", "Outer Space", "History", "Art", "Sports", "Culture", "Music", "Books", "Economics", "Business", "Chemistry", "Technology", "Food"]
    daily_db_topic = random.choice(db_topics)
    sql_topics = ["JOINS", "AGGREGATE FUNCTIONS", "STRING FUNCTIONS", "DATE FUNCTIONS", "WINDOW FUNCTIONS"]
    daily_sql_topics = random.sample(sql_topics, random.randint(1,2))

    input1 = f"Act like a computer software: return only the requested output, no additional conversations or comments. Always follow best practices when generating code and creating tables. Do not use quotation marks for table names and column names. Never include any sql comments when generating code. Never use apostrophes. Create a sophisticated relational database with 2 to 5 tables (only use postgresql compatible data types for the tables) about the following topic: {daily_db_topic}. Make it as realistic as possible. Include the concepts of primary and foreign keys, but use separate 'alter table' statements to add these constraint after creating all tables. Always include 'ALTER TABLE DROP CONSTRAINT IF EXISTS' statement before adding the constraints. Always include 'IF NOT EXISTS' and the UNIQUE(PRIMARY KEY) constraint when creating tables. Generate postgresql code to create the tables."
    input2 = "Generate postgresql code to populate these tables with example data (the data must be compatible with the data types of the tables and must not lead to an error when inserting). Make it as realistic as possible. All foreign key data points must have a correlating primary key data point in the table and column they are referencing. All tables must have more than 10 rows and at least two of the tables must have more than 15 rows. Always add 'ON CONFLICT (PRIMARY KEY) DO NOTHING' statement at the end of each 'INSERT' statement. Display the full code to populate all rows."
    input3 = "Generate postgresql code to display all example tables and data in tabular format. Output the postgresql code only, nothing else."
    input4 = f"Generate a sql question related to the relational database and data. The question must reference at least 2 tables. The question must be solvable with the relational database and example data and the solution must return at least 1 row. Include the following concepts: {daily_sql_topics}, however, do not mention concepts specifically in the question. The difficulty level of the question is very advanced. Formulate the question very concise, short, and clear, without ambiguities. Do not include any code or solutions in your response."
    input5 = "The question is too hard. Provide 3 subtle hints that will help me solve this question."
    input6 = "Act like a computer software: return only the requested output, no additional conversations or comments. Always follow best practices when generating code. Never include any sql comments when generating code. Never use apostrophes. Generate postgresql code that provides a correct solution in the most efficient way. The solution must avoid the following error: column  must appear in the GROUP BY clause or be used in an aggregate function. Do not perform any unnecessary operations."
    input7 = "Verify the solution by generating different postgresql code that correctly answers that question. Take a slightly different approach this time. The solution must avoid the following error: column  must appear in the GROUP BY clause or be used in an aggregate function. Do not perform any unesessary unnecessary operations."
    input8 = "Provide a detailed explanation of the first solution. Do not include any code in your response."
    input9 = "Provide a detailed explanation of the second solution. Do not include any code in your response."
    input_list = [input1, input2, input3, input4, input5, input6, input7, input8, input9]
    
    message_history = []
    for i in input_list:
        message_history.append({"role": "user", "content": i})
        completion = openai.ChatCompletion.create(model="gpt-4", messages=message_history)
        reply_content = completion.choices[0].message.content
        message_history.append({"role": "assistant", "content": reply_content})
    
    for i in message_history:
        i["content"] = i["content"].replace('\n', ' ')
        i["content"] = i["content"].replace('\t', ' ')
        i["content"] = i["content"].replace('```', ' ')
    
    create_tables = message_history[1]['content']
    create_tables = create_tables[create_tables.find('CREATE TABLE'):]
    
    insert_data = message_history[3]['content']
    insert_data = insert_data[insert_data.find('INSERT INTO'):]
    
    display_tables = message_history[5]['content']
    display_tables = display_tables[display_tables.find('SELECT'):]
    
    questions = message_history[7]['content']
    
    hints = message_history[9]['content']
    
    solution_code = message_history[11]['content']
    if 'sql' in solution_code[:10]:
        solution_code = solution_code.replace('sql', '')
    elif 'pgsql' in solution_code[:10]:
        solution_code = solution_code.replace('pgsql', '')
    
    solution_code2 = message_history[13]['content']
    if 'sql' in solution_code2[:10]:
        solution_code2 = solution_code2.replace('sql', '')
    elif 'pgsql' in solution_code2[:10]:
        solution_code2 = solution_code2.replace('pgsql', '')
        
    solution_explanation = message_history[15]['content']
    
    solution_explanation2 = message_history[17]['content']
    
    return message_history, create_tables, insert_data, display_tables, questions, hints, solution_code, solution_code2, solution_explanation, solution_explanation2, daily_db_topic, daily_sql_topics
  
def execute_query(query, role_hostname, role_database, role_username, role_port_id, role_pwd, query_arguments = None, result = None, len_query_list=1):
    list_of_db_queries = []
    for i in range(0, len_query_list):
        list_of_db_queries.append((query))
        
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = role_hostname,
            dbname = role_database,
            user = role_username,
            password = role_pwd,
            port = role_port_id
        )

        cur = conn.cursor()
        
        for i in range(0, len_query_list):
            if query_arguments is not None:
                cur.execute(list_of_db_queries[i], query_arguments[i])
            else:
                cur.execute(list_of_db_queries[i], query_arguments)

        if cur.pgresult_ptr is not None:
            result = cur.fetchall()
        conn.commit()
        
        return result
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def execute_query_2(query, role_hostname, role_database, role_username, role_port_id, role_pwd, aggrid_key=None):
    # handle multiline comments
    ## if /**/ in string, delete everything inbetween
    if "/*" in query and "*/" in query:
        query = re.sub('\/\*[^>]+\*\/', '', query)
    ## if open-ended /*, delete everything afterwards
    elif "/*" in query and "*/" not in query:
        head, sep, tail = query.partition('/*')
        query = head
    #query = query.replace("\n","")
    # execute multiple queries separated by ";"
    list_of_queries = []
    delimiter = ';'
    list_of_queries = [x+delimiter for x in query.strip().split(delimiter) if x]
    
    list_of_df = {}

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host = role_hostname,
            dbname = role_database,
            user = role_username,
            password = role_pwd,
            port = role_port_id
        )
        cur = conn.cursor()
        # execute all queries that are no comments (don't start with "--")
        for i in range(0,len(list_of_queries)):
            if not list_of_queries[i].strip().startswith("--"):
                cur.execute(list_of_queries[i])
                #list_of_df[i] = pd.read_sql_query(list_of_queries[i], conn)
                if cur.pgresult_ptr is not None:
                    try:
                        list_of_df[i] = pd.read_sql_query(list_of_queries[i], conn)
                    except Exception as error:
                        print("")
        conn.commit()

    except Exception as error:
        # print error
        st.write(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
    # print result of all queries
    #selected_table2 = display_options['selected_rows'][0]["Table IDs"]
    for i in list_of_df:
        #st.dataframe(list_of_df[i])
        gb = GridOptionsBuilder.from_dataframe(list_of_df[i])
        gb.configure_side_bar()
        gridOptions = gb.build()
        AgGrid(list_of_df[i], key=f"{aggrid_key}{list_of_df[i]}{query}", theme="streamlit", enable_quicksearch=False, gridOptions=gridOptions, height=232, data_return_mode="FILTERED", columns_auto_size_mode="FIT_CONTENTS", custom_css=custom_css)


#@st.cache_data(experimental_allow_widgets=True)
def create_editor(display_options, selected_id, step_editor_empty, ace_key, ace_key2, step_query, step_editor,role_hostname,role_database, role_username, role_port_id, role_pwd, image="",erd_url="",header=None, aggrid_key=None):
    st.header(header)
    try:
        # try to get the daily_tables_id
        selected_id = display_options['selected_rows'][0]["ID"]
    except Exception as error:
        # if error (no id (row) selected), show step_editor_empty (which is an empty code editor)
        step_editor_empty = st_ace(key =str(ace_key),placeholder="Write your query here", language="sql", keybinding="vscode", min_lines=20, theme="sqlserver", wrap="true",font_size=14)
        # if a query is written here, execute it
        if step_editor_empty:
            execute_query_2(query=step_editor_empty, role_hostname=role_hostname,role_database=role_database,role_username=role_username,role_port_id=role_port_id,role_pwd=role_pwd, aggrid_key=aggrid_key)
    #try:
        # if there is a value for daily_tables_id (an id (row) was selected)
    if selected_id and image!="":
        st.write("")
        try_erd_url_query = f"SELECT {str(erd_url)} from daily_tables WHERE daily_tables_id = {selected_id};"
        try_erd_url_query = execute_query(query=try_erd_url_query,role_hostname=role_hostname, role_database=role_database, role_username=role_username, role_port_id=role_port_id, role_pwd=role_pwd)[0][0]
        erd = cloudinary.api.resource_by_asset_id(try_erd_url_query)["url"]
        col1, col2, col3 = st.columns([1,6,1])

        with col1:
            st.write("")

        with col2:
            st.image(erd, width=700,use_column_width=True)

        with col3:
            st.write("")
        st.write("")
    st.write("Note: every query must end with a \" ; \".")
    if selected_id:
        try:
            # create the "create_tables" query and format it
            try_create_table_query = f"SELECT {str(step_query)} from daily_tables WHERE daily_tables_id = {selected_id};"
            try_create_table_query = execute_query(query=try_create_table_query,role_hostname=role_hostname, role_database=role_database, role_username=role_username, role_port_id=role_port_id, role_pwd=role_pwd)[0][0]
            try_create_table_query = try_create_table_query.replace("(     ", "(").replace(" )",")").replace("    "," ")
            try_create_table_query = sqlparse.format(try_create_table_query, reindent=True, keyword_case='upper', indent_tabs=False)
            try_create_table_query = re.sub(" +", " ", try_create_table_query)
            try_create_table_query = re.sub("\n", "  \n", try_create_table_query)
            # pass the "create_tables" query to the code editor
            step_editor = st_ace(key =str(ace_key2), value = try_create_table_query, language="sql", min_lines=20, keybinding="vscode", theme="sqlserver", wrap="true",font_size=14)
        except Exception as error:
            st.write("")
        # run the "create_tables" query
        execute_query_2(query=step_editor,role_hostname=role_hostname,role_database=role_database,role_username=role_username,role_port_id=role_port_id,role_pwd=role_pwd)
    else:
        delete_tables(delete_query_tables, role_hostname=role_hostname, role_database=role_database, role_username=role_username, role_port_id=role_port_id, role_pwd=role_pwd) 
        delete_tables(delete_query_schemas, role_hostname=role_hostname, role_database=role_database, role_username=role_username, role_port_id=role_port_id, role_pwd=role_pwd) 

    #except Exception as error:
            # if there is no more value for daily_tables_id (an id (row) was de-selected again), delete all tables (except for tracking tables)
    #        delete_tables(delete_query)  


def generate_user(display_options, selected_id, step_query,role_hostname,role_database, role_username, role_port_id, role_pwd,header=""):
    try:
        # try to get the daily_tables_id
        selected_id = display_options['selected_rows'][0]["ID"]
    except Exception as error:
        st.write("")

    if selected_id:
        st.subheader(header)
        try:
            # create the "create_tables" query and format it
            try_create_table_query = f"SELECT {str(step_query)} from daily_tables WHERE daily_tables_id = {selected_id};"
            try_create_table_query = execute_query(query=try_create_table_query,role_hostname=role_hostname, role_database=role_database, role_username=role_username, role_port_id=role_port_id, role_pwd=role_pwd)[0][0]
            execute_query_2(query=try_create_table_query,role_hostname=role_hostname,role_database=role_database,role_username=role_username,role_port_id=role_port_id,role_pwd=role_pwd)
        except Exception as error:
            st.write(error)


def create_texts(display_options, selected_id,step_query,role_hostname,role_database, role_username, role_port_id, role_pwd, header=None):
    st.header(header)
    try:
        # try to get the daily_tables_id
        selected_id = display_options['selected_rows'][0]["ID"]
    except Exception as error:
        # if error (no id (row) selected), show nothing
        print('')
    if selected_id:
            # create the "create_tables" query and format it
        try_create_table_query = f"SELECT {str(step_query)} from daily_tables WHERE daily_tables_id = {selected_id};"
        try_create_table_query = execute_query(query=try_create_table_query,role_hostname=role_hostname, role_database=role_database, role_username=role_username, role_port_id=role_port_id, role_pwd=role_pwd)[0][0]
        st.markdown(f'<p style="font-family:monospace; font-size:14px;font-weight: 100;background:rgb(222, 225, 230,0.25);padding:22px;border-radius:7px">{try_create_table_query}</p>', unsafe_allow_html=True)



def delete_tables(delete_query,role_hostname,role_database,role_username,role_port_id,role_pwd):
    to_delete = execute_query(query=delete_query,role_hostname=role_hostname, role_database=role_database, role_username=role_username, role_port_id=role_port_id, role_pwd=role_pwd)
    list_to_delete = []
    for i in range(0, len(to_delete)):
        list_to_delete.append(to_delete[i][0])
    string_to_delete = ''.join(x for x in list_to_delete)
    execute_query(query=string_to_delete,role_hostname=role_hostname, role_database=role_database, role_username=role_username, role_port_id=role_port_id, role_pwd=role_pwd)


#################################################################################################### Variables
# query to create tracking tables
create_tracking_tables = """
CREATE TABLE daily_tables (
    daily_tables_id INT GENERATED ALWAYS AS IDENTITY, 
    daily_db_topic VARCHAR(255) NOT NULL, 
    create_tables TEXT NOT NULL, 
    insert_data TEXT NOT NULL, 
    display_tables TEXT NOT NULL,
    question TEXT NOT NULL, 
    hints TEXT NOT NULL, 
    solution_1 TEXT NOT NULL,
    solution_2 TEXT NOT NULL, 
    solution_1_explanation TEXT NOT NULL, 
    solution_2_explanation TEXT NOT NULL,
    erd_url TEXT);
                                
CREATE TABLE daily_sql_topics (
    daily_sql_topics_id INT GENERATED ALWAYS AS IDENTITY, 
    sql_topic VARCHAR(255) NOT NULL);
    
ALTER TABLE daily_tables ADD COLUMN date_created TIMESTAMP;
ALTER TABLE daily_tables ALTER COLUMN date_created SET DEFAULT now();

ALTER TABLE daily_tables 
    ADD CONSTRAINT pk_daily_tables 
        PRIMARY KEY (daily_tables_id);

ALTER TABLE daily_sql_topics 
    ADD CONSTRAINT pk_sql_topics 
        PRIMARY KEY (daily_sql_topics_id);
    

CREATE TABLE dailytables_dailysqltopics (
    daily_tables_id INT REFERENCES daily_tables (daily_tables_id) ON UPDATE CASCADE ON DELETE CASCADE,
    daily_sql_topics_id INT REFERENCES daily_sql_topics (daily_sql_topics_id) ON UPDATE CASCADE ON DELETE CASCADE);


ALTER TABLE dailytables_dailysqltopics
    ADD CONSTRAINT pk_dailytables_dailysqltopics
        PRIMARY KEY (daily_tables_id, daily_sql_topics_id);
"""

insert_sql_topics = """
INSERT INTO daily_sql_topics(sql_topic) VALUES ('JOINS'), ('AGGREGATE FUNCTIONS'), ('STRING FUNCTIONS'), ('DATE FUNCTIONS'), ('WINDOW FUNCTIONS')
"""

# query to populate daily_tables
populate_daily_tables = """INSERT INTO daily_tables (daily_db_topic, create_tables, insert_data, display_tables, 
                                                        question, hints, solution_1, solution_2, solution_1_explanation, 
                                                        solution_2_explanation) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

# query to get the id for the dailytables_dailysqltopics table
query_daily_tables_id_junction = "SELECT MAX(daily_tables_id) FROM daily_tables;"

# query to populate dailytables_dailysqltopics
populate_dailytables_dailysqltopics = f"""INSERT INTO dailytables_dailysqltopics (daily_tables_id, daily_sql_topics_id) VALUES (%s, %s)"""


delete_query_tables = """select 'drop table if exists ' || tablename || ' cascade;' as to_delete  from pg_tables  where schemaname = 'dailysql_schema'  and tablename not in ('daily_tables', 'daily_sql_topics', 'dailytables_dailysqltopics');"""
delete_query_schemas = """select 'drop schema if exists ' || nspname || ' cascade;' as to_delete  from pg_catalog.pg_namespace WHERE (nspname NOT LIKE 'pg_%') and (nspname != 'information_schema') and (nspname != 'public')and (nspname != 'dailysql_schema');"""


# create_tables
header_create_table = "Create Tables"
selected_id = None
create_tables_query_empty = None
key_create_tables = "editor_create_tables"
key_create_tables_2 = "editor_create_tables_2"
step_query_create_tables = "create_tables"
step_editor_create_tables = None
aggrid_key_create_tables = "create_tables"

# insert_data
header_insert_data = "Insert Data"
insert_data_query_empty = None
key_insert_data = "editor_insert_data"
key_insert_data_2 = "editor_insert_data_2"
step_query_insert_data = "insert_data"
step_editor_insert_data = None
aggrid_key_insert_data = "insert_data"

# display_tables
header_display_tables = "Display Tables"
display_tables_query_empty = None
key_display_tables = "editor_display_tables"
key_display_tables_2 = "editor_display_tables_2"
step_query_display_tables = "display_tables"
step_editor_display_tables = None
aggrid_key_display_tables = "display_tables"

# question
header_question = "Question"
selected_id = None
step_query_questions = "question"

# hints
header_hints = "Hints"
selected_id = None
step_query_hints = "hints"

# solution_1_explanation
header_solution_1_explanation = "First Solution"
selected_id = None
step_query_solution_1_explanation = "solution_1_explanation"

# solution_2_explanation
header_solution_2_explanation = "Second Solution"
selected_id = None
step_query_solution_2_explanation = "solution_2_explanation"

# solution_1
header_solution_1 = ""
solution_1_query_empty = None
key_solution_1 = "editor_solution_1"
key_solution_1_2 = "editor_solution_1_2"
step_query_solution_1 = "solution_1"
step_editor_solution_1 = None
aggrid_key_solution_1 = "solution_1"

# solution_2
header_solution_2 = ""
solution_2_query_empty = None
key_solution_2 = "editor_solution_2"
key_solution_2_2 = "editor_solution_2_2"
step_query_solution_2 = "solution_2"
step_editor_solution_2 = None
aggrid_key_solution_2 = "solution_2"

# erd-url
erd_url = "erd_url"

defaultColDef = {
    "filter": True,
    "resizable": True,
    "sortable": True,  

}
custom_css = {
    ".ag-row-hover": {"background-color": "rgb(17, 63, 103,0.3) !important"},
    ".ag-header-cell-text": {"color": "#113f67 !important;"},
    ".ag-theme-alpine .ag-ltr .ag-cell": {"color": "#113f67 !important;"},
    ".ag-side-button-label": {"color": "#113f67 !important;"},
    ".ag-icon ag-icon-columns": {"color": "#113f67 !important;"},
    ".ag-side-buttons": {"background-color": "rgb(222, 225, 230,0.25) !important;"},
    ".ag-header-viewport": {"background-color": "rgb(222, 225, 230,0.25) !important;"},
}
