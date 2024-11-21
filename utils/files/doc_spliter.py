# -*- coding = utf-8 -*-
# @time:2024/7/31 13:58
# Author:david yuan
# @File:doc_spliter.py
# @Software:VeSync

'''
pip install langchain
'''
from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from vagents.vagentic.files.base import File
import os
class DocSpliter(File):

    def __init__(self, txt_path):
        self.loader = UnstructuredFileLoader(txt_path)
        # 将文本转成 Document 对象
        self.documents = self.loader.load()
        # 初始化 openai 的 embeddings 对象
        self.embeddings = OpenAIEmbeddings()
        print(f'documents: {len(self.documents)}')
        self.persist_path = 'vector_store'

    def get_spilt_docs(self):
        # 初始化文本分割器
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 0
        )

        # 切分文本
        split_documents = text_splitter.split_documents(self.documents)
        print(f'documents: {len(split_documents)}')
        return split_documents


    def qa_result(self,split_documents,query_text):
        # 将 document 通过 openai 的 embeddings 对象计算 embedding 向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
        docsearch = Chroma.from_documents(split_documents, self.embeddings)

        # 创建问答对象
        qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(),
                                         return_source_documents=True)
        # 进行问答
        result = qa({"query": query_text})
        print(result)
        return result


    def chroma_save(self):
        # 持久化数据
        docsearch = Chroma.from_documents(self.documents, self.embeddings, persist_directory=self.persist_path)
        docsearch.persist()

    def load_chroma(self):
        # 加载数据
        docsearch = Chroma(persist_directory=self.persist_path, embedding_function=self.embeddings)
        return docsearch



