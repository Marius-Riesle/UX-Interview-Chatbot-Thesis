
from promptflow import tool
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(goal: str) -> str:
    goal = json.loads(goal)["Thema"].lower()
    for key in ["nutzer","ziel","aufgabe","umgebung","ressource"]:
        if key in goal:
            if key in ["aufgabe","ressource"]:
                return key + "n"
            return key
    return "unklar"
