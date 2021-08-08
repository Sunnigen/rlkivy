from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item


player = Actor(
    char="@",
    color=(1.0, 1.0, 1.0),
    minimap_color=(255, 255, 255),
    name="Player",
    name2="player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)

orc = Actor(
    char="o",
    color=(1.0, 1.0, 1.0),
    minimap_color=(63, 127, 63),
    name="Orc",
    name2="orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
troll = Actor(
    char="T",
    color=(1.0, 1.0, 1.0),
    minimap_color=(0, 127, 0),
    name="Troll",
    name2="troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)
confusion_scroll = Item(
    char="~",
    color=(1.0, 1.0, 1.0),
    minimap_color=(207, 63, 255),
    name="Confusion Scroll",
    name2="confusion_scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
    char="~",
    color=(1.0, 1.0, 1.0),
    minimap_color=(255, 0, 0),
    name="Fireball Scroll",
    name2="fireball_scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=(1.0, 1.0, 1.0),
    minimap_color=(127, 0, 255),
    name="Health Potion",
    name2="health_potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(1.0, 1.0, 1.0),
    minimap_color=(255, 255, 0),
    name="Lightning Scroll",
    name2="lightning_scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

dagger = Item(
    char="/",
    color=(1.0, 1.0, 1.0),
    minimap_color=(0, 191, 255),
    name="Dagger",
    name2="dagger",
    equippable=equippable.Dagger()
)

sword = Item(
    char="/",
    color=(1.0, 1.0, 1.0),
    minimap_color=(0, 191, 255),
    name="Sword",
    name2="sword",
    equippable=equippable.Sword(),
)

leather_armor = Item(
    char="[",
    color=(1.0, 1.0, 1.0),
    minimap_color=(139, 69, 19),
    name="Leather Armor",
    name2="leather_armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[",
    color=(1.0, 1.0, 1.0),
    minimap_color=(139, 69, 19),
    name="Chain Mail",
    name2="chain_mail",
    equippable=equippable.ChainMail()
)
