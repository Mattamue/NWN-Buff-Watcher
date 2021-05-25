"""
Author: Mattamue
Last updated: 05/24/2021
Program: summon_cd.py

Take loglines from the main loop and create a generic
summon cooldown. Just use the one icon for all of them
and pass the name.

Using basically the same logic as abilities_call but
just for this different flavor of cooldown that's the
same across all cooldown summon abilities.

"""
import time

def summons_cd_call(logline):
    logline_split = logline.split(" ")
    # print(logline.strip()) # testing
    # print(logline_split) # testing

    try:
        min_match = "minute(s)"
        min_result = [v for v in logline_split if v.startswith(min_match)]
        minutes = int(logline_split[logline_split.index(min_result[0]) - 1])
    except:
        minutes = 0

    try:
        sec_match = "second(s)"
        sec_result = [v for v in logline_split if v.startswith(sec_match)]
        seconds = int(logline_split[logline_split.index(sec_result[0]) - 1])
    except:
        seconds = 0

    try:
        ability = ""
        # hacky, but starting at range 7 bypasses the "chat window text"... might not work on all log setups...
        for x in range(7, logline_split.index("will")):
            ability = ability + logline_split[x] + " "

    except:
        ability = "Ability error"

    return [ability[:-1], time.time() + ((minutes * 60) + seconds), "NWN-Buff-Watcher/graphics/summon_cd.png"]

if __name__ == "__main__":
    test = summons_cd_call("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Tribal Call will be available once more in 6 minute(s).\n")
    print(test)

    test2 = summons_cd_call("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Create Undead will be available once more in 6 minute(s).\n")
    print(test2)

    test3 = summons_cd_call("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Summon Fiend will be available once more in 6 minute(s).\n")
    print(test3)

    test4 = summons_cd_call("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Animal Companion will be available once more in 10 minute(s).\n")
    print(test4)

    test5 = summons_cd_call("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Summon Shadow will be available once more in 3 minute(s).\n")
    print(test5)

    test6 = summons_cd_call("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Warlock Summon Creature I will be available once more in 12 second(s).\n")
    print(test6)

    test7 = summons_cd_call("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Summon Familiar will be available once more in 10 minute(s).\n")
    print(test7)