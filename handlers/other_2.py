import openai
import asyncio
import pinecone
from aiogram import types, Dispatcher
from config.bot_config import PINECONE_API_ENV, PINECONE_API_KEY, API_KEY_CHATGPT
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from config.csv_search import output_for_user


openai.api_key = API_KEY_CHATGPT

# загрузка данных
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)

pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "prodbase"
# namespace = "database7"
namespace = "all_prod"


docsearch = Pinecone.from_existing_index(
    index_name, embeddings, namespace=namespace)


def chat_gpt(message, docsearch=docsearch, namespace=namespace, user_id=None):
    llm = ChatOpenAI(
        temperature=0.5, openai_api_key=openai.api_key)
    chain = load_qa_chain(llm, chain_type="stuff")

    query = f'{message}'
    docs = docsearch.similarity_search(query,
                                       include_metadata=True, namespace=namespace)
    temp = (chain.run(input_documents=docs, question=query))
    # return (chain.run(input_documents=docs, question=query))
    # return output_for_user(temp)
    return temp

def chat_gpt_category(message, category):
    category_dict = {
        'Веганское меню': 'vegan',
        'Доступно каждому: лучшие цены': 'dostupno',
        'Доступно только онлайн': 'only-online',
        'Здоровое питание': 'healthyfood',
        'Курица-грилль': 'gril',
        'Мало калорий': 'malocal',
        'На дачу и пикник':'piknik',
        'Новинки':'new',
        'Роллы':'rolls',
        'Много белка':'mnogobel',
        'Салаты и закуски': 'salat',
        'Семейный формат': 'family',
        'Супы':'soup'
    }
    namespace_cat = category_dict[category]
    docsearch_cat = Pinecone.from_existing_index(
    index_name, embeddings, namespace=namespace)
    return output_for_user(chat_gpt(message, docsearch_cat, namespace_cat))
    
    
    
    
    
# Обработка обычного сообщения
async def answer(message: types.Message):
    # await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    # await asyncio.sleep(3)
    # temp = f"{message}, выведи название и ссылки"
    # await message.answer(text=chat_gpt(temp))

    print('Дата сообщения: ', message.date)


def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(answer)