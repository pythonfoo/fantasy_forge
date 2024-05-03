# Fantasy Forge (working title)

Ziel ist es eine API zu entwickeln, die in der Lage ist Text Adventure oder interactive fiction Spiele zu erstellen. Das ganze soll data driven sein, es soll sehr niederschwellig möglich eigene Spiele zu entwickeln.

## Klassen

### Entity

```python
class Entity():
  name: str
  description: str
```

### Area

```python
class Area(Entity):
  name: str  # inherited from Entity
  description: str  # inherited from Entity
  contents: list[Entity]
```

### Character

```python
class Character(Entity):
  name: str  # inherited from Entity
  description: str  # inherited from Entity
  health: int
  alive: bool
```

### Player

```python
class Player(Character):
  name: str  # inherited from Entity
  description: str  # inherited from Entity
  health: int # inherited from Character
  alive: bool # inherited from Character
  main_hand: Item
  inventory: Inventory
```

### Enemy

```python
class Enemy(Entity):
  name: str  # inherited from Entity
  description: str  # inherited from Entity
  health: int # inherited from Character
  alive: bool # inherited from Character
  weapon: Weapon
  loot: Inventory
```

### Item

```python
class Item(Entity):
  name: str  # inherited from Entity
  description: str  # inherited from Entity
  moveable: bool
  carryable: bool
```

### Weapon

```python
class Weapon(Item):
  name: str  # inherited from Entity
  description: str  # inherited from Entity
  moveable: bool  # inherited from Item
  carryable: bool  # inherited from Item
  damage: int
```

### Gateway

```python
class Gateway(Entity):
  name: str  # inherited from Entity
  description: str  # inherited from Entity
  source: area
  target: area
```

### Inventory

```python
class Inventory:
  capacity: int
  contents: list[Item]
```

### Container

```python
class Container(Entity, Inventory):
  name: str  # inherited from Entity
  description: str  # inherited from Entity
  capacity: int  # inherited from Inventory
  contents: list[Item]  # inherited from Inventory
```

- Key (planned)
- Currency (planned)

## Spieler Verben

Aktionen über die der Spieler mit der Welt interagieren kann. Diese Aktionen können passiv sein und dem Spieler nur Informationen liefern oder aktiv und ihn oder seine Umgebung beeinflussen.

- Schaue (look_at)
- Benutze (equip)
- Nimm (pick up)
- Gehe zu (go_to)

## Ideen

- Rucksack Item welches die Inventarkapazität eines Spielers erhöhen kann
- Effekt Items: Items können den Spieler beinflussen, wenn Sie aufgeboben (pick_up), ausgerüstet (equip) oder benutzt werden (use)
- Attribut: moveable: bool bestimmt ob ein Item bewegt werden kann
- Attribut: carryable: bool bestimmt ob ein Item von einem Spieler aufgenommen werden kann
- Player Attribute (S.P.E.C.I.A.L)
- Chaosdorf als Setting
- Deadline für Motivation
- Zufällige Items
  - Roguelike
- Levelkurve
- Dialogoptionen
- "untouchable" Attribut für die Character Klasse, damit bestimmte Charactere nicht angegriffen werden können
- on_death Methode für Character Klasse

### Container Klasse

Ein Container ist ein Objekt in der Welt mit einem Inventar aus dem der Spieler Gegenstände entnehmen kann wie z.B. eine Truhe.

### Key Klasse

Schlüssel Objekte können mit verschiedenen anderen Objekten interagieren. So kann ein Schlüssel eine Truhe (Container) oder eine Türe (Gateway) öffnen.

### Currency Klasse

Um Handel zu ermöglichen soll der Wert von Gegenständen durch eine Währung dargestellt werden. Eine Person kann einen bestimmten Betrag dieser Währung bei sich tragen.
