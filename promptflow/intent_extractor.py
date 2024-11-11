
from promptflow import tool
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(intent: str) -> str:
    intent = json.loads(intent)

    if "Absicht" not in intent:
            print(f"error in intent_extractor!!! Formatting is bad!")
            return "antwort auf frage"  # Assume its an answer if there is a formatting error

    intent = intent["Absicht"].lower()

    if "antwort auf frage" in intent:
        return "antwort auf frage"
    elif "interview frage" in intent:
        return "interview frage"
    elif "klarstellen der frage" in intent:
        return "klarstellen der frage"
    else:
        return "anderes"
