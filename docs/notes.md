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
