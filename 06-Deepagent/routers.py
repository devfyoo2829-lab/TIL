# routers.py

def check_files(state):
    files = state.get('files', [])
    print(files)

    if files:
        return 'upload'
    else:
        return 'deep_agent'