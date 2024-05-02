# Notes

## Klassen

- Area
- Person
  - Player
  - Enemy
- Item
  - Weapon
  - Key (planned)
- Inventory
  - Container (planned)
- Gateway
- Currency (planned)

## Spieler Verben

Aktionen über die der Spieler mit der Welt interagieren kann. Diese Aktionen können passiv sein und dem Spieler nur Informationen liefern oder aktiv und ihn oder seine Umgebung beeinflussen.

- Schaue (look_at)
- Benutze (equip)
- Nimm (pick up)
- Gehe zu (go_to)

## Ideen

- Rucksack Item welches die Inventarkapazität eines Spielers erhöhen kann
- Attribut "can_be_picked_up" welches bestimmt ob ein Item vom Spieler aufgehoben werden kann
- Effekt Items: Items können den Spieler beinflussen, wenn Sie aufgeboben (pick_up), ausgerüstet (equip) oder benutzt werden (use)

### Container Klasse

Ein Container ist ein Objekt in der Welt mit einem Inventar aus dem der Spieler Gegenstände entnehmen kann wie z.B. eine Truhe.

### Key Klasse

Schlüssel Objekte können mit verschiedenen anderen Objekten interagieren. So kann ein Schlüssel eine Truhe (Container) oder eine Türe (Gateway) öffnen.

### Currency Klasse

Um Handel zu ermöglichen soll der Wert von Gegenständen durch eine Währung dargestellt werden. Eine Person kann einen bestimmten Betrag dieser Währung bei sich tragen.
