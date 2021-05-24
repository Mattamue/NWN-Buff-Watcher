"""
Author: Mattamue
Last updated: 05/20/2021
Program: abilities_call.py

Take loglines from the main loop and either

1) pick out the loglines within the main loop... will make that function even bigger
2) pass the whole logline to this function and then handle here and return a 
    string that make_buff_labelframe can use?
3) use the minutes and seconds data in the cooldown text to make a buff

Going with #3


"""


def abilities_trigger(logline):
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
        for x in range(7, logline_split.index("has")):
            ability = ability + logline_split[x] + " "

    except:
        ability = "Ability error"

    return [ability[:-1], (minutes * 60) + seconds]


if __name__ == "__main__":
    test = abilities_trigger("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Inspire Courage has a timer of 1 minute(s) and 30 second(s). You may not use Inspire Courage again for this period of time.\n")
    print(test)

    test2 = abilities_trigger("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Iron Horn has a timer of 12 second(s). You may not use Iron Horn again for this period of time.\n")
    print(test2)

    test3 = abilities_trigger("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Last Stand has a timer of 3 minute(s). You may not use Last Stand again for this period of time.\n")
    print(test3)

    test4 = abilities_trigger("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Timestop has a timer of 240.0 seconds. You may not use Timestop again for this period of time. Attempting to do so will spend the spell while producing no effect.\n")
    print(test4)

    test5 = abilities_trigger("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Warlock Summon Shadows has a timer of 3 minute(s). You may not use Warlock Summon Shadows again for this period of time.\n")
    print(test5)

    test6 = abilities_trigger("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Yoink has a timer of 1 minute(s). You may not use Yoink again for this period of time.\n")
    print(test6)

    test7 = abilities_trigger("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Barbarian Rage has a timer of 2 minute(s) and 48 second(s). You may not use Barbarian Rage again for this period of time.\n")
    print(test7)

    test8 = abilities_trigger("[CHAT WINDOW TEXT] [Sun May 23 15:53:07] Warlock Summon Shadows has a timer of 3 minute(s). You may not use Warlock Summon Shadows again for this period of time.\n")
    print(f"test 8: {test8}")