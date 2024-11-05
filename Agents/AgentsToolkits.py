#CRIANDO AGENTS PARA ANALISAR DATAFRAMES E SQL

from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

from langchain_openai import ChatOpenAI
import pandas as pd

df = pd.read_csv("DATA_FRAME_AQUI")


df.head(5)


chat = ChatOpenAI(model='gpt-3.5-turbo-0125')
agent = create_pandas_dataframe_agent(
    chat,
    df,
    verbose=True,
    agent_type='tool-calling'
)
#ISSO JA SE TRANSFORMA NUM AGENT EXECUTER ENTAO PODEMOS USAR O INVOKE

agent.invoke('input': 'Quantas linhas tem na tabela?')
agent.invoke('input': 'Qual media de idade dos passageiros?')








#SQL DATABASE
from langchain_community.utilities.sql_database import SQLDatabase

db = SQLDatabase.from_uri('sqlite:///arquivos/chinook.db')

from langchain_community.agent_toolkits.sql.base import create_sql_agent

chat = ChatOpenAI(model='gpt-3.5-turbo-0125')

agent_executor = create_sql_agent(
    chat,
    db=db,
    agent_type='tool-calling',
    verbose=True
)

for tool in agent_executor.tools:
    print(tool.name)
    print(tool.description)
    

agent_executor.invoke('input': 'Me descreva a base de dados')    
agent_executor.invoke('input': 'Qual artista possui mais albuns?')    
agent_executor.invoke('input': 'Qual cliente que mais comprou?')    