from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_openai import ChatOpenAI
from agent_graph.load_tools_config import LoadToolsConfig
from langchain_core.runnables import RunnableLambda


TOOLS_CFG = LoadToolsConfig()


class ProjectSQLAgentTool:
    """
    A tool for interacting with a B. Tech projects related SQL database using an LLM (Language Model) to generate and execute SQL queries.

    This tool enables users to ask project related questions, which are transformed into SQL queries by a language model.
    The SQL queries are executed on the provided SQLite database, and the results are processed by the language model to
    generate a final answer for the user.

    Attributes:
        sql_agent_llm (ChatOpenAI): An instance of a ChatOpenAI language model used to generate and process SQL queries.
        system_role (str): A system prompt template that guides the language model in answering user questions based on SQL query results.
        db (SQLDatabase): An instance of the SQL database used to execute queries.
        chain (RunnablePassthrough): A chain of operations that creates SQL queries, executes them, and generates a response.

    Methods:
        __init__: Initializes the ProjectSQLAgentTool by setting up the language model, SQL database, and query-answering pipeline.
    """

    def __init__(self, llm: str, sqldb_directory: str, llm_temerature: float) -> None:
        """
        Initializes the ProjectSQLAgentTool with the necessary configurations.

        Args:
            llm (str): The name of the language model to be used for generating and interpreting SQL queries.
            sqldb_directory (str): The directory path where the SQLite database is stored.
            llm_temerature (float): The temperature setting for the language model, controlling response randomness.
        """
        self.sql_agent_llm = ChatOpenAI(
            model=llm, temperature=llm_temerature)
        self.system_role = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.\n
            Question: {question}\n
            SQL Query: {query}\n
            SQL Result: {result}\n
            Answer:
            """
        self.db = SQLDatabase.from_uri(
            f"sqlite:///{sqldb_directory}")
        print(self.db.get_usable_table_names())
        print(self.db.get_usable_table_names())


        execute_query = QuerySQLDataBaseTool(db=self.db)
        write_query = create_sql_query_chain(
            self.sql_agent_llm, self.db)
        
        def print_query(inputs):
            query = write_query.invoke(inputs)
            print("\nGenerated SQL Query:\n", query)
            return {"query": query}
        
        answer_prompt = PromptTemplate.from_template(
            self.system_role)

        answer = answer_prompt | self.sql_agent_llm | StrOutputParser()
        self.chain = (
            RunnablePassthrough.assign(query=RunnableLambda(print_query))
            .assign(result=itemgetter("query") | execute_query)
            | answer
        )


@tool
def query_projects_sqldb(query: str) -> str:
    """Query the Projects SQL Database and access information about B. Tech projects students are working on. Input should be a search query."""
    agent = ProjectSQLAgentTool(
        llm=TOOLS_CFG.projects_sqlagent_llm,
        sqldb_directory=TOOLS_CFG.projects_sqldb_directory,
        llm_temerature=TOOLS_CFG.projects_sqlagent_llm_temperature
    )
    response = agent.chain.invoke({"question": query})
    return response
