"""
Модуль генератора карт для создания игровых карт.
"""
import random


def is_connected(game_map):
    """
    Проверяет, связана ли карта (все пустые клетки доступны из любой другой пустой клетки).
    
    Args:
        game_map (list): 2D список, представляющий карту
        
    Returns:
        bool: True, если карта связна, False в противном случае
    """
    height = len(game_map)
    width = len(game_map[0])
    
    # Найти первую пустую клетку
    start_x, start_y = None, None
    for y in range(height):
        for x in range(width):
            if game_map[y][x] == ' ':
                start_x, start_y = x, y
                break
        if start_x is not None:
            break
    
    if start_x is None:
        return True  # Нет пустых клеток
    
    # Провести обход в ширину от начальной точки
    visited = [[False for _ in range(width)] for _ in range(height)]
    queue = [(start_x, start_y)]
    visited[start_y][start_x] = True
    
    while queue:
        x, y = queue.pop(0)
        
        # Проверить все соседние клетки
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < width and 0 <= ny < height and 
                game_map[ny][nx] == ' ' and not visited[ny][nx]):
                visited[ny][nx] = True
                queue.append((nx, ny))
    
    # Проверить, все ли пустые клетки посещены
    for y in range(height):
        for x in range(width):
            if game_map[y][x] == ' ' and not visited[y][x]:
                return False
    
    return True

def connect_regions(game_map):
    """
    Соединяет несвязанные регионы на карте, пробивая проходы.
    
    Args:
        game_map (list): 2D список, представляющий карту
        
    Returns:
        list: Обновленная карта с соединенными регионами
    """
    height = len(game_map)
    width = len(game_map[0])
    
    # Найти все пустые регионы
    visited = [[False for _ in range(width)] for _ in range(height)]
    regions = []
    
    for y in range(height):
        for x in range(width):
            if game_map[y][x] == ' ' and not visited[y][x]:
                # Новый регион
                region = []
                queue = [(x, y)]
                visited[y][x] = True
                
                while queue:
                    cx, cy = queue.pop(0)
                    region.append((cx, cy))
                    
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = cx + dx, cy + dy
                        
                        if (0 <= nx < width and 0 <= ny < height and 
                            game_map[ny][nx] == ' ' and not visited[ny][nx]):
                            visited[ny][nx] = True
                            queue.append((nx, ny))
                
                regions.append(region)
    
    # Если только один регион, карта уже связна
    if len(regions) <= 1:
        return game_map
    
    # Соединить все регионы
    connected = [0]  # Список индексов уже соединенных регионов
    
    while len(connected) < len(regions):
        best_distance = float('inf')
        best_connection = None
        
        # Перебрать все возможные соединения между соединенными и несоединенными регионами
        for i in connected:
            for j in range(len(regions)):
                if j not in connected:
                    # Найти ближайшие клетки между регионами
                    for cell1 in regions[i]:
                        for cell2 in regions[j]:
                            dist = abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])
                            
                            if dist < best_distance:
                                best_distance = dist
                                best_connection = (cell1, cell2)
        
        # Создать путь между ближайшими клетками
        if best_connection:
            cell1, cell2 = best_connection
            x1, y1 = cell1
            x2, y2 = cell2
            
            # Определить направление пути
            path_cells = []
            x, y = x1, y1
            
            # Сначала двигаемся по x
            while x != x2:
                x += 1 if x2 > x else -1
                path_cells.append((x, y))
            
            # Затем по y
            while y != y2:
                y += 1 if y2 > y else -1
                path_cells.append((x, y))
            
            # Пробиваем проход
            for x, y in path_cells:
                game_map[y][x] = ' '
            
            # Добавляем новый соединенный регион
            for j in range(len(regions)):
                if j not in connected and any((x, y) in regions[j] for x, y in path_cells):
                    connected.append(j)
    
    return game_map


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
    
    # Добавить несколько случайных проходов через вертикальную стену
    for _ in range(2):  # Добавим еще пару проходов
        y = random.randint(1, height - 2)
        if y != height // 2:  # Не трогаем уже существующий проход
            game_map[y][wall_x] = ' '
    
    # Добавить несколько случайных проходов через горизонтальную стену
    for _ in range(2):  # Добавим еще пару проходов
        x = random.randint(1, width - 2)
        if x != width // 3:  # Не трогаем уже существующий проход
            game_map[wall_y][x] = ' '
    
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
    
    # Проверить связность карты и соединить несвязанные регионы
    if not is_connected(game_map):
        game_map = connect_regions(game_map)
    
    # Сделать дополнительные проходы для улучшения соединения
    for _ in range(width * height // 100):  # Количество проходов зависит от размера карты
        x = random.randint(1, width - 2)
        y = random.randint(1, height - 2)
        
        # Проверяем, не создаем ли мы острова путем удаления этой стены
        if game_map[y][x] == '#':
            game_map[y][x] = ' '
            
            # Если карта стала несвязной, возвращаем стену на место
            if not is_connected(game_map):
                game_map[y][x] = '#'
    
    return game_map
