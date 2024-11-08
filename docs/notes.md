# Fantasy Forge (working title)

Ziel ist es eine API zu entwickeln, die in der Lage ist Text Adventure oder interactive fiction Spiele zu erstellen. Das ganze soll data driven sein, es soll sehr niederschwellig möglich eigene Spiele zu entwickeln.

## Spieler Verben

Aktionen über die der Spieler mit der Welt interagieren kann. Diese Aktionen können passiv sein und dem Spieler nur Informationen liefern oder aktiv und ihn oder seine Umgebung beeinflussen.

- Schaue (look_at)
- Benutze (equip)
- Nimm (pick up)
- Gehe zu (go_to)

## Ideen

- Rucksack Item welches die Inventarkapazität eines Spielers erhöhen kann
- Effekt Items: Items können den Spieler beinflussen, wenn Sie aufgeboben (pick_up), ausgerüstet (equip) oder benutzt werden (use)
- Player Attribute (S.P.E.C.I.A.L)
- Chaosdorf als Setting
- Deadline für Motivation
- Zufällige Items
  - Roguelike
  - zufällige Loot-Drops
- Enemies können angreifen beim Betreten des Raums
- Waffen für Enemies
- Levelkurve
- Dialogoptionen
- "untouchable" Attribut für die Character Klasse, damit bestimmte Charactere nicht angegriffen werden können
- on_death Methode für Character Klasse
- Versteckte Items/Entitys, die nicht beim look around erscheinen (Attribut "visible")
- Versteckte Gateways, z.B. trapdoors
- grauer, weißer und schwarzer Hut in der Garderobe
- Betreten des Hackspace braucht Katzenohren

### Key Klasse

Schlüssel Objekte können mit verschiedenen anderen Objekten interagieren. So kann ein Schlüssel eine Truhe (Container) oder eine Türe (Gateway) öffnen.

### Currency Klasse

Um Handel zu ermöglichen soll der Wert von Gegenständen durch eine Währung dargestellt werden. Eine Person kann einen bestimmten Betrag dieser Währung bei sich tragen.

## Aufbau

Derzeitiges Vorhaben:

- ein Repo mit Framework das man per bspw `pipx` installieren und dann spielen kann, batteries included
- das Repo enthält auch Devtools:
  - Downloader: Welten werden als Repos nachgeladen, unabhängig von GitHub, eine Beispielwelt wird implizit bei der Initialisierung geladen
  - einen Wizard: neue Welten können "from scratch" erstellt werden, ähnlich wie `uv init` oder `pdm init`
- dann brauchen wir eine Versionierung um Kompatibilität zu prüfen
- syntaktische/semantische Prüfungen wären sinnvoll (sind alle benötigten Keys beim Import da, sind die Werte sinnvoll, …)

## Lootmatching

- bspw haben Waffen einen Schadenswert. Schwierige Level enthalten schwierige Gegner die mit "guten" Waffen einfacher besiegt werden können
- Lootdropping soll auch ein wenig zufällig sein, aber tendenziell von Gegnern/Leveln abhängen (und sich auch bspw nicht zu häufig wiederholen)
- sinnvoller, als ausschließlich bei den Gegnern ein feststehendes, mögliches Set an Waffen zu definieren, oder bei den Waffen ein Set an Gegnern, wäre es Lootmatching zu machen
- dann bräuchte man einen `LootMatcher` der eine Welt nimmt, eine generelle Config, einen Gegner bzw. ein Subjekt und eine Matching-Config wie man das zuordnen möchte, also Wahrscheinlichkeiten, und am Ende hat das Subjekt eine Liste an Items; man kann aber auch über die Wahrscheinlichkeit 0 bzw 1 angeben, dass etwas nicht vorkommt oder vorkommen muss und so explizit auswählen

## from Objects to Quests to a Story

So we have rooms and enemies and things in rooms. So we could start by adding some objects that "do more" than having a description. And doors that can only be opened with certain keys … and then have puzzle games, right? Also quests/tasks/puzzles would help to create a better file/level structure.

Completely fictional ideas for quests:

- lice at Chaosdorf, collect them all to contain the outbreak
- talk with our landlord about DMX and collect DMX controller and DMX lights
- there is a mouse at Chaosdorf and you have to remove all openly stored food, catch the mouse to release it outside (being outside gives endless possibilities)
- and somehow quests should follow a story that we can implement … it doesn't have to be long, but it should be somewhat entertaining
