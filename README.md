---
title: WhartonHackaithon
emoji: 📊
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 4.25.0
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# MoodShaker

For this homework assignment, we have implemented a AI GM of the Mausritter game

You can download a PDF of the game from [here](https://losing-games.itch.io/mausritter)


## Environment Setup

First, get the the homework repo, then create a virtual environment, and then install
the dependencies.

```
$ mkdir hw4
$ cd hw4
$ python3.10 -m venv venv
$ source venv/bin/activate
(venv) $ pip install jupyter 'kani[openai]' d20
```

If you’re using VS code then you can send your OPENAI_API_KEY to it when you launch it from the command line:

```
$ cd path/to/hw4
$ source venv/bin/activate
(venv) $ HELICONE_API_KEY=sk-helicone-XXXXXXX-XXXXXX code .
```

You should replace `sk-helicone-XXXXXXX-XXXXXX` with your Helicone key.

## Part 1

This is a simple dice rolling function test and using Kani to make the AI understand our prompts and instructions.

For example, our prompt is:

```
    Roll the dice provided by the model and return the result to it.

    Args:
        dice (str): The dice to roll, in RPG notation, e.g. 'd20', '1d8', '3d6', '4d6kh3', or '2d20kl1'
        - `d20` means: Roll a single 20-sided die
        - `1d8` means: Roll a single 8-sided die
        - `3d6` means: Roll three 6-sided dice, add them together
        - `4d6kh3` means: Roll four six-sided dice, add the highest three together
        - `2d20kl1` means: Roll two d20s, keep the lower ("disadvantage" in D&D, "advantage" in Mausritter)

    Returns:
        str: The result of the dice roll
```

## Part 2 Character Creation

We are able to use Kani AI to create a character by letting it rolling a dice to decide on the important features. 
We used the LLM created description from before to make a portrait of the mouse. 
This worked quite nicely overall and generated a portrait of a moues that matched the description very well.
We found it interesting how it generated the description text (or at least attempted to do so) as part of the portrait.
This isn't optimal, and it probably would have been best to be generated without that. However, it did generate the Title & Subtitle
quite nicely. It feels like this could have been found in a TTRPG game. 

Here is a description of the character: 

```
Milo Thistle, the generous yet wrathful blacksmith, is known for his strength and dexterity, despite his unimposing physical size. His fur, a tan color with patchy spots, is as frizzy as an autumn leaf. As a Blacksmith, he has a meticulous eye for detail, crafting the finest weapons and armor in the village. Born under the storm sign, his generous nature is occasionally superseded by his unpredictable wrath, causing Milo to forge weapons that can be stunningly beautiful and terrifying at the same time.'
```
And its image ![character](dalle/Imagine_a_tan-colored_mouse_named_Milo_Thistle_who_works_as_a_village_blacksmith_Despite_his_unimpos.png)

## Part 3 

We implemented a `roll_save` function to let the AI GM roll a dice when the character is facing some challenges, and need to make a save against either 'strength', 'dexterity' or 'will'.

### Structured vs Structureless GM Prompt 

We tested with structured and structureless GM prompts. 

The structure one:
```
Introduce the world to the players and challenges in it, then introduce the mouse character to the player with its description: 
{my_mouse.description}.
Tell the player the strength, dexterity, will, hp, pips, background, birthsign, disposition, coat, and physical detail of the mouse.
When the game start, set some traps for the mouse. If the mouse is doing something risky where the outcome is uncertain and failure has conequences, ask the player to make a save against either strength, dexterity or will by calling the 'roll_save' function. You should choose what is the trait_value that the user should against, and if the save is at disadvantage or not.
```

And the structureless one:
```
Introduce the world to the players and challenges in it, then introduce the mouse character to the player with its description: {my_mouse.description}.
Describe challenges to the player and ask them to make saves against strength, dexterity, or will as needed.

```

The structureless GM was able to create a narration of the character and describe the world and challenges to the player. However, it couldn't roll dice for the player. I have to ask it explicitly to roll saves and provide outcomes based on the player's actions. This made the game less efficient.The structured GM, on the other hand, was able to roll saves and provide outcomes based on the player's actions by calling the "roll_save" function. This allowed for a more interactive and engaging experience. Also, the structured GM was able to provide more detailed description of each traits of the character, and specific responses to the player's actions. Thus, the structured GM was more effective at running the game, while the structureless GM was suited for simple storytelling and world-building. 

## Extension

For the extension we implemented the ability for Kani/ChatGPT to call the generate_image function to visualzie the scene the player is in currently. We have an example of it in IMAGE_GAMEPLAY.md. Overall, it works smoothly, but we had some minor issues at first. We could not tell ChatGPT that the function generated images outright, otherwise it would get confused and say "Sorry but I cannot generate images." It is also very inconsistent, but that is expected with the state of DALL E right now.



