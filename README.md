# NWN-Buff-Watcher
Watches chat log output from the 2002 game Neverwinter Nights and creates a topmost window to watch spell and cooldown durations

![NWN Buff Watcher](https://i.imgur.com/JDOha8n.png)

Updates:
v1.1 time update, a few features, and bugfixes.

    feature: update for Arelith time change enhancement #66
    bugfix: domain spells added #64
    bugfix: added Divine Power #63
    bugfix: regenerate corrected to turns per level #62
    bugfix: chatlog days single digit ability error fixed #60
    bugfix: opening locks (or any skill check) causes dispel window bug fixed #57
    feature: intimidate added as a trigger #56
    feature: taunt added as a trigger #55
    bugfix: One With The Land corrected to One with the Land #54
    bugfix: wand of freedom corrected to Wand of Freedom of Movement #53

Features:

    Durations of buffs from potions, scrolls, and wands based on in-game item level
    Tracking durations and spells from items like Dust of Disappearance; I’m sure this list could be expanded if anyone wants to share more items, but I’ve captured most everything crafting and the few module items I’m aware of
    Enter character information for more accurate durations from modifiers
    Loremaster levels calculate increased durations for wands and scrolls
    Spell Focus feats are calculated for things like Invisibility, True Seeing, and Aura of Vitality
    Caster levels and extend meta-magic for casted buffs
    Specialist wizard signature spell cooldowns and unique durations for Illusion and Divination
    Class ability cooldowns are tracked and thankfully, because Arelith outputs are sane and similar, cooldowns for complex things like Blinding Speed are accurate
    Enter charisma modifier and Divine Champion levels for accurate Wrath, Might, and Shield durations
    Tracking of staggered Bard Song, Turn Undead, and Smite cooldowns (with the caveat that the cooldowns themselves in-game are not exactly 10 minutes, so these will drift)
    Tracking innate ability cooldowns and duration of abilities like Duergar Invisibility; this is the first example of the limitations of the Watcher as it can only collect the “uses Innate Ability” from the chatlog and cannot know what ability the player is using, but this is solved by allowing the user to select the ability they wish to track from the buff window itself with a drop-down menu
    Tracking Knockdown duration on a single target, subject to the same limitations of the chatlog
    Handling player-made potions (and hence a longer duration) with a toggle on the character window depending on what type of potions you use
    Tracks durations of summons and tracks durations of cooldowns for those classes that have refreshed summon casting
    Spell cooldowns like Clarity, Time Stop, and Greater Restoration are captured
    Edge cases for things like Improved Invisibility actually being two spells in Arelith and how the Invisibility duration can be adjusted in like three different ways, are handled
    User can destroy a buff that was removed in some way that’s not capturable, for example if a summon is killed or unsummoned
    Rest button to quickly clear all buffs and cooldowns, except for the Scry and godsave cooldowns
    When dispelled and breached, removed spells are removed from the Watcher and displayed in another pop-up
    Damage shields not stacking
    Ability to add your own custom triggers. Requires JSON editing. Player-made items are sometimes branded and change in the chatlog. That means they’ll be missed by the normal triggers looking for “Bull’s Strength” if the potion is renamed to “Maggie’s Magical Strong Juice”. Today, it would be possible for you to simply add another entry to the JSON -- trust me it isn’t hard -- but in the future I have it on my todo list to make it possible to add these custom items from the Watcher.
    
Setting up the Watcher:

Get the Watcher (or the source code) from https://github.com/Mattamue/NWN-Buff-Watcher
Unzip the exe and its JSON and graphics sub-folders anywhere
Have your chat logging turned on
![chat logging options](https://i.imgur.com/C1m5g34.png)
    Setup the watcher and open the "nwclientLog1" (the location of the log for you is probably in the same directory as mine in this screen shot): 
![settings, open chat log](https://i.imgur.com/ZoWMOjn.png)

FAQ/Other:
I'm sure I will expand the with edits as questions come up. Please let me know of any bugs or issues. I'm open to the idea of people helping with the code if you want to add a feature or fix a bug. That can all be handled on the GitHub. Python is a pretty easy language to learn. I know because I've learned it these past few months and I've added lots of comments to the source code about how it works.

How do I extend spells?
You've keyed in into a limitation of using the chatlog. There's not way to tell from "User casts Bull's Strength" it it's maximized, extended, empowered, still, or silent. To address this, click on the buff in the Watcher and choose if its extended:

![extend](https://i.imgur.com/XW5u0Re.png)

So after you cast an extended spell you have to go into the Watcher and set if its extended. If you mis-click you can un-check or re-check as needed. The Watcher will remember the duration either way.
