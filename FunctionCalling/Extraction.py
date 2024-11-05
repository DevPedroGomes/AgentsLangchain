#EXTRACTION - 

texto = '''A Apple foi fundada em 1 de abril de 1976 por Steve Wozniak, Steve Jobs e Ronald Wayne 
com o nome de Apple Computers, na Califórnia. O nome foi escolhido por Jobs após a visita do pomar 
de maçãs da fazenda de Robert Friedland, também pelo fato do nome soar bem e ficar antes da Atari 
nas listas telefônicas.

O primeiro protótipo da empresa foi o Apple I que foi demonstrado na Homebrew Computer Club em 1975, 
as vendas começaram em julho de 1976 com o preço de US$ 666,66, aproximadamente 200 unidades foram 
vendidas,[21] em 1977 a empresa conseguiu o aporte de Mike Markkula e um empréstimo do Bank of America.'''

from langchain.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_core.utils.function_calling import convert_to_openai_function
'Data do acontecimento no formato yyyy-mm-dd'

class Acontecimento(BaseModel):
    """Informacoes sobre um acontecimento"""
    
    data: str = Field(description="Data do acontecimento no formato yyyy-mm-dd")
    acontecimento: str = Field(description="Acontecimento extraido do texto")
    
    
class ListaAcontecimentos(BaseModel):
    """Acontecimentos para extracao"""
    
    acontecimentos: List[Acontecimento] = Field(description="Lista de Acontecimentos presentes no texto informado")
    
    
tools_acontecimentos = convert_to_openai_function(ListaAcontecimentos)
tools_acontecimentos


#AGORA EXTRAINDO OS DADOS

from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Extraia as frases de acontecimentos. Elas devem ser extraidas integralmente'),
    ('user', '{input}')
])

chat = ChatOpenAI()

from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser

chain = (prompt 
         | chat.bind(functions=[tools_acontecimentos], function_call = {'name': 'ListaAcontecimentos'})
         | JsonKeyOutputFunctionsParser(key_name='acontecimos'))    


chain.invoke({'input': texto})











#EXTRAINDO INFORMACOES DA WEB
from langchain_community.document_loaders.web_base import WebBaseLoader

loader = WebBaseLoader('URL_AQUI')

page = loader.load()
#ISSO TRAZ UM CONTEUDO DESFORMATADO

from langchain.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_core.utils.function_calling import convert_to_openai_function

class BlogPost(BaseModel):
    """Informacoes sobre um post de blog"""
    
    titulo: str = Field(description='O titulo do post de blog')
    autor: str = Field(description='O autor do post')
    data: str = Field(description='A data da publicacao do post')
    
    
class BlogSite(BaseModel):
    """Lista de blog posts de um site"""
    
    posts: List[BlogPost] = Field(description='Lista de posts de blog do site')
    

tool_blog = convert_to_openai_function(BlogSite)        

from langchain.output_parsers.openai_functions import JsonKeyOutputFunctionsParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages([
    ('system', 'Extraia da pagina todos os posts de blog com autor e data'),
    ('user', '{input}')
])

chat = ChatOpenAI()

chain = (prompt
         | chat.bind(functions=[tool_blog], function_call={'name': 'BlogSite'})
         | JsonKeyOutputFunctionsParser(key_name='posts'))

chain.invoke({'input': page})