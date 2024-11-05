
from promptflow import tool
import time


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(start_zeit: int, gesamtzeit: int, time_spent:dict) -> str:
    aktuelle_zeit = time.time()
    diff_zeit = (aktuelle_zeit - start_zeit) / 60
    restliche_zeit = gesamtzeit - diff_zeit
    # TODO konkret auf die Verteilung der Zeit auf die verschiedenen Goals eingehen
    output_str = f"Du hast noch {str(int(restliche_zeit))} Minuten Zeit übrig (insgesamt dauert das Interview 25 Minuten)." 
    if restliche_zeit < 10:
        output_str += "\nAchte darauf auch noch auf Themen einzugehen, in denen du bisher wenig Erkenntnisse erlangt hast oder in denen du bisher wenig Zeit verbracht hast."
    elif restliche_zeit < 5:
        output_str += "\nEs ist wichtig das du in allen Themen Informationen gesammelt hast! gehe auf Themen ein, in denen du bisher wenig Erkenntnisse erlangt hast oder in denen du bisher wenig Zeit verbracht hast."
    
    output_str += "\n\nBisher hast du so viel Zeit für jedes Thema verwendet:"
    for key in time_spent:
        output_str += f"\n{key}: {int(time_spent[key] /60)} Minuten"
    return output_str
