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

# create tracking tables
## run once only
### execute_query(query = create_tracking_tables)

#113f67
#87c0cd

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

st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    padding-left:40px;
}
[data-testid="block-container"] a {
    color: #113f67 !important;           
}
</style>
''', unsafe_allow_html=True)

st.title("Documentation (WIP)")
st.subheader("[App Overview](#app_overview)")
st.markdown("- [App Workflow](#app_workflow)")
st.markdown("- [ChatGPT-4 Prompts](#chatgpt4)")
st.markdown("- [Permissions](#permissions)")
st.markdown("- [Table Structure (ERD)](#structure)")

st.subheader("[Code Implementation](#code_implementation)")
st.markdown("- [Create Virtual Environment](#virtual_environment)")
st.markdown("- [Create Database](#create_database)")
st.markdown("- [Create Schema](#create_schema)")
st.markdown("- [Create Roles](#create_roles)")
st.markdown("- [Create Tracking Tables](#tracking_tables)")

st.subheader("[Commonly Used Queries](#common_queries)")
st.markdown("- [Data Query (DQL)](#dql)")
st.markdown("- [Data Definition (DDL)](#ddl)")
st.markdown("- [Data Manipulation (DML)](#dml)")
st.markdown("- [Data Control (DCL)](#dcl)")

st.subheader("[Sources](#source)")
st.title("")
st.divider()

st.title("1. App Overview", anchor="app_overview")
st.subheader("App Workflow", anchor="app_workflow")
st.write("WIP")
st.subheader("ChatGPT-4 Prompts", anchor="chatgpt4")
with st.expander("Show", expanded=True):
    st.write("1. Create Tables")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">Act like a computer software: return only the requested output, no additional conversations or comments. Always follow best practices when generating code and creating tables. Do not use quotation marks for table names and column names. Never include any sql comments when generating code. Never use apostrophes. Create a sophisticated relational database with 2 to 5 tables (only use postgresql compatible data types for the tables) about the following topic: (daily_db_topic). Make it as realistic as possible. Include the concepts of primary and foreign keys, but use separate 'alter table' statements to add these constraint after creating all tables. Always include 'ALTER TABLE DROP CONSTRAINT IF EXISTS' statement before adding the constraints. Always include 'IF NOT EXISTS' and the UNIQUE(PRIMARY KEY) constraint when creating tables. Generate postgresql code to create the tables.</p>""", unsafe_allow_html=True)
    st.divider()
    st.write("2. Insert Data")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">Generate postgresql code to populate these tables with example data (the data must be compatible with the data types of the tables and must not lead to an error when inserting). Make it as realistic as possible. All foreign key data points must have a correlating primary key data point in the table and column they are referencing. All tables must have more than 10 rows and at least two of the tables must have more than 15 rows. Always add 'ON CONFLICT (PRIMARY KEY) DO NOTHING' statement at the end of each 'INSERT' statement. Display the full code to populate all rows.</p>""", unsafe_allow_html=True)
    st.divider()
    st.write("3. Display Tables")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">Generate postgresql code to display all example tables and data in tabular format. Output the postgresql code only, nothing else.</p>""", unsafe_allow_html=True)
    st.divider()
    st.write("4. Generate Question")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">Generate a sql question related to the relational database and data. The question must reference at least 2 tables. The question must be solvable with the relational database and example data and the solution must return at least 1 row. Include the following concepts: (daily_sql_topics), however, do not mention concepts specifically in the question. The difficulty level of the question is very advanced. Formulate the question very concise, short, and clear, without ambiguities. Do not include any code or solutions in your response.</p>""", unsafe_allow_html=True)
    st.divider()
    st.write("5. Generate Hints")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">The question is too hard. Provide 3 subtle hints that will help me solve this question.</p>""", unsafe_allow_html=True)
    st.divider()
    st.write("6. Generate First Solution")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">Act like a computer software: return only the requested output, no additional conversations or comments. Always follow best practices when generating code. Never include any sql comments when generating code. Never use apostrophes. Generate postgresql code that provides a correct solution in the most efficient way. The solution must avoid the following error: column  must appear in the GROUP BY clause or be used in an aggregate function. Do not perform any unnecessary operations.</p>""", unsafe_allow_html=True)
    st.divider()
    st.write("7. Generate Second Solution")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">Verify the solution by generating different postgresql code that correctly answers that question. Take a slightly different approach this time. The solution must avoid the following error: column  must appear in the GROUP BY clause or be used in an aggregate function. Do not perform any unesessary unnecessary operations.</p>""", unsafe_allow_html=True)
    st.divider()
    st.write("8. Provide First Solution Explanation")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">Provide a detailed explanation of the first solution. Do not include any code in your response.</p>""", unsafe_allow_html=True)
    st.divider()
    st.write("9. Provide Second Solution Explanation")
    st.markdown(f"""<p style="font-family:monospace; font-size:14px;font-weight: 100;padding:22px;border-radius:7px">Provide a detailed explanation of the second solution. Do not include any code in your response.</p>""", unsafe_allow_html=True)
st.write("")
st.subheader("Table Structure (ERD)", anchor="structure")
with st.expander("Show", expanded=True):
    erd_tracking = cloudinary.api.resource_by_asset_id("a4f6d0b51c15e66cdfc872a043cbd693")["url"]
    col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.write("")

with col2:
    st.image(erd_tracking, width=700,use_column_width=True)

with col3:
    st.write("")
st.write("")
st.subheader("Permissions", anchor="permissions")
with st.expander("Show", expanded=True):
    st.caption("Schema permissions include: _CREATE_, _USAGE_.")
    st.code("""   schema          | create (admin) | usage (admin) | usage (user) | usage (user)
    -----------------+----------------+---------------+--------------+--------------
    dailysql_schema | t              | t             | t            | t
    """, language="")
    st.write("")
    st.caption("Table permissions include: _SELECT_, _INSERT_, _UPDATE_, _DELETE_, _TRUNCATE_, _REFERENCES_, _TRIGGER_.")
    st.code("""   table_name                 | privilege_type |      role
    ----------------------------+----------------+----------------
    daily_tables               | INSERT         | dailysql_admin
    daily_tables               | SELECT         | dailysql_admin
    daily_tables               | UPDATE         | dailysql_admin
    daily_tables               | DELETE         | dailysql_admin
    daily_tables               | TRUNCATE       | dailysql_admin
    daily_tables               | REFERENCES     | dailysql_admin
    daily_tables               | TRIGGER        | dailysql_admin
    daily_tables               | SELECT         | dailysql_user
    daily_sql_topics           | INSERT         | dailysql_admin
    daily_sql_topics           | SELECT         | dailysql_admin
    daily_sql_topics           | UPDATE         | dailysql_admin
    daily_sql_topics           | DELETE         | dailysql_admin
    daily_sql_topics           | TRUNCATE       | dailysql_admin
    daily_sql_topics           | REFERENCES     | dailysql_admin
    daily_sql_topics           | TRIGGER        | dailysql_admin
    daily_sql_topics           | SELECT         | dailysql_user
    dailytables_dailysqltopics | INSERT         | dailysql_admin
    dailytables_dailysqltopics | SELECT         | dailysql_admin
    dailytables_dailysqltopics | UPDATE         | dailysql_admin
    dailytables_dailysqltopics | DELETE         | dailysql_admin
    dailytables_dailysqltopics | TRUNCATE       | dailysql_admin
    dailytables_dailysqltopics | REFERENCES     | dailysql_admin
    dailytables_dailysqltopics | TRIGGER        | dailysql_admin
    dailytables_dailysqltopics | SELECT         | dailysql_user
    ----------------------------+----------------+----------------
    newly created tables       | ALL            | dailysql_admin
    newly created tables       | ALL            | dailysql_user
    """, language="")

st.divider()

st.title("2. Code Implementation", anchor="code_implementation")
st.subheader("Create Virtual Environment (vscode command line)", anchor="virtual_environment")
with st.expander("Show", expanded=True):
    st.write("Create virtual environment")
    st.code("python -m venv .dailysql", language="")
    st.divider()
    st.write("Activate virtual environment")
    st.code(".dailysql\Scripts\\activate", language="")
    st.divider()
    st.write("Deactivate virtual environment")
    st.code("deactivate", language="")

st.write("")
st.subheader("Create Database: :orange[_dailysql_]  (psql command line)", anchor="create_database")
with st.expander("Show", expanded=True):
    st.write("Check current database")
    st.code("SELECT current_database();", language="sql")
    st.divider()
    st.write("Create new database called :orange[_dailysql_]")
    st.code("CREATE DATABASE dailysql;", language="sql")
    st.divider()
    st.write("List all databases")
    st.code("\l or \l+", language="")
    st.divider()
    st.write("Switch to :orange[_dailysql_] database")
    st.code("\c dailysql;", language="")

st.write("")
st.subheader("Create Schema: :orange[_dailysql_schema_]  (psql command line)", anchor="create_schema")
with st.expander("Show", expanded=True):
    st.write("Check current schema")
    st.code("SELECT current_schema();", language="sql")
    st.divider()
    st.write("Create new schema called :orange[_dailysql_schema_]")
    st.code("CREATE SCHEMA dailysql_schema;", language="sql")
    st.divider()
    st.write("List all schemas")
    st.code("\dn or \dn+", language="")
    st.divider()
    st.write("Switch to :orange[_dailysql_schema_] schema")
    st.caption("Change for current session only.")
    st.code("SET SEARCH_PATH = dailysql;", language="sql")
    st.write("")
    st.write("")
    st.caption("Change default schema permanently.")
    st.code("ALTER DATABASE dailysql SET search_path TO dailysql_schema;", language="sql")

st.write("")
st.subheader("Create Roles and Grant Permissions (psql command line)", anchor="create_roles")
with st.expander("Show", expanded=True):
    st.write("Check current user")
    st.caption("The current user is :orange[_postgres_].")
    st.code("SELECT current_user;", language="sql")
    st.divider()
    st.write("Create roles for admin (:orange[_dailysql_admin_]) and users (:orange[_dailysql_user_])")
    st.code("CREATE ROLE dailysql_admin LOGIN PASSWORD 'password';", language="sql")
    st.code("CREATE ROLE dailysql_user LOGIN PASSWORD 'password';", language="sql")
    st.divider()
    st.write("List all roles and permissions (database permissions)")
    st.caption("List of permissions: [_link_](https://www.postgresql.org/docs/current/sql-createrole.html)")
    st.code("\du or \du+ ", language="")
    st.divider()
    st.write("Grant permissions to roles (schema and table permissions) (_implement after creating tracking tables in the next step_)")
    st.caption("Schema permissions include: _CREATE_, _USAGE_. Grant ALL schema permissions in schema :orange[_dailysql_schema_] to role :orange[_dailysql_admin_]. Grant only _USAGE_ permission to role :orange[_dailysql_user_].")
    st.code("GRANT ALL ON SCHEMA dailysql_schema TO dailysql_admin;", language="sql")
    st.code("GRANT USAGE ON SCHEMA dailysql_schema TO dailysql_user;", language="sql")
    st.write("")
    st.write("")
    st.caption("Table permissions include: _SELECT_, _INSERT_, _UPDATE_, _DELETE_, _TRUNCATE_, _REFERENCES_, _TRIGGER_. Grant ALL table permissions on ALL tables in schema :orange[_dailysql_schema_] to roles :orange[_dailysql_admin_] and :orange[_dailysql_user_]. Note: Role :orange[_dailysql_user_] should only have _SELECT_ permission on tracking tables.")
    st.code("GRANT ALL ON ALL TABLES IN SCHEMA dailysql_schema TO dailysql_admin;", language="sql")
    st.code("GRANT ALL ON ALL TABLES IN SCHEMA dailysql_schema TO dailysql_user;", language="sql")
    st.code("""REVOKE  INSERT, UPDATE, DELETE, TRUNCATE, REFERENCES, TRIGGER 
ON TABLE daily_tables, daily_sql_topics, dailytables_dailysqltopics FROM dailysql_user;""", language="sql")
    st.write("")
    st.write("")
    st.caption("Set default permissions (ALL on ALL tables) for future tables for role :orange[_dailysql_user_].")
    st.code("ALTER DEFAULT privileges IN SCHEMA dailysql_schema GRANT ALL TO dailysql_user;", language="sql")

st.write("")
st.subheader("Create Tracking Tables: :orange[_daily_tables_], :orange[_daily_sql_topics_], :orange[_dailytables_dailysqltopics_]  (psql command line)", anchor="tracking_tables")
with st.expander("Show", expanded=True):
    st.write("Create tracking tables and add constraints")
    st.caption("Establish a many-to-many relationship bewteern :orange[_daily_tables_] and :orange[_daily_sql_topics_] by creating the junction table :orange[_dailytables_dailysqltopics_].")
    st.code("""
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
    
ALTER TABLE daily_tables 
            ADD COLUMN date_created TIMESTAMP;

ALTER TABLE daily_tables 
            ALTER COLUMN date_created 
                SET DEFAULT now();

ALTER TABLE daily_tables 
    ADD CONSTRAINT pk_daily_tables 
        PRIMARY KEY (daily_tables_id);

ALTER TABLE daily_sql_topics 
    ADD CONSTRAINT pk_sql_topics 
        PRIMARY KEY (daily_sql_topics_id);
    

CREATE TABLE dailytables_dailysqltopics (
    daily_tables_id INT REFERENCES daily_tables (daily_tables_id) 
    ON UPDATE CASCADE ON DELETE CASCADE,
    daily_sql_topics_id INT REFERENCES daily_sql_topics (daily_sql_topics_id) 
    ON UPDATE CASCADE ON DELETE CASCADE);


ALTER TABLE dailytables_dailysqltopics
    ADD CONSTRAINT pk_dailytables_dailysqltopics
        PRIMARY KEY (daily_tables_id, daily_sql_topics_id);
""", language="sql")
st.divider()

st.title("3. Commonly Used Queries", anchor="common_queries")
sql_commands = cloudinary.api.resource_by_asset_id("bff98ad125805f11e16575667cb8e2d7")["url"]
col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.write("")

with col2:
    st.image(sql_commands, width=700,use_column_width=True)

with col3:
    st.write("")

st.subheader("Data Query (DQL)", anchor="dql")
with st.expander("Show", expanded=True):
    st.write("SELECT :orange[_id_], :orange[_date_], :orange[_DB topic_], :orange[_SQL topics_] from :orange[_daily_tables_] and :orange[_daily_sql_topics_]")
    st.code("""SELECT a.daily_tables_id AS ID, a.date_created AS Date, a.daily_db_topic AS DB_Topic, b.sql_topic AS SQL_Topic 
FROM daily_tables AS a INNER JOIN dailytables_dailysqltopics AS c ON a.daily_tables_id = c.daily_tables_id 
INNER JOIN daily_sql_topics AS b ON b.daily_sql_topics_id = c.daily_sql_topics_id;""", language="sql")
    st.divider()
st.subheader("Data Definition (DDL)", anchor="ddl")
with st.expander("Show", expanded=True):
    st.write("SELECT all tables from schema :orange[_dailysql_schema_]")
    st.code("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'dailysql_schema';""", language="sql")
    st.caption("Or")
    st.code("""SELECT tablename FROM pg_tables  WHERE schemaname = 'dailysql_schema';""", language="sql")
    st.divider()
    st.write("SELECT all schemas except for schema :orange[_public_]")
    st.code("""SELECT nspname AS schema_name FROM pg_catalog.pg_namespace 
WHERE (nspname NOT LIKE 'pg_%') AND (nspname != 'information_schema') 
AND (nspname != 'public');""", language="sql")
    st.divider()
    st.write("DELETE all tables except for tables :orange[_daily_tables_] and :orange[_daily_sql_topics_]")
    st.caption("This only returns a table with delete queries. To delete the tables, execute these queries.")
    st.code("""SELECT 'DROP TABLE IF EXISTS ' || tablename || ' CASCADE;' AS to_delete  
FROM pg_tables  
WHERE schemaname = 'dailysql_schema' and tablename NOT IN ('daily_tables', 'daily_sql_topics');""", language="sql")
    st.divider()

st.write("")
st.subheader("Data Manipulation (DML)", anchor="dml")
with st.expander("Show", expanded=True):
    st.write("UPDATE value in specific cell in table :orange[_daily_tables_]")
    st.code("""UPDATE daily_tables SET create_tables = 'test' WHERE daily_tables_id = 4;""", language="sql")
    st.divider()

st.write("")
st.subheader("Data Control (DCL)", anchor="dcl")
with st.expander("Show", expanded=True):
    st.write("SELECT all permissions from all roles on table :orange[_daily_tables_]")
    st.code("""SELECT grantee, privilege_type FROM information_schema.role_table_grants WHERE table_name='daily_tables';""", language="sql")
    st.divider()
    st.write("SELECT all permissions from roles :orange[_dailysql_admin_] and :orange[_dailysql_user_] in schema :orange[_dailysql_schema_]")
    st.code("""
WITH "names"("name") AS (
SELECT n.nspname AS "name"
FROM pg_catalog.pg_namespace n
WHERE n.nspname !~ '^pg_'
AND n.nspname <> 'information_schema'
) SELECT "name",
  pg_catalog.has_schema_privilege('dailysql_admin', "name", 'CREATE') AS "create (admin)",
  pg_catalog.has_schema_privilege('dailysql_admin', "name", 'USAGE') AS "usage (admin)",
  pg_catalog.has_schema_privilege('dailysql_user', "name", 'USAGE') AS "usage (user)",
  pg_catalog.has_schema_privilege('dailysql_user', "name", 'USAGE') AS "usage (user)"
    FROM "names";
""", language="sql")
    st.divider()
st.divider()

st.title("4. Sources", anchor="source")
with st.expander("Show", expanded=True):
    st.write("Logo: https://logo.com/")
    st.write("SQL-Commands Picture: https://www.geeksforgeeks.org/sql-ddl-dql-dml-dcl-tcl-commands/")
    st.write("Cheat Sheet: https://www.postgresqltutorial.com/")
    st.write("CSS Animation: https://codepen.io/rick1295/pen/ExRJvzJ")


    

