# backend.py
from daytona import Daytona
from langchain_daytona import DaytonaSandbox

sandbox = Daytona().create()
dt_backend = DaytonaSandbox(sandbox=sandbox)