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

    # goal args
    raw_goal_args = context["vars"].get("goal_args")

    if raw_goal_args is None:
        raise ValueError(f"raw_goal_args are not set!")
    
    goal_args = json.loads(raw_goal_args)
    processed_goal_args = replace_current_time_in_vars(goal_args)

    # eval args
    raw_eval_args = context["vars"].get("eval_args")

    if raw_eval_args is None:
        raise ValueError(f"raw_eval_args are not set!")
    
    eval_args = json.loads(raw_eval_args)
    processed_eval_args = replace_current_time_in_vars(eval_args)


    # Promptflow call
    pf = PFClient()

    # Goal nodes
    goal_0 = pf.test(
        node="goal_0",
        flow=flow_path,
        inputs=processed_goal_args,
    )  
    
    goal_1 = pf.test(
        node="goal_1",
        flow=flow_path,
        inputs=processed_goal_args,
    )  
    
    goal_2 = pf.test(
        node="goal_2",
        flow=flow_path,
        inputs=processed_goal_args,
    ) 

    # eval nodes
    processed_eval_args["vorschlag_1"] = goal_0
    processed_eval_args["vorschlag_2"] = goal_1
    processed_eval_args["vorschlag_3"] = goal_2
    
    goal_eval_0 = pf.test(
        node="goal_eval_0",
        flow=flow_path,
        inputs=processed_eval_args,
    )  
    
    goal_eval_1 = pf.test(
        node="goal_eval_1",
        flow=flow_path,
        inputs=processed_eval_args,
    )  
    
    goal_eval_2 = pf.test(
        node="goal_eval_2",
        flow=flow_path,
        inputs=processed_eval_args,
    )   

    # goal extractor
    extractor_args = {
        "goal_0": goal_0,
        "goal_1": goal_1,
        "goal_2": goal_2,
        "goal_eval_0": goal_eval_0,
        "goal_eval_1": goal_eval_1,
        "goal_eval_2": goal_eval_2
    }
    extracted_goal = pf.test(
        node="goal_eval_extractor",
        flow=flow_path,
        inputs=extractor_args,
    )   


    return {
        "output":{
            "extracted_goal": extracted_goal,
            "goal_0": goal_0,
            "goal_1": goal_1,
            "goal_2": goal_2,
            "goal_eval_0": goal_eval_0,
            "goal_eval_1": goal_eval_1,
            "goal_eval_2": goal_eval_2
            }
        }
