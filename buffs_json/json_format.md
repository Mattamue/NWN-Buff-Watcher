# Json format

Sample entries in a list:
````json
    },
    "uses Wand of Blood Frenzy": {
        "name": "Blood Frenzy",
        "duration": "6",
        "caster_level": "7",
        "icon": "graphics/blood_frenzy.png"
    },
    "uses Wand of Bull's Strength": {
        "name": "Bull's Strength",
        "duration": "360",
        "caster_level": "15",
        "icon": "graphics/bulls.png"
    },
    "uses Wand of Camouflage": {
        "name": "Camouflage",
        "duration": "600",
        "caster_level": "5",
        "icon": "graphics/camouflage.png"
    },
````

Single entry:
````json
    "uses Wand of Blood Frenzy": {
        "name": "Blood Frenzy",
        "duration": "6",
        "caster_level": "7",
        "icon": "graphics/blood_frenzy.png"
    }
````

Each entry starts with a "capture something from the chatlog" and then a section that breaks down what that buff does in the {} brackets, then finally a comma after the bracket and the pattern starts again until the last entry which doesn't get a comma.

## Name

Name is a unique name that's used to overrwrite duplicates and for a few characters to be displayed over the buff.

## Duration

Duration is the "1hr / level" or "1 turn / level" langauge of the game extrapolated into seconds.

    A duration of 1 hour per level is really 360 seconds because, on Arelith, an hour in game is six minutes, which is 360 seconds. Then you can take that times the caster level of the item to get the duration. There is some tricky stuff handled in other areas, like the Loremaster's ability to change the caster level of scrolls. Other one-offs like clarity getting a base 5 rounds is also handled elsewhere. This JSON info is for the straight basic details of the buff. Some buffs have things like 8640 seconds and 1 caster level, these are 24 hour buffs so they aren't multiplied by 1 at all, but keeping that in there allows the code to apply to all the buffs with as few edge cases as possible. Another edge case, Resistance is always 2 turns, no matter what level its cast at, so it's always 120 seconds. 

## Icon

Icon is the .png that's used on the buff watcher. They're normal images from NWN unless its a cooldown, then it's shaded red.