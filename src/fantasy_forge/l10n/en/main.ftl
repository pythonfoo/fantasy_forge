character-name-prompt = Current character name is { $default_name }. Would you like to change it? (Press enter to keep)
character-name-change-successful = Successfully changed name to { $chosen_name }! Your hormones should arrive soon...
player-description = the heroic player
bare-hands-name = bare hands
bare-hands-description = the harmful hands of the player
look-at-message = You look at { INTER($object) }.
entity-not-seen = There is no { $entity }.
look-around-begin = You take a look around the { $area-name }. It is { $area-description }. You see:
look-around-single = * { INTER($object) }
pick-up-item-menu = Please select your option:
pick-up-item-message = You picked up { INTER($item) } and put it in your inventory.
entity-does-not-exist = { $entity } does not exist.
item-vanished = The item has vanished before your eyes.
item-is-in-inventory = You already picked up this item.
pick-up-failed-message = You can't pick up this item.
pick-up-failed-inv-full = You can't pick up this item right now, your inventory is full.
go-failed-message = You can't go there.
equip-item-message = You equipped { INTER($item) }.
unequip-item-message = You took of { INTER($item)} and took it in your inventory.
cannot-equip = You can't equip { INTER($weapon) }.
attack-character-message = { INTER($source) } attacks { INTER($target) }{ EXISTS($weapon) ->
    [true] { "" } with { $weapon }
    *[false] { "" }
}.
attack-character-alive-message = { INTER($target) } remains at { NUM($health) } health points.
attack-character-dead-message = { INTER($target) } vanished.
attack-drop-begin = { INTER($target) } dropped { NUM($loot_count) } items:
attack-drop-single = { INTER($item) }
player-health-remaining = You have { NUM($health) } health remaining.
player-died = You died.
cannot-attack = Cannot attack { INTER($target) }.
cannot-use-message = You can't use { EXISTS($other) ->
    [true] { INTER($other) } with{ " " }
    *[false] { "" }
}{ INTER($self) }.
armour-detail = {$type}: {EXISTS($item) ->
    [true] {$item-name} ({NUM($item-defense)} defense)
    *[false] Nothing
}.
drop-not-found = You can't drop { $item }.
dropped = You dropped { INTER($item) }.
enter-area-message = You are now in { $area }. You see:
inventory-look-message = In the inventory you find { $items }.
inventory-look-empty-message = Your inventory is empty.
inventory-capacity-message = Maximum capacity ({ NUM($capacity) }) reached.
inventory-item-not-found-message = Item { $item } couldn't be found.
gateway-unlock-message = { INTER($name) } unlocked.
gateway-lock-message = { INTER($name) } is now locked.
gateway-locked-message = You can't use { INTER($gateway) } because it is locked.
gateway-key-needed = You need a key to open { INTER($name) }.
gateway-no-keys = You can't use { INTER($name) } like that.
gateway-on-look-locked = It is locked.

void-name = the void
void-description = a place filled with nothingness
shell-invalid-command = This is not a valid command.
shell-invalid-command-suggest = This is not a valid command. Did you mean { $closest_cmd }?
quit-game-message-light = There is some light on the horizon, the first dancing rays of the sun.
quit-game-message-dark = There is only pure nothingness that stares into your soul.
quit-game-message-turtles = You look around, it's turtles, all the way down.
quit-game-message-fractals = You trip over a geometric pattern containing itself, containing itself, containing itself, …
quit-game-message-treasure = You realize that the real treasure are the friendships you formed on your journey.
quit-game-message-cat = You spectate a cute cat meowing at you. meow :3
quit-game-message-dog = You pet a good doggo who wants to play fetch. wruff :3
quit-game-message-dream = You realize that you are in your bed and, how lame, it was all a dream.
unknown-language-error = Unknown language "{ $language }"
