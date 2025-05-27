import discord
import os
from discord.ext import commands
import requests
import json
import random

with open("donnees.json", "r+") as f:
    data = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

triste_mots = ["depressif", "deprime", "mauvaise humeur", "malheureux", "colere", "miserable", "deprimant", "triste"]
starter_encourageant = ["tu peux le faire !", "t'es une bonne personne/bot !"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote

def update_encouragements(encouraging_message):
    if "encouragements" in data.keys():
        encouragements = data["encouragements"]
        encouragements.append(encouraging_message)
        data["encouragements"] = encouragements
    else:
        data["encouragements"] = [encouraging_message]

def delete_encouragements(index):
    encouragements = data["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    data["encouragements"] = encouragements

def save_data():
    with open("donnees.json", "w") as f:
        json.dump(data, f, indent=4)

@client.event
async def on_ready():
    print("Je suis connecte en tant que {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith("$inspire"):
        await message.channel.send(get_quote())

    options = starter_encourageant
    if "encouragements" in data.keys():
        options += data["encouragements"]

    if any(word in msg for word in triste_mots):
        await message.channel.send(random.choice(options))
    
    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ",1)[1]
        update_encouragements(encouraging_message)
        save_data()
        await message.channel.send("Nouveau message encourageant ajoute.")
    
    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in data.keys():
            index = int(message.split("$del",1)[1])
            delete_encouragements(index)
            save_data()
            encouragements = data["encouragements"]
        await message.channel.send(encouragements)

client.run(os.getenv("TOKEN"))