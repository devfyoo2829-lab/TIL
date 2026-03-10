# tools.py
from langchain.tools import tool
from vectorstore import retriever

@tool
def retrieve_blog_posts(query: str) -> str:
    """AI, LLM에 관련된 정보를 블로글 글에서 검색 후 return"""
    docs = retriever.invoke(query)
    # docs 는 메타데이터를 포함한 리스트 -> LLM 은 내용만 들어있는 str 이면 충분하다.
    # 전처리 작업
    return '\n\n'.join([doc.page_content for doc in docs])