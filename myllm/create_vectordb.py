# from langchain_chroma import Chroma
# from langchain_community.document_loaders import PyMuPDFLoader
# from langchain_community.document_loaders import UnstructuredMarkdownLoader,UnstructuredFileLoader,TextLoader,UnstructuredPDFLoader
# from langchain_unstructured import UnstructuredLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from tqdm import tqdm
# from pathlib import Path
# import os
#
# #获取文件路径函数
# def get_files(dir_path):
#     #args:dir_path,目标文件夹路径
#     #目前支持.txt .md .pdf
#     file_list=[]
#     for filepath,dirnames,filenames in os.walk(dir_path):
#         for filename in filenames:
#             if filename.endswith(".pdf")or filename.endswith(".md")or filename.endswith(".txt"):
#                 file_list.append(os.path.join(filepath, filename))
#                 print(filename)
#     return file_list
#
#
# #加载文件函数
# def get_text(dir_path):
#     print("start get text")
#     #args:dir_path,目标文件夹路径
#     #首先调用上文定义的函数得到目标文件路径列表
#     file_list=get_files(dir_path)
#     print(file_list)
#     #docs存放之后的纯文本对象
#     docs=[]
#     count=0
#     for one_file in tqdm(file_list):
#         file_type=one_file.split('.')[-1]
#         print(count)
#         count+=1
#         if file_type=='pdf':
#             loader=PyMuPDFLoader(one_file)
#         elif file_type=='md':
#             loader=UnstructuredMarkdownLoader(one_file)
#         elif file_type=='txt':
#             loader=TextLoader(one_file)
#         else:
#             continue
#         docs.extend(loader.load())
#     return docs
#
#
# #目标文件夹
# tar_dir=[
#     "../resources",
# ]
#
#
# #加载目标文件
# docs=[]
# for path in tar_dir:
#     docs.extend(get_text(path))
#     print(docs)
#
#
# #对文本进行分块
# text_splitter=RecursiveCharacterTextSplitter(chunk_size=5000,chunk_overlap=10)
# split_docs=text_splitter.split_documents(docs)
#
#
# #加载开源词向量模型
# embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#
#
# #构建向量化数据库
# #定义持久化路径
# persistent_directory='../vectordb'
# #加载数据库
# vectordb=Chroma.from_documents(documents=split_docs,embedding=embeddings,persist_directory=persistent_directory)
