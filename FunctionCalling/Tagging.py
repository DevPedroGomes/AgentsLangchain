#TAGGING - INTERPRETANDO DADOS COM FUNCOES

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.utils.function_calling import convert_to_openai_function

text = 'Eu gosto muito de Programacao'

class Sentimento(BaseModel):
    '''Define o sentimento e a lingua da mensagem enviada'''
    
    sentimento : str = Field(description='Sentimento do texto. Deve ser"pos", "neg" ou "nd" para nao definido')
    lingua : str = Field(description=text)
    
    
tool_sentimento = convert_to_openai_function(Sentimento)
tool_sentimento


from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    ('system', 'Pense com cuidado ao categorizar o texto conforme as instrucoes'),
    ('user', '{input}')
)    
chat = ChatOpenAI()

chain = prompt | chat.bind(functions=[tool_sentimento], function_call={'name': 'Sentimento'})

chain.invoke({'input': 'Eu gosto muito de programacao'})






#PARSENADO A SAIDA PARA OBTERMOS APENAS O QUE INTERESSA
#UTILIZANDO JSONOUTPUTPARSER
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

chain = (prompt
         | chat.bind(functions=[tool_sentimento], function_call={'name': 'Sentimento'})
         | JsonOutputFunctionsParser())
chain.invoke({'input': 'Eu gosto muito de programacao'})







#UM EXEMPLO MAIS INTERESSANTE



duvidas = [
    'Bom dia, gostaria de saber se há um certificado final para cada trilha ou se os certificados são somente para os cursos e projetos? Obrigado!',
    'In Etsy, Amazon, eBay, Shopify https://pint77.com Pinterest+SEO +II = high sales results',
    'Boa tarde, estou iniciando hoje e estou perdido. Tenho vários objetivos. Não sei nada programação, exceto que utilizo o Power automate desktop da Microsoft. Quero aprender tudo na plataforma que se relacione ao Trading de criptomoedas. Quero automatizar Tradings, fazer o sistema reconhecer padrões, comprar e vender segundo critérios que eu defina, etc. Também tenho objetivos de aprender o máximo para utilizar em automações no trabalho também, que envolve a área jurídica e trabalho em processos. Como sou fã de eletrônica e tenho cursos na área, também queria aprender o que precisa para automatizacões diversas. Existe algum curso ou trilha que me prepare com base para todas essas áreas ao mesmo tempo e a partir dele eu aprenda isoladamente aquilo que seria exigido para aplicar aos meus projetos?',
    'Bom dia, Havia pedido cancelamento de minha mensalidade no mes 2 e continuaram cobrando. Peço cancelamento da assinatura. Peço por gentileza, para efetivarem o cancelamento da assomatura e pagamento.',
    'Bom dia. Não estou conseguindo tirar os certificados dos cursos que concluí. Por exemplo, já consegui 100% no python starter, porém, não consigo tirar o certificado. Como faço?',
    'Bom dia. Não enconte no site o preço de um curso avulso. SAberiam me informar?'
    ]

from enum import Enum

from langchain.pydantic_v1 import BaseModel, Field

class SetorEnum(str, Enum):
    atentimendo_cliente = 'atendimento_cliente'
    duvidas_aluno = 'duvidas_aluno'
    vendas = 'vendas'
    spam = 'spam'


class DirecionaSetorResponsavel(BaseModel):
    """Direciona a duvida d eum cliente ou aluno, para o setor responsavel"""
    
    setor : SetorEnum
    
    
from langchain_core.utils.function_calling import convert_to_openai_function

tool_direcionamento = convert_to_openai_function(DirecionaSetorResponsavel)

    
prompt = ChatPromptTemplate.from_messages(
    ('system', 'Pense com cuidado ao categorizar o texto conforme as instrucoes'),
    ('user', '{input}')
)    
chat = ChatOpenAI()

chain = (prompt | chat.bind(functions=[tool_direcionamento], function_call={'name': 'DirecionaSetorResponsavel'})
         | JsonOutputFunctionsParser())

duvida = duvidas[0]

resposta = chain.invoke({'input': duvida})
print()


print('Duvida: ', duvida)
print('Resposta: ', resposta)

