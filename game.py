"""
Игровой модуль, содержащий основной класс Game, который управляет состоянием игры.
"""
import os
import sys
import random
from time import sleep

from map_generator import generate_standard_map, generate_random_map
from entities import Player, Enemy
from ui import UI
from combat import process_combat


class Game:
    """
    Основной игровой класс, управляющий состоянием игры, включая игрока, врагов,
    карту и игровой цикл.
    """
    def __init__(self):
        """Инициализация игрового состояния."""
        self.running = False
        self.current_map = None
        self.map_width = 0
        self.map_height = 0
        self.player = None
        self.enemies = []
        self.turn = 0
        self.ui = UI()
        self.debug_mode = False
        self.message_log = []
        
    def start(self):
        """Начать новую игру."""
        self.running = True
        
        # Показать приветственный экран
        self.ui.show_welcome_screen()
        
        # Получить выбор карты от игрока
        map_choice = self.ui.get_map_choice()
        
        if map_choice == '1':
            # Стандартная карта
            self.current_map = generate_standard_map()
            self.map_width = len(self.current_map[0])
            self.map_height = len(self.current_map)
        else:
            # Случайная карта с размером, указанным игроком
            width = self.ui.get_map_size("width")
            height = self.ui.get_map_size("height")
            self.current_map = generate_random_map(width, height)
            self.map_width = width
            self.map_height = height
            
        # Создание игрока
        player_name = self.ui.get_player_name()
        player_class = self.ui.get_player_class()
        
        # Поиск подходящей начальной позиции для игрока
        player_x, player_y = self.find_valid_position()
        self.player = Player(player_name, player_class, player_x, player_y)
        
        # Добавление врагов на карту
        self.spawn_enemies(3 + random.randint(0, 2))  # 3-5 врагов
        
        # Добавление сообщений в лог
        self.message_log.append("Игра началась. Используйте WASD или стрелки для перемещения.")
        self.message_log.append(f"Игрок {player_name} создан как {player_class}.")
        
    def find_valid_position(self):
        """Найти подходящую (пустую) позицию на карте."""
        while True:
            x = random.randint(1, self.map_width - 2)
            y = random.randint(1, self.map_height - 2)
            if self.current_map[y][x] == ' ':
                return x, y
    
    def spawn_enemies(self, num_enemies):
        """Создать указанное количество врагов на случайных позициях на карте."""
        enemy_types = ["Гоблин", "Орк", "Тролль", "Скелет"]
        
        for _ in range(num_enemies):
            enemy_type = random.choice(enemy_types)
            enemy_x, enemy_y = self.find_valid_position()
            
            # Убедиться, что враг не создается слишком близко к игроку
            while abs(enemy_x - self.player.x) < 5 and abs(enemy_y - self.player.y) < 5:
                enemy_x, enemy_y = self.find_valid_position()
                
            # Создать врага с типом и случайными характеристиками
            enemy = Enemy(enemy_type, enemy_x, enemy_y)
            self.enemies.append(enemy)
            
    def process_input(self):
        """Обработка ввода игрока."""
        action = self.ui.get_player_action()
        
        # Направления движения
        if action == 'w':  # Вверх
            self.move_player(0, -1)
        elif action == 's':  # Вниз
            self.move_player(0, 1)
        elif action == 'a':  # Влево
            self.move_player(-1, 0)
        elif action == 'd':  # Вправо
            self.move_player(1, 0)
        elif action == 'q':  # Выход
            self.running = False
        elif action == 'debug':  # Переключение режима отладки
            self.debug_mode = not self.debug_mode
            self.message_log.append(f"Режим отладки {'включен' if self.debug_mode else 'выключен'}")
            
    def move_player(self, dx, dy):
        """
        Попытка переместить игрока в указанном направлении.
        
        Args:
            dx (int): Изменение x-координаты
            dy (int): Изменение y-координаты
        """
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Проверка, находится ли новая позиция в пределах карты
        if 0 <= new_x < self.map_width and 0 <= new_y < self.map_height:
            # Проверка столкновения со стеной
            if self.current_map[new_y][new_x] == '#':
                self.message_log.append("Вы не можете проходить сквозь стены!")
                return
            
            # Проверка столкновения с врагом
            enemy_at_pos = self.get_enemy_at_position(new_x, new_y)
            if enemy_at_pos:
                # Начать бой с врагом
                combat_result = process_combat(self.player, enemy_at_pos)
                for message in combat_result["messages"]:
                    self.message_log.append(message)
                
                # Проверка, побежден ли враг
                if enemy_at_pos.hp <= 0:
                    self.message_log.append(f"{enemy_at_pos.name} побежден!")
                    self.enemies.remove(enemy_at_pos)
                
                # Если игрок побежден, завершить игру
                if self.player.hp <= 0:
                    self.message_log.append("Вы побеждены!")
                    self.running = False
                    return
            else:
                # Переместить игрока
                self.player.x = new_x
                self.player.y = new_y
                self.message_log.append(f"Переместились в ({new_x}, {new_y})")
                
            # Игрок переместился или атаковал, завершить его ход
            self.complete_turn()
    
    def get_enemy_at_position(self, x, y):
        """
        Проверить, есть ли враг на указанной позиции.
        
        Args:
            x (int): X-координата
            y (int): Y-координата
            
        Returns:
            Enemy or None: Враг на позиции, или None если врага там нет
        """
        for enemy in self.enemies:
            if enemy.x == x and enemy.y == y:
                return enemy
        return None
        
    def complete_turn(self):
        """Завершить текущий ход и передать ход врагам."""
        self.turn += 1
        
        # Ход врагов
        for enemy in self.enemies:
            self.move_enemy(enemy)
            
    def move_enemy(self, enemy):
        """
        Переместить врага на основе простого ИИ.
        
        Args:
            enemy (Enemy): Враг для перемещения
        """
        # Простой ИИ: Если игрок близко, двигаться к игроку, иначе двигаться случайно
        player_distance = abs(enemy.x - self.player.x) + abs(enemy.y - self.player.y)
        
        if player_distance < 5:  # Если игрок в пределах "видимости"
            # Двигаться к игроку
            dx = 0
            dy = 0
            
            if enemy.x < self.player.x:
                dx = 1
            elif enemy.x > self.player.x:
                dx = -1
                
            if enemy.y < self.player.y:
                dy = 1
            elif enemy.y > self.player.y:
                dy = -1
                
            # Приоритет горизонтального или вертикального движения
            if random.choice([True, False]):
                if dx != 0:
                    self.try_move_enemy(enemy, dx, 0)
                elif dy != 0:
                    self.try_move_enemy(enemy, 0, dy)
            else:
                if dy != 0:
                    self.try_move_enemy(enemy, 0, dy)
                elif dx != 0:
                    self.try_move_enemy(enemy, dx, 0)
        else:
            # Случайное движение
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            dx, dy = random.choice(directions)
            self.try_move_enemy(enemy, dx, dy)
    
    def try_move_enemy(self, enemy, dx, dy):
        """
        Попытка переместить врага в указанном направлении.
        
        Args:
            enemy (Enemy): Враг для перемещения
            dx (int): Изменение x-координаты
            dy (int): Изменение y-координаты
        """
        new_x = enemy.x + dx
        new_y = enemy.y + dy
        
        # Проверка, находится ли новая позиция в пределах карты
        if 0 <= new_x < self.map_width and 0 <= new_y < self.map_height:
            # Проверка столкновения со стеной
            if self.current_map[new_y][new_x] == '#':
                return
            
            # Проверка столкновения с игроком
            if new_x == self.player.x and new_y == self.player.y:
                # Начать бой с игроком
                combat_result = process_combat(enemy, self.player)
                for message in combat_result["messages"]:
                    self.message_log.append(message)
                
                # Если игрок побежден, завершить игру
                if self.player.hp <= 0:
                    self.message_log.append("Вы побеждены!")
                    self.running = False
                return
            
            # Проверка столкновения с другими врагами
            for other_enemy in self.enemies:
                if other_enemy != enemy and other_enemy.x == new_x and other_enemy.y == new_y:
                    return
            
            # Переместить врага
            enemy.x = new_x
            enemy.y = new_y
            
    def update(self):
        """Обновить состояние игры."""
        # Проверка условия победы
        if not self.enemies:
            self.message_log.append("Поздравляем! Вы победили всех врагов!")
            self.message_log.append("Нажмите любую клавишу для выхода...")
            input()
            self.running = False
            
    def render(self):
        """Отображение текущего состояния игры на консоли."""
        self.ui.clear_screen()
        
        # Создание копии карты для отображения сущностей
        render_map = [list(row) for row in self.current_map]
        
        # Добавление врагов на карту
        for enemy in self.enemies:
            # Показать разные типы врагов разными символами
            if enemy.name.lower() == "гоблин":
                enemy_char = 'г'
            elif enemy.name.lower() == "орк":
                enemy_char = 'о'
            elif enemy.name.lower() == "тролль":
                enemy_char = 'Т'
            elif enemy.name.lower() == "скелет":
                enemy_char = 'с'
            else:
                enemy_char = 'В'
            render_map[enemy.y][enemy.x] = enemy_char
            
        # Добавление игрока на карту
        render_map[self.player.y][self.player.x] = '@'
        
        # Печать карты
        for row in render_map:
            print(''.join(row))
            
        # Печать характеристик игрока
        print("\n" + "=" * 40)
        print(f"Игрок: {self.player.name} ({self.player.char_class})")
        print(f"HP: {self.player.hp}/{self.player.max_hp} | SP: {self.player.sp}/{self.player.max_sp} | DMG: {self.player.dmg} | ARM: {self.player.arm}")
        print("=" * 40)
        
        # Печать лога сообщений (последние 5 сообщений)
        print("\nЛог сообщений:")
        for message in self.message_log[-5:]:
            print(f"- {message}")
            
        # Печать управления и легенды
        print("\nУправление: WASD = движение, Q = выход, ВВЕДИТЕ 'debug' = режим отладки")
        print("\nЛегенда: @ = Игрок, г = Гоблин, о = Орк, Т = Тролль, с = Скелет, # = Стена")
        
        # Печать отладочной информации если включен режим отладки
        if self.debug_mode:
            print("\n=== ОТЛАДОЧНАЯ ИНФОРМАЦИЯ ===")
            print(f"Ход: {self.turn}")
            print(f"Позиция игрока: ({self.player.x}, {self.player.y})")
            print(f"Количество врагов: {len(self.enemies)}")
            for i, enemy in enumerate(self.enemies):
                print(f"Враг {i+1}: {enemy.name} в ({enemy.x}, {enemy.y}) - HP: {enemy.hp}/{enemy.max_hp}")
            print("==============================")
