#AGORA ADICIONANDO UMA MEMORIA AO AGENT

#LANGCHAIN AGENT EXECUTOR

from langchain.agents import AgentExecutor
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.schema.agent import AgentFinish
from langchain.agents.format_scratchpad import format_to_openai_function_messages

chat = ChatOpenAI()


tools = [busca_wikipedia, retorna_temperatura_atual]

tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = {tool.name: tool for tool in tools}

chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()

#O AGENT:

prompt = ChatPromptTemplate.from_messages(
    ('system', 'Voce eh um assistente amigavel chamado Jarvis'),
    ('user', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad')
)

pass_through = RunnablePassthrough.assign(
    agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps']) 
)

agent_chain = pass_through | prompt | chain.invoke(functions=tools_json) | OpenAIFunctionsAgentOutputParser()


#O AGENT EXECUTOR:

def run_agent(input):
    passo_intermediarios = []
    
    while True:
        resposta = agent_chain.invoke({
            'input': input,
            'intermediate_steps' : passo_intermediarios
        })
        if isinstance(resposta, AgentFinish):
            return resposta
        observacao = tool_run[resposta.tool].run(resposta.tool_input)
        passo_intermediarios.append((resposta, observacao))
        
        
run_agent('Qual a temperatura de Florianopolis?')

#LANGCHAIN AGENT EXECUTOR

agent_executor = AgentExecutor(
    agent = agent_chain,
    tools=tools,
    verbose=True
)

resposta = agent_executor.invoke({'input': 'Qual a temperatura de Porto Alegre?'})





#AGORA ADICIONANDO A MEMORIA


from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

memory = ConversationBufferMemory(
    return_messages=True,
    memory_key='chat_history'
)

prompt = ChatPromptTemplate.from_messages(
    ('system', 'Voce eh um assistente amigavel chamado Jarvis'),
    MessagesPlaceholder(variable_name='chat_history') #VALOR TEM QUE SER IGUAL A MEMORY KEY SETADA NA MEMORY
    ('user', '{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad')
)

pass_through = RunnablePassthrough.assign(
    agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps'])
)

agent_chain = pass_through | prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()



agent_executor = AgentExecutor(
    agent = agent_chain,
    tools=tools,
    memory=memory
    verbose=True
)


