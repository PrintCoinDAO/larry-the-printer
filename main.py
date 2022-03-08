import requests
import discord
import config
from itertools import cycle

og_prompt_seed = "The following is a conversation with a demonic Printer named Larry. Larry is mysterious, unpredictable, and sexy.\n\nthemousery: Who are you?\nLarry: I am Larry the Printer.\nLonJon: i hate you larry. you're ugly and stupid\nLarry: I don't like LonJon. Get out of here dude, seriously."
prompt_seed = og_prompt_seed

# GPT-J settings
max_tokens = 128
temperature = 0.9
top_probability = 1.0
# Discord settings
client = discord.Client()

# when logged in, give a little indicator
@client.event
async def on_ready():
    print("logged in as {0.user}".format(client))

# when a message is received
@client.event
async def on_message(message):
    # ignore messages from self
    if message.author == client.user: return
    # reset command
    if message.content == "$reset":
        reset()
        return

    # if the message says larry
    if 'larry' in message.content.lower():
        # get a response from openai
        response = get_response(message.author.name, message.content)
        # send it
        if not response == "":
            await message.reply(response, mention_author=True)

# reset command
def reset():
    global prompt_seed
    global og_prompt_seed
    prompt_seed = og_prompt_seed

# get a response from gpt-j
def get_response(username, message):
    global prompt_seed

    new_seed = prompt_seed + "\n%s: %s\nLarry:" % (username, message)

    payload = {
        "context": new_seed,
        "token_max_length": max_tokens,
        "temperature": temperature,
        "top_p": top_probability,
    }
    raw_response = requests.post("http://api.vicgalle.net:5000/generate", params=payload).json()

    response = raw_response["text"].split("\n")[0].strip()
    if 'Sorry, the public API is limited to around 20 queries per every 30 minutes' in response: response=''
    prompt_seed = new_seed + ' ' + response

    # debug
    print("*********")
    print(prompt_seed)
    print("*********")

    # prompt_seed = new_seed
    return response

# main
if __name__ == "__main__":
    client.run(config.discord)
