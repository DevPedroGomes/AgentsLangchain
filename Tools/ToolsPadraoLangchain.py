#ARXIV - FERRAMENTA UTILIZADA PARA RETORNAR RESUMOS DE ARTIGOS CIENTIFICOS DE UM TEMA SOLICITADO

from langchain_community.utilities.arxiv import ArxivAPIWrapper
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import StructuredTool

class ArxivArgs(BaseModel):
    query : str = Field(description='Query de busca no Arxiv')
    
tool_arxiv = StructuredTool.from_function(
    func=ArxivAPIWrapper(top_k_results=3).run,
    args_schema=ArxivArgs,
    name='arxiv',
    description=(
        "Uma ferramenta em torno do Arxiv.org. "
        "Útil para quando você precisa responder a perguntas sobre Física, Matemática, "
        "Ciência da Computação, Biologia Quantitativa, Finanças Quantitativas, Estatística, "
        "Engenharia Elétrica e Economia utilizando artigos científicos do arxiv.org. "
        "A entrada deve ser uma consulta de pesquisa em inglês."
    ),
    return_direct=True
)   

print('Descricao: ', tool_arxiv.description)
print('Args: ', tool_arxiv.args)


tool_arxiv.run({'query': 'LLM'})







#INSTANCIANDO TOOL JA PRONTA DO LANGCHAIN

from langchain_community.tools.arxiv.tool import ArxivQueryRun

tool_arxiv_Queryrun = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=3))








#CRIANDO TOOL USANDO LOAD_TOOLS

from langchain.agents import load_tools

tools = load_tools({'arxiv'})
tool_arxiv = tools[0]







#PYTHON REPL


from langchain_experimental.tools.python.tool import PythonREPLTool

tool_repl = PythonREPLTool()
print('Descricao: ', tool_repl.description)
print('Args: ', tool_repl.args)


tool_repl.run({'query': 'print("oi")'})






#STACKOVERFLOW

from langchain.agents import load_tools

tools = load_tools({'stackexchange'})
tool_stack = tools[0]

print('Descricao: ', tool_stack.description)
print('Args: ', tool_stack.args)


tool_stack.run({'query': 'Langchain load_tools'})












#FILE SYSTEM

from langchain_community.agent_toolkits.file_management.toolkit import FileManagementToolkit

tool_kit = FileManagementToolkit(
    root_dir='arquivos',
    selected_tools=['write_file', 'read_file', 'file_search', 'list_directory']
)

tools = tool_kit.get_tools()

for tool in tools:
    print('Nome: ', tool.name)
    print('Descricao: ', tool.description)
    print('Args: ', tool.args)
    

#exemplo de aplicacao
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
tools_json = [convert_to_openai_function(tool) for tool in tools]
tool_run = {tool.name: tool for tool in tools}

prompt = ChatPromptTemplate.from_messages(
    ('system', 'Voce eh um assistente amigavel capaz de gerenciar arquivos'),
    ('user', '{input}')
)

chat = ChatOpenAI()

from langchain.agents.agent import AgentFinish

def roteamento(resultado):
    if isinstance(resultado, AgentFinish):
        return resultado.return_values['output']
    else:
        return tool_run[resultado.tool].run(resultado.tool)
    
    

chain = prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser() | roteamento


chain.invoke({'input': 'O que voce eh capaz de fazer?'})
chain.invoke({'input': 'Quais arquivos pdf voce tem na pasta?'})
chain.invoke({'input': 'Quais arquivos .txt voce tem na pasta?'})
chain.invoke({'input': 'Crie um arquivo txt chamado notas, com o seguinte conteudo: "Isso foi feito por uma LLM!"'})
chain.invoke({'input': 'Leia o arquivo notas.txt"'})

