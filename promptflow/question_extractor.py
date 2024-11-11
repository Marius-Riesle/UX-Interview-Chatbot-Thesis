
from promptflow import tool
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(question: str) -> str:
    question_json = json.loads(question)
    if "Endfrage" not in question_json:
        return "Es tut mir leid, da ist wohl etwas schief gelaufen, wiederhole deine Antwort bitte. Wende dich bitte an Marius falls dieser Fehler weiterhin auftritt."
    
    return question_json["Endfrage"]
    
