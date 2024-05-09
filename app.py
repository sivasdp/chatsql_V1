import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import mysql.connector
import os

os.environ['GROQ_API_KEY']="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"
# Load secret variables from env file
load_dotenv()

# Function to establish connection with database
def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)


# Function to generate SQL Query
def get_sql_chain(db):
    template = """
        You are a senior-level data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

        <SCHEMA>{schema}</SCHEMA>

        Conversation History: {chat_history}

        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

        For example:
        Question: which 3 artists have most tracks?
        SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BYz track_count DESC LIMIT 3;
        Question: Name 10 artists
        SQL Query: SELECT name FROM Artist LIMIT 10

        Your turn:

        Question: {question}
        SQL Query:
    """

    # Prompt
    prompt = ChatPromptTemplate.from_template(template=template)
    # Language model
    # llm = ChatOpenAI()
    llm = ChatGroq(model="Mixtral-8x7b-32768", temperature=0)

    # Tool -> This function to return the details/schema of the database 
    def get_schema(_):
        return db.get_table_info()
        
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )


# Function to convert SQL Query into Natural Language
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    # Get the SQL Chain for query
    sql_chain = get_sql_chain(db)

    template = """
        You are a senior data analyst at a company. You are interacting with a user who is asking you about the company's database.
        Based on the table schema below, question, sql query, and sql response, first write the sql query and keep the query formatted and structured but don't add its reference anywhere then write a natural language response. Do not wrap the SQL query and natural language response in any other text, not even backticks.

        <SCHEMA>{schema}</SCHEMA>
        
        SQL Query:\n
        Natural Language Response:\n

        Conversation History: {chat_history}
        SQL Query: <SQL>{query}</SQL>
        Question: {question}
        SQL Response: {response}
    """
    # Format the prompt
    prompt = ChatPromptTemplate.from_template(template=template)
    # Language Model
    # llm = ChatOpenAI()
    llm = ChatGroq(model="Mixtral-8x7b-32768", temperature=0)

    # Make chain
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"])
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history
    })


# Initialize chat_history   
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database.")
    ]

# page config
st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_baloon:")
st.title("Chat with MySQL Database")

# sidebar
with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat application using MySQL. Connect to the database and start chatting.")

    # Taking inputs to connect with the database
    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value="root", key="User")
    st.text_input("Password", type="password", key="Password")
    st.text_input("Database", key="Database")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            # Initializing the database
            try:
                db = init_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                if db not in st.session_state:
                    st.session_state.db = db
                    st.success("Connected to database!")
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")


# Interactive chat interface                                            
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)


# User question
user_query = st.chat_input("Type a message...")

if user_query is not None and user_query != "":
    # Add user question into "chat_history"
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)
    
    with st.chat_message("AI"):
        # Call response function
        response  = get_response(user_query, st.session_state.db, st.session_state.chat_history)
        st.markdown(response)

    # Add AI response into "chat_history"
    st.session_state.chat_history.append(AIMessage(content=response))


