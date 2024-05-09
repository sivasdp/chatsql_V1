# Chat with MySQL Database

## Overview
SQL Assistant and Chatbot is a powerful tool that allows users to interact with their MySQL databases using natural language. Whether you're a beginner learning SQL or an experienced data analyst, this application makes querying databases intuitive and efficient. With its user-friendly interface and advanced AI capabilities, SQL Assistant and Chatbot is suitable for a wide range of use cases. Leveraging the integration of OpenAI's GPT and Mixtral LLM models, it enables the development of a chatbot that can interpret natural language queries, generate SQL queries, and fetch results from a SQL database seamlessly.


## Features
- **Natural Language Processing**: Uses OpenAI ChatGPT and Mistral LLM models to interpret and respond to user queries in natural language.
- **SQL Query Generation**: Dynamically generates SQL queries based on the user's natural language input.
- **Database Interaction**: Connects to a SQL database to retrieve query results, demonstrating practical database interaction.
- **Streamlit GUI**: Features a user-friendly interface built with Streamlit, making it easy for users of all skill levels.
- **Python-based**: Entirely coded in Python, showcasing best practices in software development with modern technologies.


## Brief Explanation of How the Chatbot Works

The chatbot works by taking a user's natural language query, converting it into a SQL query using chatGPT and Mixtral, executing the query on a SQL database, and then presenting the results back to the user in natural language and also SQL query. This process involves several steps of data processing and interaction with the OpenAI API, Mixtral API and a SQL database, all seamlessly integrated into a Streamlit application.

Consider the following diagram to understand how the different chains and components are built:
![mysql-chains](https://github.com/Shashank1130/Chat-with-MySQL-Database/assets/107529934/ecc2ad08-1345-4cdc-a5b7-c1bbf31d83d3)


## Use Cases
- **Product Manager Insights**: Gain valuable insights from data without needing to write SQL queries. The chatbot provides both natural language responses and the corresponding SQL queries for transparency and learning purposes.

- **Interactive Learning Tool**: The chatbot serves as a dynamic platform for exploring and learning SQL concepts hands-on. Users of all levels, whether students, educators, or hobbyists, can gain practical experience and insights into database management and querying. 

- **Quick Data Analysis**: Analysts can quickly retrieve insights from databases without writing complex queries, allowing them to focus on analyzing the data and deriving actionable insights.

- **Decision Support**: Executives and decision-makers can use the chatbot to quickly access key metrics and insights to inform strategic decisions.

There are many more use cases where SQL Assistant and Chatbot can provide value, making it a versatile tool for various industries and roles.


## Installation
Ensure you have Python installed on your machine. Then clone this repository:

```bash
git clone [repository-link]
cd [repository-directory]
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create your own .env file with the necessary variables, including your OpenAI API key and Groq API Key for Mixtral LLM Model:

```bash
OPENAI_API_KEY = "your secret api key" 
GROQ_API_KEY = "your secret api key"
```

## Usage
To launch the Streamlit app and interact with the chatbot:

```bash
streamlit run app.py
```

## License
MIT 













