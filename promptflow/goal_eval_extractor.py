
from promptflow import tool
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(goal_0: str,goal_1: str,goal_2: str,goal_eval_0: str,goal_eval_1: str,goal_eval_2: str,) -> str:
    goals = [goal_0, goal_1, goal_2]
    goal_evals = [goal_eval_0, goal_eval_1, goal_eval_2]
    counted = ""
    most_common = -1
    for goal_eval in goal_evals:
        goal_eval = json.loads(goal_eval)
        if "Bester_Vorschlag" not in goal_eval:
            print(f"error in goal_eval_extractor!!! Formatting is bad!")
            break   # if there is an formatting issue
        goal_eval = goal_eval["Bester_Vorschlag"]
        
        if "1" in goal_eval and "1" in counted:
            most_common = 1
            break 
        elif "2" in goal_eval and "2" in counted:
            most_common = 2
            break 
        elif "3" in goal_eval and "3" in counted:
            most_common = 3
            break 
        else:
            counted += goal_eval
    
    if most_common < 0:
        return goal_1 
    else:
        return goals[most_common-1]
    
