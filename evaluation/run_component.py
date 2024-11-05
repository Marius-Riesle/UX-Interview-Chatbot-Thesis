from promptflow.client import PFClient
import time
import json

### Functions called by config file(s) ###

# recursively goes throught data, to find and replace+eval CURRENT_TIMEs 
def replace_current_time_in_vars(data):
    # Recursive function to evaluate expressions and replace CURRENT_TIME
    if isinstance(data, dict):
        return {k: replace_current_time_in_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_current_time_in_vars(item) for item in data]
    elif isinstance(data, str):
        # Check if "CURRENT_TIME" is in the string
        if "CURRENT_TIME" in data:
            # Replace CURRENT_TIME with the actual current time
            current_time = str(int(time.time()))
            expression = data.replace("CURRENT_TIME", current_time)
            
            # Use regex to identify if it's an expression and evaluate it safely
            try:
                # Evaluate the expression if it contains math (like CURRENT_TIME - (10*60))
                result = eval(expression)
                return result
            except Exception as e:
                # If eval fails, return the original string
                print(f"Could not evaluate expression: {expression}, error: {e}")
                return expression
        else:
            return data
    else:
        return data

# function that gets called on test execution
def call_api(prompt, options, context):
    # getting the config of the current provider
    config = options.get("config", None)

    # getting the provider options
    flow_path = config.get("flow_path", None)
    node_name = config.get("node_name", None)

    raw_args = context["vars"].get("args")

    if raw_args is None:
        raise ValueError(f"args are not set!")
    
    args = json.loads(raw_args)
    processed_args = replace_current_time_in_vars(args)


    # Promptflow call
    pf = PFClient()

    # using the format conversation node
    node = pf.test(
        node=node_name,
        flow=flow_path,
        inputs=processed_args,
    )  

    return {"output":node}
