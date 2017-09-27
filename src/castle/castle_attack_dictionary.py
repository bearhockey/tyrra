import random


def translate_damage(damage, enemy="the enemy"):
    text = "You do {0} damage to {1}".format(damage, enemy)
    if damage == 1:
        text = random.choice(["You graze {0} with your weapon, causing slight discomfort.".format(enemy),
                              "You injure {0} slighty, {0} is annoyed.".format(enemy),
                              "You stumble awkwardly into {0} weapon-first, causing some damage.".format(enemy)])
    elif damage == 2:
        text = random.choice(["You swing your weapon towards {0}'s chest, striking a solid blow.".format(enemy),
                              "You lunge at {0} and deliver pain!".format(enemy),
                              "You take your shot at {0} and land some decent damage".format(enemy)])
    elif damage == 3:
        text = random.choice(["You furiously attack {0} and deal some severe punishment.".format(enemy),
                              "Your rage overcomes you and {0} succumbs to an onslaught of blows.".format(enemy),
                              "{0} says, \"Ouch!\" as you plunge your weapon into their thigh.".format(enemy)])
    elif damage > 3:
        text = "Damn son, that's harsh."
    return text
