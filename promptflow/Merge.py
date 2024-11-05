
from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool( string_2: str, string_3: str, string_4: str, string_5: str) -> str:
    return  (string_2 or "") + (string_3 or "") + (string_4 or "") + (string_5 or "")
