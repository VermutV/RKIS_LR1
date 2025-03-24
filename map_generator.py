"""
Модуль генератора карт для создания игровых карт.
"""
import random


def generate_standard_map():
    """
    Создать стандартную карту с предопределенной планировкой.
    
    Returns:
        list: 2D список, представляющий карту, где '#' - стена, а ' ' - пустое пространство
    """
    # Создать стандартную карту 20x10
    width, height = 20, 10
    
    # Инициализировать карту только со стенами
    game_map = [['#' for _ in range(width)] for _ in range(height)]
    
    # Создать пустые пространства в центре
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            game_map[y][x] = ' '
    
    # Добавить несколько внутренних стен для более интересной карты
    # Добавить вертикальную стену с проходом
    wall_x = width // 2
    for y in range(1, height - 1):
        if y != height // 2:
            game_map[y][wall_x] = '#'
    
    # Добавить горизонтальную стену с проходом
    wall_y = height // 2
    for x in range(1, width - 1):
        if x != width // 3:
            game_map[wall_y][x] = '#'
    
    # Добавить несколько случайных стен
    for _ in range(10):
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        game_map[y][x] = '#'
        
    return game_map


def generate_random_map(width, height):
    """
    Создать случайную карту с заданными размерами.
    
    Args:
        width (int): Ширина карты
        height (int): Высота карты
        
    Returns:
        list: 2D список, представляющий карту, где '#' - стена, а ' ' - пустое пространство
    """
    # Инициализировать карту только со стенами
    game_map = [['#' for _ in range(width)] for _ in range(height)]
    
    # Создать пустые пространства с помощью клеточного автомата
    # Сначала случайно заполнить внутреннюю область стенами и пустыми пространствами
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if random.random() < 0.6:  # 60% шанс быть пустым
                game_map[y][x] = ' '
    
    # Применить правила клеточного автомата для создания более естественных пещер
    for _ in range(3):  # Применить правила несколько раз
        new_map = [row[:] for row in game_map]  # Создать копию карты
        
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # Подсчитать стены в окрестности 3x3
                wall_count = 0
                for ny in range(y - 1, y + 2):
                    for nx in range(x - 1, x + 2):
                        if 0 <= ny < height and 0 <= nx < width and game_map[ny][nx] == '#':
                            wall_count += 1
                
                # Применить правила клеточного автомата
                if game_map[y][x] == '#':
                    # Если у стены меньше 4 соседей-стен, сделать её пустой
                    if wall_count < 4:
                        new_map[y][x] = ' '
                else:
                    # Если у пустого пространства больше 5 соседей-стен, сделать его стеной
                    if wall_count > 5:
                        new_map[y][x] = '#'
        
        game_map = new_map
    
    # Убедиться, что достаточно пустых пространств (не менее 40% внутренней области)
    empty_count = sum(row.count(' ') for row in game_map)
    inner_area = (width - 2) * (height - 2)
    min_empty = int(inner_area * 0.4)
    
    if empty_count < min_empty:
        # Добавить больше пустых пространств
        spaces_to_add = min_empty - empty_count
        attempts = 0
        
        while spaces_to_add > 0 and attempts < 1000:
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)
            
            if game_map[y][x] == '#':
                game_map[y][x] = ' '
                spaces_to_add -= 1
            
            attempts += 1
            
    # Убедиться, что внешняя граница состоит только из стен
    for y in range(height):
        game_map[y][0] = '#'
        game_map[y][width - 1] = '#'
    
    for x in range(width):
        game_map[0][x] = '#'
        game_map[height - 1][x] = '#'
    
    return game_map
