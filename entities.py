"""
Модуль сущностей, содержащий классы для игрока, врагов и других игровых объектов.
"""
import random


class Entity:
    """Базовый класс для всех игровых сущностей."""
    
    def __init__(self, name, x, y):
        """
        Инициализация сущности.
        
        Args:
            name (str): Имя сущности
            x (int): X-координата
            y (int): Y-координата
        """
        self.name = name
        self.x = x
        self.y = y
        self.char = '?'  # Символ для отображения по умолчанию
        self.max_hp = 10
        self.hp = self.max_hp
        self.max_sp = 10  # Очки заклинаний/выносливости
        self.sp = self.max_sp
        self.dmg = 1
        self.arm = 0  # Броня


class Player(Entity):
    """Класс игрока."""
    
    def __init__(self, name, char_class, x, y):
        """
        Инициализация персонажа игрока.
        
        Args:
            name (str): Имя игрока
            char_class (str): Класс персонажа (например, Воин, Маг, Разбойник)
            x (int): X-координата
            y (int): Y-координата
        """
        super().__init__(name, x, y)
        self.char = '@'
        self.char_class = char_class
        
        # Установка характеристик в зависимости от класса персонажа
        if char_class.lower() == "воин" or char_class.lower() == "warrior":
            self.max_hp = 30
            self.hp = self.max_hp
            self.max_sp = 10
            self.sp = self.max_sp
            self.dmg = 3
            self.arm = 2
        elif char_class.lower() == "маг" or char_class.lower() == "mage":
            self.max_hp = 15
            self.hp = self.max_hp
            self.max_sp = 30
            self.sp = self.max_sp
            self.dmg = 5
            self.arm = 0
        elif char_class.lower() == "разбойник" or char_class.lower() == "rogue":
            self.max_hp = 20
            self.hp = self.max_hp
            self.max_sp = 20
            self.sp = self.max_sp
            self.dmg = 4
            self.arm = 1
        else:  # Класс по умолчанию
            self.max_hp = 20
            self.hp = self.max_hp
            self.max_sp = 20
            self.sp = self.max_sp
            self.dmg = 2
            self.arm = 1


class Enemy(Entity):
    """Класс врага."""
    
    def __init__(self, enemy_type, x, y):
        """
        Инициализация врага.
        
        Args:
            enemy_type (str): Тип врага (например, Гоблин, Орк, Тролль)
            x (int): X-координата
            y (int): Y-координата
        """
        super().__init__(enemy_type, x, y)
        self.char = 'В'  # В - враг
        
        # Установка характеристик в зависимости от типа врага
        if enemy_type.lower() == "гоблин" or enemy_type.lower() == "goblin":
            self.max_hp = 10
            self.hp = self.max_hp
            self.max_sp = 5
            self.sp = self.max_sp
            self.dmg = 2
            self.arm = 0
        elif enemy_type.lower() == "орк" or enemy_type.lower() == "orc":
            self.max_hp = 20
            self.hp = self.max_hp
            self.max_sp = 10
            self.sp = self.max_sp
            self.dmg = 3
            self.arm = 1
        elif enemy_type.lower() == "тролль" or enemy_type.lower() == "troll":
            self.max_hp = 30
            self.hp = self.max_hp
            self.max_sp = 5
            self.sp = self.max_sp
            self.dmg = 4
            self.arm = 2
        elif enemy_type.lower() == "скелет" or enemy_type.lower() == "skeleton":
            self.max_hp = 15
            self.hp = self.max_hp
            self.max_sp = 0
            self.sp = self.max_sp
            self.dmg = 3
            self.arm = 1
        else:  # Враг по умолчанию
            self.max_hp = 15
            self.hp = self.max_hp
            self.max_sp = 10
            self.sp = self.max_sp
            self.dmg = 2
            self.arm = 1
            
        # Добавление случайности в характеристики врага
        self.max_hp += random.randint(-2, 2)
        self.hp = self.max_hp
        self.dmg += random.randint(-1, 1)
        if self.dmg < 1:
            self.dmg = 1
