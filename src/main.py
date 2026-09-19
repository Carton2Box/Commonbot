import os
import shlex
import pyperclip as pc
from google import genai
from google.genai import types
import typer
import pickle
#with open("file.pkl", "rb") as file:
#        print(pickle.load(file))
#quit()
recentprompt = None
client = None
data = {
    "api": None,
    "currenttxt": None,
    "model": "gemini-3.8-flash"
}
app = typer.Typer()
if os.path.getsize("file.pkl") > 0:
    with open("file.pkl", "rb") as file:
        data = pickle.load(file)
if data["api"] == None:
    print("please run newapi")

@app.command()
def newmodel(model:str):
    data.update({"model":model})

@app.command()
def firststart():
    simple = {
    "api": None,
    "currenttxt": None,
    "model": "gemini-3.8-flash"
    }
    with open("file.pkl", "wb") as file:
            pickle.dump(simple, file)
    print("done")

@app.command()
def newapi():
    api = pc.paste()
    data.update({"api":api})
    print("api updated")

@app.command()
def newtxt():
    txt = pc.paste()
    data.update({"currenttxt": txt})
    print("txt updated")

@app.command()
def quest(choiceortext : str):
    client = genai.Client(api_key=data["api"])
    que = pc.paste()
    prompt = "Please read the following text and answer my question in AAA: BBB\n And here is the question: CCC"
    if choiceortext == "choice":
        prompt = prompt.replace("AAA", "a single letter")
    elif choiceortext == "text":
        prompt = prompt.replace("AAA", "a short paragraph")
    prompt = prompt.replace("BBB", data["currenttxt"])
    prompt = prompt.replace("CCC", que)
    global recentprompt
    recentprompt = prompt
    print(prompt)
    interaction = client.interactions.create(
        model=data["model"],
        input=prompt
    )
    print(interaction.output_text)

@app.command()
def askagain():
    interaction = client.interactions.create(
            model=data["model"],
            input = recentprompt
    )
    print(interaction.output_text)

@app.command()
def save():
    with open("file.pkl", "wb") as file:
        pickle.dump(data,file)
    print("saved")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo("Welcome to Commonbot! Type 'exit' to quit.")
        while True:
            try:
                user_input = typer.prompt(">>")
                if user_input.strip().lower() in ["exit", "quit"]:
                    break
                args = shlex.split(user_input)
                if not args:
                    continue
                app(args)
            except SystemExit:
                continue
            except Exception as e:
                typer.echo(f"Error: {e}")

if __name__ == "__main__":
    app()