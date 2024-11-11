
from promptflow import tool
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(goal: str, last_goal: str) -> str:
    goal = json.loads(goal)
    if "Thema" not in goal:
        print(f"error in goal_extractor!!! Formatting is bad!")
        return last_goal
    goal = goal["Thema"].lower()
    
    for key in ["nutzer","ziel","umgebung","ressource"]:
        if key in goal:
            if key == "ressource":
                return key + "n"
            return key
    return last_goal
