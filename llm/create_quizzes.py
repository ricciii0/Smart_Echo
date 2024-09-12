from openai import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from oauthlib.uri_validate import query
from sentence_transformers import SentenceTransformer
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from config import Config
import json
quiz_template = """
请根据以下文本，生成1道单项选择题，以及对应的答案与解析,并将生成的问题，选项，答案，解释，按照JSON格式输出。
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
每个选项的理由说明都应该由;结尾。
输出示例：
EXAMPLE JSON OUTPUT:
{
    "question": "世界上最长的河流是哪一条河流？",
    "option":"A.长江 B.珠穆朗玛峰 C.尼罗河 D.密西西比河",
    "answer": "C"，
    "rationale":"A:不正确，长江是世界第三长河，中国第一长河，不是世界最长的河流; B:不正确，珠穆朗玛峰是一座山峰，而不是一条河流;C:正确，尼罗河是世界最长的河流;D:不正确，密西西比河是世界第四长河，不是世界最长的河流"
}
"""

client = OpenAI(api_key=Config.API_KEY, base_url="https://api.deepseek.com")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb=Chroma(persist_directory='../vectordb',embedding_function=embeddings)

input_query="毛泽东"
# query_embedded=embeddings.embed_query(query)
doc_list=vectordb.similarity_search(input_query)
text=""
for doc in doc_list:
    t=doc.page_content
    text=text+t
print(text)

messages=[
    {"role":"system","content":quiz_template},
    {"role":"user","content":text}
]
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={
        'type': 'json_object'
    }
)

print(json.loads(response.choices[0].message.content))