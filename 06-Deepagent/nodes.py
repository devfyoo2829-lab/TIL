# nodes.py
from state import State
from backend import dt_backend


def upload(state: State):
    dt_backend.upload_files(
    [
        ('/home/daytona/data/sales_data.csv', csv_bytes)
    ]
)