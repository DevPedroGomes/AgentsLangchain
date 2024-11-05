#UTILIZANO DECORADOR TOOL, COM @
from langchain.agents import tool

@tool
def retorna_temperatura_atual(localidade: str):
    """Faz busca online e retorna temperatura de localidade"""
    return '25c'

#DESCREVENDO ARGUMENTOS
from langchain.pydantic_v1 import BaseModel,Field

class RetornaTempArgs(BaseModel):
    """"""
    localidade: str = Field(description='Localidade a ser buscada', example=['Sao Paulo', 'Porto Alegre'])
    
@tool(args_schema=RetornaTempArgs)
def retorna_temperatura_atual(localidade: str):
    """Faz buca online e retorna temperatura de uma localidade"""
    return '25c'

retorna_temperatura_atual.invoke({'localidade': 'Porto Alegre'})






#CRIANDO TOOL COM STRUCTUREDTOOL
#OUTRA FORMA

from langchain.tools import StructuredTool

class RetornaTempArgs(BaseModel):
    """"""
    localidade: str = Field(description='Localidade a ser buscada', example=['Sao Paulo', 'Porto Alegre'])
    
@tool(args_schema=RetornaTempArgs)
def retorna_temperatura_atual(localidade: str):
    return '25c'

tool_temp = StructuredTool.from_function(
    func="retorna_temperatura_atual",
    name='ToolTemperatura',
    args_schema='RetornaTempArgs',
    description='Faz buca online e retorna temperatura de uma localidade',
    return_direct=True
)
    
tool_temp.name
tool_temp.args
tool_temp.description



tool_temp.invoke({'localidade': 'Sao Paulo'})    