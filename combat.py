"""
Модуль боя для обработки сражений между сущностями.
"""
import random


def process_combat(attacker, defender):
    """
    Обработка боя между двумя сущностями.
    
    Args:
        attacker (Entity): Атакующая сущность
        defender (Entity): Защищающаяся сущность
        
    Returns:
        dict: Словарь, содержащий результаты боя
    """
    messages = []
    
    # Расчет урона
    base_damage = attacker.dmg
    
    # Добавить случайности к урону (±20%)
    damage_variation = random.uniform(0.8, 1.2)
    raw_damage = int(base_damage * damage_variation)
    
    # Применить уменьшение брони (каждая единица брони уменьшает урон на 10%, максимум 80%)
    armor_reduction = min(0.8, defender.arm * 0.1)
    final_damage = max(1, int(raw_damage * (1 - armor_reduction)))
    
    # Нанести урон защищающемуся
    defender.hp -= final_damage
    
    # Создать сообщения боя
    messages.append(f"{attacker.name} атакует {defender.name} и наносит {final_damage} урона!")
    
    if defender.arm > 0:
        messages.append(f"Броня {defender.name} поглотила {raw_damage - final_damage} урона.")
    
    messages.append(f"У {defender.name} осталось {max(0, defender.hp)}/{defender.max_hp} ОЗ.")
    
    # Особые эффекты в зависимости от типа персонажа
    if hasattr(attacker, 'char_class') and (attacker.char_class.lower() == "маг" or attacker.char_class.lower() == "mage") and attacker.sp >= 5:
        # У мага есть шанс сотворить заклинание, если у него достаточно очков заклинаний
        if random.random() < 0.3:  # 30% шанс сотворить заклинание
            spell_damage = random.randint(3, 8)
            defender.hp -= spell_damage
            attacker.sp -= 5
            messages.append(f"{attacker.name} творит магическую стрелу на {spell_damage} дополнительного урона!")
            messages.append(f"У {defender.name} осталось {max(0, defender.hp)}/{defender.max_hp} ОЗ.")
    
    if hasattr(attacker, 'char_class') and (attacker.char_class.lower() == "разбойник" or attacker.char_class.lower() == "rogue"):
        # У разбойника есть шанс на критический удар
        if random.random() < 0.2:  # 20% шанс на критический удар
            crit_damage = random.randint(2, 5)
            defender.hp -= crit_damage
            messages.append(f"{attacker.name} наносит критический удар на {crit_damage} дополнительного урона!")
            messages.append(f"У {defender.name} осталось {max(0, defender.hp)}/{defender.max_hp} ОЗ.")
    
    # Return combat results
    return {
        "attacker": attacker.name,
        "defender": defender.name,
        "damage": final_damage,
        "messages": messages,
        "defender_hp_remaining": max(0, defender.hp)
    }
