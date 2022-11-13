import discord 
import os
import requests
import json 
from googletrans import Translator
import random
from replit import db
from keep_alive import keep_alive

translator = Translator()

DELETE = 0
print("$$$")

sad_words = ['trist', 'deprimat', 'fără speranță', 'nefericit', 'lipsit de voință', 'nicio speranță', 'nervos', 'deprimant']

starter_encouragements = [
  "Viața e frumoasă",
  "Totul o să fie bine",
  "Ești o persoană minunată / bot"
  
]

client = discord.Client()

if "responding" not in db.keys():
  db["responding"] = True

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


@client.event

async def on_ready():
  print('Ne-am conectat ca {0.user}'.format(client))

@client.event

async def on_message(message):
  global DELETE
  if message.author == client.user:
    return 

  msg = message.content
  
  if msg.startswith('$hello'):
    await message.channel.send('Hello')

  if msg.startswith('$citat'):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    translator = Translator()
    out = translator.translate(json_data[0]['q'], dest='ro')
    quote = out.text + " -" + json_data[0]['a']
    await message.channel.send(quote)

  
  if db["responding"]:
    options = starter_encouragements

    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
  
  if msg.startswith("$nou"):
    encouraging_message = msg.split("$nou", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("Nou mesaj motivational adaugat.")

  if msg.startswith("$del"):
    encouragements = []
    global DELETE
    if "encouragements" in db.keys():
      global index
      index = int(msg.split("$del",1)[1])
      words = db["encouragements"]
      await message.channel.send(f"Vrei să ștergi mesajul {words[index]}? D/N")
      DELETE = 2
        
  if msg.startswith("D") and DELETE == 2:
    delete_encouragement(index)
    encouragements = db["encouragements"]
    await message.channel.send(encouragements)
    DELETE = 0

  if msg.startswith("N") and DELETE == 2:
    await message.channel.send("Sarcina abandonata")
    DELETE = 0
  
  if DELETE == 2 and msg.startswith("$del") == False:
    await message.channel.send("Mesajul nerecunoscut. Trimite din nou.")

  if msg.startswith("$list") and DELETE!=2:
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$responding"):
    value = msg.split("$responding",1)[1]

    if value.lower():
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN'))
