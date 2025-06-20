# game/renderer.py
"""
負責渲染遊戲畫面，包括迷宮、Pac-Man、鬼魂和分數顯示。
"""
import pygame
import math
from .entities.pellets import PowerPellet, ScorePellet
from .entities.pacman import PacMan
from .entities.ghost import Ghost
from typing import List, Tuple

from .maze_generator import Map
from config import BLACK, DARK_GRAY, GRAY, GREEN, PINK, RED, BLUE, ORANGE, YELLOW, WHITE, LIGHT_BLUE, CELL_SIZE, TILE_BOUNDARY, TILE_WALL, TILE_PATH, TILE_POWER_PELLET, TILE_GHOST_SPAWN, TILE_DOOR
from .game import Game

class Renderer:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, screen_width: int, screen_height: int):
        """
        初始化渲染器。

        Args:
            screen (pygame.Surface): Pygame 畫面物件。
            font (pygame.font.Font): 用於渲染文字的字體。
            screen_width (int): 螢幕寬度。
            screen_height (int): 螢幕高度。
        """
        self.screen = screen
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height

    def render(self, game: 'Game', control_mode: str, frame_count: int) -> None:
        """
        渲染遊戲畫面。

        Args:
            game (Game): 遊戲實例。
            control_mode (str): 當前控制模式名稱。
            frame_count (int): 動畫幀計數器。
        """
        self.screen.fill(BLACK)  # 清空畫面

        # 渲染迷宮
        maze = game.get_maze()
        for y in range(maze.height):
            for x in range(maze.width):
                tile = maze.get_tile(x, y)

                # 獲取相鄰格子的資訊
                tile_up = maze.get_tile(x, y + 1)
                tile_down = maze.get_tile(x, y - 1)
                tile_left = maze.get_tile(x - 1, y)
                tile_right = maze.get_tile(x + 1, y)

                # 判斷是否為邊界
                up_w = (tile_up == TILE_WALL)
                down_w = (tile_down == TILE_WALL)
                left_w = (tile_left == TILE_WALL)
                right_w = (tile_right == TILE_WALL)

                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # 計算格子矩形
                if tile == TILE_BOUNDARY:
                    pygame.draw.rect(self.screen, DARK_GRAY, rect)  # 繪製邊界（深灰色）
                elif tile == TILE_PATH:
                    pygame.draw.rect(self.screen, BLACK, rect)  # 繪製路徑（黑色）
                elif tile == TILE_POWER_PELLET:
                    pygame.draw.rect(self.screen, BLACK, rect)  # 繪製能量球位置（黑色）
                elif tile == TILE_GHOST_SPAWN:
                    pygame.draw.rect(self.screen, BLACK, rect)  # 繪製鬼魂生成位置（黑色）
                elif tile == TILE_DOOR:
                    pygame.draw.rect(self.screen, GRAY, rect)  # 繪製門（灰色）
                elif tile == TILE_WALL:
                    # 根據相鄰格子的資訊選擇牆壁圖片
                    if up_w and down_w and left_w and right_w:
                        wall_img_path = f"./assert/image/wall/center.png"
                    elif up_w and down_w and left_w and not right_w:
                        wall_img_path = f"./assert/image/wall/T_l.png"
                    elif up_w and down_w and not left_w and right_w:
                        wall_img_path = f"./assert/image/wall/T_r.png"
                    elif up_w and not down_w and left_w and right_w:
                        wall_img_path = f"./assert/image/wall/T_d.png"
                    elif not up_w and down_w and left_w and right_w:
                        wall_img_path = f"./assert/image/wall/T_u.png"
                    elif up_w and not down_w and not left_w and right_w:
                        wall_img_path = f"./assert/image/wall/corner_dr.png"
                    elif up_w and not down_w and left_w and not right_w:
                        wall_img_path = f"./assert/image/wall/corner_dl.png"
                    elif not up_w and down_w and left_w and not right_w:
                        wall_img_path = f"./assert/image/wall/corner_ul.png"
                    elif not up_w and down_w and not left_w and right_w:
                        wall_img_path = f"./assert/image/wall/corner_ur.png"
                    elif not up_w and not down_w and left_w and right_w:
                        wall_img_path = f"./assert/image/wall/horizontal.png"
                    elif up_w and down_w and not left_w and not right_w:
                        wall_img_path = f"./assert/image/wall/vertical.png"
                    elif up_w and not down_w and not left_w and not right_w:
                        wall_img_path = f"./assert/image/wall/convex_u.png"
                    elif not up_w and down_w and not left_w and not right_w:
                        wall_img_path = f"./assert/image/wall/convex_d.png"
                    elif not up_w and not down_w and left_w and not right_w:
                        wall_img_path = f"./assert/image/wall/convex_r.png"
                    elif not up_w and not down_w and not left_w and right_w:
                        wall_img_path = f"./assert/image/wall/convex_l.png"
                    elif not up_w and not down_w and not left_w and not right_w:
                        wall_img_path = f"./assert/image/wall/dot.png"
                        
                    load_wall = pygame.image.load(wall_img_path).convert_alpha()
                    self.screen.blit(load_wall, (x * CELL_SIZE, y * CELL_SIZE))  # 繪製牆壁圖片

        # 渲染能量球
        for pellet in game.get_power_pellets():
            pellet_rect = pygame.Rect(
                pellet.x * CELL_SIZE + CELL_SIZE // 4,
                pellet.y * CELL_SIZE + CELL_SIZE // 4,
                CELL_SIZE // 2, CELL_SIZE // 2)  # 計算能量球矩形（居中，半格大小）
            pygame.draw.ellipse(self.screen, ORANGE, pellet_rect)  # 繪製藍色圓形能量球

        # 渲染分數球
        for score_pellet in game.get_score_pellets():
            score_pellet_rect = pygame.Rect(
                score_pellet.x * CELL_SIZE + CELL_SIZE * 3 // 8,
                score_pellet.y * CELL_SIZE + CELL_SIZE * 3 // 8,
                CELL_SIZE // 4, CELL_SIZE // 4)  # 計算分數球矩形（居中，半格大小）
            pygame.draw.ellipse(self.screen, ORANGE, score_pellet_rect)  # 繪製橙色圓形分數球
        
        # 渲染鬼魂
        for ghost in game.get_ghosts():
            if ghost.returning_to_spawn:
                ghost_img_path = f"./assert/image/ghosts/ghost_return.png"
                ghost.alpha = int(128 + 127 * math.sin(frame_count * 0.5))  # 閃爍效果
            elif ghost.edible and ghost.edible_timer > 0:
                if ghost.edible_timer < 1 and frame_count % 2 < 1:
                    ghost_img_path = f"./assert/image/ghosts/ghost_edible_white.png"
                elif ghost.edible_timer < 2 and frame_count % 4 < 2: 
                    ghost_img_path = f"./assert/image/ghosts/ghost_edible_white.png"
                elif ghost.edible_timer < 3 and frame_count % 6 < 3:
                    ghost_img_path = f"./assert/image/ghosts/ghost_edible_white.png"
                elif ghost.edible_timer < 4 and frame_count % 8 < 4:   
                    ghost_img_path = f"./assert/image/ghosts/ghost_edible_white.png"
                elif ghost.edible_timer < 5 and frame_count % 10 < 5: 
                    ghost_img_path = f"./assert/image/ghosts/ghost_edible_white.png"
                else: 
                    ghost_img_path = f"./assert/image/ghosts/ghost_edible.png"
                ghost.alpha = 255
            else:
                while True:
                    frame_count_mod = frame_count // 5
                    if frame_count_mod % 2 == 0:
                        ghost_img_path = f"./assert/image/ghosts/{ghost.name}.png"
                    elif frame_count_mod % 2 == 1:
                        ghost_img_path = f"./assert/image/ghosts/{ghost.name}_2.png"
                    break
                ghost.alpha = 255

            load_ghost = pygame.image.load(ghost_img_path).convert_alpha()
            load_ghost = pygame.transform.scale(load_ghost, (CELL_SIZE * 5 // 6, CELL_SIZE * 5 // 6))  # 調整鬼魂圖片大小
            load_ghost.set_alpha(ghost.alpha)
            self.screen.blit(load_ghost, (ghost.current_x - CELL_SIZE * 5 // 12, ghost.current_y - CELL_SIZE * 5 // 12))
            
        # 渲染 Pac-Man
        pacman = game.get_pacman()
        pacman_rect = pygame.Rect(
            pacman.current_x - CELL_SIZE // 4,
            pacman.current_y - CELL_SIZE // 4,
            CELL_SIZE // 2, CELL_SIZE // 2)
        
        if game.is_death_animation_playing():
            # 死亡動畫：縮小 Pac-Man
            progress = game.get_death_animation_progress()  # 動畫進度（0 到 1）
            scale = 1.0 - progress  # 縮放比例，從 1 減小到 0
            radius = int(CELL_SIZE // 2 * scale)  # 計算縮放後的圓半徑
            pacman_center = (
                pacman.current_x,
                pacman.current_y,
                )  # Pac-Man 當前中心坐標
            if radius > 0:
                pygame.draw.circle(self.screen, YELLOW, pacman_center, radius)  # 繪製縮小的黃色圓形
        else:
            # 正常繪製 Pac-Man
            pacman_rl_img_path = f"./assert/image/pacman/right_l.png"
            pacman_rm_img_path = f"./assert/image/pacman/right_m.png"
            pacman_rs_img_path = f"./assert/image/pacman/right_s.png"
            pacman_dl_img_path = f"./assert/image/pacman/down_l.png"
            pacman_dm_img_path = f"./assert/image/pacman/down_m.png"
            pacman_ds_img_path = f"./assert/image/pacman/down_s.png"
            pacman_ul_img_path = f"./assert/image/pacman/up_l.png"
            pacman_um_img_path = f"./assert/image/pacman/up_m.png"
            pacman_us_img_path = f"./assert/image/pacman/up_s.png"
            pacman_ll_img_path = f"./assert/image/pacman/left_l.png"
            pacman_lm_img_path = f"./assert/image/pacman/left_m.png"
            pacman_ls_img_path = f"./assert/image/pacman/left_s.png"
            pacman_c_img_path = f"./assert/image/pacman/closed.png"
            pacman_img_path = pacman_rl_img_path

            while True :
                frame_count_mod = frame_count // 3
                if (pacman.target_x - pacman.x) > 0: 
                    if( frame_count_mod % 4 == 0):
                        pacman_img_path = pacman_rl_img_path
                    elif( frame_count_mod % 4 == 1):
                        pacman_img_path = pacman_rm_img_path
                    elif( frame_count_mod % 4 == 2):
                        pacman_img_path = pacman_rs_img_path
                    else:
                        pacman_img_path = pacman_c_img_path
                elif (pacman.target_x - pacman.x) < 0:
                    if ( frame_count_mod % 4 == 0):
                        pacman_img_path = pacman_ll_img_path
                    elif ( frame_count_mod % 4 == 1):
                        pacman_img_path = pacman_lm_img_path
                    elif ( frame_count_mod % 4 == 2):
                        pacman_img_path = pacman_ls_img_path
                    else:
                        pacman_img_path = pacman_c_img_path
                elif (pacman.target_y - pacman.y) > 0:
                    if ( frame_count_mod % 4 == 0):
                        pacman_img_path = pacman_dl_img_path
                    elif ( frame_count_mod % 4 == 1):
                        pacman_img_path = pacman_dm_img_path
                    elif ( frame_count_mod % 4 == 2):   
                        pacman_img_path = pacman_ds_img_path
                    else:
                        pacman_img_path = pacman_c_img_path
                elif (pacman.target_y - pacman.y) < 0:
                    if ( frame_count_mod % 4 == 0):
                        pacman_img_path = pacman_ul_img_path
                    elif ( frame_count_mod % 4 == 1):       
                        pacman_img_path = pacman_um_img_path
                    elif ( frame_count_mod % 4 == 2):
                        pacman_img_path = pacman_us_img_path
                    else:
                        pacman_img_path = pacman_c_img_path
                else:
                    pacman_img_path = pacman_c_img_path
                break
            load_pacman = pygame.image.load(pacman_img_path).convert_alpha()
            self.screen.blit(load_pacman, (pacman.current_x - CELL_SIZE * 5 // 12, pacman.current_y - CELL_SIZE * 5 // 12))

        # 渲染分數和控制模式
        score_text = self.font.render(f"Score: {pacman.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        mode_text = self.font.render(control_mode, True, WHITE)
        self.screen.blit(mode_text, (self.screen_width - 150, 10))