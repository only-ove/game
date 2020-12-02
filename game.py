# -*- coding: utf-8 -*-
"""
@ Author: Chaozhan Li
@ Description: 
"""
import os
import random
import sys

import pygame


IMAGEDIR = ""
MUSIC = ""
SCREENSIZE = (800, 800)
GRAY = (192, 192, 192)
WHITE = (255, 255, 255, 27)
FPS = 60

MUSIC_PLAYING = False
MOVIE_PLAYING = False


def read_image_randomly(image_list):
    # file_names = os.listdir(IMAGEDIR)
    # image_path = os.path.join(IMAGEDIR, random.choice(file_names))
    image_path = random.choice(image_list)
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, SCREENSIZE)


def play_music(music_list):
    pygame.mixer.init()
    if len(music_list) == 1:
        pygame.mixer.music.load(music_list[0])
        pygame.mixer.music.play(-1, 0.0)
    else:
        for music in music_list:
            pygame.mixer.music.load(music)
            pygame.mixer.music.play()
            pygame.mixer.music.queue(music)
            pygame.mixer.music.set_endevent(-1)


def play_movie(file_path):
    if MUSIC_PLAYING:
        pygame.mixer.quit()
    movie = pygame.movie.Movie(file_path)
    movie_screen = pygame.Surface(SCREENSIZE).convert()

    movie.set_display(movie_screen)
    movie.play()
    return movie_screen


def get_music_image_list():
    music_list = []
    image_list = []
    movie_list = []
    current_dir = os.getcwd()
    all_files = [f for f in os.listdir(current_dir)]
    for f in all_files:
        f = os.path.join(current_dir, f)
        if os.path.isdir(f):
            child_all_files = [child_f for child_f in os.listdir(os.path.join(current_dir, f))]
            for child_f in child_all_files:
                child_f = os.path.join(f, child_f)
                if os.path.isfile(child_f):
                    music_list, image_list, movie_list = add_image_or_music_list(child_f, music_list, image_list, movie_list)
        elif os.path.isfile(f):
            music_list, image_list, movie_list = add_image_or_music_list(f, music_list, image_list, movie_list)
    return music_list, image_list, movie_list


def add_image_or_music_list(f, music_list, image_list, movie_list):
    if f.endswith(".mp3") or f.endswith(".ogg") or f.endswith(".wav"):
        music_list.append(f)
    elif f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png") or f.endswith(".gif"):
        image_list.append(f)
    elif f.endswith(".mp4") or f.endswith(".rmvb") or f.endswith(".mkv") or f.endswith(".avi"):
        movie_list.append(f)
    return music_list, image_list, movie_list


def get_love():
    current_dir = os.getcwd()
    all_files = [f for f in os.listdir(current_dir)]
    dir_list = []
    for f in all_files:
        if f.startswith("."):
            continue
        f = os.path.join(current_dir, f)
        if os.path.isdir(f):
            dir_list.append(f)
    if len(dir_list) == 1 and dir_list[0].split("/")[-1].lower() == "love":
        return True
    else:
        return False


def get_text():
    current_dir = os.getcwd()
    all_files = [f for f in os.listdir(current_dir)]
    text_list = []
    text_files_list = []
    for f in all_files:
        f = os.path.join(current_dir, f)
        print(f)
        if os.path.isfile(f) and (f.endswith(".txt") or os.path.splitext(f)[-1] == ".txt"):
            text_files_list.append(f)
    print(text_files_list)
    for file in text_files_list:
        try:
            with open(file, "r", encoding="utf-8") as f:
                f_text_list = f.readlines()
        except:
            with open(file, "r", encoding="gbk") as f:
                f_text_list = f.readlines()
        # for line in f_text_list:
        #     if len(line) > 8:
        #         text_list.append("\n".join([line[:8], line[8:]]))
        #     else:
        #         text_list.append(line)
        text_list.extend([line for line in f_text_list])
    return text_list


def set_font(text):
    # font_object = pygame.font_object.Font("./Songti.ttc", 90)
    # font_object.set_italic(True)
    font_object = pygame.font.SysFont("freesansbold.ttf", 90, bold=True, italic=True)
    create_text = font_object.render(text, True, (0, 0, 0), (255, 255, 255))
    return create_text


class Button(object):

    def __init__(self, ai_setttings, screen, msg):  # msg为要在按钮中显示的文本
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 150, 50  # 这种赋值方式很不错
        self.button_color = (72, 61, 139)  # 设置按钮的rect对象颜色为深蓝
        self.text_color = (255, 255, 255)  # 设置文本的颜色为白色
        # self.font = pygame.font.SysFont(None, 40)  # 设置文本为默认字体，字号为40

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center  # 创建按钮的rect对象，并使其居中

        self.deal_msg(msg)  # 渲染图像

    def deal_msg(self, msg):
        """将msg渲染为图像，并将其在按钮上居中"""
        # self.msg_img = self.font.render(msg, True, self.text_color, self.button_color)  # render将存储在msg的文本转换为图像
        self.msg_img = set_font(msg)
        self.msg_img_rect = self.msg_img.get_rect()  # 根据文本图像创建一个rect
        self.msg_img_rect.center = self.rect.center  # 将该rect的center属性设置为按钮的center属性

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)  # 填充颜色
        self.screen.blit(self.msg_img, self.msg_img_rect)  # 将该图像绘制到屏幕


def main():
    pygame.init()
    clock = pygame.time.Clock()
    music_list, image_list, movie_list = get_music_image_list()
    global MUSIC_PLAYING
    if len(music_list) > 0:
        MUSIC_PLAYING = True
        play_music(music_list)
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    screen = pygame.display.set_mode(SCREENSIZE)
    current_love_image = 0
    current_love_movie = 0
    if get_love():
        pygame.display.set_caption("No noe but you!")
    else:
        pygame.display.set_caption("刮刮乐")
    surface = pygame.Surface(SCREENSIZE).convert_alpha()
    text_list = get_text()
    if len(text_list) > 0:
        surface.fill(WHITE)
        image_used = set_font("start")
    else:
        surface.fill(GRAY)
        image_used = read_image_randomly(image_list)
    n = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)

        mouse_event = pygame.mouse.get_pressed()
        if get_love():
            screen.blit(image_used, (0, 0))
            if mouse_event[0] or mouse_event[2] or mouse_event[1]:
                # image_used = read_image_randomly(image_list)
                if current_love_image <= len(image_list):
                    image = pygame.image.load(image_list[current_love_image])
                    image_used = pygame.transform.scale(image, SCREENSIZE)
                    screen.blit(image_used, (0, 0))
                    current_love_image = current_love_image + 1
                if current_love_image > len(image_list) and len(movie_list) > 0 and current_love_movie <= len(movie_list):
                    movie_screen = play_movie(movie_list[current_love_movie])
                    screen.blit(movie_screen, (0, 0))
                    current_love_movie = current_love_movie + 1

        else:
            if mouse_event[0]:
                pygame.draw.circle(surface, WHITE, pygame.mouse.get_pos(), 40)
            elif mouse_event[2]:
                n = n + 1
                surface.fill(GRAY)
                if len(text_list) > 0:
                    # surface.fill(WHITE)
                    text_used = random.choice(text_list)
                    image_used = set_font(text_used)
                else:
                    image_used = read_image_randomly(image_list)

            if len(text_list) > 0:
                if not n:
                    screen.blit(image_used, (300, 280))

                else:
                    screen.blit(image_used, (30, 280))
            else:
                screen.blit(image_used, (0, 0))
            screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)
        if pygame.mixer.music.get_endevent() == -1:
            MUSIC_PLAYING = True
            play_music(music_list)


if __name__ == '__main__':
    main()
