#!/usr/bin/env python3
from halo import Halo
from sys import argv, stdout, exit
from random import choice
from asyncio import get_event_loop
from .main import *

args = argv[1:]
if not args or "about" in args:
    stdout.write(f"""animality version {version}

website: https://animality.xyz
discord: https://discord.gg/ESPMP7BEeJ
github: https://github.com/animal-api/animality-py
supported animals: {len(animals)}

API made by Hamburger#0001.
CLI made by null#8626.

run "animality help" to see the usage.
""")
    exit(0)

elif "help" in args:
    a = '\n  '.join(animals)
    stdout.write(f"""usage:
  fetching data from the API:
    animality [animal]
    animality [animal1] [animal2] [animal3] ...
    animality random

  others:
    animality help
    animality about

list of supported animals:
  {a}
""")
    exit(0)

halo = Halo(spinner="line", text="requesting...", color="white").start()

async def fetch(animal: str) -> None:
    global halo
    halo.text = f"requesting '{animal}'..."
    
    return_type = 0
    try:
        response = await get(animal)
        halo.succeed(f"success.\nanimal: {animal}\nfact: {response.fact}\nimage: {response.image}")
    except Exception as e:
        halo.fail(f"error: {e}")
        return_type = 1
    exit(return_type)

async def fetch_multiple(args: list) -> None:
    global halo
    animality = AnimalityClient()
    data = ""

    for arg in args:
        halo.text = f"requesting '{arg}' ({data.count('l: ') + 1}/{len(args)})..."
        response = await animality.get(arg)
        data += f"animal: {arg}\nfact: {response.fact}\nimage: {response.image}\n\n"

    await animality.close()
    halo.succeed(f"success.\n{data[:-1]}")
    exit(0)

if "random" in args:
    get_event_loop().run_until_complete(fetch(choice(animals)))
elif len(args) == 1:
    get_event_loop().run_until_complete(fetch(args[0]))

if len(args) > 15:
    halo.fail("error: you can only input up to 15 animals at a time.")
    exit(1)

for animal in args:
    if animal not in animals:
        halo.fail(f"error: the animal: '{animal}' is not supported yet.")
        exit(1)

get_event_loop().run_until_complete(fetch_multiple(args))