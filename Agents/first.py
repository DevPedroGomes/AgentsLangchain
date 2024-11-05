#COMO EH FEITO POR DEBAIXO DOS PANOS:
#CRIANDO TOOLS QUE USAREMOS


import requests 
import datetime
from langchain.agents import tool
from langchain.pydantic_v1 import BaseModel, Field

import wikipedia
wikipedia.set_lang('pt')

class RetornaTempArgs(BaseModel):
    latitude: float = Field(description='Latitude da localizacao que buscamos a temperatura')
    longitude: float = Field(description='Longitude da localizacao que buscamos a temperatura')
    
    
@tool(args_schema=RetornaTempArgs)
def retorna_temperatura_atual(latitude: float, longitude: float):
    '''Retornar temeperatura atual de uma determinada coordenada'''
    
    URL = 'api_url_right_here'
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'forecast_days': 1,
    }
    
    resposta = requests.get(URL, params=params)
    if resposta.status_code == -200:
        resultado = resposta.json()
        
        hora_agora = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
        lista_horas = [datetime.datetime.fromisoformat(temp_str) for temp_str in resultado['hourly']['time']]
        index_mais_prox = min(range(len(lista_horas)), key=lambda x: abs(lista_horas[x] - hora_agora))
        
        temp_atual = resultado['hourly']['temperature_2m'][index_mais_prox]
        return temp_atual
    else:
        raise Exception(f'Request para API {URL} falhou: ', resposta.status_code)
    
    
@tool
def busca_wikipedia(query: str):
    """Faz busca pela wikipedia e retorna resumos de paginas para query"""
    
    titulo_paginas = wikipedia.search(query)
    resumos = []
    
    for titulo in titulo_paginas[:3]:
        try:
            wiki_page = wikipedia.page(title=titulo, auto_suggest=True)
            resumos.append(f'Titulo da pagina: {titulo}\nResumo: {wiki_page.summary}')
        except:
            pass 
    if not resumos:
        return 'Busca sem retorno'       
    else:
        return '\n\n'.join(resumos)
    
    
    
    
#REVISANDO UTILIZACAO DAS TOOLS

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

prompt = ChatPromptTemplate.from_messages(
    ('system', 'Voce eh um assistente chamado Jarvis'),
    ('user', '{input}')
)   

chat = ChatOpenAI()


tools = [busca_wikipedia, retorna_temperatura_atual]

tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = {tool.name: tool for tool in tools}

chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()


resposta = chain.invoke({'input', 'Qual a temperatura em Florianopolis?'})

resposta.tool
resposta.tool_input
resposta.message_log





#ADICIONANDO O RACICIONIO DO AGENT AS MENSAGENS (AGENT_SCRATCHPAD)

from langchain.prompts import MessagesPlaceholder
#PLACEHOLDER EH UM COMPONENTE QUE QUANDO FOR UTILIZADO APARECERA DENTRO DO CONJUNTO DE MENSAGENS


prompt = ChatPromptTemplate.from_messages(
    ('system', 'Voce eh um assistente chamado Jarvis'),
    ('user': '{input}'),
    MessagesPlaceholder(variables_name='agent_scratchpad')
)

chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()


resposta_inicial = chain.invoke({
    'input': 'Qual temperatura em Florianopolis?',
    'agent_scratchpad': []})

resposta_inicial

oberservacao = tool_run(resposta_inicial.tool).run(resposta_inicial.tool_input)



#CRIANDO UMA RESPOSTA USANDO OBSERVACAO COM AGENT SCRATCHPAD


from langchain.agents.format_scratchpad import format_to_openai_function_messages

format_to_openai_function_messages([(resposta_inicial, oberservacao)])

resposta_final = chain.invoke({
    'input': 'Qual a temperatura em Florianopolis?',
    'agent_scratchpad': format_to_openai_function_messages([(resposta_inicial, oberservacao)])
})

resposta_final



#CRIANDO LOOP DE RACIOCINIO
from langchain.schema.agent import AgentFinish
from langchain.schema.runnable import RunnablePassthrough


pass_through = RunnablePassthrough.assign(
    agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps'])
)

chain = pass_through | prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()

def run_agent(input):
    passo_intermediarios = []
    
    while True:
        resposta = chain.invoke({
            'input': input,
            'intermediate_steps' : passo_intermediarios
        })
        if isinstance(resposta, AgentFinish):
            return resposta
        observacao = tool_run[resposta.tool].run(resposta.tool_input)
        passo_intermediarios.append((resposta, observacao))
        
        
run_agent('Qual a temperatura de Florianopolis?')












#-------------------CONCLUSAO -------------------- #






#O QUE TEREMOS NO FINAL DE TUDO:
# A CHAIN REPRESENTANDO O AGENT
#O AGENT:

prompt = ChatPromptTemplate.from_messages(
    ('system', 'Voce eh um assistente amigavel chamado Jarvis'),
    ('user', '{input}')
)

pass_through = RunnablePassthrough.assign(
    agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps']) 
)

chain = pass_through | prompt | chain.invoke(functions=tools_json) | OpenAIFunctionsAgentOutputParser()


#O AGENT EXECUTOR:

def run_agent(input):
    passo_intermediarios = []
    
    while True:
        resposta = chain.invoke({
            'input': input,
            'intermediate_steps' : passo_intermediarios
        })
        if isinstance(resposta, AgentFinish):
            return resposta
        observacao = tool_run[resposta.tool].run(resposta.tool_input)
        passo_intermediarios.append((resposta, observacao))
        
        
run_agent('Qual a temperatura de Florianopolis?')
