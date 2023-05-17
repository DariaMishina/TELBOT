from dotenv import dotenv_values
import openai
from aiogram import Dispatcher, types
from aiogram.types import ChatActions
from aiogram.dispatcher.filters import Text
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.document_loaders import CSVLoader
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.indexes import VectorstoreIndexCreator
import asyncio
from config.bot_config import API_KEY_CHATGPT, bot
import os

# os.environ['OPENAI_API_KEY'] = API_KEY_CHATGPT


# openai_api_key = API_KEY_CHATGPT

# loader = CSVLoader(file_path='./data/catalog.csv',
#                    encoding='utf8', csv_args={'delimiter': ';'})
# # data = loader.load()
# # embeddings = OpenAIEmbeddings(openai_api_key=API_KEY_CHATGPT)
# # vectorstore = FAISS.from_documents(data, embeddings)
# index_creator = VectorstoreIndexCreator()
# docsearch = index_creator.from_loaders([loader])
# chain = RetrievalQA.from_chain_type(llm=ChatOpenAI(
#     temperature=0.5, model_name='gpt-3.5-turbo'), retriever=docsearch.vectorstore.as_retriever(), input_key="question")
# # chain = ConversationalRetrievalChain.from_llm(llm=ChatOpenAI(
# #     temperature=0, model_name='gpt-3.5-turbo'), retriever=vectorstore.as_retriever(), chain_type='stuff')


# def chat_gpt(msg):
#     question = f'{msg}'
#     # query = f"Представь, что ты электронный помошник по подбору блюд. {question} \
#     # Формат вывода: 'product_name | Link' в столбик."
#     # response = chain({"question": query, 
#     #                     "chat_history": ''})
#     # return response["answer"]
#     response = chain({'question': question})
#     return response['result']

    
async def answer(message: types.Message):
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(3)
    # await message.answer(text=chat_gpt(message))
    await message.answer(text=message)

    print('Дата сообщения: ', message.date)

def register_handler(dp:Dispatcher):
    dp.register_message_handler(answer)