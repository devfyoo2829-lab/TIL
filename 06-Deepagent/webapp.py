#webapp.py
# Slack -> 메시지 들어온 알람 -> webapp.py 에서 받고 -> Agent 실행

from fastapi import FastAPI, Request
from app import graph

from langchain.messages import HumanMessage

app = FastAPI()

# localhost: 2024/slack/
@app.post('/slack/webhook')
async def slack_webhook(req: Request):
    from pprint import pprint
    print('------------------------------')
    payload = await req.json()
    text = payload['event'].get('text','')
    files_info = payload['event'].get('files',[])
    files = []
    for file in files_info:
        files.append(
        {
            'name':file['name'],
            'link':file['url_private_download'],
        }
        )
    result = graph.ainvoke({
        'messages':[HumanMessage(content=text)],
        'files':files
    })
    return {'ok': True}

# 최초 등록 때만 쓰는 코드
# return {'challenge': payload['challenge']}