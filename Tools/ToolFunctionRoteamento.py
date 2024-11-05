import requests
import datetime
from langchain.agents import tool
from langchain.pydantic_v1 import BaseModel, Field
import wikipedia

# Definindo o schema para o tool de temperatura
class RetornaTempArgs(BaseModel):
    latitude: float = Field(description='Latitude da localidade que buscamos a temperatura')
    longitude: float = Field(description='Longitude da localidade que buscamos a temperatura')

@tool(args_schema=RetornaTempArgs)
def retorna_temperatura_atual(latitude: float, longitude: float):
    '''Retorna a temperatura atual para uma dada coordenada'''
    URL = "URL_AQUI_DA_API"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 1,
    }
    
    resposta = requests.get(URL, params=params)
    
    if resposta.status_code == 200:
        resultado = resposta.json()
        hora_agora = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        lista_horas = [
            datetime.datetime.fromisoformat(temp_str)
            for temp_str in resultado["hourly"]["time"]
        ]
        index_mais_prox = min(
            range(len(lista_horas)), key=lambda x: abs(lista_horas[x] - hora_agora)
        )
    
        temp_atual = resultado["hourly"]["temperature_2m"][index_mais_prox]
        return temp_atual
    else:
        raise Exception(f'Request para API {URL} falhou {resposta.status_code}')


# Criando tool de busca no Wikipedia
wikipedia.set_lang('pt')

@tool
def busca_wikipedia(query: str):
    """Faz uma busca no Wikipedia e retorna resumos de páginas"""
    page_titles = wikipedia.search(query)
    resumos = []
    for title in page_titles[:3]:
        try:
            wiki_page = wikipedia.page(title=title, auto_suggest=True)
            resumos.append(f'Título da página: {title}\nResumo: {wiki_page.summary}')
        except Exception as e:
            pass 
    if not resumos:
        return "Busca não teve retorno"
    else:
        return '\n\n'.join(resumos)


# Testando a tool completa com chain e tudo
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_function

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Você é um assistente amigável'),
    ('user', '{input}')
])

chat = ChatOpenAI()
tools = [busca_wikipedia, retorna_temperatura_atual]
tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = {tool.name: tool for tool in tools}

chain = prompt | chat.bind(functions=tools)
chain.invoke({'input': 'Olá'})


#O QUE PODEMOS FAZER COM TOOLRUN:
tool_run['busca_wikipedia'].invoke({'query': 'Isaac Asimov'})



#UTILIZANDO A OPENAIFUNCTIONSAGENTSOUTPUTPARSERS

from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()

chain.invoke({'input': 'Quem foi Isac Asimov'})





#RODANDO AS FERRAMENTAS

from langchain.agents.agent import AgentFinish

def roteamento(resultado):
    if isinstance(resultado, AgentFinish):
        return resultado.return_values['output']
    else:
        return tool_run[resultado.tool].run(resultado.tool)
    
    

chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser() | roteamento

chain.invoke({'input': 'Ola'})
chain.invoke({'input': 'Quem foi Isaac Asimov?'})
    