# nodes.py
from state import State
from backend import dt_backend
import requests

def upload(state: State):
    files = state['files']
    upload_paths = [] #업로드 된 경로를 모을 리스트

    for file in files:
        # Step 1: Slack에서 파일 다운로드 (바이너리로 받기)
        response = requests.get(file['link'])
        file_binary = response.content # 파일의 실제 데이터 (바이너리)

        # Step 2: Daytona 샌드박스에 업로드
        save_path = f"/home/daytona/data/{file['name']}.csv"
        dt_backend.upload_files(
            [
                (save_path, file_binary)
            ]
        )
        # Step 3: 업로드된 경로를 목록에 추가
        upload_paths.append(save_path)
    
    # Step 4: State 업데이트 (다음 노드가 경로를 알 수 있도록)
    return {'upload_paths': upload_paths}

    # dt_backend.upload_files(
    #     [
    #         ('/home/daytona/data/sales_data.csv', csv_bytes)
    #     ]
    # )
    # return {'messages': [{'role': 'ai', 'content': 'ok'}]}

    def analyze(state: State):
        upload_paths = state['upload_paths']
        user_message = state['message']

        # TIP 핵심: Deep Agent에게 파일 위치를 먼저 알려줌
        # 위치를 모르면 분석이 끝나지 않는 문제 발생!
        file_location_prompt = "\n".join([
            f"- {path}" for path in upload_paths
        ])

        full_prompt = f"""아래 경로에 분석할 파일이 저장되어 있습니다: {file_location_prompt}
        사용자 요청: {user_message}"""
        
        # Deep Agent 호출
        result = dt_backend.run_agent(full_prompt)
        return {'result': result}
    