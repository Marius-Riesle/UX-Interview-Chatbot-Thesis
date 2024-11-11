
from promptflow import tool
import json

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(new_insights: str, insights: dict) -> str:
    new_insights = new_insights.lower()
    new_insights = json.loads(new_insights)

    if "erkenntnisse" not in new_insights:
            print(f"error in insights!!! Formatting is bad!")
            return insights  # Return original insights if no "erkenntnisse" key is found

    new_insights = new_insights["erkenntnisse"]

    for key in insights:
        if key in new_insights:
            for insight in new_insights[key]:
                insights[key] += "\n" + insight
        if key[:-1] in new_insights: #ressource statt ressourcen
            for insight in new_insights[key[:-1]]:
                insights[key] += "\n" + insight
        if key+"e" in new_insights: #ziele statt ziel
            for insight in new_insights[key+"e"]:
                insights[key] += "\n" + insight
        if key+"en" in new_insights: #umgebungen statt umgebung
            for insight in new_insights[key+"en"]:
                insights[key] += "\n" + insight
        

    return insights
