"""
Модуль пользовательского интерфейса для обработки интерфейса и ввода.
"""
import sys
import os


class UI:
    """Класс для обработки пользовательского интерфейса и ввода."""
    
    def __init__(self):
        """Инициализация UI."""
        self.debug_mode = False
    
    def show_welcome_screen(self):
        """Отображение приветственного экрана."""
        self.clear_screen()
        print("=" * 60)
        print("ДОБРО ПОЖАЛОВАТЬ В РОГАЛИК ПРИКЛЮЧЕНИЕ НА PYTHON")
        print("=" * 60)
        print("\nВы оказались в таинственном подземелье, полном врагов.")
        print("Исследуйте подземелье, побеждайте врагов и постарайтесь выжить!\n")
        print("\nУправление:")
        print("  WASD или стрелки: Перемещение")
        print("  Q: Выход из игры")
        print("  Введите 'debug' в любой момент: Переключение режима отладки")
        print("  Введите 'more' во время выбора типа карты: Больше врагов")
        print("=" * 60)
        input("\nНажмите Enter для продолжения...")
        
    def clear_screen(self):
        """Очистка экрана консоли."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def get_map_choice(self):
        """
        Получение выбора типа карты игроком.
        
        Returns:
            str: '1' для стандартной карты, '2' для случайной карты
        """
        while True:
            print("\nВыберите тип карты:")
            print("1. Стандартная карта")
            print("2. Случайная карта с настраиваемым размером")
            print("Введите 'more' для режима с увеличенным количеством врагов")
            
            choice = input("Введите ваш выбор (1, 2 или more): ").strip()
            
            if choice in ('1', '2', 'more'):
                return choice
            else:
                print("Неверный выбор. Пожалуйста, введите 1, 2 или more.")
                
    def get_map_size(self, dimension):
        """
        Получение нужного размера карты от игрока.
        
        Args:
            dimension (str): Измерение для получения (ширина или высота)
            
        Returns:
            int: Размер указанного измерения
        """
        dimension_ru = "ширину" if dimension == "width" else "высоту"
        while True:
            try:
                size = int(input(f"Введите {dimension_ru} карты (10-50): ").strip())
                if 10 <= size <= 50:
                    return size
                else:
                    print(f"Пожалуйста, введите {dimension_ru} от 10 до 50.")
            except ValueError:
                print("Пожалуйста, введите корректное число.")
                
    def get_player_name(self):
        """
        Получение имени игрока.
        
        Returns:
            str: Имя игрока
        """
        while True:
            name = input("\nВведите имя вашего персонажа: ").strip()
            if name:
                return name
            else:
                print("Имя не может быть пустым.")
                
    def get_player_class(self):
        """
        Получение класса персонажа игрока.
        
        Returns:
            str: Класс персонажа игрока
        """
        valid_classes = ["warrior", "mage", "rogue"]
        
        while True:
            print("\nВыберите класс персонажа:")
            print("1. Воин (Высокий HP, Хорошая броня, Средний урон)")
            print("2. Маг (Низкий HP, Нет брони, Высокий урон)")
            print("3. Разбойник (Средний HP, Низкая броня, Высокий урон)")
            
            choice = input("Введите ваш выбор (1, 2 или 3): ").strip()
            
            if choice == '1':
                return "Воин"
            elif choice == '2':
                return "Маг"
            elif choice == '3':
                return "Разбойник"
            else:
                print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")
                
    def get_player_action(self):
        """
        Получение следующего действия игрока.
        
        Returns:
            str: Действие игрока
        """
        # Упрощенная версия, работающая в любой системе
        action = input("Введите действие (w/a/s/d/q/debug): ").lower()
        
        # Проверка на команду отладки
        if action.lower() == 'debug':
            return 'debug'
        
        # Принимаем только первый символ введенной строки
        if action and action[0] in ['w', 'a', 's', 'd', 'q']:
            return action[0]
        else:
            return ' '  # Пробел означает "нет действия"
