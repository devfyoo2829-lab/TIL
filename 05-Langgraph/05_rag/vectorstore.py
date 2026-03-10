# vectorstore.py
from bs4.filter import SoupStrainer  # uv pip install beautifulsoup4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

bs4_strainer = SoupStrainer(class_=('post-title', 'post-header', 'post-content'))

urls = [
    "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2024-07-07-hallucination/",
    "https://lilianweng.github.io/posts/2025-05-01-thinking/",
]

docs = [WebBaseLoader(web_path=url, bs_kwargs={'parse_only': bs4_strainer}).load() for url in urls]

docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
chunks = text_splitter.split_documents(docs_list)

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')

vectorstore = InMemoryVectorStore(embedding=embeddings)
ids = vectorstore.add_documents(chunks)

retriever = vectorstore.as_retriever(search_kwargs={'k': 4})