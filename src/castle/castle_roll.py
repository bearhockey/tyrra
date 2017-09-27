import random


def roll_dice(dice_number):
    dice = []
    for _ in range(0, dice_number):
        dice.append(random.randint(0, 9))
    return dice


def roll_hit(dexterity=1, accuracy=1, bonus=0, dodge=1):
    dice = roll_dice(dexterity + accuracy + bonus)
    hits = count_success(dice)
    botch = is_botched(dice)
    return (hits - dodge), botch


def roll_damage(attack=3, hit_dice=0, bonus=0, soak=0, minimum=1):
    pool = attack + hit_dice + bonus - soak
    if pool <= minimum:
        pool = minimum
    dice = roll_dice(pool)
    damage = count_success(dice, allow_crit=False)
    if damage < 1:
        return 1
    else:
        return damage


def count_success(dice, allow_crit=True):
    success = 0
    for d in dice:
        if d > 6:
            success += 1
        elif d == 0:
            if allow_crit:
                success += 2
            else:
                success += 1
    return success


def count_botch(dice):
    botch = 0
    for d in dice:
        if d == 1:
            botch += 1
    return botch


def is_botched(dice):
    botch_count = count_botch(dice)
    if botch_count > count_success(dice):
        return botch_count
    else:
        return 0


