# nodes.py
from langchain.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import MessagesState

from tools import retrieve_blog_posts
from prompts import REWRITE_QUESTION_PROMPT, GENERATE_ANSWER_PROMPT


res_llm = init_chat_model('gpt-4.1', temperature=0)


def generate_query_or_respond(state: MessagesState):
    """llm이 사용자 대화를 기반으로 바로 답변을 생성하거나
    RAG를 위한 query 를 결정한다."""
    tllm = res_llm.bind_tools([retrieve_blog_posts])
    res = tllm.invoke(state['messages'])
    return {'messages': [res]}


def rewrite_question(state: MessagesState):
    """사용자 질문을 재 작성"""
    messages = state['messages']
    # TODO: 나중에 전체 맥락을 이해하고 질문을 정제하는 것으로 바꾸기
    question = messages[0].content
    prompt = REWRITE_QUESTION_PROMPT.format(original_question=question)
    response = res_llm.invoke(prompt)
    return {'messages': [HumanMessage(content=response.content)]}


def generate_answer(state: MessagesState):
    """최종 답변 생성"""
    question = state['messages'][0].content  # 원본 질문
    docs = state['messages'][-1].content  # 마지막 RAG docs
    prompt = GENERATE_ANSWER_PROMPT.format(question=question, docs=docs)
    res = res_llm.invoke(prompt)
    return {'messages': [res]}