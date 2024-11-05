#AGENTS DA PROPRIA LANGCHAIN

#TOOL CALLING

#EXEMPLO: UMA FERRAMENTA QUE UTILIZA PYTHON E AO TER ACESSO, FAZER UNS CALCULOS MAIS ROBUSTOS
from langchain_experimental.tools import PythonAstREPLTool
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


tools = [PythonAstREPLTool()]

system_message = '''Voce eh um assistente amigavel, chamado Jarvis. Certifique-se de usar a ferramenta PythonAstREPLTool para auxiliar a responder as perguntas'''

prompt = ChatPromptTemplate.from_messages(
    ('system', system_message),
    ('placeholder', '{chat_history}')
    ('human', '{input}'),
    ('placeholder', '{agent_scratchpad}')
)

chat = ChatOpenAI()

agent = create_tool_calling_agent(chat, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke('input', 'Qual eh oecimo valor da sequencia fibonacci ')















#ReAct
#UMA TECNICA DE ENGENHARIA DE PROMPT PARA INTERAGIR COM FERRAMENTAS EXTERNAS PARA RECUPERAR INFORMACOES ADICIONAIS QUE LEVAM A RESPOSTAS CONFIAVEIS


from langchain.agents import create_react_agent
