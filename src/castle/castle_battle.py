import src.castle.castle_roll as roll


def get_soak(self):
    # should return stamina plus armor but
    return 1


def take_damage(self, damage):
    self.current_hp -= damage


def melee_attack(attacker, defender, bonus=0):
    # print("\n{0} melee attacking {1}".format(attacker.name, defender.name))
    result, botch = roll.roll_hit(dexterity=attacker.stats["DEX"],
                                  accuracy=attacker.get_accuracy(),
                                  bonus=bonus,
                                  dodge=defender.stats["DEX"])
    if botch:
        # self.take_damage(botch)
        # player should take damage maybe?
        return 0
    elif result < 1:
        # MISSED
        return 0
    damage = roll.roll_damage(attack=attacker.stats["STR"],
                              hit_dice=result,
                              soak=defender.get_soak(),
                              minimum=1)
    # opponent.take_damage(damage)
    return damage
