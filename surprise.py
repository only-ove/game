# -*- coding: utf-8 -*-
"""
@ Author: Chaozhan Li
@ Description: 
"""
import os
import random
import sys
import time

import pygame


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


def get_music_image_list():
    music_list = []
    image_list = []
    current_dir = os.getcwd()
    all_files = [f for f in os.listdir(current_dir)]
    for f in all_files:
        f = os.path.join(current_dir, f)
        if os.path.isdir(f) and not f.endswith(".love"):
            child_all_files = [child_f for child_f in os.listdir(os.path.join(current_dir, f))]
            for child_f in child_all_files:
                child_f = os.path.join(f, child_f)
                if os.path.isfile(child_f):
                    music_list, image_list = add_image_or_music_list(child_f, music_list, image_list)
        elif os.path.isfile(f):
            music_list, image_list = add_image_or_music_list(f, music_list, image_list)
    return music_list, image_list


def add_image_or_music_list(f, music_list, image_list):
    if f.endswith(".mp3") or f.endswith(".ogg") or f.endswith(".wav"):
        music_list.append(f)
    elif f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png") or f.endswith(".gif"):
        image_list.append(f)
    return music_list, image_list


def get_love():
    current_dir = os.getcwd()
    all_files = [f for f in os.listdir(current_dir)]
    love_image_dict = {}
    for f in all_files:
        if f.startswith(".") and f == ".love":
            f = os.path.join(current_dir, f)
            for child_f in os.listdir(f):
                child_f = os.path.join(f, child_f)
                # print(child_f)
                if os.path.isdir(child_f) and child_f.endswith("i"):
                    print(child_f)
                    i_image_list = [os.path.join(child_f, image) for image in os.listdir(child_f) if
                                    not image.endswith(".mp3")]
                    love_image_dict["i"] = i_image_list
                    i_music_list = [os.path.join(child_f, image) for image in os.listdir(child_f) if
                                    image.endswith(".mp3")]
                    love_image_dict["i_music"] = i_music_list
                if os.path.isdir(child_f) and child_f.endswith("l"):
                    l_image_list = [os.path.join(child_f, image) for image in os.listdir(child_f)]
                    love_image_dict["l"] = l_image_list
                    l_music_list = [os.path.join(child_f, image) for image in os.listdir(child_f) if
                                    image.endswith(".mp3")]
                    love_image_dict["l_music"] = l_music_list
                if os.path.isdir(child_f) and child_f.endswith("u"):
                    u_image_list = [os.path.join(child_f, image) for image in os.listdir(child_f)]
                    love_image_dict["u"] = u_image_list
                    u_music_list = [os.path.join(child_f, image) for image in os.listdir(child_f) if
                                    image.endswith(".mp3")]
                    love_image_dict["u_music"] = u_music_list
    if len(love_image_dict) > 0:
        return love_image_dict
    else:
        return False


def get_text():
    current_dir = os.getcwd()
    all_files = [f for f in os.listdir(current_dir)]
    text_list = []
    text_files_list = []
    for f in all_files:
        f = os.path.join(current_dir, f)
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
        text_list.extend([line for line in f_text_list])
    return text_list


def set_font(text):
    font_name = pygame.font.match_font("Songti")
    print(font_name)
    font_object = pygame.font.Font(font_name, 90)
    # font_object.set_bold(True)
    font_object.set_italic(True)
    # font_object = pygame.font.SysFont(font_name, 90, bold=True, italic=True)
    create_text = font_object.render(text, True, (0, 0, 0), (255, 255, 255))
    return create_text


def main():
    pygame.init()
    clock = pygame.time.Clock()
    music_list, image_list = get_music_image_list()
    print(image_list)
    love_image_dict = get_love()
    global MUSIC_PLAYING
    if len(music_list) > 0:
        MUSIC_PLAYING = True
        play_music(music_list)
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    screen = pygame.display.set_mode(SCREENSIZE)
    current_i_image = 0
    current_l_image = 0
    current_u_image = 0
    pygame.display.set_caption("刮刮乐")
    surface = pygame.Surface(SCREENSIZE).convert_alpha()
    text_list = get_text()
    print(text_list)
    if len(text_list) > 0:
        surface.fill(WHITE)
        image_used = set_font("start")
    else:
        surface.fill(GRAY)
        image_used = read_image_randomly(image_list)
    n = 0
    while True:
        key_list = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(-1)

        mouse_event = pygame.mouse.get_pressed()
        if love_image_dict and key_list[pygame.K_i]:
            i_image_list = love_image_dict["i"]
            i_music_list = love_image_dict["i_music"]
            if i_music_list:
                play_music(i_music_list)
            print(current_i_image)
            if current_i_image > 0:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                continue
            print(i_image_list)
            current_i_image = current_i_image + 1
            for i_image in i_image_list:
                image = pygame.image.load(i_image)
                image_used = pygame.transform.scale(image, SCREENSIZE)
                screen.blit(image_used, (0, 0))
                pygame.display.update()
                clock.tick(FPS)
                time.sleep(10)
                if current_i_image == len(i_image_list):
                    break
        elif love_image_dict and key_list[pygame.K_l]:
            l_image_list = love_image_dict["l"]
            l_music_list = love_image_dict["l_music"]
            if l_music_list:
                play_music(l_music_list)
            print(current_l_image)
            if current_l_image > 0:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                continue
            print(l_image_list)
            current_l_image = current_l_image + 1
            for l_image in l_image_list:
                image = pygame.image.load(l_image)
                image_used = pygame.transform.scale(image, SCREENSIZE)
                screen.blit(image_used, (0, 0))
                pygame.display.update()
                clock.tick(FPS)
                time.sleep(10)
                if current_l_image == len(l_image_list):
                    break
        elif love_image_dict and key_list[pygame.K_u]:
            u_image_list = love_image_dict["u"]
            u_music_list = love_image_dict["u_music"]
            if u_music_list:
                play_music(u_music_list)
            print(current_u_image)
            if current_u_image > 0:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                continue
            print(u_image_list)
            current_u_image = current_u_image + 1
            for u_image in u_image_list:
                image = pygame.image.load(u_image)
                image_used = pygame.transform.scale(image, SCREENSIZE)
                screen.blit(image_used, (0, 0))
                pygame.display.update()
                clock.tick(FPS)
                time.sleep(10)
                if current_i_image == len(u_image_list):
                    break
        else:
            current_i_image = 0
            current_l_image = 0
            current_u_image = 0
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
