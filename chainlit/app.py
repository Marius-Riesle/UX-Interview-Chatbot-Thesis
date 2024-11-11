import chainlit as cl
from promptflow.client import load_flow
from dotenv import load_dotenv
import time
from datetime import datetime
import os
import pickle


load_dotenv()

### Suport functions ###

# Function to save variables to a pickle file
def save_vars(file_path):
    chat_history = cl.user_session.get("chat_history")
    starting_unix = cl.user_session.get("starting_unix")
    current_theme = cl.user_session.get("current_theme")
    time_spent = cl.user_session.get("time_spent") 
    insights = cl.user_session.get("insights") 
    
    data = {
        "chat_history": chat_history,
        "current_theme": current_theme,
        "starting_unix": starting_unix,
        "time_spent": time_spent,
        "insights": insights
    }

    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

# Function to restore variables from a pickle file
def restore_vars(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)

        user_name = cl.user_session.get("user").identifier

        cl.user_session.set("chat_history", data["chat_history"] or [])
        cl.user_session.set("current_theme", data["current_theme"] or "nutzer")
        cl.user_session.set("starting_unix", data["starting_unix"] or int(time.time()))
        cl.user_session.set("time_spent", data["time_spent"] or {"nutzer": 0, "ziel": 0,"umgebung": 0,"ressourcen": 0})
        cl.user_session.set("insights", data["insights"] or {"nutzer": f"- der Nutzer heißt {user_name}", "ziel": "","umgebung": "","ressourcen": ""})


# Accesses the default promptflow
def use_promptflow(input: str):
    chat_history = cl.user_session.get("chat_history")
    starting_unix = cl.user_session.get("starting_unix")
    time_spent = cl.user_session.get("time_spent")
    insights = cl.user_session.get("insights")
    current_theme = cl.user_session.get("current_theme")

    flow = load_flow(source="promptflow", environment_variables={"PF_DISABLE_TRACING": True})   # PF_DISABLE_TRACING has to be set as environment var
    result = flow(message=input, chat_history=chat_history, starting_unix=starting_unix, time_spent=time_spent, insights=insights, current_theme=current_theme)


    # add to time spent since last chatbot response
    last_response_time = cl.user_session.get("last_response_time") 
    if last_response_time is not None and chat_history[-1]["outputs"]["goal"] in time_spent:
        delta_question_time = time.time() - last_response_time
        time_spent[chat_history[-1]["outputs"]["goal"]] += int(delta_question_time)
    time_spent = cl.user_session.set("time_spent", time_spent)

    cl.user_session.set("last_response_time", int(time.time()))
    cl.user_session.set("insights", result["insights"])
    cl.user_session.set("current_theme", result["goal"] or current_theme)


    # append to chat_history
    chat_history = chat_history[-5:] #TODO festlegen wie viele chat Nachrichten immer mitgenommen werden
    chat_history.append( 
        {
            "inputs": {"message": input,
                       "intent": result["intent"]},
            "outputs": {
                "response": result["response"],
                "goal": result["goal"],
            },
        }
    )
    cl.user_session.set("chat_history", chat_history)

    return result


### Events ###

@cl.on_message
async def main(message: cl.Message):
    # send empty message so "Running" is displayed
    msg = cl.Message(content="", author="Chatbot")
    await msg.send()

    # save the new chat messages
    file_name = f'./chats/{cl.user_session.get("user").identifier}.txt'
    with open(file_name, 'a') as file:
        # Write each item on a new line
        timestamp = datetime.now().strftime('%H:%M:%S')
        file.write(f"{timestamp} user: {message.content}\n")

    # if interview is over
    if cl.user_session.get("starting_unix") is not None and time.time() - cl.user_session.get("starting_unix") > 1500:
        msg.author = "Chatbot"
        response = "Danke für die Teilnahme!\nDas Chatbot Interview ist hiermit beendet. Schreibe oder rufe Marius einfach an."
        for i in range(int(len(response)/3)+2):
            msg.content = response[:i*3]
            await msg.update()
            time.sleep(0.05)
        return

    exec_time = time.time()
    # execute promptflow equal to use_promptflow(message.content)
    response = await cl.make_async(use_promptflow)(
        message.content
    )

    # give context info as step if admin
    if cl.user_session.get("user").metadata["role"] == "admin":
        # user_session_data
        async with cl.Step(name="user_session_data", type="tool") as step:
            step.input = {
                "chat_history" : cl.user_session.get("chat_history"),
                "starting_unix" : cl.user_session.get("starting_unix"),
                "current_theme" : cl.user_session.get("current_theme"),
                "time_spent" : cl.user_session.get("time_spent"),
                "insights" : cl.user_session.get("insights"),
            }

        # response_data
        async with cl.Step(name="response_data", type="tool") as step:
            step.input = response

    print(time.time()- exec_time)
    # fake stream message
    msg.author = "Chatbot"
    for i in range(int(len(response["response"])/3)+2):
        msg.content = response["response"][:i*3]
        await msg.update()
        time.sleep(0.05)


    # save the new chat messages
    file_name = f'./chats/{cl.user_session.get("user").identifier}.txt'
    with open(file_name, 'a') as file:
        # Write each item on a new line
        response = response["response"]
        timestamp = datetime.now().strftime('%H:%M:%S')
        file.write(f"{timestamp} bot: {response}\n")


@cl.on_chat_start
async def on_chat_start():
    user_name = cl.user_session.get("user").identifier

    file_name_txt = f'./chats/{user_name}.txt'
    file_name_pkl = f'./chats/{user_name}.pkl'

    # if user_session_data was saved
    if os.path.exists(file_name_pkl):
        restore_vars(file_name_pkl)
    else:
        cl.user_session.set("chat_history", [] or cl.user_session.get("chat_history"))
        cl.user_session.set("current_theme", "nutzer")
        cl.user_session.set("starting_unix", int(time.time()))
        cl.user_session.set("time_spent", {"nutzer": 0, "ziel": 0,"umgebung": 0,"ressourcen": 0})
        cl.user_session.set("insights", {"nutzer": f"- der Nutzer heißt {user_name}", "ziel": "","umgebung": "","ressourcen": ""})

    # If messages were saved
    if os.path.exists(file_name_txt):
        last_bot_message = cl.user_session.get("chat_history")[-1]["outputs"]["response"]
        await cl.Message(content=last_bot_message, author="Chatbot").send()

        # Add a reconnection info to file
        with open(file_name_txt, 'a') as file:
            zeit = datetime.now().strftime("%H:%M:%S")
            file.write(f"\n\nChat wurde um {zeit} weitergeführt:\n\n")
    else:
        content=f'Hallo {user_name}, herzlich willkommen zum Interview!\n\nEs freut mich, dass du dir die Zeit nimmst. Wenn du Fragen hast – sei es zu den einzelnen Fragen oder zum Interviewablauf – kannst du jederzeit nachfragen.\n Nimm dir für deine Antworten gerne so viel Zeit, wie du benötigst, und beschreibe deine Gedanken ruhig ausführlich. Denk daran: Hier geht es um deine persönliche Sichtweise, es gibt also keine "falschen" Antworten!\n\nDann starten wir direkt:\nKönntest du dich kurz vorstellen und etwas über deine berufliche Tätigkeit erzählen?'
        msg = cl.Message(content=content, author="Chatbot")
        await msg.send()

        chat_history = []
        chat_history.append(
            {
                "inputs": {"question": "",
                        "intent": "anderes"},
                "outputs": {
                    "response": f'Herzlich willkommen zum Interview!\n\nEs freut mich, dass du dir die Zeit nimmst. Wenn du Fragen hast – sei es zu den einzelnen Fragen oder zum Interviewablauf – kannst du jederzeit nachfragen.\n Nimm dir für deine Antworten gerne so viel Zeit, wie du benötigst, und beschreibe deine Gedanken ruhig ausführlich. Denk daran: Hier geht es um deine persönliche Sichtweise, es gibt also keine "falschen" Antworten!\n\nDann starten wir direkt:\nKönntest du dich kurz vorstellen und etwas über deine berufliche Tätigkeit erzählen?',
                    "goal": "nutzer",
                },
            }
        )
        cl.user_session.set("chat_history", chat_history)


@cl.on_chat_end
def on_chat_end():
    # save the user_session_data to a pkl file
    user_name = cl.user_session.get("user").identifier
    file_name = f'./chats/{user_name}.pkl'

    save_vars(file_name)

    print("The user disconnected!")


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # if user enters mre as password he is admin
    if password == "mre": 
        return cl.User(
            identifier=username, metadata={"role": "admin", "provider": "credentials"}
        )
    # if he enters anything else he is user
    else:
        return cl.User(
            identifier=username, metadata={"role": "user", "provider": "credentials"}
        )
