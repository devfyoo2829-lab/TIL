# routers.py
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langgraph.graph import MessagesState

from prompts import GRADE_PROMPT


grader_llm = init_chat_model('gpt-4.1', temperature=0)


class GradeDocuments(BaseModel):
    """문서를 yes/no 로 질문과 연관있는지 평가"""
    binary_score: str = Field(description='연관성 점수: 연관 있으면 "yes", 연관 없으면 "no"')


def grade_document(state: MessagesState):
    """검색해온 문서가 사용자 질문과 관련이 있는지 체크 후 다음 노드 결정"""
    question = state['messages'][0].content
    docs = state['messages'][-1].content

    prompt = GRADE_PROMPT.format(question=question, docs=docs)
    ollm = grader_llm.with_structured_output(GradeDocuments)
    res = ollm.invoke([{'role': 'user', 'content': prompt}])

    score = res.binary_score

    if score == 'yes':
        return 'generate_answer'
    else:
        return 'rewrite_question'