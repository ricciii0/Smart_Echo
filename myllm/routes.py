from flask import Blueprint, request, jsonify
from openai import OpenAI
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader,TextLoader,UnstructuredPDFLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from flask_cors import CORS
myllm = Blueprint('myllm', __name__)
CORS(myllm, supports_credentials=True)  # 启用CORS，允许跨域请求

client = OpenAI(api_key="", base_url="https://api.deepseek.com")
quiz_template = """
请根据给定的话题，生成1道单项选择题，以及对应的答案与解析,并将生成的问题，选项，答案，解释，按照JSON格式输出。
输出结果的要求:
问题应简明扼要，明确以文本信息为基础；
试着生成一个可以由整个文本而不是单个句子回答的问题；
在提出问题时，请不要引用所提供的文档，也不要说 “根据所提供的上下文”、“如文档所述”、“根据所给文档 ”或任何类似的话；
问题应该尽可能具有较强的逻辑推理要求；
单项选择题应该有4个选项，有且仅有1个正确选项；
答案应该只输出选项的字母序号；
在答案选择中，避免使用 “以上皆是 ”和 “以上皆非”；
所有理由应以 “正确 ”或 “不正确 ”开头；
所有答案选项（包括正确答案和干扰项）都必须有自己的理由说明；
输出示例：
EXAMPLE JSON OUTPUT:
{
    "question": "世界上最长的河流是哪一条河流？",
    "option":"A.长江 B.珠穆朗玛峰 C.尼罗河 D.密西西比河",
    "answer": "C",
    "rationale":"A:不正确，长江是世界第三长河，中国第一长河，不是世界最长的河流; B:不正确，珠穆朗玛峰是一座山峰，而不是一条河流;C:正确，尼罗河是世界最长的河流;D:不正确，密西西比河是世界第四长河，不是世界最长的河流"
}
"""

@myllm.route('/generate_vectordb', methods=['GET', 'POST'])
def generate_vectordb():
    #有待完善
    if request.method == 'POST':
        file=request.files['file']
        if not file:
            return jsonify({"error":"No file"}), 400
        file_type = file.split('.')[-1]
        file.save(f'./uploads/{file.filename}')
        file_path=f'./uploads/{file.filename}'
        docs=[]
        if file_type=='pdf':
            loader=PyMuPDFLoader(file_path)
        elif file_type=='md':
            loader=UnstructuredMarkdownLoader(file_path)
        elif file_type=='txt':
            loader=TextLoader(file_path)
        else:
            return jsonify({"error":"Unsupported file type"}), 400
        docs=loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        split_docs = text_splitter.split_documents(docs)
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        persistent_directory = '../vectordb'
        vectordb = Chroma.from_documents(documents=split_docs, embedding=embeddings,
                                         persist_directory=persistent_directory)
        return jsonify({"message":"Successfully generated vector database"}),201

@myllm.route('/generate_quizzes',methods=['GET', 'POST'])
def generate_quizzes():
    #有待完善
    if request.method == 'POST':
        query=request.json['query']
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        query_embedded=embeddings.embed(query)
        doc_list=Chroma.similarity_search_by_vector(query_embedded)
        text=""
        for doc in doc_list:
            t=doc.page_content
            text=text+t
        prompt=quiz_template.format(text=text)
        client.chat.with_raw_response.completions.create(prompt=prompt)


@myllm.route('/ai_answer', methods=['GET','POST'])
def ai_answer():
    if request.method == 'POST':
        input=request.json['input']
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful teaching assistant and your duty is to answer students' questions"},
                {"role": "user", "content": input},
            ],
            max_tokens=2048,
            temperature=2.0,
            stream=False
        )
        return response.choices[0].message.content

@myllm.route('/ai_quiz', methods=['GET','POST'])
def ai_quiz():
    if request.method == 'POST':
        input=request.json['input']
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": f"You are a helpful teaching assistant and your duty is to generate a quiz{quiz_template}"},
                {"role": "user", "content": f"Here are the theme of the quizzes you should generate:{input}"},
            ],
            max_tokens=2048,
            temperature=2.0,
            stream=False
        )
        return response.choices[0].message.content
