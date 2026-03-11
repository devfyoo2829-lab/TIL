from langgraph.graph import MessagesState


class State(MessagesState):
    files: list
    upload_paths: list

'''
{
    'files': ['a.csv', 'b.py'],
    'upload_paths': [
        '/home/daytona/data/a.csv',
        '/home/daytona/data/b.csv'
        ],
    'messages': [
        HumanMessage(content='hi'),
        AIMessage(content='hello')
    ]
}
'''