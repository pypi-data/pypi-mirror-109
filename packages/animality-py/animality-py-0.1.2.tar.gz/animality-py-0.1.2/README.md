# animality-py
Python Wrapper for https://animality.xyz<br>
Discord Server: https://discord.gg/ESPMP7BEeJ<br>
Made for burber. (Hamburger#0001)<br>
## Installation
```bash
$ pip install animality-py
```

## Simple Usage
```py
import animality
from asyncio import get_event_loop

async def run():
    animal = await animality.get("dog")
    print(animal.name, animal.image, animal.fact)
    random = await animality.random()
    print(random.name, random.image, random.fact)

get_event_loop().run_until_complete(run())
```

## Using a session
```py
from animality import AnimalityClient
from asyncio import get_event_loop

async def run():
    animality = AnimalityClient()
    animal = await animality.get("dog")
    print(animal.name, animal.image, animal.fact)
    random = await animality.random()
    print(random.name, random.image, random.fact)

get_event_loop().run_until_complete(run())
```

## Using the CLI
Get an animal.
```bash
$ animality.py cat
```

Get a random animal.
```bash
$ animality.py random
```

Get multiple animals. (up to 15)
```bash
$ animality.py cat dog panda bunny
```