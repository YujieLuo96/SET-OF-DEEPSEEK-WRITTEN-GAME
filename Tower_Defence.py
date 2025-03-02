import pygame
import sys
import math
import random
import os
from pygame.locals import *

# 初始化Pygame
pygame.init()
pygame.font.init()

# 设置中文显示编码
try:
    # 尝试设置环境变量以支持中文
    os.environ['SDL_VIDEODRIVER'] = 'windows'  # 在Windows上可能有帮助
    os.environ['PYTHONIOENCODING'] = 'utf-8'  # 设置Python IO编码
except:
    pass

# Unicode编码支持
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 游戏窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('高级塔防游戏')


# 加载游戏资源
def load_image(name, size=None, alpha=False):
    """加载图像资源并调整大小"""
    try:
        if alpha:
            image = pygame.Surface(size, pygame.SRCALPHA)
            # 绘制一个更详细的图形
            return image
        else:
            image = pygame.Surface(size)
            image.fill((100, 100, 100))
            # 由于无法实际加载外部图像，我们创建更详细的表面
            return image
    except:
        # 创建一个备用表面
        if alpha:
            image = pygame.Surface(size, pygame.SRCALPHA)
        else:
            image = pygame.Surface(size)
        return image


# 创建更详细的游戏元素
def create_tower_image(tower_type, size):
    """创建更详细的塔图像"""
    colors = {
        'archer': (60, 100, 180),  # 深蓝色
        'fire': (200, 60, 35),  # 深红色
        'ice': (100, 200, 255),  # 冰蓝色
        'lightning': (220, 180, 40),  # 金黄色
        'poison': (120, 50, 120)  # 深紫色
    }

    base_color = colors.get(tower_type, (100, 100, 100))

    image = pygame.Surface((size, size), pygame.SRCALPHA)

    # 塔基座
    pygame.draw.rect(image, (80, 80, 80), (0, size // 2, size, size // 2))
    pygame.draw.rect(image, (60, 60, 60), (size // 8, size // 4, size * 3 // 4, size // 4))

    # 塔主体
    if tower_type == 'archer':
        # 箭塔 - 带有箭窗的塔
        pygame.draw.rect(image, base_color, (size // 4, 0, size // 2, size // 2))
        pygame.draw.rect(image, (40, 70, 120), (size * 3 // 8, size // 8, size // 4, size // 4))
        # 塔顶
        points = [(size // 4, 0), (size * 3 // 4, 0), (size * 7 // 8, -size // 4), (size // 8, -size // 4)]
        adjusted_points = [(p[0], p[1] + size // 2) for p in points]
        pygame.draw.polygon(image, (50, 80, 140), adjusted_points)

    elif tower_type == 'fire':
        # 火塔 - 顶部有火焰的塔
        pygame.draw.rect(image, base_color, (size // 4, 0, size // 2, size // 2))
        # 火焰
        points = [(size // 3, -size // 4), (size // 2, -size // 2), (size * 2 // 3, -size // 4)]
        for i in range(3):
            adjusted_points = [(p[0], p[1] + size // 2) for p in points]
            pygame.draw.polygon(image, (230, 60 + i * 40, 20), adjusted_points)
            points = [(p[0] + size // 12, p[1] - size // 12) for p in points]

    elif tower_type == 'ice':
        # 冰塔 - 顶部有冰晶的塔
        pygame.draw.rect(image, base_color, (size // 4, 0, size // 2, size // 2))
        # 冰晶
        pygame.draw.polygon(image, (200, 240, 255),
                            [(size // 2, -size // 3), (size * 3 // 5, -size // 6),
                             (size * 3 // 4, -size // 3), (size * 3 // 5, -size // 2),
                             (size // 2, -size * 2 // 3), (size * 2 // 5, -size // 2),
                             (size // 4, -size // 3), (size * 2 // 5, -size // 6)],
                            0)
        adjusted_points = [(p[0], p[1] + size // 2) for p in
                           [(size // 2, -size // 2), (size * 3 // 5, -size // 4), (size * 2 // 5, -size // 4)]]
        pygame.draw.polygon(image, (150, 220, 255), adjusted_points)

    elif tower_type == 'lightning':
        # 闪电塔 - 顶部有闪电的塔
        pygame.draw.rect(image, base_color, (size // 4, 0, size // 2, size // 2))
        # 闪电
        points = [(size // 2, -size // 2), (size * 3 // 8, -size // 4), (size // 2, -size // 8),
                  (size * 3 // 8, size // 8), (size * 5 // 8, -size // 8), (size // 2, -size // 4)]
        adjusted_points = [(p[0], p[1] + size // 2) for p in points]
        pygame.draw.polygon(image, (255, 255, 100), adjusted_points)

    elif tower_type == 'poison':
        # 毒素塔 - 顶部有毒素瓶的塔
        pygame.draw.rect(image, base_color, (size // 4, 0, size // 2, size // 2))
        # 毒素瓶
        pygame.draw.rect(image, (150, 70, 150), (size * 3 // 8, -size // 8, size // 4, size // 4))
        points = [(size * 3 // 8, -size // 8), (size * 5 // 8, -size // 8), (size // 2, -size // 3)]
        adjusted_points = [(p[0], p[1] + size // 2) for p in points]
        pygame.draw.polygon(image, (150, 70, 150), adjusted_points)
        # 毒素泡泡
        for i in range(3):
            x = size // 2 + random.randint(-size // 8, size // 8)
            y = size // 4 + random.randint(-size // 8, size // 8)
            r = random.randint(size // 20, size // 12)
            pygame.draw.circle(image, (180, 100, 180, 150), (x, y), r)

    return image


def create_monster_image(monster_type, size):
    """创建更详细的怪物图像"""
    image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

    if monster_type == 'goblin':
        # 哥布林
        # 身体
        pygame.draw.circle(image, (30, 120, 40), (size, size), size)
        # 眼睛
        pygame.draw.circle(image, (255, 255, 255), (size - size // 3, size - size // 3), size // 4)
        pygame.draw.circle(image, (255, 255, 255), (size + size // 3, size - size // 3), size // 4)
        pygame.draw.circle(image, (0, 0, 0), (size - size // 3, size - size // 3), size // 8)
        pygame.draw.circle(image, (0, 0, 0), (size + size // 3, size - size // 3), size // 8)
        # 嘴
        pygame.draw.arc(image, (0, 0, 0), (size - size // 2, size, size, size // 2), 0, math.pi, 2)
        # 耳朵
        pygame.draw.polygon(image, (30, 100, 40), [(size - size // 2, size - size // 2),
                                                   (size - size, size - size),
                                                   (size - size // 3, size - size // 1.5)])
        pygame.draw.polygon(image, (30, 100, 40), [(size + size // 2, size - size // 2),
                                                   (size + size, size - size),
                                                   (size + size // 3, size - size // 1.5)])
        # 武器 - 小刀
        pygame.draw.line(image, (120, 120, 120), (size + size * 0.7, size + size * 0.3),
                         (size + size * 0.9, size + size * 0.5), 3)

    elif monster_type == 'ogre':
        # 食人魔
        # 身体
        pygame.draw.circle(image, (100, 70, 30), (size, size), size)
        # 眼睛
        pygame.draw.circle(image, (255, 255, 255), (size - size // 3, size - size // 3), size // 5)
        pygame.draw.circle(image, (255, 255, 255), (size + size // 3, size - size // 3), size // 5)
        pygame.draw.circle(image, (255, 0, 0), (size - size // 3, size - size // 3), size // 10)
        pygame.draw.circle(image, (255, 0, 0), (size + size // 3, size - size // 3), size // 10)
        # 嘴
        pygame.draw.arc(image, (0, 0, 0), (size - size // 2, size, size, size // 2), 0, math.pi, 3)
        # 牙齿
        pygame.draw.rect(image, (255, 255, 255), (size - size // 4, size + size // 8, size // 6, size // 6))
        pygame.draw.rect(image, (255, 255, 255), (size + size // 8, size + size // 8, size // 6, size // 6))
        # 角
        pygame.draw.polygon(image, (80, 50, 20), [(size - size // 2, size - size // 1.5),
                                                  (size - size, size - size * 1.2),
                                                  (size - size // 4, size - size // 1.2)])
        pygame.draw.polygon(image, (80, 50, 20), [(size + size // 2, size - size // 1.5),
                                                  (size + size, size - size * 1.2),
                                                  (size + size // 4, size - size // 1.2)])
        # 武器 - 巨大木棒
        pygame.draw.line(image, (120, 80, 40), (size - size * 0.8, size + size * 0.4),
                         (size - size * 0.5, size + size * 0.8), 6)

    elif monster_type == 'ghost':
        # 幽灵
        # 身体
        points = []
        for i in range(8):
            angle = math.pi * 2 * i / 8
            r = size + random.randint(-size // 8, size // 8)
            points.append((size + r * math.cos(angle), size + r * math.sin(angle)))
        pygame.draw.polygon(image, (200, 200, 230, 150), points)
        # 眼睛
        pygame.draw.circle(image, (0, 0, 0), (size - size // 3, size - size // 3), size // 6)
        pygame.draw.circle(image, (0, 0, 0), (size + size // 3, size - size // 3), size // 6)
        # 嘴
        pygame.draw.arc(image, (0, 0, 0), (size - size // 2, size, size, size // 2), math.pi, math.pi * 2, 2)
        # 飘动的底部
        for i in range(3):
            offset = i * size // 2
            height = random.randint(size // 4, size // 2)
            pygame.draw.ellipse(image, (200, 200, 230, 100),
                                (size - size // 2 + offset, size + size // 2, size // 3, height))

    elif monster_type == 'dragon':
        # 龙
        # 身体
        pygame.draw.circle(image, (180, 30, 30), (size, size), size)
        # 眼睛
        pygame.draw.circle(image, (255, 255, 0), (size - size // 3, size - size // 3), size // 5)
        pygame.draw.circle(image, (255, 255, 0), (size + size // 3, size - size // 3), size // 5)
        pygame.draw.circle(image, (0, 0, 0), (size - size // 3, size - size // 3), size // 10)
        pygame.draw.circle(image, (0, 0, 0), (size + size // 3, size - size // 3), size // 10)
        # 角
        pygame.draw.polygon(image, (150, 20, 20), [(size - size // 3, size - size // 1.5),
                                                   (size - size // 1.5, size - size * 1.5),
                                                   (size - size // 5, size - size)])
        pygame.draw.polygon(image, (150, 20, 20), [(size + size // 3, size - size // 1.5),
                                                   (size + size // 1.5, size - size * 1.5),
                                                   (size + size // 5, size - size)])
        # 嘴
        pygame.draw.polygon(image, (150, 20, 20), [(size - size // 3, size + size // 8),
                                                   (size + size // 3, size + size // 8),
                                                   (size, size + size // 2)])
        # 火焰
        flame_points = [(size, size + size // 3)]
        for i in range(5):
            angle = math.pi / 6 - math.pi / 3 * random.random()
            r = size // 2 + random.randint(0, size // 2)
            flame_points.append((size + r * math.cos(angle),
                                 size + size // 3 + r * math.sin(angle)))
        flame_points.append((size, size + size // 3))
        pygame.draw.polygon(image, (255, 150, 50), flame_points)

        # 翅膀
        wing_points_left = [
            (size - size // 2, size - size // 4),
            (size - size, size - size // 2),
            (size - size * 1.3, size),
            (size - size * 1.1, size + size // 3),
            (size - size // 2, size + size // 4)
        ]
        pygame.draw.polygon(image, (220, 50, 50), wing_points_left)

        wing_points_right = [
            (size + size // 2, size - size // 4),
            (size + size, size - size // 2),
            (size + size * 1.3, size),
            (size + size * 1.1, size + size // 3),
            (size + size // 2, size + size // 4)
        ]
        pygame.draw.polygon(image, (220, 50, 50), wing_points_right)

    elif monster_type == 'ice_elemental':
        # 冰元素
        # 身体
        points = []
        for i in range(8):
            angle = math.pi * 2 * i / 8
            r = size + random.randint(-size // 10, size // 10)
            points.append((size + r * math.cos(angle), size + r * math.sin(angle)))
        pygame.draw.polygon(image, (150, 200, 255, 200), points)
        # 冰晶
        for i in range(4):
            angle = math.pi * 2 * i / 4
            x1 = size + size * 0.7 * math.cos(angle)
            y1 = size + size * 0.7 * math.sin(angle)
            x2 = size + size * 1.3 * math.cos(angle)
            y2 = size + size * 1.3 * math.sin(angle)
            pygame.draw.line(image, (220, 240, 255), (x1, y1), (x2, y2), size // 8)
        # 眼睛
        pygame.draw.circle(image, (220, 240, 255), (size - size // 3, size - size // 3), size // 5)
        pygame.draw.circle(image, (220, 240, 255), (size + size // 3, size - size // 3), size // 5)
        pygame.draw.circle(image, (100, 150, 255), (size - size // 3, size - size // 3), size // 10)
        pygame.draw.circle(image, (100, 150, 255), (size + size // 3, size - size // 3), size // 10)

        # 冰晶光环
        for i in range(5):
            angle = math.pi * 2 * i / 5
            x = size + size * 0.9 * math.cos(angle)
            y = size + size * 0.9 * math.sin(angle)
            pygame.draw.circle(image, (200, 230, 255, 150), (x, y), size // 6)

    elif monster_type == 'dark_knight':
        # 新增黑暗骑士
        # 身体 - 盔甲
        pygame.draw.circle(image, (50, 50, 80), (size, size), size)

        # 头盔
        helmet_points = [
            (size - size // 2, size - size // 2),
            (size - size // 1.5, size - size),
            (size + size // 1.5, size - size),
            (size + size // 2, size - size // 2)
        ]
        pygame.draw.polygon(image, (70, 70, 100), helmet_points)

        # 面甲
        pygame.draw.rect(image, (30, 30, 50), (size - size // 2, size - size // 2, size, size // 3))

        # 眼睛 - 红色发光
        pygame.draw.circle(image, (255, 0, 0), (size - size // 4, size - size // 3), size // 10)
        pygame.draw.circle(image, (255, 0, 0), (size + size // 4, size - size // 3), size // 10)

        # 披风
        cape_points = [
            (size - size // 2, size - size // 4),
            (size + size // 2, size - size // 4),
            (size + size // 1.2, size + size),
            (size - size // 1.2, size + size)
        ]
        pygame.draw.polygon(image, (100, 20, 20), cape_points)

        # 盾牌
        shield_points = [
            (size - size * 0.8, size - size // 3),
            (size - size * 0.5, size - size // 2),
            (size - size * 0.5, size + size // 2),
            (size - size * 0.8, size + size // 3)
        ]
        pygame.draw.polygon(image, (130, 130, 150), shield_points)
        pygame.draw.polygon(image, (80, 80, 100), shield_points, 2)

        # 黑色大剑
        pygame.draw.line(image, (40, 40, 40),
                         (size + size * 0.6, size - size * 0.2),
                         (size + size * 1.0, size + size * 0.6), 6)
        # 剑柄
        pygame.draw.line(image, (100, 80, 30),
                         (size + size * 0.55, size - size * 0.25),
                         (size + size * 0.5, size - size * 0.4), 4)

        # 暗黑气息
        for i in range(6):
            angle = math.pi * 2 * i / 6
            r = size * 1.2
            x = size + r * math.cos(angle)
            y = size + r * math.sin(angle)
            smoke_size = random.randint(size // 6, size // 4)
            pygame.draw.circle(image, (70, 50, 90, 120), (x, y), smoke_size)

    return image


def create_projectile_image(damage_type, size):
    """创建更详细的投射物图像"""
    image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

    if damage_type == 'physical':
        # 箭矢
        pygame.draw.line(image, (50, 50, 50), (size - size, size), (size + size, size), size // 4)
        pygame.draw.polygon(image, (50, 50, 50),
                            [(size + size // 2, size - size // 3),
                             (size + size, size),
                             (size + size // 2, size + size // 3)])
        # 羽毛
        pygame.draw.polygon(image, (200, 200, 200),
                            [(size - size, size - size // 4),
                             (size - size // 2, size),
                             (size - size, size + size // 4)])

    elif damage_type == 'fire':
        # 火球
        for i in range(3):
            color = (255, 100 + i * 50, 0, 255 - i * 40)
            offset = i * size // 4
            pygame.draw.circle(image, color, (size, size), size - offset)
        # 火花
        for i in range(5):
            angle = math.pi * 2 * i / 5
            x = size + size * 0.8 * math.cos(angle)
            y = size + size * 0.8 * math.sin(angle)
            pygame.draw.circle(image, (255, 255, 100, 150), (x, y), size // 4)

    elif damage_type == 'ice':
        # 冰锥
        pygame.draw.polygon(image, (200, 240, 255),
                            [(size, size - size),
                             (size + size // 2, size),
                             (size, size + size),
                             (size - size // 2, size)])
        # 雪花图案
        for i in range(3):
            angle = math.pi * i / 3
            pygame.draw.line(image, (255, 255, 255),
                             (size, size),
                             (size + size * math.cos(angle), size + size * math.sin(angle)),
                             size // 6)
            pygame.draw.line(image, (255, 255, 255),
                             (size, size),
                             (size + size * math.cos(angle + math.pi), size + size * math.sin(angle + math.pi)),
                             size // 6)

    elif damage_type == 'lightning':
        # 闪电
        points = [(size - size // 2, size - size),
                  (size, size - size // 2),
                  (size - size // 4, size),
                  (size + size // 2, size - size // 4),
                  (size + size // 4, size + size // 2),
                  (size, size)]
        pygame.draw.polygon(image, (255, 255, 100), points)
        # 电光效果
        for i in range(3):
            start_point = random.choice(points)
            end_point = (start_point[0] + random.randint(-size // 2, size // 2),
                         start_point[1] + random.randint(-size // 2, size // 2))
            pygame.draw.line(image, (255, 255, 255), start_point, end_point, size // 8)

    elif damage_type == 'poison':
        # 毒液球
        pygame.draw.circle(image, (120, 50, 120), (size, size), size // 2)
        # 毒液滴
        for i in range(4):
            angle = math.pi * 2 * i / 4
            x1 = size + size // 2 * math.cos(angle)
            y1 = size + size // 2 * math.sin(angle)
            x2 = size + size * math.cos(angle)
            y2 = size + size * math.sin(angle)
            pygame.draw.line(image, (150, 70, 150), (x1, y1), (x2, y2), size // 4)
            pygame.draw.circle(image, (180, 100, 180), (x2, y2), size // 4)

    return image


def create_map_tile(is_path=False, size=30):
    """创建地图瓦片图像"""
    image = pygame.Surface((size, size))

    if is_path:
        # 路径瓦片
        base_color = (180, 160, 120)  # 土路颜色
        image.fill(base_color)

        # 添加一些细节 - 小石子和纹理
        for _ in range(5):
            x = random.randint(0, size)
            y = random.randint(0, size)
            radius = random.randint(1, 3)
            color_offset = random.randint(-20, 20)
            stone_color = (
                max(50, min(255, base_color[0] + color_offset)),
                max(50, min(255, base_color[1] + color_offset)),
                max(50, min(255, base_color[2] + color_offset))
            )
            pygame.draw.circle(image, stone_color, (x, y), radius)
    else:
        # 非路径瓦片 - 草地
        base_color = (50, 150, 50)
        image.fill(base_color)

        # 添加一些草的细节
        for _ in range(8):
            x = random.randint(0, size)
            y = random.randint(0, size)
            width = random.randint(2, 4)
            height = random.randint(4, 8)
            color_offset = random.randint(-30, 10)
            grass_color = (
                max(0, min(255, base_color[0] + color_offset)),
                max(0, min(255, base_color[1] + color_offset)),
                max(0, min(255, base_color[2] + color_offset))
            )
            pygame.draw.ellipse(image, grass_color, (x, y, width, height))

    return image


def create_effect_animation(effect_type, size):
    """创建效果动画帧"""
    frames = []

    if effect_type == 'explosion':
        # 爆炸效果的多个帧
        for i in range(5):
            frame = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            radius = size // 2 + i * size // 4
            pygame.draw.circle(frame, (255, 200 - i * 30, 0, 255 - i * 50), (size, size), radius)
            pygame.draw.circle(frame, (255, 255, 0, 200 - i * 40), (size, size), radius * 2 // 3)
            frames.append(frame)

    elif effect_type == 'freeze':
        # 冰冻效果的多个帧
        for i in range(4):
            frame = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            # 雪花图案
            for j in range(6):
                angle = math.pi * j / 3 + i * math.pi / 12
                length = size * (0.5 + i * 0.2)
                pygame.draw.line(frame, (200, 240, 255, 200 - i * 40),
                                 (size, size),
                                 (size + length * math.cos(angle), size + length * math.sin(angle)),
                                 size // 8)
            frames.append(frame)

    elif effect_type == 'poison_cloud':
        # 毒云效果的多个帧
        for i in range(5):
            frame = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)

            # 绘制多个交叠的圆形创建云状效果
            for j in range(8):
                radius = size // 2 + random.randint(-size // 6, size // 6)
                x = size + size * math.cos(j * math.pi / 4 + i * math.pi / 8) * 0.5
                y = size + size * math.sin(j * math.pi / 4 + i * math.pi / 8) * 0.5
                pygame.draw.circle(frame, (150, 70, 150, 100), (x, y), radius)

            # 添加一些小毒泡
            for j in range(4):
                x = size + random.randint(-size, size)
                y = size + random.randint(-size, size)
                r = random.randint(size // 10, size // 5)
                pygame.draw.circle(frame, (180, 100, 180, 150), (x, y), r)

            frames.append(frame)

    return frames


# 加载游戏字体
def load_game_fonts():
    """加载游戏中使用的字体，确保支持中文字符"""
    try:
        # 尝试使用系统中支持中文的字体
        system_fonts = pygame.font.get_fonts()
        chinese_fonts = [
            "simsun", "nsimsun", "simhei", "microsoftyahei", "microsoftyaheibold",
            "msgothic", "simkai", "arialuni", "microsoftjhenghei"
        ]

        # 查找可用的中文字体
        font_name = None
        for name in chinese_fonts:
            if name.lower() in system_fonts:
                font_name = name
                break

        # 如果找到支持中文的字体，使用它
        if font_name:
            fonts = {
                'small': pygame.font.SysFont(font_name, 16),
                'medium': pygame.font.SysFont(font_name, 20),
                'large': pygame.font.SysFont(font_name, 32),
                'title': pygame.font.SysFont(font_name, 48),
            }
        else:
            # 如果没有找到，尝试使用默认字体
            print("警告：未找到支持中文的系统字体，尝试使用默认字体")
            fonts = {
                'small': pygame.font.Font(None, 16),
                'medium': pygame.font.Font(None, 20),
                'large': pygame.font.Font(None, 32),
                'title': pygame.font.Font(None, 48),
            }
    except Exception as e:
        print(f"加载字体时出错: {e}")
        # 回退到系统默认字体
        fonts = {
            'small': pygame.font.Font(None, 16),
            'medium': pygame.font.Font(None, 20),
            'large': pygame.font.Font(None, 32),
            'title': pygame.font.Font(None, 48),
        }

    return fonts


# 生成游戏资源
game_resources = {
    'towers': {},
    'monsters': {},
    'projectiles': {},
    'effects': {},
    'map_tiles': {},
    'ui': {},
    'fonts': load_game_fonts()
}

# 生成塔图像
for tower_type in ['archer', 'fire', 'ice', 'lightning', 'poison']:
    game_resources['towers'][tower_type] = create_tower_image(tower_type, 40)

# 生成怪物图像
for monster_type in ['goblin', 'ogre', 'ghost', 'dragon', 'ice_elemental']:
    game_resources['monsters'][monster_type] = create_monster_image(monster_type, 20)

# 生成投射物图像
for damage_type in ['physical', 'fire', 'ice', 'lightning', 'poison']:
    game_resources['projectiles'][damage_type] = create_projectile_image(damage_type, 8)

# 生成地图瓦片
game_resources['map_tiles']['grass'] = create_map_tile(False, 30)
game_resources['map_tiles']['path'] = create_map_tile(True, 30)

# 生成效果动画
game_resources['effects']['explosion'] = create_effect_animation('explosion', 30)
game_resources['effects']['freeze'] = create_effect_animation('freeze', 30)
game_resources['effects']['poison_cloud'] = create_effect_animation('poison_cloud', 30)


# 创建UI元素
def create_ui_elements():
    """创建游戏UI元素"""
    ui = {}

    # 按钮背景
    button = pygame.Surface((100, 40))
    button.fill((100, 180, 100))
    # 添加按钮细节
    pygame.draw.rect(button, (120, 200, 120), (2, 2, 96, 36))
    pygame.draw.rect(button, (80, 160, 80), (0, 0, 100, 40), 2)
    ui['button'] = button

    # 按钮悬停效果
    button_hover = button.copy()
    pygame.draw.rect(button_hover, (150, 230, 150), (2, 2, 96, 36))
    pygame.draw.rect(button_hover, (100, 180, 100), (0, 0, 100, 40), 2)
    ui['button_hover'] = button_hover

    # 面板背景
    panel = pygame.Surface((200, 300))
    panel.fill((50, 50, 50))
    pygame.draw.rect(panel, (70, 70, 70), (2, 2, 196, 296))
    pygame.draw.rect(panel, (100, 100, 100), (4, 4, 192, 292), 2)
    ui['panel'] = panel

    # 信息条背景
    info_bar = pygame.Surface((WINDOW_WIDTH, 40))
    info_bar.fill((50, 50, 70))
    pygame.draw.rect(info_bar, (70, 70, 90), (0, 0, WINDOW_WIDTH, 40), 2)
    ui['info_bar'] = info_bar

    # 塔选择栏背景
    tower_bar = pygame.Surface((WINDOW_WIDTH, 60))
    tower_bar.fill((50, 50, 70))
    pygame.draw.rect(tower_bar, (70, 70, 90), (0, 0, WINDOW_WIDTH, 60), 2)
    ui['tower_bar'] = tower_bar

    # 生命图标
    heart = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.polygon(heart, (220, 50, 50),
                        [(8, 4), (6, 2), (2, 4), (2, 8), (8, 14), (14, 8), (14, 4), (10, 2), (8, 4)])
    ui['heart'] = heart

    # 金币图标
    coin = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.circle(coin, (220, 180, 50), (8, 8), 7)
    pygame.draw.circle(coin, (250, 220, 100), (8, 8), 5)
    pygame.draw.circle(coin, (220, 180, 50), (8, 8), 3)
    ui['coin'] = coin

    # 波次图标
    wave = pygame.Surface((16, 16), pygame.SRCALPHA)
    for i in range(3):
        pygame.draw.arc(wave, (50, 150, 220),
                        (0, 8 - i * 3, 16, 8), 0, math.pi, 2)
    ui['wave'] = wave

    # 分数图标
    score = pygame.Surface((16, 16), pygame.SRCALPHA)
    pygame.draw.polygon(score, (220, 220, 100),
                        [(8, 0), (10, 6), (16, 6), (11, 10), (13, 16),
                         (8, 12), (3, 16), (5, 10), (0, 6), (6, 6)])
    ui['score'] = score

    return ui


game_resources['ui'] = create_ui_elements()

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
BROWN = (165, 42, 42)

# 游戏设置
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 20)
large_font = pygame.font.SysFont('Arial', 32)

# 游戏路径设置（怪物移动的路径点）
PATH = [
    (0, 150), (100, 150), (100, 300), (300, 300),
    (300, 150), (500, 150), (500, 400), (700, 400), (800, 400)
]

# 玩家资源
player_resources = {
    'gold': 500,
    'lives': 20,
    'wave': 0,
    'score': 0
}

# 怪物类型定义
MONSTER_TYPES = {
    'goblin': {
        'hp': 150,  # 增加HP值
        'speed': 1.5,
        'damage': 1,
        'reward': 20,
        'color': GREEN,
        'size': 20,
        'resistance': {'fire': 0.1, 'ice': 0.3, 'lightning': 0.1},  # 增加基础抗性
        'description': '基础怪物，移动速度较快'
    },
    'ogre': {
        'hp': 380,  # 增加HP值
        'speed': 0.8,
        'damage': 3,  # 增加伤害值
        'reward': 40,
        'color': BROWN,
        'size': 30,
        'resistance': {'fire': 0.4, 'ice': 0.1, 'lightning': 0.2},  # 增加抗性
        'description': '高血量怪物，移动缓慢但造成更多伤害'
    },
    'ghost': {
        'hp': 120,  # 增加HP值
        'speed': 2.2,  # 增加速度
        'damage': 2,  # 增加伤害
        'reward': 30,
        'color': (200, 200, 230),
        'size': 18,
        'resistance': {'fire': 0.3, 'ice': 0.1, 'lightning': 0.7},  # 增加抗性
        'description': '快速怪物，对闪电有很高抗性'
    },
    'dragon': {
        'hp': 650,  # 大幅增加HP
        'speed': 1.0,
        'damage': 5,  # 大幅增加伤害
        'reward': 100,
        'color': RED,
        'size': 35,
        'resistance': {'fire': 0.9, 'ice': 0.2, 'lightning': 0.3},  # 增加抗性
        'description': '精英怪物，对火焰几乎免疫'
    },
    'ice_elemental': {
        'hp': 250,  # 增加HP值
        'speed': 1.2,
        'damage': 3,  # 增加伤害值
        'reward': 50,
        'color': (150, 200, 255),
        'size': 25,
        'resistance': {'fire': 0.3, 'ice': 0.95, 'lightning': 0.2},  # 增加抗性
        'description': '元素怪物，对冰冻效果几乎免疫'
    },
    'dark_knight': {  # 新增高级怪物类型
        'hp': 500,
        'speed': 1.1,
        'damage': 4,
        'reward': 80,
        'color': (50, 50, 80),
        'size': 32,
        'resistance': {'fire': 0.5, 'ice': 0.5, 'lightning': 0.5, 'physical': 0.3},  # 全面抗性
        'description': '黑暗骑士，拥有全面的元素抗性和物理防御'
    },
}

# 塔类型定义
TOWER_TYPES = {
    'archer': {
        'cost': 100,
        'damage': 30,
        'range': 150,
        'fire_rate': 1.0,  # 攻击间隔（秒）
        'color': BLUE,
        'size': 25,
        'damage_type': 'physical',
        'description': '基础塔，有较好的射程和攻击速度',
        'upgrade': {
            'cost': 100,
            'damage_bonus': 20,
            'range_bonus': 25,
            'fire_rate_bonus': 0.2
        }
    },
    'fire': {
        'cost': 150,
        'damage': 40,
        'range': 120,
        'fire_rate': 1.2,
        'color': RED,
        'size': 25,
        'damage_type': 'fire',
        'description': '火焰塔，对普通怪物有额外伤害，但对火焰抗性怪物效果较差',
        'special_ability': 'burn',  # 灼烧效果
        'upgrade': {
            'cost': 150,
            'damage_bonus': 25,
            'range_bonus': 15,
            'fire_rate_bonus': 0.1
        }
    },
    'ice': {
        'cost': 150,
        'damage': 25,
        'range': 130,
        'fire_rate': 1.5,
        'color': (100, 200, 255),
        'size': 25,
        'damage_type': 'ice',
        'description': '冰塔，攻击会减缓敌人移动速度',
        'special_ability': 'slow',  # 减速效果
        'upgrade': {
            'cost': 150,
            'damage_bonus': 15,
            'range_bonus': 20,
            'fire_rate_bonus': 0.15
        }
    },
    'lightning': {
        'cost': 200,
        'damage': 50,
        'range': 100,
        'fire_rate': 1.8,
        'color': YELLOW,
        'size': 25,
        'damage_type': 'lightning',
        'description': '闪电塔，可以同时攻击多个敌人',
        'special_ability': 'chain',  # 链式闪电效果
        'upgrade': {
            'cost': 200,
            'damage_bonus': 30,
            'range_bonus': 10,
            'fire_rate_bonus': 0.1
        }
    },
    'poison': {
        'cost': 175,
        'damage': 20,
        'range': 140,
        'fire_rate': 1.3,
        'color': PURPLE,
        'size': 25,
        'damage_type': 'poison',
        'description': '毒素塔，攻击会持续对敌人造成伤害',
        'special_ability': 'poison',  # 中毒效果
        'upgrade': {
            'cost': 175,
            'damage_bonus': 10,
            'range_bonus': 15,
            'fire_rate_bonus': 0.12,
            'duration_bonus': 1  # 毒素持续时间增加
        }
    },
}

# 游戏状态
game_state = {
    'selected_tower_type': None,
    'towers': [],
    'monsters': [],
    'projectiles': [],
    'effects': [],
    'wave_active': False,
    'game_over': False,
    'victory': False,
    'last_spawn_time': 0,
    'spawn_delay': 1.5,  # 怪物生成间隔（秒）
    'current_wave_monsters': [],
    'sidebar_active': False,
    'selected_tower': None,
    'background_particles': [],  # 背景粒子效果
    'camera_shake': 0,  # 镜头震动效果
    'tooltip': None,  # 悬停提示
    'notifications': [],  # 游戏通知
    'game_speed': 1,  # 游戏速度倍率，默认为1
    'acceleration_active': False,  # 加速状态标志
    'speed_level': 0,  # 速度等级：0=正常，1=2倍速，2=3倍速
    'ui_animation_time': 0,  # UI动画计时器
    'ui_theme': {  # UI主题颜色
        'primary': (60, 80, 120),  # 主色调
        'secondary': (80, 120, 180),  # 次要色调
        'accent': (220, 180, 60),  # 强调色
        'background': (30, 30, 40),  # 背景色
        'text': (230, 230, 240),  # 文本色
        'success': (80, 180, 80),  # 成功色
        'warning': (220, 160, 40),  # 警告色
        'danger': (200, 60, 60),  # 危险色
        'info': (60, 160, 220),  # 信息色
    }
}

# 波次配置
WAVES = [
    # 第1波
    {'goblin': 12},
    # 第2波
    {'goblin': 18, 'ogre': 3},
    # 第3波
    {'goblin': 15, 'ogre': 6, 'ghost': 4},
    # 第4波
    {'goblin': 18, 'ogre': 10, 'ghost': 6},
    # 第5波
    {'goblin': 12, 'ogre': 12, 'ghost': 12, 'ice_elemental': 3},
    # 第6波
    {'goblin': 15, 'ogre': 15, 'ghost': 15, 'ice_elemental': 6, 'dark_knight': 1},
    # 第7波
    {'goblin': 20, 'ogre': 18, 'ghost': 18, 'ice_elemental': 12, 'dark_knight': 2},
    # 第8波
    {'goblin': 25, 'ogre': 20, 'ghost': 18, 'ice_elemental': 15, 'dragon': 1, 'dark_knight': 3},
    # 第9波
    {'goblin': 30, 'ogre': 25, 'ghost': 20, 'ice_elemental': 18, 'dragon': 2, 'dark_knight': 4},
    # 第10波（最终波）
    {'goblin': 40, 'ogre': 30, 'ghost': 30, 'ice_elemental': 25, 'dragon': 5, 'dark_knight': 8},
]


# 类定义
class Monster:
    def __init__(self, monster_type):
        self.type = monster_type
        self.properties = MONSTER_TYPES[monster_type].copy()
        self.max_hp = self.properties['hp']
        self.hp = self.max_hp
        self.speed = self.properties['speed']
        self.damage = self.properties['damage']
        self.reward = self.properties['reward']
        self.color = self.properties['color']
        self.size = self.properties['size']
        self.resistance = self.properties['resistance']
        self.path_index = 0
        self.position = list(PATH[0])
        self.effects = []  # 状态效果（减速、灼烧等）
        self.animation_frame = 0
        self.animation_speed = 0.2  # 动画速度
        self.facing_right = True  # 面向右侧

    def move(self, time_delta=1.0):
        if self.path_index >= len(PATH) - 1:
            # 怪物到达终点
            player_resources['lives'] -= self.damage
            return True

        # 计算目标点
        target = PATH[self.path_index + 1]

        # 计算方向和距离
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # 确定怪物朝向
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

        # 处理状态效果
        current_speed = self.speed
        for effect in self.effects[:]:
            if effect['type'] == 'slow':
                current_speed *= effect['value']  # 减速效果

        # 更新动画帧
        self.animation_frame = (self.animation_frame + self.animation_speed * time_delta) % 4

        # 如果距离很小，进入下一段路径
        if distance < current_speed * time_delta:
            self.path_index += 1
            return False

        # 移动怪物
        move_x = dx / distance * current_speed * time_delta
        move_y = dy / distance * current_speed * time_delta
        self.position[0] += move_x
        self.position[1] += move_y

        return False

    def take_damage(self, amount, damage_type=None):
        # 应用抗性
        if damage_type in self.resistance:
            amount = amount * (1 - self.resistance[damage_type])

        self.hp -= amount

        # 添加受击闪烁效果
        self.hit_effect = 5  # 闪烁帧数

        return self.hp <= 0

    def draw(self, surface):
        # 获取怪物图像并应用朝向
        monster_image = game_resources['monsters'][self.type]

        # 绘制怪物（带有动画效果）
        pos_x = int(self.position[0])
        pos_y = int(self.position[1])

        # 应用小幅上下移动模拟走路动画
        bounce_offset = math.sin(self.animation_frame * math.pi) * 3

        # 根据朝向调整绘制
        if not self.facing_right:
            # 如果朝左，翻转图像
            monster_image = pygame.transform.flip(monster_image, True, False)

        # 受击闪烁效果
        if hasattr(self, 'hit_effect') and self.hit_effect > 0:
            # 创建一个临时表面并应用闪烁效果
            flash_image = monster_image.copy()
            flash_image.fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_ADD)
            surface.blit(flash_image,
                         (pos_x - monster_image.get_width() // 2,
                          pos_y - monster_image.get_height() // 2 + bounce_offset))
            self.hit_effect -= 1
        else:
            surface.blit(monster_image,
                         (pos_x - monster_image.get_width() // 2,
                          pos_y - monster_image.get_height() // 2 + bounce_offset))

        # 绘制高级血条
        bar_width = self.size * 2.5
        bar_height = 6
        border = 1
        hp_ratio = self.hp / self.max_hp

        # 血条背景和边框
        pygame.draw.rect(surface, (40, 40, 40),
                         (int(self.position[0] - bar_width / 2) - border,
                          int(self.position[1] - self.size - 15) - border,
                          bar_width + border * 2, bar_height + border * 2))

        # 血条
        pygame.draw.rect(surface, (200, 30, 30),
                         (int(self.position[0] - bar_width / 2),
                          int(self.position[1] - self.size - 15),
                          bar_width, bar_height))

        # 当前血量
        pygame.draw.rect(surface, (30, 180, 30),
                         (int(self.position[0] - bar_width / 2),
                          int(self.position[1] - self.size - 15),
                          int(bar_width * hp_ratio), bar_height))

        # 获取状态效果图标
        effect_y = int(self.position[1] - self.size - 25)
        effect_x = int(self.position[0] - bar_width / 2)
        effect_size = 8

        # 绘制状态效果图标
        for effect in self.effects:
            icon_bg = pygame.Surface((effect_size * 2, effect_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(icon_bg, (40, 40, 40, 180), (effect_size, effect_size), effect_size)

            if effect['type'] == 'slow':
                pygame.draw.circle(icon_bg, (100, 200, 255), (effect_size, effect_size), effect_size - 1)
                # 绘制雪花状图案
                for i in range(4):
                    angle = math.pi * i / 2
                    pygame.draw.line(icon_bg, (255, 255, 255),
                                     (effect_size, effect_size),
                                     (effect_size + (effect_size - 2) * math.cos(angle),
                                      effect_size + (effect_size - 2) * math.sin(angle)),
                                     1)

            elif effect['type'] == 'burn':
                pygame.draw.circle(icon_bg, (220, 50, 20), (effect_size, effect_size), effect_size - 1)
                # 绘制火焰图案
                points = [(effect_size, effect_size - effect_size / 2)]
                for i in range(3):
                    angle = math.pi / 6 + math.pi / 3 * i
                    r = effect_size / 2
                    points.append((effect_size + r * math.cos(angle),
                                   effect_size + r * math.sin(angle)))
                pygame.draw.polygon(icon_bg, (255, 180, 50), points)

            elif effect['type'] == 'poison':
                pygame.draw.circle(icon_bg, (120, 40, 120), (effect_size, effect_size), effect_size - 1)
                # 绘制毒液滴图案
                for i in range(3):
                    angle = 2 * math.pi / 3 * i + math.pi / 6
                    x = effect_size + (effect_size - 2) * math.cos(angle)
                    y = effect_size + (effect_size - 2) * math.sin(angle)
                    pygame.draw.circle(icon_bg, (180, 100, 180), (x, y), effect_size / 3)

            # 显示效果持续时间
            if effect['duration'] > 0:
                arc_rect = pygame.Rect(effect_x - 1, effect_y - 1, effect_size * 2 + 2, effect_size * 2 + 2)
                progress = min(1.0, effect['duration'] / 3.0)  # 基于3秒的标准持续时间
                pygame.draw.arc(surface, (220, 220, 220), arc_rect,
                                -math.pi / 2, -math.pi / 2 + 2 * math.pi * progress, 2)

            surface.blit(icon_bg, (effect_x, effect_y))
            effect_x += effect_size * 2 + 2  # 间隔


class Tower:
    def __init__(self, tower_type, position):
        self.type = tower_type
        self.properties = TOWER_TYPES[tower_type].copy()
        self.position = position
        self.damage = self.properties['damage']
        self.range = self.properties['range']
        self.fire_rate = self.properties['fire_rate']
        self.last_fire_time = 0
        self.color = self.properties['color']
        self.size = self.properties['size']
        self.damage_type = self.properties.get('damage_type', 'physical')
        self.special_ability = self.properties.get('special_ability', None)
        self.upgrade_level = 0
        self.max_upgrade_level = 5  # 修改为最大5级升级
        self.targets = []  # 当前目标（对于链式闪电等能力）
        self.animation_frame = 0
        self.rotation = 0  # 炮塔旋转角度
        self.attack_animation = 0  # 攻击动画帧

    def can_fire(self, current_time):
        return current_time - self.last_fire_time >= self.fire_rate

    def find_target(self, monsters):
        # 找到范围内的第一个怪物
        for monster in monsters:
            dx = monster.position[0] - self.position[0]
            dy = monster.position[1] - self.position[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance <= self.range:
                return monster

        return None

    def find_targets(self, monsters, max_targets=3):
        # 为链式闪电等效果找到多个目标
        targets = []
        for monster in monsters:
            dx = monster.position[0] - self.position[0]
            dy = monster.position[1] - self.position[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance <= self.range:
                targets.append(monster)
                if len(targets) >= max_targets:
                    break

        return targets

    def fire(self, current_time, monsters):
        if not self.can_fire(current_time):
            return []

        projectiles = []

        if self.special_ability == 'chain':
            # 链式闪电效果
            targets = self.find_targets(monsters, 3)
            self.targets = targets  # 保存当前目标用于绘制

            if targets:
                self.last_fire_time = current_time
                self.attack_animation = 5  # 设置攻击动画持续5帧
                for target in targets:
                    projectiles.append(
                        Projectile(self.position, target, self.damage, self.damage_type, self.special_ability))
        else:
            # 普通发射
            target = self.find_target(monsters)
            if target:
                self.targets = [target]  # 保存当前目标用于绘制
                self.last_fire_time = current_time
                self.attack_animation = 5  # 设置攻击动画

                # 更新塔的旋转角度以面向目标
                dx = target.position[0] - self.position[0]
                dy = target.position[1] - self.position[1]
                self.rotation = math.atan2(dy, dx)

                projectiles.append(
                    Projectile(self.position, target, self.damage, self.damage_type, self.special_ability))

        return projectiles

    def upgrade(self):
        if self.upgrade_level >= self.max_upgrade_level:
            return False

        upgrade_cost = self.properties['upgrade']['cost']
        if player_resources['gold'] < upgrade_cost:
            return False

        player_resources['gold'] -= upgrade_cost
        self.upgrade_level += 1

        # 应用升级加成
        self.damage += self.properties['upgrade']['damage_bonus']
        self.range += self.properties['upgrade']['range_bonus']
        self.fire_rate -= self.properties['upgrade']['fire_rate_bonus']  # 减少发射间隔时间
        self.fire_rate = max(0.2, self.fire_rate)  # 确保不低于最小值

        # 添加升级特效
        game_state['effects'].append({
            'type': 'upgrade',
            'position': self.position,
            'frame': 0,
            'max_frames': 20,
        })

        return True

    def draw(self, surface, selected=False):
        # 获取塔图像
        tower_image = game_resources['towers'][self.type]

        # 如果当前有攻击动画，应用闪烁或缩放效果
        if self.attack_animation > 0:
            # 创建一个略大的图像表示攻击状态
            attack_scale = 1.1 + (self.attack_animation / 25.0)
            tower_image_scaled = pygame.transform.scale(
                tower_image,
                (int(tower_image.get_width() * attack_scale),
                 int(tower_image.get_height() * attack_scale))
            )

            # 逐渐恢复正常大小
            self.attack_animation -= 1

            # 绘制塔基础
            base_rect = pygame.Rect(
                self.position[0] - 20,
                self.position[1] - 20,
                40, 40
            )
            pygame.draw.rect(surface, (100, 100, 100), base_rect)
            pygame.draw.rect(surface, (70, 70, 70), base_rect, 2)

            # 绘制塔（带旋转和缩放）
            rotated_image = tower_image_scaled
            if self.type != 'lightning':  # 闪电塔不旋转
                rotated_image = pygame.transform.rotate(tower_image_scaled, -self.rotation * 180 / math.pi - 90)

            surface.blit(
                rotated_image,
                (self.position[0] - rotated_image.get_width() // 2,
                 self.position[1] - rotated_image.get_height() // 2)
            )
        else:
            # 绘制塔基础
            base_rect = pygame.Rect(
                self.position[0] - 20,
                self.position[1] - 20,
                40, 40
            )
            pygame.draw.rect(surface, (100, 100, 100), base_rect)
            pygame.draw.rect(surface, (70, 70, 70), base_rect, 2)

            # 绘制塔（带旋转）
            rotated_image = tower_image
            if self.type != 'lightning' and self.targets:  # 闪电塔不旋转，且只有有目标时才旋转
                rotated_image = pygame.transform.rotate(tower_image, -self.rotation * 180 / math.pi - 90)

            surface.blit(
                rotated_image,
                (self.position[0] - rotated_image.get_width() // 2,
                 self.position[1] - rotated_image.get_height() // 2)
            )

        # 如果选中则显示范围和高亮效果
        if selected:
            # 绘制半透明范围指示器
            range_surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (200, 200, 200, 40), (self.range, self.range), self.range)
            pygame.draw.circle(range_surface, (255, 255, 255, 120), (self.range, self.range), self.range, 2)

            # 绘制脉动效果
            pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) * 0.5  # 0到1之间的脉动值
            pulse_radius = int(self.range - 5 + pulse * 10)
            pygame.draw.circle(range_surface, (255, 255, 255, 50), (self.range, self.range), pulse_radius, 1)

            surface.blit(range_surface,
                         (self.position[0] - self.range, self.position[1] - self.range))

            # 绘制选中高亮边框
            pygame.draw.rect(surface, (255, 255, 100),
                             (self.position[0] - 22, self.position[1] - 22, 44, 44), 2)

        # 绘制升级等级指示器
        if self.upgrade_level > 0:
            stars_y = self.position[1] + tower_image.get_height() // 2 + 5
            stars_width = 14 * self.upgrade_level
            stars_x = self.position[0] - stars_width // 2

            for i in range(self.upgrade_level):
                # 绘制星星图标
                star_points = []
                for j in range(5):
                    angle = math.pi / 2 + j * 2 * math.pi / 5
                    star_points.append((
                        stars_x + i * 14 + 7 + 6 * math.cos(angle),
                        stars_y + 7 + 6 * math.sin(angle)
                    ))
                    angle += math.pi / 5
                    star_points.append((
                        stars_x + i * 14 + 7 + 3 * math.cos(angle),
                        stars_y + 7 + 3 * math.sin(angle)
                    ))

                pygame.draw.polygon(surface, (255, 220, 0), star_points)
                pygame.draw.polygon(surface, (180, 150, 0), star_points, 1)

        # 如果有目标，绘制攻击特效
        for target in self.targets:
            if target in game_state['monsters']:  # 确保目标仍然存在
                if self.damage_type == 'lightning':
                    # 闪电效果 - 锯齿状线条
                    start_x, start_y = self.position
                    end_x, end_y = target.position

                    # 计算距离和分段数
                    distance = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
                    segments = max(3, int(distance / 20))

                    # 绘制锯齿状闪电
                    points = [self.position]
                    for i in range(1, segments):
                        # 计算段上的点位置
                        ratio = i / segments
                        segment_x = start_x + (end_x - start_x) * ratio
                        segment_y = start_y + (end_y - start_y) * ratio

                        # 添加随机偏移
                        offset = 10 * math.sin(pygame.time.get_ticks() / 100 + i)
                        normal_x = (end_y - start_y) / distance
                        normal_y = -(end_x - start_x) / distance

                        points.append((
                            segment_x + normal_x * offset,
                            segment_y + normal_y * offset
                        ))

                    points.append(target.position)

                    # 闪电主体
                    if len(points) >= 2:
                        pygame.draw.lines(surface, (255, 255, 100), False, points, 3)

                    # 闪电光晕
                    if self.attack_animation > 0:
                        for i in range(1, len(points)):
                            pygame.draw.line(surface, (255, 255, 200, 150), points[i - 1], points[i], 5)

                elif self.damage_type == 'fire':
                    # 火焰效果 - 从塔到目标的渐变色线条
                    start_pos = pygame.Vector2(self.position)
                    end_pos = pygame.Vector2(target.position)

                    # 创建一个渐变色表面
                    length = int((end_pos - start_pos).length())
                    angle = math.atan2(end_pos.y - start_pos.y, end_pos.x - start_pos.x)

                    if self.attack_animation > 0:
                        # 在攻击动画期间显示火焰效果
                        beam_width = 6
                        gradient = pygame.Surface((length, beam_width), pygame.SRCALPHA)

                        for x in range(length):
                            ratio = x / length
                            # 火焰从黄色到红色的渐变
                            color = (255, int(255 * (1 - ratio)), 0, int(200 * (1 - ratio * 0.5)))
                            pygame.draw.line(gradient, color, (x, 0), (x, beam_width), 1)

                        # 旋转渐变
                        rotated_gradient = pygame.transform.rotate(gradient, -math.degrees(angle))

                        # 确定绘制位置
                        offset = pygame.Vector2(-rotated_gradient.get_width() / 2, -rotated_gradient.get_height() / 2)
                        pos = start_pos + (end_pos - start_pos) / 2 + offset

                        surface.blit(rotated_gradient, pos)

                elif self.damage_type == 'ice':
                    # 冰冻效果 - 从塔到目标的冰晶粒子
                    start_pos = pygame.Vector2(self.position)
                    end_pos = pygame.Vector2(target.position)

                    if self.attack_animation > 0:
                        # 在攻击动画期间显示冰晶效果
                        particles = 12
                        for i in range(particles):
                            ratio = i / particles
                            pos = start_pos.lerp(end_pos, ratio)
                            size = random.randint(2, 4)

                            # 蓝色冰晶粒子
                            pygame.draw.circle(surface, (150, 220, 255), (int(pos.x), int(pos.y)), size)
                            pygame.draw.circle(surface, (200, 240, 255), (int(pos.x), int(pos.y)), size // 2)

                elif self.damage_type == 'poison':
                    # 毒素效果 - 从塔到目标的绿色/紫色粒子
                    start_pos = pygame.Vector2(self.position)
                    end_pos = pygame.Vector2(target.position)

                    if self.attack_animation > 0:
                        # 在攻击动画期间显示毒素效果
                        particles = 10
                        for i in range(particles):
                            ratio = i / particles
                            # 添加一些随机偏移
                            offset = random.randint(-5, 5)
                            normal = pygame.Vector2(-(end_pos.y - start_pos.y),
                                                    end_pos.x - start_pos.x).normalize() * offset

                            pos = start_pos.lerp(end_pos, ratio) + normal
                            size = random.randint(3, 5)

                            # 紫色毒素粒子
                            pygame.draw.circle(surface, (160, 60, 160), (int(pos.x), int(pos.y)), size)
                            pygame.draw.circle(surface, (200, 100, 200), (int(pos.x), int(pos.y)), size // 2)

                else:  # 物理攻击
                    # 默认攻击特效 - 从塔到目标的虚线
                    if self.attack_animation > 0:
                        pygame.draw.line(surface, (200, 200, 200),
                                         self.position, target.position, 2)


class Projectile:
    def __init__(self, start_pos, target, damage, damage_type, special_ability=None):
        self.position = list(start_pos)
        self.target = target
        self.damage = damage
        self.damage_type = damage_type
        self.special_ability = special_ability
        self.speed = 5
        self.size = 5
        self.rotation = 0
        self.trail = []  # 轨迹点
        self.max_trail_length = 5  # 最大轨迹长度

        # 计算初始角度
        dx = target.position[0] - start_pos[0]
        dy = target.position[1] - start_pos[1]
        self.rotation = math.atan2(dy, dx)

        # 根据伤害类型设置颜色
        if damage_type == 'fire':
            self.color = RED
        elif damage_type == 'ice':
            self.color = (100, 200, 255)
        elif damage_type == 'lightning':
            self.color = YELLOW
        elif damage_type == 'poison':
            self.color = PURPLE
        else:
            self.color = BLUE

    def move(self):
        if self.target not in game_state['monsters']:
            return True  # 目标不存在，移除投射物

        # 保存当前位置到轨迹
        self.trail.append(list(self.position))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

        # 计算方向和距离
        dx = self.target.position[0] - self.position[0]
        dy = self.target.position[1] - self.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # 更新旋转角度
        self.rotation = math.atan2(dy, dx)

        # 如果距离很小，击中目标
        if distance < self.speed:
            self.hit_target()
            return True

        # 移动投射物
        move_x = dx / distance * self.speed
        move_y = dy / distance * self.speed
        self.position[0] += move_x
        self.position[1] += move_y

        return False

    def hit_target(self):
        # 添加击中特效
        game_state['effects'].append({
            'type': 'hit',
            'position': list(self.target.position),
            'damage_type': self.damage_type,
            'frame': 0,
            'max_frames': 10,
        })

        # 计算伤害并检查怪物是否死亡
        if self.target.take_damage(self.damage, self.damage_type):
            # 怪物死亡，添加死亡特效
            if self.damage_type == 'fire':
                effect_type = 'explosion'
            elif self.damage_type == 'ice':
                effect_type = 'freeze'
            elif self.damage_type == 'poison':
                effect_type = 'poison_cloud'
            else:
                effect_type = 'explosion'

            game_state['effects'].append({
                'type': effect_type,
                'position': list(self.target.position),
                'frame': 0,
                'max_frames': len(game_resources['effects'][effect_type]),
            })

            game_state['monsters'].remove(self.target)
            player_resources['gold'] += self.target.reward
            player_resources['score'] += self.target.reward

        # 应用特殊效果
        if self.special_ability == 'slow':
            # 减速效果
            slow_effect = {
                'type': 'slow',
                'value': 0.5,  # 速度减半
                'duration': 3.0  # 持续3秒
            }
            # 避免效果叠加
            for effect in self.target.effects:
                if effect['type'] == 'slow':
                    effect['duration'] = max(effect['duration'], slow_effect['duration'])
                    break
            else:
                self.target.effects.append(slow_effect)

        elif self.special_ability == 'burn':
            # 灼烧效果（每秒造成额外伤害）
            burn_effect = {
                'type': 'burn',
                'damage': self.damage * 0.2,  # 每秒造成伤害的20%
                'duration': 3.0  # 持续3秒
            }
            # 避免效果叠加
            for effect in self.target.effects:
                if effect['type'] == 'burn':
                    effect['duration'] = max(effect['duration'], burn_effect['duration'])
                    break
            else:
                self.target.effects.append(burn_effect)

        elif self.special_ability == 'poison':
            # 中毒效果（每秒造成额外伤害）
            poison_effect = {
                'type': 'poison',
                'damage': self.damage * 0.15,  # 每秒造成伤害的15%
                'duration': 5.0  # 持续5秒
            }
            # 避免效果叠加
            for effect in self.target.effects:
                if effect['type'] == 'poison':
                    effect['duration'] = max(effect['duration'], poison_effect['duration'])
                    break
            else:
                self.target.effects.append(poison_effect)

    def draw(self, surface):
        # 绘制轨迹
        if self.trail:
            if self.damage_type == 'fire':
                # 火焰轨迹
                for i, pos in enumerate(self.trail):
                    alpha = int(255 * (i + 1) / len(self.trail))
                    size = int(self.size * (i + 1) / len(self.trail))
                    # 火焰颜色从黄色到红色
                    color = (255, min(255, int(100 + 155 * i / len(self.trail))), 0, alpha)
                    pygame.draw.circle(surface, color, (int(pos[0]), int(pos[1])), size)

            elif self.damage_type == 'ice':
                # 冰冻轨迹
                for i, pos in enumerate(self.trail):
                    alpha = int(200 * (i + 1) / len(self.trail))
                    trail_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surf, (150, 220, 255, alpha), (4, 4), 3)
                    pygame.draw.circle(trail_surf, (200, 240, 255, alpha), (4, 4), 2)
                    surface.blit(trail_surf, (int(pos[0] - 4), int(pos[1] - 4)))

            elif self.damage_type == 'lightning':
                # 闪电轨迹
                for i in range(len(self.trail) - 1):
                    # 闪电余辉
                    alpha = int(150 * (i + 1) / len(self.trail))
                    pygame.draw.line(surface, (255, 255, 100, alpha),
                                     (int(self.trail[i][0]), int(self.trail[i][1])),
                                     (int(self.trail[i + 1][0]), int(self.trail[i + 1][1])),
                                     i + 1)

            elif self.damage_type == 'poison':
                # 毒素轨迹
                for i, pos in enumerate(self.trail):
                    alpha = int(200 * (i + 1) / len(self.trail))
                    size = int(self.size * 0.8 * (i + 1) / len(self.trail))
                    pygame.draw.circle(surface, (150, 70, 150, alpha), (int(pos[0]), int(pos[1])), size)
                    if i % 2 == 0:  # 每隔一个点添加毒泡
                        pygame.draw.circle(surface, (180, 100, 180, alpha // 2),
                                           (int(pos[0] + random.randint(-3, 3)),
                                            int(pos[1] + random.randint(-3, 3))),
                                           size // 2)

            else:  # 物理攻击
                # 箭矢轨迹
                for i, pos in enumerate(self.trail[:-1]):
                    alpha = int(100 * (i + 1) / len(self.trail))
                    pygame.draw.line(surface, (200, 200, 200, alpha),
                                     (int(pos[0]), int(pos[1])),
                                     (int(self.trail[i + 1][0]), int(self.trail[i + 1][1])),
                                     1)

        # 绘制投射物本身
        if self.damage_type == 'physical':
            # 箭矢
            arrow_image = game_resources['projectiles']['physical']
            rotated_arrow = pygame.transform.rotate(arrow_image, -math.degrees(self.rotation) - 90)
            surface.blit(rotated_arrow,
                         (int(self.position[0] - rotated_arrow.get_width() // 2),
                          int(self.position[1] - rotated_arrow.get_height() // 2)))

        elif self.damage_type == 'fire':
            # 火球
            fire_image = game_resources['projectiles']['fire']
            # 添加旋转动画效果
            angle = (pygame.time.get_ticks() // 30) % 360
            rotated_fire = pygame.transform.rotate(fire_image, angle)
            surface.blit(rotated_fire,
                         (int(self.position[0] - rotated_fire.get_width() // 2),
                          int(self.position[1] - rotated_fire.get_height() // 2)))

        elif self.damage_type == 'ice':
            # 冰晶
            ice_image = game_resources['projectiles']['ice']
            # 冰晶缓慢旋转
            angle = (pygame.time.get_ticks() // 50) % 360
            rotated_ice = pygame.transform.rotate(ice_image, angle)
            surface.blit(rotated_ice,
                         (int(self.position[0] - rotated_ice.get_width() // 2),
                          int(self.position[1] - rotated_ice.get_height() // 2)))

        elif self.damage_type == 'lightning':
            # 闪电球
            lightning_image = game_resources['projectiles']['lightning']
            # 闪电快速闪烁旋转
            angle = (pygame.time.get_ticks() // 20) % 360
            rotated_lightning = pygame.transform.rotate(lightning_image, angle)
            surface.blit(rotated_lightning,
                         (int(self.position[0] - rotated_lightning.get_width() // 2),
                          int(self.position[1] - rotated_lightning.get_height() // 2)))

        elif self.damage_type == 'poison':
            # 毒液球
            poison_image = game_resources['projectiles']['poison']
            # 毒液球摇晃旋转
            angle = math.sin(pygame.time.get_ticks() / 200) * 30
            rotated_poison = pygame.transform.rotate(poison_image, angle)
            surface.blit(rotated_poison,
                         (int(self.position[0] - rotated_poison.get_width() // 2),
                          int(self.position[1] - rotated_poison.get_height() // 2)))


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None, icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.is_hovered = False
        self.icon = icon
        self.pressed = False
        self.press_time = 0

        # 添加动画变量
        self.animation_offset = 0
        self.animation_direction = 1

    def draw(self, surface):
        # 确定按钮状态颜色
        if self.pressed:
            color = (max(0, self.color[0] - 40), max(0, self.color[1] - 40), max(0, self.color[2] - 40))
            offset = 2  # 按下时的偏移
        elif self.is_hovered:
            color = self.hover_color
            offset = 0
            # 应用悬停动画
            self.animation_offset += 0.2 * self.animation_direction
            if abs(self.animation_offset) > 2:
                self.animation_direction *= -1
        else:
            color = self.color
            offset = 0
            self.animation_offset = 0
            self.animation_direction = 1

        # 绘制按钮底层阴影
        shadow_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (50, 50, 50, 180), shadow_rect, border_radius=5)

        # 绘制按钮主体
        button_rect = pygame.Rect(self.rect.x, self.rect.y + offset, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, color, button_rect, border_radius=5)

        # 绘制按钮边框
        border_color = (50, 50, 50) if not self.is_hovered else (255, 255, 255)
        pygame.draw.rect(surface, border_color, button_rect, 2, border_radius=5)

        # 绘制内部高光（立体效果）
        if not self.pressed:
            highlight_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2 + offset, self.rect.width - 4, 10)
            pygame.draw.rect(surface, (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30)),
                             highlight_rect, border_radius=3)

        # 解析多行文本
        lines = self.text.split('\n')

        # 绘制文本
        total_height = len(lines) * 20
        start_y = self.rect.centery - total_height // 2 + offset

        for i, line in enumerate(lines):
            text_surface = game_resources['fonts']['medium'].render(line, True, (20, 20, 20))
            text_rect = text_surface.get_rect(centerx=self.rect.centerx,
                                              y=start_y + i * 22)

            # 绘制文本阴影
            shadow_rect = text_rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            shadow_surface = game_resources['fonts']['medium'].render(line, True, (0, 0, 0, 150))
            surface.blit(shadow_surface, shadow_rect)

            # 绘制正常文本
            surface.blit(text_surface, text_rect)

        # 如果有图标，绘制图标
        if self.icon and self.icon in game_resources['ui']:
            icon_size = game_resources['ui'][self.icon].get_size()
            icon_pos = (self.rect.x + 10, self.rect.centery - icon_size[1] // 2 + offset)
            surface.blit(game_resources['ui'][self.icon], icon_pos)

        # 绘制悬停发光效果
        if self.is_hovered:
            glow_surf = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
            glow_rect = pygame.Rect(5, 5, self.rect.width, self.rect.height)
            pygame.draw.rect(glow_surf, (255, 255, 200, 50 + int(self.animation_offset * 10)),
                             glow_rect, border_radius=8)
            surface.blit(glow_surf, (self.rect.x - 5, self.rect.y - 5 + offset))

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # 处理按下动画
        if self.pressed:
            current_time = pygame.time.get_ticks()
            if current_time - self.press_time > 200:  # 200毫秒后恢复
                self.pressed = False

        return self.is_hovered

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.pressed = True
                self.press_time = pygame.time.get_ticks()

                if self.action:
                    self.action()
                    return True
        return False


# 游戏辅助函数
def can_place_tower(position):
    # 检查是否在有效位置（不在路径上）
    for i in range(len(PATH) - 1):
        start = PATH[i]
        end = PATH[i + 1]

        # 检查垂直或水平路径段
        if start[0] == end[0]:  # 垂直段
            x_min, x_max = start[0] - 30, start[0] + 30
            y_min, y_max = min(start[1], end[1]) - 30, max(start[1], end[1]) + 30
            if x_min <= position[0] <= x_max and y_min <= position[1] <= y_max:
                return False
        elif start[1] == end[1]:  # 水平段
            x_min, x_max = min(start[0], end[0]) - 30, max(start[0], end[0]) + 30
            y_min, y_max = start[1] - 30, start[1] + 30
            if x_min <= position[0] <= x_max and y_min <= position[1] <= y_max:
                return False

    # 检查是否与其他塔重叠
    for tower in game_state['towers']:
        dx = tower.position[0] - position[0]
        dy = tower.position[1] - position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < 40:  # 塔之间的最小距离
            return False

    # 检查是否在游戏区域内
    if position[0] < 50 or position[0] > 700 or position[1] < 50 or position[1] > 550:
        return False

    return True


def start_wave():
    if player_resources['wave'] >= len(WAVES):
        game_state['victory'] = True
        return

    wave_data = WAVES[player_resources['wave']]
    game_state['current_wave_monsters'] = []

    for monster_type, count in wave_data.items():
        for _ in range(count):
            game_state['current_wave_monsters'].append(monster_type)

    random.shuffle(game_state['current_wave_monsters'])
    game_state['wave_active'] = True
    game_state['last_spawn_time'] = pygame.time.get_ticks() / 1000

    # 添加波次开始通知
    add_notification(f"第 {player_resources['wave'] + 1} 波开始!", (255, 200, 100))


def spawn_monster():
    if not game_state['current_wave_monsters']:
        game_state['wave_active'] = False
        player_resources['wave'] += 1
        return

    monster_type = game_state['current_wave_monsters'].pop(0)
    monster = Monster(monster_type)
    game_state['monsters'].append(monster)

    # 添加出生效果
    game_state['effects'].append({
        'type': 'spawn',
        'position': list(monster.position),
        'frame': 0,
        'max_frames': 10,
    })


def update_game_state():
    current_time = pygame.time.get_ticks() / 1000

    # 应用游戏速度倍率
    speed_multipliers = [1.0, 2.0, 3.0]  # 三种速度倍率：1倍、2倍、3倍
    time_delta = 1.0 / FPS * speed_multipliers[game_state['speed_level']]

    # 更新UI动画计时器
    game_state['ui_animation_time'] += time_delta

    # 检查游戏是否结束
    if player_resources['lives'] <= 0:
        game_state['game_over'] = True

    # 更新背景粒子效果
    update_background_particles()

    # 更新摄像机震动
    if game_state['camera_shake'] > 0:
        game_state['camera_shake'] -= 1 * speed_multipliers[game_state['speed_level']]

    # 更新通知消息
    update_notifications()

    # 更新怪物状态
    for monster in game_state['monsters'][:]:
        # 处理怪物状态效果（中毒、灼烧等）
        for effect in monster.effects[:]:
            if effect['type'] in ['burn', 'poison']:
                damage = effect['damage'] / FPS * speed_multipliers[game_state['speed_level']]
                monster.hp -= damage

                # 添加伤害数字效果
                if random.random() < 0.1:  # 只显示部分伤害数字，避免过多
                    add_damage_number(monster.position, damage, effect['type'])

                if monster.hp <= 0:
                    add_gold_effect(monster.position, monster.reward)
                    add_death_effect(monster)
                    game_state['monsters'].remove(monster)
                    player_resources['gold'] += monster.reward
                    player_resources['score'] += monster.reward
                    break

            # 按游戏速度更新效果持续时间
            effect['duration'] -= time_delta
            if effect['duration'] <= 0:
                monster.effects.remove(effect)

        if monster in game_state['monsters']:  # 确保怪物仍然存在
            if monster.move(time_delta):  # 返回True表示到达终点
                game_state['monsters'].remove(monster)
                # 添加生命损失效果
                add_notification(f"损失 {monster.damage} 生命值!", (255, 100, 100))
                game_state['camera_shake'] = 10

    # 更新塔状态和发射投射物
    for tower in game_state['towers']:
        new_projectiles = tower.fire(current_time, game_state['monsters'])
        game_state['projectiles'].extend(new_projectiles)

    # 更新投射物状态
    for projectile in game_state['projectiles'][:]:
        if projectile.move():  # 返回True表示需要移除
            game_state['projectiles'].remove(projectile)

    # 怪物生成
    if game_state['wave_active'] and game_state['current_wave_monsters']:
        # 按游戏速度调整生成延迟
        spawn_delay = game_state['spawn_delay'] / speed_multipliers[game_state['speed_level']]
        if current_time - game_state['last_spawn_time'] >= spawn_delay:
            spawn_monster()
            game_state['last_spawn_time'] = current_time

    # 检查是否完成一波
    if game_state['wave_active'] and not game_state['current_wave_monsters'] and not game_state['monsters']:
        game_state['wave_active'] = False
        player_resources['wave'] += 1

        # 添加完成波次通知
        if player_resources['wave'] < len(WAVES):
            add_notification(f"第 {player_resources['wave']} 波完成!", (100, 255, 100))
            # 给予波次奖励
            bonus = 50 + player_resources['wave'] * 10
            player_resources['gold'] += bonus
            add_notification(f"获得奖励: {bonus} 金币", (255, 220, 100))
        else:
            # 所有波次完成
            game_state['victory'] = True


# 新增辅助函数
def update_background_particles():
    """更新背景粒子效果"""
    # 随机生成新的背景粒子
    if random.random() < 0.05 and len(game_state['background_particles']) < 50:
        particle = {
            'position': [random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)],
            'color': (
            random.randint(180, 255), random.randint(180, 255), random.randint(180, 255), random.randint(20, 80)),
            'size': random.randint(1, 3),
            'life': random.randint(50, 200),
            'velocity': [random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)]
        }
        game_state['background_particles'].append(particle)

    # 更新现有粒子
    for particle in game_state['background_particles'][:]:
        particle['position'][0] += particle['velocity'][0]
        particle['position'][1] += particle['velocity'][1]
        particle['life'] -= 1

        if particle['life'] <= 0:
            game_state['background_particles'].remove(particle)


def add_damage_number(position, damage, damage_type):
    """添加伤害数字特效"""
    if damage_type == 'burn':
        color = (255, 100, 50)
    elif damage_type == 'poison':
        color = (180, 100, 180)
    else:
        color = (255, 50, 50)

    game_state['effects'].append({
        'type': 'damage_number',
        'position': list(position),
        'value': int(damage),
        'color': color,
        'velocity': [random.uniform(-0.5, 0.5), -1.5],
        'life': 40
    })


def add_gold_effect(position, amount):
    """添加金币获取特效"""
    game_state['effects'].append({
        'type': 'gold_reward',
        'position': list(position),
        'value': amount,
        'velocity': [0, -1],
        'life': 60
    })

    # 添加闪光粒子
    for _ in range(5):
        angle = random.random() * math.pi * 2
        speed = random.uniform(0.5, 2)
        game_state['effects'].append({
            'type': 'gold_particle',
            'position': list(position),
            'velocity': [math.cos(angle) * speed, math.sin(angle) * speed],
            'size': random.randint(2, 4),
            'life': random.randint(20, 40)
        })


def add_death_effect(monster):
    """添加怪物死亡特效"""
    position = monster.position
    monster_size = monster.size

    # 根据怪物类型创建不同颜色的粒子
    base_color = monster.color

    for _ in range(15):
        angle = random.random() * math.pi * 2
        speed = random.uniform(1, 3)
        size = random.randint(2, max(3, monster_size // 3))
        life = random.randint(20, 50)

        # 随机调整颜色
        color_variance = 30
        color = (
            max(0, min(255, base_color[0] + random.randint(-color_variance, color_variance))),
            max(0, min(255, base_color[1] + random.randint(-color_variance, color_variance))),
            max(0, min(255, base_color[2] + random.randint(-color_variance, color_variance))),
            255
        )

        game_state['effects'].append({
            'type': 'death_particle',
            'position': list(position),
            'velocity': [math.cos(angle) * speed, math.sin(angle) * speed],
            'size': size,
            'color': color,
            'life': life,
            'gravity': 0.1
        })


def update_notifications():
    """更新屏幕通知"""
    for notification in game_state['notifications'][:]:
        notification['life'] -= 1
        notification['position'][1] -= 0.5  # 向上移动

        if notification['life'] <= 0:
            game_state['notifications'].remove(notification)


def add_notification(text, color=(255, 255, 255)):
    """添加屏幕通知"""
    game_state['notifications'].append({
        'text': text,
        'color': color,
        'position': [WINDOW_WIDTH // 2, WINDOW_HEIGHT - 150],
        'life': 120  # 显示2秒
    })


def draw_game():
    # 计算镜头抖动偏移
    shake_offset = (0, 0)
    if game_state['camera_shake'] > 0:
        shake_offset = (
            random.randint(-3, 3) * game_state['camera_shake'] / 10,
            random.randint(-3, 3) * game_state['camera_shake'] / 10
        )

    # 绘制背景（草地格子）
    tile_size = 30
    for y in range(0, WINDOW_HEIGHT, tile_size):
        for x in range(0, WINDOW_WIDTH, tile_size):
            window.blit(game_resources['map_tiles']['grass'],
                        (int(x + shake_offset[0]), int(y + shake_offset[1])))

    # 绘制背景粒子
    for particle in game_state['background_particles']:
        pygame.draw.circle(
            window,
            particle['color'],
            (int(particle['position'][0] + shake_offset[0]),
             int(particle['position'][1] + shake_offset[1])),
            particle['size']
        )

    # 绘制路径
    path_width = 30
    for i in range(len(PATH) - 1):
        # 计算路径段的方向和长度
        start_x, start_y = PATH[i]
        end_x, end_y = PATH[i + 1]

        # 计算路径段的方向
        dx = end_x - start_x
        dy = end_y - start_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # 绘制路径段（使用瓦片而不是线条）
        steps = int(distance / path_width) + 1
        for step in range(steps):
            progress = step / steps
            x = start_x + dx * progress
            y = start_y + dy * progress
            window.blit(
                game_resources['map_tiles']['path'],
                (int(x - path_width // 2 + shake_offset[0]),
                 int(y - path_width // 2 + shake_offset[1]))
            )

    # 绘制特效层
    for effect in game_state['effects'][:]:
        if effect['type'] in ['explosion', 'freeze', 'poison_cloud']:
            # 动画特效
            if effect['frame'] < effect['max_frames']:
                effect_image = game_resources['effects'][effect['type']][effect['frame']]
                window.blit(
                    effect_image,
                    (int(effect['position'][0] - effect_image.get_width() // 2 + shake_offset[0]),
                     int(effect['position'][1] - effect_image.get_height() // 2 + shake_offset[1]))
                )
                effect['frame'] += 1
            else:
                game_state['effects'].remove(effect)

        elif effect['type'] == 'hit':
            # 简单的击中闪光
            if effect['frame'] < effect['max_frames']:
                radius = 10 - effect['frame'] // 2
                if effect['damage_type'] == 'fire':
                    colors = [(255, 100, 0, 150 - 15 * effect['frame']),
                              (255, 200, 0, 100 - 10 * effect['frame'])]
                elif effect['damage_type'] == 'ice':
                    colors = [(100, 200, 255, 150 - 15 * effect['frame']),
                              (200, 240, 255, 100 - 10 * effect['frame'])]
                elif effect['damage_type'] == 'lightning':
                    colors = [(255, 255, 0, 150 - 15 * effect['frame']),
                              (255, 255, 180, 100 - 10 * effect['frame'])]
                elif effect['damage_type'] == 'poison':
                    colors = [(150, 70, 150, 150 - 15 * effect['frame']),
                              (180, 100, 180, 100 - 10 * effect['frame'])]
                else:
                    colors = [(200, 200, 200, 150 - 15 * effect['frame']),
                              (255, 255, 255, 100 - 10 * effect['frame'])]

                # 创建一个透明表面来绘制发光效果
                hit_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
                pygame.draw.circle(hit_surf, colors[0], (radius * 2, radius * 2), radius * 2)
                pygame.draw.circle(hit_surf, colors[1], (radius * 2, radius * 2), radius)

                window.blit(
                    hit_surf,
                    (int(effect['position'][0] - radius * 2 + shake_offset[0]),
                     int(effect['position'][1] - radius * 2 + shake_offset[1]))
                )

                effect['frame'] += 1
            else:
                game_state['effects'].remove(effect)

        elif effect['type'] == 'upgrade':
            # 升级特效 - 向上升起的星星
            if effect['frame'] < effect['max_frames']:
                for i in range(5):
                    angle = math.pi * 2 * i / 5 + effect['frame'] / 10
                    radius = 20 - effect['frame'] / 2
                    x = effect['position'][0] + radius * math.cos(angle)
                    y = effect['position'][1] - effect['frame'] - radius * math.sin(angle)

                    # 星星大小和透明度随帧递减
                    size = 5 - effect['frame'] / 5
                    alpha = 255 - effect['frame'] * 12

                    # 绘制星星
                    star_points = []
                    for j in range(5):
                        star_angle = math.pi / 2 + j * 2 * math.pi / 5
                        star_points.append((
                            x + size * math.cos(star_angle),
                            y + size * math.sin(star_angle)
                        ))
                        star_angle += math.pi / 5
                        star_points.append((
                            x + size / 2 * math.cos(star_angle),
                            y + size / 2 * math.sin(star_angle)
                        ))

                    if len(star_points) >= 3:  # 确保有足够的点
                        # 创建一个透明表面来绘制带透明度的星星
                        star_surf = pygame.Surface((int(size * 4), int(size * 4)), pygame.SRCALPHA)
                        # 调整点的坐标以适应新表面
                        adjusted_points = [(p[0] - x + size * 2, p[1] - y + size * 2) for p in star_points]
                        pygame.draw.polygon(star_surf, (255, 220, 0, alpha), adjusted_points)
                        window.blit(
                            star_surf,
                            (int(x - size * 2 + shake_offset[0]), int(y - size * 2 + shake_offset[1]))
                        )

                effect['frame'] += 1
            else:
                game_state['effects'].remove(effect)

        elif effect['type'] == 'damage_number':
            # 伤害数字特效
            effect['position'][0] += effect['velocity'][0]
            effect['position'][1] += effect['velocity'][1]
            effect['life'] -= 1

            if effect['life'] > 0:
                # 计算透明度，使其在生命周期结束时淡出
                alpha = min(255, int(effect['life'] * 6))
                text_color = effect['color'] + (alpha,)

                # 渲染伤害数字
                damage_text = game_resources['fonts']['small'].render(
                    str(effect['value']), True, text_color
                )

                window.blit(
                    damage_text,
                    (int(effect['position'][0] - damage_text.get_width() // 2 + shake_offset[0]),
                     int(effect['position'][1] + shake_offset[1]))
                )
            else:
                game_state['effects'].remove(effect)

        elif effect['type'] == 'gold_reward':
            # 金币获取特效
            effect['position'][0] += effect['velocity'][0]
            effect['position'][1] += effect['velocity'][1]
            effect['life'] -= 1

            if effect['life'] > 0:
                # 计算透明度，使其在生命周期结束时淡出
                alpha = min(255, int(effect['life'] * 4))
                # 淡入效果
                alpha = min(alpha, (60 - effect['life']) * 10) if effect['life'] > 50 else alpha

                # 渲染金币文本
                gold_text = game_resources['fonts']['medium'].render(
                    f"+{effect['value']}", True, (255, 220, 50, alpha)
                )

                # 添加闪光效果
                glow_surf = pygame.Surface(
                    (gold_text.get_width() + 10, gold_text.get_height() + 6),
                    pygame.SRCALPHA
                )
                glow_surf.fill((255, 220, 50, alpha // 4))

                window.blit(
                    glow_surf,
                    (int(effect['position'][0] - glow_surf.get_width() // 2 + shake_offset[0]),
                     int(effect['position'][1] - 3 + shake_offset[1]))
                )

                window.blit(
                    gold_text,
                    (int(effect['position'][0] - gold_text.get_width() // 2 + shake_offset[0]),
                     int(effect['position'][1] + shake_offset[1]))
                )
            else:
                game_state['effects'].remove(effect)

        elif effect['type'] == 'gold_particle':
            # 金币粒子特效
            effect['position'][0] += effect['velocity'][0]
            effect['position'][1] += effect['velocity'][1]
            effect['life'] -= 1

            if effect['life'] > 0:
                alpha = min(255, effect['life'] * 6)
                pygame.draw.circle(
                    window,
                    (255, 220, 50, alpha),
                    (int(effect['position'][0] + shake_offset[0]),
                     int(effect['position'][1] + shake_offset[1])),
                    effect['size']
                )
            else:
                game_state['effects'].remove(effect)

        elif effect['type'] == 'death_particle':
            # 死亡粒子特效
            effect['velocity'][1] += effect['gravity']  # 添加重力效果
            effect['position'][0] += effect['velocity'][0]
            effect['position'][1] += effect['velocity'][1]
            effect['life'] -= 1

            if effect['life'] > 0:
                alpha = min(255, effect['life'] * 6)
                color = effect['color'][:3] + (alpha,)

                pygame.draw.circle(
                    window,
                    color,
                    (int(effect['position'][0] + shake_offset[0]),
                     int(effect['position'][1] + shake_offset[1])),
                    max(1, int(effect['size'] * effect['life'] / effect['life'] * 0.8))
                )
            else:
                game_state['effects'].remove(effect)

    # 绘制塔
    for tower in game_state['towers']:
        tower.draw(window, tower == game_state['selected_tower'])

    # 绘制投射物
    for projectile in game_state['projectiles']:
        projectile.draw(window)

    # 绘制怪物
    for monster in game_state['monsters']:
        monster.draw(window)

    # 绘制通知消息
    for notification in game_state['notifications']:
        # 计算透明度
        alpha = min(255, notification['life'] * 2)
        # 对于新消息，淡入效果
        alpha = min(alpha, (120 - notification['life']) * 10) if notification['life'] > 100 else alpha

        # 准备文本颜色，添加透明度
        color = notification['color'] + (alpha,)

        # 渲染文本
        text = game_resources['fonts']['large'].render(notification['text'], True, color)

        # 添加发光背景
        glow_surf = pygame.Surface((text.get_width() + 20, text.get_height() + 10), pygame.SRCALPHA)
        glow_color = (notification['color'][0] // 2, notification['color'][1] // 2,
                      notification['color'][2] // 2, alpha // 4)
        pygame.draw.rect(glow_surf, glow_color,
                         (0, 0, text.get_width() + 20, text.get_height() + 10),
                         border_radius=10)

        # 绘制消息
        window.blit(glow_surf,
                    (notification['position'][0] - text.get_width() // 2 - 10,
                     notification['position'][1] - text.get_height() // 2 - 5))

        window.blit(text,
                    (notification['position'][0] - text.get_width() // 2,
                     notification['position'][1] - text.get_height() // 2))

    # 绘制UI
    draw_ui()

    # 绘制塔选择界面
    if game_state['selected_tower_type']:
        mouse_pos = pygame.mouse.get_pos()

        # 获取塔图像
        tower_image = game_resources['towers'][game_state['selected_tower_type']]

        if can_place_tower(mouse_pos):
            # 显示塔的预览和范围
            window.blit(tower_image,
                        (mouse_pos[0] - tower_image.get_width() // 2,
                         mouse_pos[1] - tower_image.get_height() // 2))

            # 绘制半透明范围指示器
            range_radius = TOWER_TYPES[game_state['selected_tower_type']]['range']
            range_surface = pygame.Surface((range_radius * 2, range_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(range_surface, (200, 200, 200, 40), (range_radius, range_radius), range_radius)
            pygame.draw.circle(range_surface, (255, 255, 255, 80), (range_radius, range_radius), range_radius, 2)
            window.blit(range_surface, (mouse_pos[0] - range_radius, mouse_pos[1] - range_radius))

            # 添加提示信息
            tower_type = game_state['selected_tower_type']
            tower_desc = TOWER_TYPES[tower_type]['description']
            tower_cost = TOWER_TYPES[tower_type]['cost']

            tooltip_text = f"{tower_type.capitalize()} - {tower_cost}金币"
            tooltip_desc = tower_desc

            # 创建提示文本
            text1 = game_resources['fonts']['medium'].render(tooltip_text, True, (255, 255, 255))
            text2 = game_resources['fonts']['small'].render(tooltip_desc, True, (220, 220, 220))

            # 计算提示框大小
            tooltip_width = max(text1.get_width(), text2.get_width()) + 20
            tooltip_height = text1.get_height() + text2.get_height() + 15

            # 创建提示背景
            tooltip_x = min(mouse_pos[0] + 20, WINDOW_WIDTH - tooltip_width - 10)
            tooltip_y = min(mouse_pos[1] - tooltip_height - 10, WINDOW_HEIGHT - tooltip_height - 10)

            tooltip_bg = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
            tooltip_bg.fill((0, 0, 0, 200))
            window.blit(tooltip_bg, (tooltip_x, tooltip_y))

            # 绘制边框
            pygame.draw.rect(window, (100, 100, 100),
                             (tooltip_x, tooltip_y, tooltip_width, tooltip_height),
                             1, border_radius=5)

            # 绘制文本
            window.blit(text1, (tooltip_x + 10, tooltip_y + 5))
            window.blit(text2, (tooltip_x + 10, tooltip_y + text1.get_height() + 10))

        else:
            # 显示无法放置的提示
            invalid_tower = tower_image.copy()
            invalid_tower.fill((200, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)
            window.blit(invalid_tower,
                        (mouse_pos[0] - tower_image.get_width() // 2,
                         mouse_pos[1] - tower_image.get_height() // 2))

            # 显示无法放置的提示文本
            text = game_resources['fonts']['small'].render("无法放置", True, (255, 50, 50))
            text_x = mouse_pos[0] - text.get_width() // 2
            text_y = mouse_pos[1] - tower_image.get_height() // 2 - 20
            # 文本背景
            text_bg = pygame.Surface((text.get_width() + 10, text.get_height() + 6), pygame.SRCALPHA)
            text_bg.fill((0, 0, 0, 180))
            window.blit(text_bg, (text_x - 5, text_y - 3))
            window.blit(text, (text_x, text_y))

    # 绘制侧边栏（选中塔的详细信息）
    if game_state['sidebar_active'] and game_state['selected_tower']:
        draw_sidebar()

    # 绘制游戏结束/胜利画面
    if game_state['game_over']:
        draw_game_over()
    elif game_state['victory']:
        draw_victory()

    pygame.display.update()


def draw_ui():
    # 使用UI主题色
    ui_theme = game_state['ui_theme']

    # 绘制顶部状态栏 - 使用主题背景色
    info_bar_height = 40
    info_bar = pygame.Surface((WINDOW_WIDTH, info_bar_height), pygame.SRCALPHA)
    info_bar.fill((ui_theme['background'][0], ui_theme['background'][1], ui_theme['background'][2], 230))
    window.blit(info_bar, (0, 0))

    # 添加渐变和玻璃质感
    gradient = pygame.Surface((WINDOW_WIDTH, info_bar_height), pygame.SRCALPHA)
    for i in range(info_bar_height):
        alpha = int(40 - i * 30 / info_bar_height)
        pygame.draw.line(gradient, (255, 255, 255, alpha), (0, i), (WINDOW_WIDTH, i))
    window.blit(gradient, (0, 0))

    # 顶部边框线
    pygame.draw.line(window, (ui_theme['secondary'][0], ui_theme['secondary'][1], ui_theme['secondary'][2], 150),
                     (0, info_bar_height - 1), (WINDOW_WIDTH, info_bar_height - 1), 2)

    # 计算资源图标和文本位置
    resource_spacing = 140
    icon_text_gap = 5
    base_x = 20
    base_y = 12

    def clamp_color(color):
        """Ensure color values stay within valid range (0-255)"""
        if len(color) == 3:
            return (
                max(0, min(255, int(color[0]))),
                max(0, min(255, int(color[1]))),
                max(0, min(255, int(color[2])))
            )
        elif len(color) == 4:  # Handle colors with alpha channel
            return (
                max(0, min(255, int(color[0]))),
                max(0, min(255, int(color[1]))),
                max(0, min(255, int(color[2]))),
                max(0, min(255, int(color[3])))
            )
        return color

    # 创建流光动画效果的函数
    def draw_glow_text(text, position, color, glow_color, shadow=True):
        x, y = position
        # 先渲染文本
        text_surf = game_resources['fonts']['medium'].render(text, True, color)

        # 应用脉动效果
        pulse = (math.sin(game_state['ui_animation_time'] * 3) + 1) * 0.5  # 0到1之间的脉动值

        # 渐变闪光效果
        glow_alpha = int(50 + 80 * pulse)
        glow_surf = pygame.Surface((text_surf.get_width() + 8, text_surf.get_height() + 4), pygame.SRCALPHA)
        glow_rect = pygame.Rect(4, 2, text_surf.get_width(), text_surf.get_height())
        glow_color = (glow_color[0], glow_color[1], glow_color[2], glow_alpha)
        pygame.draw.rect(glow_surf, glow_color, glow_rect, border_radius=4)
        window.blit(glow_surf, (x - 4, y - 2))

        # 阴影效果
        if shadow:
            shadow_text = game_resources['fonts']['medium'].render(text, True, (0, 0, 0, 180))
            window.blit(shadow_text, (x + 1, y + 1))

        # 主文本
        window.blit(text_surf, (x, y))


    # 绘制金币资源
    coin_icon = game_resources['ui']['coin']
    window.blit(coin_icon, (base_x, base_y))
    # 使用主题强调色作为金币文本色
    draw_glow_text(str(player_resources['gold']), (base_x + coin_icon.get_width() + icon_text_gap, base_y),
                   ui_theme['accent'], (ui_theme['accent'][0] // 2, ui_theme['accent'][1] // 2, 0))

    # 绘制生命资源
    heart_icon = game_resources['ui']['heart']
    window.blit(heart_icon, (base_x + resource_spacing, base_y))
    # 根据生命值变化色彩（低生命值为红色警告）
    if player_resources['lives'] <= 5:
        lives_color = ui_theme['danger']
        glow_color = (ui_theme['danger'][0] // 2, 0, 0)
    else:
        lives_color = (255, 150, 150)
        glow_color = (120, 30, 30)
    draw_glow_text(str(player_resources['lives']),
                   (base_x + resource_spacing + heart_icon.get_width() + icon_text_gap, base_y),
                   lives_color, glow_color)

    # 绘制波次信息
    wave_icon = game_resources['ui']['wave']
    window.blit(wave_icon, (base_x + resource_spacing * 2, base_y))
    # 使用主题信息色作为波次文本色
    draw_glow_text(f"{player_resources['wave'] + 1}/{len(WAVES)}",
                   (base_x + resource_spacing * 2 + wave_icon.get_width() + icon_text_gap, base_y),
                   ui_theme['info'], (0, 60, 120))

    # 绘制分数信息
    score_icon = game_resources['ui']['score']
    window.blit(score_icon, (base_x + resource_spacing * 3, base_y))
    draw_glow_text(str(player_resources['score']),
                   (base_x + resource_spacing * 3 + score_icon.get_width() + icon_text_gap, base_y),
                   (255, 255, 150), (100, 100, 0))

    # 绘制加速按钮
    speed_button_width = 90
    speed_button_x = WINDOW_WIDTH - speed_button_width - 140  # 放在下一波按钮左侧
    speed_button_y = 5

    # 设置按钮颜色（根据速度等级）
    speed_colors = [
        clamp_color(ui_theme['primary']),  # 正常速度
        clamp_color(ui_theme['info']),  # 2倍速
        clamp_color((100, 100, 220))  # 3倍速
    ]
    speed_hover_colors = [
        clamp_color((ui_theme['primary'][0] + 40, ui_theme['primary'][1] + 40, ui_theme['primary'][2] + 40)),
        clamp_color((ui_theme['info'][0] + 40, ui_theme['info'][1] + 40, ui_theme['info'][2] + 40)),
        clamp_color((140, 140, 255))
    ]

    speed_level = game_state['speed_level']
    button_color = speed_colors[speed_level]
    button_hover_color = speed_hover_colors[speed_level]
    speed_texts = ["正常速度", "2倍速", "3倍速"]

    # 创建按钮
    speed_button = Button(
        speed_button_x,
        speed_button_y,
        speed_button_width,
        30,
        speed_texts[speed_level],
        button_color,
        button_hover_color
    )
    speed_button.check_hover(pygame.mouse.get_pos())
    speed_button.draw(window)

    # 如果加速状态激活，添加额外的视觉指示
    if game_state['speed_level'] > 0:
        # 绘制动态指示器
        pulse = (math.sin(game_state['ui_animation_time'] * 5) + 1) * 0.5  # 0到1之间快速脉动

        # 速度指示图标
        speed_text = game_resources['fonts']['medium'].render(f"{game_state['speed_level'] + 1}x", True,
                                                              (220 + int(pulse * 35), 220 + int(pulse * 35), 255))

        # 绘制光晕效果
        glow_surf = pygame.Surface((speed_text.get_width() + 10, speed_text.get_height() + 6), pygame.SRCALPHA)
        glow_color = (120, 140, 255, int(50 + 80 * pulse))
        pygame.draw.rect(glow_surf, glow_color, (0, 0, speed_text.get_width() + 10, speed_text.get_height() + 6),
                         border_radius=8)
        window.blit(glow_surf, (speed_button_x + speed_button_width + 2, speed_button_y + 2))

        # 显示速度指示文本
        window.blit(speed_text, (speed_button_x + speed_button_width + 7, speed_button_y + 5))

    # 绘制底部塔选择栏
    tower_bar_height = 70
    tower_bar = pygame.Surface((WINDOW_WIDTH, tower_bar_height), pygame.SRCALPHA)
    tower_bar.fill((ui_theme['background'][0], ui_theme['background'][1], ui_theme['background'][2], 230))
    window.blit(tower_bar, (0, WINDOW_HEIGHT - tower_bar_height))

    # 添加渐变效果
    gradient = pygame.Surface((WINDOW_WIDTH, tower_bar_height), pygame.SRCALPHA)
    for i in range(tower_bar_height):
        alpha = int(i * 30 / tower_bar_height)
        pygame.draw.line(gradient, (255, 255, 255, alpha), (0, i), (WINDOW_WIDTH, i))
    window.blit(gradient, (0, WINDOW_HEIGHT - tower_bar_height))

    # 顶部边框线
    pygame.draw.line(window, (ui_theme['secondary'][0], ui_theme['secondary'][1], ui_theme['secondary'][2], 150),
                     (0, WINDOW_HEIGHT - tower_bar_height), (WINDOW_WIDTH, WINDOW_HEIGHT - tower_bar_height), 2)

    # 绘制塔选择标题
    title_text = game_resources['fonts']['medium'].render("防御塔:", True, ui_theme['text'])
    window.blit(title_text, (15, WINDOW_HEIGHT - tower_bar_height + 8))

    # 绘制塔按钮
    # 计算按钮的合适位置 - 均匀分布在底部栏
    total_towers = len(TOWER_TYPES)
    button_width = 110
    button_spacing = 10
    total_width = total_towers * button_width + (total_towers - 1) * button_spacing
    start_x = (WINDOW_WIDTH - total_width) / 2

    y_pos = WINDOW_HEIGHT - tower_bar_height + 15

    for i, (tower_type, properties) in enumerate(TOWER_TYPES.items()):
        # 确定按钮位置
        x_pos = start_x + i * (button_width + button_spacing)

        # 确定按钮颜色
        if player_resources['gold'] >= properties['cost']:
            color = ui_theme['success']
            hover_color = (ui_theme['success'][0] + 40, ui_theme['success'][1] + 40, ui_theme['success'][2] + 40)
        else:
            color = ui_theme['danger']
            hover_color = (ui_theme['danger'][0] + 40, ui_theme['danger'][1] + 40, ui_theme['danger'][2] + 40)

        # 创建按钮文本
        button_text = f"{tower_type}\n{properties['cost']}金"

        # 创建并绘制按钮
        tower_button = Button(x_pos, y_pos, button_width, 40, button_text, color, hover_color)
        tower_button.check_hover(pygame.mouse.get_pos())
        tower_button.draw(window)

        # 绘制塔图标
        tower_image = game_resources['towers'][tower_type]
        tower_scale = 0.8
        scaled_tower = pygame.transform.scale(
            tower_image,
            (int(tower_image.get_width() * tower_scale),
             int(tower_image.get_height() * tower_scale))
        )
        window.blit(scaled_tower,
                    (x_pos + button_width // 2 - scaled_tower.get_width() // 2,
                     y_pos - scaled_tower.get_height() // 2 - 10))

    # 绘制波次控制按钮
    if not game_state['wave_active'] and not game_state['current_wave_monsters']:
        # 创建闪烁效果 - 脉动颜色和大小
        pulse = (math.sin(game_state['ui_animation_time'] * 3) + 1) * 0.5  # 0到1的脉动值
        button_color = clamp_color((
            ui_theme['success'][0] + pulse * 50,
            ui_theme['success'][1] + pulse * 50,
            ui_theme['success'][2] + pulse * 20
        ))

        button_size = 120 + int(pulse * 10)

        wave_button = Button(
            WINDOW_WIDTH - button_size - 10,
            5,
            button_size,
            30,
            "开始下一波",
            button_color,
            clamp_color((button_color[0] + 30, button_color[1] + 30, button_color[2] + 30)),
            icon="wave"
        )
        wave_button.check_hover(pygame.mouse.get_pos())
        wave_button.draw(window)

        # 添加一个提示光晕
        glow_surf = pygame.Surface((button_size + 20, 40), pygame.SRCALPHA)
        glow_color = (ui_theme['accent'][0], ui_theme['accent'][1], 50, int(50 + 50 * pulse))
        pygame.draw.rect(glow_surf, glow_color, (0, 0, button_size + 20, 40), border_radius=10)
        window.blit(glow_surf, (WINDOW_WIDTH - button_size - 20, 0))


def draw_sidebar():
    tower = game_state['selected_tower']
    sidebar_width = 230
    sidebar_rect = pygame.Rect(WINDOW_WIDTH - sidebar_width, 40, sidebar_width, WINDOW_HEIGHT - 110)

    # 绘制半透明背景层
    sidebar_bg = pygame.Surface((sidebar_width, WINDOW_HEIGHT - 110), pygame.SRCALPHA)
    sidebar_bg.fill((20, 20, 40, 220))
    window.blit(sidebar_bg, (WINDOW_WIDTH - sidebar_width, 40))

    # 绘制装饰边框
    pygame.draw.rect(window, (100, 100, 150), sidebar_rect, 2, border_radius=10)
    pygame.draw.line(window, (100, 100, 150),
                     (sidebar_rect.left + 10, sidebar_rect.top + 40),
                     (sidebar_rect.right - 10, sidebar_rect.top + 40),
                     2)

    # 添加顶部高光
    highlight = pygame.Surface((sidebar_width - 4, 8), pygame.SRCALPHA)
    highlight.fill((255, 255, 255, 30))
    window.blit(highlight, (WINDOW_WIDTH - sidebar_width + 2, 42))

    # 绘制标题
    title_text = game_resources['fonts']['large'].render(f"{tower.type} 塔", True, (220, 220, 255))
    title_shadow = game_resources['fonts']['large'].render(f"{tower.type} 塔", True, (0, 0, 0))
    title_x = sidebar_rect.centerx - title_text.get_width() // 2
    window.blit(title_shadow, (title_x + 2, sidebar_rect.top + 8 + 2))
    window.blit(title_text, (title_x, sidebar_rect.top + 8))

    # 显示塔图像
    tower_image = game_resources['towers'][tower.type]
    tower_x = sidebar_rect.centerx - tower_image.get_width() // 2
    tower_y = sidebar_rect.top + 55
    window.blit(tower_image, (tower_x, tower_y))

    # 绘制星级
    if tower.upgrade_level > 0:
        stars_width = 25 * tower.upgrade_level
        stars_x = sidebar_rect.centerx - stars_width // 2
        stars_y = tower_y + tower_image.get_height() + 5

        for i in range(tower.upgrade_level):
            # 绘制星星
            star_points = []
            for j in range(5):
                angle = math.pi / 2 + j * 2 * math.pi / 5
                star_points.append((
                    stars_x + i * 25 + 12 + 10 * math.cos(angle),
                    stars_y + 12 + 10 * math.sin(angle)
                ))
                angle += math.pi / 5
                star_points.append((
                    stars_x + i * 25 + 12 + 5 * math.cos(angle),
                    stars_y + 12 + 5 * math.sin(angle)
                ))

            # 绘制星星发光效果
            glow_surf = pygame.Surface((25, 25), pygame.SRCALPHA)
            pygame.draw.polygon(glow_surf, (255, 255, 150, 80),
                                [(p[0] - stars_x - i * 25, p[1] - stars_y) for p in star_points])
            window.blit(glow_surf, (stars_x + i * 25, stars_y - 2))

            # 绘制实际星星
            pygame.draw.polygon(window, (255, 220, 0), star_points)
            pygame.draw.polygon(window, (180, 150, 0), star_points, 1)

    # 信息内容起始位置
    y_pos = tower_y + tower_image.get_height() + 35
    if tower.upgrade_level > 0:
        y_pos += 25

    # 创建属性面板背景
    panel_height = 120
    panel_rect = pygame.Rect(sidebar_rect.left + 10, y_pos, sidebar_width - 20, panel_height)
    panel_bg = pygame.Surface((sidebar_width - 20, panel_height), pygame.SRCALPHA)
    panel_bg.fill((50, 50, 70, 180))
    window.blit(panel_bg, (panel_rect.left, panel_rect.top))
    pygame.draw.rect(window, (100, 100, 130), panel_rect, 2, border_radius=5)

    # 添加属性面板标题
    panel_title = game_resources['fonts']['medium'].render("塔属性", True, (220, 220, 255))
    window.blit(panel_title, (panel_rect.centerx - panel_title.get_width() // 2, panel_rect.top + 5))
    pygame.draw.line(window, (100, 100, 150),
                     (panel_rect.left + 10, panel_rect.top + 25),
                     (panel_rect.right - 10, panel_rect.top + 25),
                     1)

    # 显示属性信息
    prop_x = panel_rect.left + 15
    prop_y = panel_rect.top + 35
    prop_spacing = 20

    # 伤害和伤害类型
    damage_icon = "❯"
    damage_text = game_resources['fonts']['medium'].render(
        f"{damage_icon} 伤害: {tower.damage} ({tower.damage_type})",
        True, (255, 200, 200)
    )
    window.blit(damage_text, (prop_x, prop_y))
    prop_y += prop_spacing

    # 射程
    range_icon = "◎"
    range_text = game_resources['fonts']['medium'].render(
        f"{range_icon} 射程: {tower.range}",
        True, (200, 255, 200)
    )
    window.blit(range_text, (prop_x, prop_y))
    prop_y += prop_spacing

    # 攻击速度
    speed_icon = "⟳"
    rate_text = game_resources['fonts']['medium'].render(
        f"{speed_icon} 攻击间隔: {tower.fire_rate:.1f}秒",
        True, (200, 200, 255)
    )
    window.blit(rate_text, (prop_x, prop_y))
    prop_y += prop_spacing

    # 特殊能力
    if tower.special_ability:
        ability_icon = "✧"
        ability_name = tower.special_ability
        if ability_name == 'slow':
            ability_display = "减速"
            ability_color = (150, 220, 255)
        elif ability_name == 'burn':
            ability_display = "灼烧"
            ability_color = (255, 150, 100)
        elif ability_name == 'chain':
            ability_display = "链式攻击"
            ability_color = (255, 255, 150)
        elif ability_name == 'poison':
            ability_display = "中毒"
            ability_color = (200, 150, 255)
        else:
            ability_display = ability_name
            ability_color = (255, 255, 255)

        ability_text = game_resources['fonts']['medium'].render(
            f"{ability_icon} 特殊能力: {ability_display}",
            True, ability_color
        )
        window.blit(ability_text, (prop_x, prop_y))

    # 升级区域
    y_pos = panel_rect.bottom + 15

    if tower.upgrade_level < tower.max_upgrade_level:
        # 创建升级面板背景
        upgrade_panel_height = 110
        upgrade_rect = pygame.Rect(sidebar_rect.left + 10, y_pos, sidebar_width - 20, upgrade_panel_height)
        upgrade_bg = pygame.Surface((sidebar_width - 20, upgrade_panel_height), pygame.SRCALPHA)
        upgrade_bg.fill((50, 70, 50, 180))
        window.blit(upgrade_bg, (upgrade_rect.left, upgrade_rect.top))
        pygame.draw.rect(window, (100, 130, 100), upgrade_rect, 2, border_radius=5)

        # 升级标题
        upgrade_title = game_resources['fonts']['medium'].render("升级信息", True, (220, 255, 220))
        window.blit(upgrade_title, (upgrade_rect.centerx - upgrade_title.get_width() // 2, upgrade_rect.top + 5))
        pygame.draw.line(window, (100, 150, 100),
                         (upgrade_rect.left + 10, upgrade_rect.top + 25),
                         (upgrade_rect.right - 10, upgrade_rect.top + 25),
                         1)

        # 升级信息
        info_x = upgrade_rect.left + 15
        info_y = upgrade_rect.top + 35

        upgrade_info = [
            {"text": f"+{tower.properties['upgrade']['damage_bonus']} 伤害", "color": (255, 200, 200)},
            {"text": f"+{tower.properties['upgrade']['range_bonus']} 射程", "color": (200, 255, 200)},
            {"text": f"-{tower.properties['upgrade']['fire_rate_bonus']:.1f} 攻击间隔", "color": (200, 200, 255)}
        ]

        for info in upgrade_info:
            info_text = game_resources['fonts']['medium'].render(info["text"], True, info["color"])
            window.blit(info_text, (info_x, info_y))
            info_y += 20

        # 升级按钮
        upgrade_cost = tower.properties['upgrade']['cost']
        if player_resources['gold'] >= upgrade_cost:
            upgrade_color = (80, 180, 80)
            hover_color = (120, 220, 120)
        else:
            upgrade_color = (150, 70, 70)
            hover_color = (200, 100, 100)

        upgrade_button = Button(
            upgrade_rect.centerx - 80,
            upgrade_rect.bottom - 35,
            160, 30,
            f"升级 ({upgrade_cost}金)",
            upgrade_color,
            hover_color
        )
        upgrade_button.check_hover(pygame.mouse.get_pos())
        upgrade_button.draw(window)

    else:
        # 已达最大等级提示
        max_label = game_resources['fonts']['medium'].render("已达到最大等级", True, (220, 220, 100))
        max_x = sidebar_rect.centerx - max_label.get_width() // 2
        window.blit(max_label, (max_x, y_pos + 10))

        # 添加最大等级装饰
        max_icon_size = 30
        max_icon_y = y_pos + 35

        # 左侧装饰
        pygame.draw.polygon(window, (220, 220, 100),
                            [(sidebar_rect.centerx - 60, max_icon_y),
                             (sidebar_rect.centerx - 40, max_icon_y - max_icon_size // 2),
                             (sidebar_rect.centerx - 20, max_icon_y),
                             (sidebar_rect.centerx - 40, max_icon_y + max_icon_size // 2)])

        # 右侧装饰
        pygame.draw.polygon(window, (220, 220, 100),
                            [(sidebar_rect.centerx + 60, max_icon_y),
                             (sidebar_rect.centerx + 40, max_icon_y - max_icon_size // 2),
                             (sidebar_rect.centerx + 20, max_icon_y),
                             (sidebar_rect.centerx + 40, max_icon_y + max_icon_size // 2)])

    # 出售按钮区域
    sell_value = int(sum([TOWER_TYPES[tower.type]['cost']] +
                         [TOWER_TYPES[tower.type]['upgrade']['cost']] * tower.upgrade_level) * 0.7)

    sell_button = Button(
        sidebar_rect.centerx - 80,
        sidebar_rect.bottom - 40,
        160, 30,
        f"出售 (+{sell_value}金)",
        (180, 60, 60),
        (220, 100, 100),
        icon="coin"
    )
    sell_button.check_hover(pygame.mouse.get_pos())
    sell_button.draw(window)


def draw_game_over():
    # 创建多层渐变背景
    overlay1 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay1.fill((50, 0, 0, 180))

    overlay2 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for i in range(WINDOW_HEIGHT):
        alpha = max(0, 150 - i * 150 / WINDOW_HEIGHT)
        pygame.draw.line(overlay2, (100, 0, 0, int(alpha)), (0, i), (WINDOW_WIDTH, i))

    window.blit(overlay1, (0, 0))
    window.blit(overlay2, (0, 0))

    # 创建游戏结束中央面板
    panel_width = 400
    panel_height = 300
    panel_x = WINDOW_WIDTH // 2 - panel_width // 2
    panel_y = WINDOW_HEIGHT // 2 - panel_height // 2

    # 面板背景
    panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel.fill((30, 30, 50, 230))
    window.blit(panel, (panel_x, panel_y))

    # 面板边框
    pygame.draw.rect(window, (100, 50, 50),
                     (panel_x, panel_y, panel_width, panel_height),
                     3, border_radius=10)

    # 面板内部装饰
    pygame.draw.line(window, (150, 50, 50),
                     (panel_x + 20, panel_y + 60),
                     (panel_x + panel_width - 20, panel_y + 60),
                     2)

    # 标题文本
    game_over_text = game_resources['fonts']['title'].render("游戏结束!", True, (255, 100, 100))
    game_over_shadow = game_resources['fonts']['title'].render("游戏结束!", True, (0, 0, 0))
    title_x = WINDOW_WIDTH // 2 - game_over_text.get_width() // 2
    title_y = panel_y + 15

    # 添加脉动效果
    pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) * 0.5  # 0到1之间的脉动值
    title_glow = pygame.Surface((game_over_text.get_width() + 20, game_over_text.get_height() + 20), pygame.SRCALPHA)
    glow_color = (255, 100, 100, int(100 * pulse))
    pygame.draw.rect(title_glow, glow_color,
                     (0, 0, game_over_text.get_width() + 20, game_over_text.get_height() + 20),
                     border_radius=10)
    window.blit(title_glow, (title_x - 10, title_y - 10))

    window.blit(game_over_shadow, (title_x + 2, title_y + 2))
    window.blit(game_over_text, (title_x, title_y))

    # 分数信息
    score_label = game_resources['fonts']['large'].render("最终分数", True, (200, 200, 255))
    score_text = game_resources['fonts']['large'].render(f"{player_resources['score']}", True, (255, 255, 255))

    score_label_x = WINDOW_WIDTH // 2 - score_label.get_width() // 2
    score_text_x = WINDOW_WIDTH // 2 - score_text.get_width() // 2

    window.blit(score_label, (score_label_x, panel_y + 90))
    window.blit(score_text, (score_text_x, panel_y + 130))

    # 波次信息
    wave_label = game_resources['fonts']['medium'].render(f"通过波次: {player_resources['wave']}/{len(WAVES)}",
                                                          True, (200, 200, 255))
    wave_x = WINDOW_WIDTH // 2 - wave_label.get_width() // 2
    window.blit(wave_label, (wave_x, panel_y + 170))

    # 创建重新开始按钮
    restart_button = Button(
        WINDOW_WIDTH // 2 - 75,
        panel_y + panel_height - 60,
        150, 40,
        "重新开始",
        (80, 100, 180),
        (120, 150, 230)
    )
    restart_button.check_hover(pygame.mouse.get_pos())
    restart_button.draw(window)

    # 添加装饰元素 - 破碎效果
    for _ in range(20):
        angle = random.random() * math.pi * 2
        distance = random.randint(panel_width // 2, panel_width)
        length = random.randint(20, 80)
        thickness = random.randint(1, 3)

        start_x = WINDOW_WIDTH // 2 + int(math.cos(angle) * distance)
        start_y = WINDOW_HEIGHT // 2 + int(math.sin(angle) * distance)
        end_x = start_x + int(math.cos(angle) * length)
        end_y = start_y + int(math.sin(angle) * length)

        color = (150 + random.randint(0, 100),
                 50 + random.randint(0, 50),
                 50 + random.randint(0, 50))

        pygame.draw.line(window, color, (start_x, start_y), (end_x, end_y), thickness)


def draw_victory():
    # 创建多层渐变背景
    overlay1 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay1.fill((0, 50, 0, 180))

    overlay2 = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for i in range(WINDOW_HEIGHT):
        alpha = max(0, 150 - i * 150 / WINDOW_HEIGHT)
        pygame.draw.line(overlay2, (0, 100, 0, int(alpha)), (0, i), (WINDOW_WIDTH, i))

    window.blit(overlay1, (0, 0))
    window.blit(overlay2, (0, 0))

    # 创建胜利中央面板
    panel_width = 400
    panel_height = 320
    panel_x = WINDOW_WIDTH // 2 - panel_width // 2
    panel_y = WINDOW_HEIGHT // 2 - panel_height // 2

    # 面板背景
    panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel.fill((30, 50, 30, 230))
    window.blit(panel, (panel_x, panel_y))

    # 面板边框
    pygame.draw.rect(window, (50, 150, 50),
                     (panel_x, panel_y, panel_width, panel_height),
                     3, border_radius=10)

    # 面板内部装饰
    pygame.draw.line(window, (80, 180, 80),
                     (panel_x + 20, panel_y + 70),
                     (panel_x + panel_width - 20, panel_y + 70),
                     2)

    # 标题文本
    victory_text = game_resources['fonts']['title'].render("胜利!", True, (100, 255, 100))
    victory_shadow = game_resources['fonts']['title'].render("胜利!", True, (0, 0, 0))
    title_x = WINDOW_WIDTH // 2 - victory_text.get_width() // 2
    title_y = panel_y + 15

    # 添加脉动发光效果
    pulse = (math.sin(pygame.time.get_ticks() / 200) + 1) * 0.5  # 0到1之间的脉动值
    title_glow = pygame.Surface((victory_text.get_width() + 30, victory_text.get_height() + 30), pygame.SRCALPHA)
    glow_color = (100, 255, 100, int(100 * pulse))
    pygame.draw.rect(title_glow, glow_color,
                     (0, 0, victory_text.get_width() + 30, victory_text.get_height() + 30),
                     border_radius=15)
    window.blit(title_glow, (title_x - 15, title_y - 15))

    window.blit(victory_shadow, (title_x + 2, title_y + 2))
    window.blit(victory_text, (title_x, title_y))

    # 分数信息
    score_label = game_resources['fonts']['large'].render("最终分数", True, (200, 255, 200))
    score_text = game_resources['fonts']['large'].render(f"{player_resources['score']}", True, (255, 255, 255))

    score_label_x = WINDOW_WIDTH // 2 - score_label.get_width() // 2
    score_text_x = WINDOW_WIDTH // 2 - score_text.get_width() // 2

    window.blit(score_label, (score_label_x, panel_y + 100))
    window.blit(score_text, (score_text_x, panel_y + 140))

    # 通关信息
    complete_text = game_resources['fonts']['medium'].render("恭喜您成功击退所有敌人!", True, (200, 255, 200))
    complete_x = WINDOW_WIDTH // 2 - complete_text.get_width() // 2
    window.blit(complete_text, (complete_x, panel_y + 180))

    waves_text = game_resources['fonts']['medium'].render(f"完成 {len(WAVES)} 波次挑战", True, (180, 230, 180))
    waves_x = WINDOW_WIDTH // 2 - waves_text.get_width() // 2
    window.blit(waves_text, (waves_x, panel_y + 210))

    # 创建重新开始按钮
    restart_button = Button(
        WINDOW_WIDTH // 2 - 75,
        panel_y + panel_height - 60,
        150, 40,
        "再次挑战",
        (80, 180, 80),
        (120, 230, 120)
    )
    restart_button.check_hover(pygame.mouse.get_pos())
    restart_button.draw(window)

    # 添加装饰元素 - 星光效果
    for _ in range(30):
        x = random.randint(0, WINDOW_WIDTH)
        y = random.randint(0, WINDOW_HEIGHT)
        size = random.randint(1, 4)
        brightness = random.randint(150, 255)
        color = (200, brightness, 200, random.randint(100, 255))

        # 绘制星星
        star_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(star_surf, color, (size, size), size)
        window.blit(star_surf, (x, y))

        # 有时添加光芒
        if random.random() > 0.7:
            for i in range(4):
                angle = math.pi / 2 * i
                end_x = x + int(math.cos(angle) * size * 2)
                end_y = y + int(math.sin(angle) * size * 2)
                pygame.draw.line(window, (color[0], color[1], color[2], color[3] // 2),
                                 (x + size, y + size), (end_x, end_y), 1)


def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # 处理塔放置
            if game_state['selected_tower_type']:
                if can_place_tower(mouse_pos):
                    # 放置塔
                    tower_cost = TOWER_TYPES[game_state['selected_tower_type']]['cost']
                    if player_resources['gold'] >= tower_cost:
                        new_tower = Tower(game_state['selected_tower_type'], mouse_pos)
                        game_state['towers'].append(new_tower)
                        player_resources['gold'] -= tower_cost

                        # 添加特效
                        add_notification(f"已建造 {game_state['selected_tower_type']} 塔", (100, 200, 255))

                    game_state['selected_tower_type'] = None

            # 处理选中已有的塔
            else:
                # 检查是否点击了任何塔
                for tower in game_state['towers']:
                    dx = tower.position[0] - mouse_pos[0]
                    dy = tower.position[1] - mouse_pos[1]
                    distance = math.sqrt(dx ** 2 + dy ** 2)

                    if distance < tower.size:
                        game_state['selected_tower'] = tower
                        game_state['sidebar_active'] = True
                        break
                else:
                    # 如果点击的不是塔，检查是否是UI元素

                    # 检查加速按钮
                    speed_button_width = 80
                    speed_button_rect = pygame.Rect(WINDOW_WIDTH - speed_button_width - 140, 5, speed_button_width, 30)
                    if speed_button_rect.collidepoint(mouse_pos):
                        # 切换速度等级（在三个速度之间循环）
                        game_state['speed_level'] = (game_state['speed_level'] + 1) % 3

                        # 更新加速状态标志
                        game_state['acceleration_active'] = game_state['speed_level'] > 0

                        # 设置游戏速度
                        speed_values = [1, 2, 3]
                        game_state['game_speed'] = speed_values[game_state['speed_level']]

                        # 添加状态变更通知
                        speed_names = ["正常", "2x", "3x"]
                        add_notification(f"游戏速度: {speed_names[game_state['speed_level']]}",
                                         (100, 180, 255))

                    # 检查塔按钮
                    # 计算按钮位置
                    tower_bar_height = 70
                    total_towers = len(TOWER_TYPES)
                    button_width = 110
                    button_spacing = 10
                    total_width = total_towers * button_width + (total_towers - 1) * button_spacing
                    start_x = (WINDOW_WIDTH - total_width) / 2
                    y_pos = WINDOW_HEIGHT - tower_bar_height + 15

                    for i, tower_type in enumerate(TOWER_TYPES):
                        x_pos = start_x + i * (button_width + button_spacing)
                        button_rect = pygame.Rect(x_pos, y_pos, button_width, 40)

                        if button_rect.collidepoint(mouse_pos):
                            if player_resources['gold'] >= TOWER_TYPES[tower_type]['cost']:
                                game_state['selected_tower_type'] = tower_type
                            else:
                                add_notification("金币不足!", (255, 100, 100))
                            break

                    # 检查波次按钮
                    if not game_state['wave_active'] and not game_state['current_wave_monsters']:
                        wave_button = pygame.Rect(WINDOW_WIDTH - 130, 5, 120, 30)
                        if wave_button.collidepoint(mouse_pos):
                            start_wave()

                    # 如果侧边栏是活动的，检查侧边栏按钮
                    if game_state['sidebar_active'] and game_state['selected_tower']:
                        sidebar_rect = pygame.Rect(WINDOW_WIDTH - 230, 40, 230, WINDOW_HEIGHT - 110)

                        if sidebar_rect.collidepoint(mouse_pos):
                            tower = game_state['selected_tower']

                            # 升级按钮
                            if tower.upgrade_level < tower.max_upgrade_level:
                                upgrade_button = pygame.Rect(
                                    sidebar_rect.centerx - 80,
                                    sidebar_rect.bottom - 150,
                                    160, 30
                                )
                                if upgrade_button.collidepoint(mouse_pos):
                                    if tower.upgrade():
                                        # 升级成功的通知
                                        add_notification(f"{tower.type}塔升级到 {tower.upgrade_level} 级",
                                                         (100, 255, 100))

                            # 出售按钮
                            sell_button = pygame.Rect(
                                sidebar_rect.centerx - 80,
                                sidebar_rect.bottom - 40,
                                160, 30
                            )
                            if sell_button.collidepoint(mouse_pos):
                                # 出售塔
                                sell_value = int(sum([TOWER_TYPES[tower.type]['cost']] +
                                                     [TOWER_TYPES[tower.type]['upgrade'][
                                                          'cost']] * tower.upgrade_level) * 0.7)
                                player_resources['gold'] += sell_value
                                game_state['towers'].remove(tower)
                                game_state['selected_tower'] = None
                                game_state['sidebar_active'] = False

                                # 添加出售通知
                                add_notification(f"已出售塔，获得 {sell_value} 金币", (255, 220, 100))
                        else:
                            # 如果点击了侧边栏外部，关闭侧边栏
                            game_state['sidebar_active'] = False
                            game_state['selected_tower'] = None

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # 取消选择塔类型
                game_state['selected_tower_type'] = None

                # 关闭侧边栏
                if game_state['sidebar_active']:
                    game_state['sidebar_active'] = False
                    game_state['selected_tower'] = None

            elif event.key == K_SPACE:
                # 开始下一波
                if not game_state['wave_active'] and not game_state['current_wave_monsters']:
                    start_wave()

            # 快捷键选择塔
            elif event.key >= K_1 and event.key <= K_5:
                tower_index = event.key - K_1
                if tower_index < len(TOWER_TYPES):
                    tower_type = list(TOWER_TYPES.keys())[tower_index]
                    if player_resources['gold'] >= TOWER_TYPES[tower_type]['cost']:
                        game_state['selected_tower_type'] = tower_type
                    else:
                        add_notification("金币不足!", (255, 100, 100))

            # 游戏速度切换快捷键
            elif event.key == K_f:
                # 切换速度等级（在三个速度之间循环）
                game_state['speed_level'] = (game_state['speed_level'] + 1) % 3

                # 更新加速状态标志
                game_state['acceleration_active'] = game_state['speed_level'] > 0

                # 设置游戏速度
                speed_values = [1, 2, 3]
                game_state['game_speed'] = speed_values[game_state['speed_level']]

                # 添加状态变更通知
                speed_names = ["正常", "2x", "3x"]
                add_notification(f"游戏速度: {speed_names[game_state['speed_level']]}",
                                 (100, 180, 255))


def main():
    # 游戏主循环
    running = True
    while running:
        handle_events()

        # 使用固定的时间步长，考虑游戏速度
        if not game_state['game_over'] and not game_state['victory']:
            update_game_state()

        draw_game()
        clock.tick(FPS)


if __name__ == "__main__":
    main()