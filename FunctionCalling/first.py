#CRIANDO ESTRUTURA DE FUNCTION CALLING COM LANGCHAIN
#INTRODUCAO AO PYDANTIC, UMA FORMA DE CRIAR CLASSES
from pydantic import BaseModel

class pydPessoa(BaseModel):
    nome: str
    idade: int
    peso: float
    
    

adriano = pydPessoa(nome="Adriano", idade=32, peso=68)
print(adriano)
print(adriano.peso)
print(adriano.idade)



from typing import List

class inTocTeam(BaseModel):
    employeess : List[pydPessoa]
    
inTocTeam(employeess=[pydPessoa(nome="Jackson", idade=30, peso=100)])    
    
    
# FUNCTION CALLING COM LANGCHAIN


from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional

class UnidadeEnum(str, Enum):
    celcius = 'celsius'
    fahrenheit = 'fahrenreit'

class ObterTemperaturaAtual(BaseModel):
    """Obtem a temperatura atual de uma determinada localidade"""
    local : str = Field(description='O nome da cidade', examples=['Sao Paulo', 'Porto Alegre'])
    unidade : Optional[UnidadeEnum]

from langchain_core.utils.function_calling import convert_to_openai_function

tool_temperatura = convert_to_openai_function(ObterTemperaturaAtual)
print(tool_temperatura)


#AGORA COMO USAR O MODELO, CHAMANDO A TOOL
from langchain_openai import ChatOpenAI

chat = ChatOpenAI()

resposta = chat.invoke('Qual a temperatura de Porto Alegre', function=[tool_temperatura])



#OUTRA FORMA USANDO BIND



chat = ChatOpenAI()

chat_com_func = chat.bind(functions=[tool_temperatura])
resposta = chat.invoke('Qual a temperatura atual em Porto Alegre?')
print(resposta)


#OBRIGAR O MODELO A SEMPRE USAR A FUNCAO
resposta = chat.invoke(
    "Qual a temperatura atual em Porto Alegre?",
    functions=tool_temperatura,
    function_call={'name': "ObterTemperaturaAtual"} 
)
resposta



#AGORA COMO ADICIONAR ISSO A UMA CHAIN


from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Voce eh um assistente amigavel chamado Jack'),
    ('user', '{input}')
])

chain = prompt | chat.bind(functions=[tool_temperatura])

chain.invoke({'input': 'Ola, Qual a temperatura em Florianopolis?'})

