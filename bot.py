import discord
import os
from discord.ext import commands
import requests
import json
import random
import asyncio
from pathlib import Path
import vt
from dotenv import load_dotenv
load_dotenv()
import hashlib

def calculer_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

VT_API_KEY = os.getenv("VT_API_KEY")
os.makedirs("temp", exist_ok=True)

with open("donnees.json", "r+") as f:
    data = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

triste_mots = ["depressif", "deprime", "mauvaise humeur", "malheureux", "colere", "miserable", "deprimant", "triste"]
starter_encourageant = ["tu peux le faire !", "t'es une bonne personne/bot !"]

class ExceptionTropLourd(Exception):
    pass

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

async def scan_file_discord(api_key: str, file_path: str, message, wait: bool = True):
  """
  Scan a file privately (plus mtn) on VirusTotal.

  Args:
      api_key: VirusTotal API key
      file_path: Path to file to scan
      wait: Wait for scan completion
  """
  async with vt.Client(api_key) as client:
    try:
        path_obj = Path(file_path)
        sha256 = calculer_sha256(file_path)


        if path_obj.stat().st_size > 650 * 1024 * 1024:
            raise ExceptionTropLourd("Le fichier dépasse 650 Mo.")
    
        if path_obj.stat().st_size > 32 * 1024 * 1024:
            upload_url = await client.get_upload_url()
            with open(file_path, "rb") as f:
                analysis = await client.scan_file_async(f, upload_url=upload_url)
                analysis = await client.get_object_async(f"/analyses/{analysis.id}")
                
        else:
            with open(file_path, "rb") as f:
                analysis = await client.scan_file_async(f)
                analysis = await client.get_object_async(f"/analyses/{analysis.id}")




        await message.channel.send("Scan submitted successfully")
        await message.channel.send(f"Analysis ID: {analysis.id}")
        scan_url = f"https://www.virustotal.com/gui/file/{sha256}/detection"

        await message.channel.send(f"Voir l’analyse complète : {scan_url}")

        if wait:
            await message.channel.send(f"Scan Status: {analysis.status}")
            if hasattr(analysis, "stats"):
                await message.channel.send("Detection Stats:")
                for k, v in analysis.stats.items():
                    await message.channel.send(f"  {k}: {v}")

    except ExceptionTropLourd as e:
        await message.channel.send(str(e))

    except vt.error.APIError as e:
        await message.channel.send(f"API Error: {e}")

    except Exception as e:  # pylint: disable=broad-exception-caught
        await message.channel.send(f"Error: {e}")


    finally:

        try:
            os.remove(file_path)
            print(f"Fichier supprimé : {file_path}")

        except Exception as cleanup_error:
            print(f"Impossible de supprimer le fichier : {cleanup_error}")

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

    if msg.startswith("$scan") and message.attachments:
        attachement = message.attachments[0]
        file_path = f"temp/{attachement.filename}"
        await attachement.save(file_path)

        await scan_file_discord(api_key=VT_API_KEY, file_path=file_path, message=message, wait=True)


client.run(os.getenv("TOKEN"))