"""Main Game Module

Sets up the main game window, and goes through the appropriate methods to progress through the game

"""
import pygame
import sys
import doctest
# import pickle
from pygame.locals import *
from Wall import Wall
import MidCraft
import FastCraft
import TankCraft
import EnemySprite1
import EnemySprite2
import EnemySprite3
import EnemySprite4
import HealthPower
import BoostPower
from random import randint


blue = pygame.Color(0, 153, 255)
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
teal = pygame.Color(0, 255, 255)
yellow = pygame.Color(255, 255, 0)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)

fps = 30
win_width = 800
win_height = 800
window_size = (win_width, win_height)
pause = False


def main():
    """Main Method

    Creates the appropriate pygame setup (window size, fps_clock, screen, window caption) for game and starts the
    main while loop

    """
    global screen, fps_clock, font, background
    pygame.init()
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode(window_size)
    font = pygame.font.SysFont('gameassets/Anonymous Pro.tff', 20, False, False)
    beegee = pygame.image.load('gameassets/Grid2.png').convert()
    background = pygame.transform.smoothscale(beegee, (800, 800))
    icon = pygame.image.load('gameassets/fire-ball.png')
    pygame.display.set_icon(icon)
    screen.blit(background, (0, 0))
    pygame.display.set_caption('Shape Evader')
    while True:
        splash()
        difficulty = diffchoice()
        ship = shipchoice()
        pygame.mixer.music.load('gameassets/mainmusic.ogg')
        pygame.mixer.music.play(-1, 0.0)
        cond, time = runlevel1(difficulty, ship)
        pygame.mixer.music.stop()
        nextchoice = grats(cond, time, ship)
        # scoresave('1', ship, time, difficulty)
        if nextchoice == 'level2':
            print('test', time)
            pygame.mixer.music.load('gameassets/mainmusic.ogg')
            pygame.mixer.music.play(-1, 0.0)
            cond2, time2 = runlevel2(difficulty, ship)
            pygame.mixer.music.stop()
            grats(cond2, time2, ship)
            # scoresave('2', ship, time, difficulty)
        else:
            pygame.quit()
            sys.exit()


def splash():
    """Splash Screen

    Creates the main menu page the player has to go through to get to the game
    Contains game title and provides instruction to start game

    """
    mfont = pygame.font.SysFont('gameassets/Anonymous Pro.tff', 100, False, False)
    sfont = pygame.font.SysFont('gameassets/Anonymous Pro.tff', 50, False, False)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

            ################################

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    return
            ###############################
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), [150, 100, 550, 80], 5)
        text = 'SHAPE EVADER'
        screen.blit(mfont.render(text, True, yellow), (152, 110))
        space = 'Press Space to Continue'
        screen.blit(sfont.render(space, True, teal), (200, 700))
        pygame.display.update()


def diffchoice():
    """
    Screen where player chooses their difficulty, can't be changed until restart.

    Args:
        None

    Returns:
        int: difficulty choice: 1 for easy, 2 for medium, 3 for hard

    """
    sfont = pygame.font.SysFont('gameassets/Anonymous Pro.tff', 50, False, False)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

            ################################

            elif event.type == KEYDOWN:
                if event.key == K_1 or event.key == K_KP1:
                    return 1
                elif event.key == K_2 or event.key == K_KP2:
                    return 2
                elif event.key == K_3 or event.key == K_KP3:
                    return 3
            ###############################
        screen.blit(background, (0, 0))
        etext = '1. Easy, piece of cake'
        mtext = '2. Medium, rare'
        htext = '3. Hard, maybe a bit too hard'
        screen.blit(sfont.render(etext, True, white), (150, 300))
        screen.blit(sfont.render(mtext, True, white), (150, 400))
        screen.blit(sfont.render(htext, True, white), (150, 500))

        pygame.display.flip()


def shipchoice():
    """Ship Choice Screen

    Choice of craft/ship is made here, can't be changed until restart. Contained in while loop that doesn't end until
    user exits or makes a choice.

    Args:
        None

    Returns:
        str: The ship choice: 'fast' for the fast ship, 'mid' for the All-Around Ship, and 'tank' for the Tank
    """
    sfont = pygame.font.SysFont('gameassets/Anonymous Pro.tff', 50, False, False)
    choice_sprite_list = pygame.sprite.Group()
    ship1 = FastCraft.Craft(80, 280)
    ship2 = MidCraft.Craft(90, 390)
    ship3 = TankCraft.Craft(50, 470)
    choice_sprite_list.add(ship1)
    choice_sprite_list.add(ship2)
    choice_sprite_list.add(ship3)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()
            ################################
            elif event.type == KEYDOWN:
                if event.key == K_1 or event.key == K_KP1:
                    return 'fast'
                elif event.key == K_2 or event.key == K_KP2:
                    return 'mid'
                elif event.key == K_3 or event.key == K_KP3:
                    return 'tank'
            ###############################
        screen.blit(background, (0, 0))
        choice_sprite_list.draw(screen)
        etext = '1. Fast Craft'
        mtext = '2. All-Around Craft'
        htext = '3. Tank'
        screen.blit(sfont.render(etext, True, white), (150, 300))
        screen.blit(sfont.render(mtext, True, white), (150, 400))
        screen.blit(sfont.render(htext, True, white), (150, 500))

        pygame.display.update()


def runlevel1(difficulty, craftchoice):
    """Level 1 contained here, will use the difficulty and craftchoice params to draw and play out accordingly.

    Args:
        difficulty (int): 1, 2, or 3, difficulty of choice dictated by player in prior screen

        craftchoice (str): fast, mid, tank, craft of choice dictated by player in prior screen

    Returns:
        str: 'over' or 'continue', for game over screen or continuation screen respectively.
    """
    global pause
    # laser_timing = USEREVENT + 1
    count_up = USEREVENT + 2
    spawn_more = USEREVENT + 3
    powerup_spawn = USEREVENT + 4
    spawn_time = 10000
    if difficulty == 1:
        spawn_time *= 1
    elif difficulty == 2:
        spawn_time *= 0.60
    elif difficulty == 3:
        spawn_time *= 0.25
    pygame.time.set_timer(spawn_more, int(spawn_time))
    powerup_time = randint(5000, 7000)
    total_time = 0
    total_obs = 0
    display_time(total_time)
    pygame.time.set_timer(count_up, 1000)
    pygame.time.set_timer(powerup_spawn, powerup_time)
    # Sprite Stuff
    all_sprite_list = pygame.sprite.Group()
    laser_list = pygame.sprite.Group()
    powerup_list = pygame.sprite.Group()
    ###########################################
    # Backgroud List
    # laser_list, grid_canvas = createlasers(40, 40)

    # laser = BackgroundTest.Laser(40, 40, pygame.Color(0, 255, 204))
    for x in range(0, 3 * difficulty, 1):
        spawn(laser_list, all_sprite_list, randint(200, 600), randint(-10, 10))
    # obstacles = startsquares(400)
    # circ = onecirclaser(400)
    # # laser_list.add(laser)
    # laser_list.add(obstacles)
    # laser_list.add(circ)
    # all_sprite_list.add(obstacles)
    # all_sprite_list.add(circ)
    ###########################################
    # Walls
    wall_list = pygame.sprite.Group()
    leftwall = Wall(-1, 0, 1, 800)
    topwall = Wall(0, -1, 800, 1)
    rightwall = Wall(799, 0, 1, 800)
    bottomwall = Wall(0, 799, 800, 1)

    wall_list.add(leftwall)
    wall_list.add(topwall)
    wall_list.add(rightwall)
    wall_list.add(bottomwall)
    all_sprite_list.add(leftwall)
    all_sprite_list.add(rightwall)
    all_sprite_list.add(topwall)
    all_sprite_list.add(bottomwall)
    ###########################################
    # Craft Stuff
    # boostimg = pygame.image.load('gameassets/1430802008.png')
    if craftchoice == 'fast':
        craft = FastCraft.Craft(10, 10)
    elif craftchoice == 'mid':
        craft = MidCraft.Craft(10, 10)
    elif craftchoice == 'tank':
        craft = TankCraft.Craft(10, 10)
    craft.walls = wall_list
    all_sprite_list.add(craft)

    # sounds
    errorsound = pygame.mixer.Sound('gameassets/error.ogg')
    powerupsound = pygame.mixer.Sound('gameassets/vgbeep.ogg')
    boostsound = pygame.mixer.Sound('gameassets/boost.ogg')
    hurtsound = pygame.mixer.Sound('gameassets/hurt.ogg')
    ##########################################
    while True:  # <--- main game loop
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()
            ################################
            elif event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    craft.changespeed(-15, 0)
                elif event.key == pygame.K_RIGHT:
                    craft.changespeed(15, 0)
                elif event.key == pygame.K_UP:
                    craft.changespeed(0, -15)
                elif event.key == pygame.K_DOWN:
                    craft.changespeed(0, 15)
                elif event.key == K_SPACE:
                    if craft.boost > 0:
                        boostsound.play()
                        craft.boost -= 10
                        for laser in laser_list:
                            laser.update(4)
                    else:
                        errorsound.play()
                elif event.key == K_p:
                    pause = True
                    paused()
            elif event.type == KEYUP:
                if event.key == pygame.K_LEFT:
                    craft.changespeed(15, 0)
                elif event.key == pygame.K_RIGHT:
                    craft.changespeed(-15, 0)
                elif event.key == pygame.K_UP:
                    craft.changespeed(0, 15)
                elif event.key == pygame.K_DOWN:
                    craft.changespeed(0, -15)

            elif event.type == count_up:
                total_time += 1
            elif event.type == spawn_more:
                spawn(laser_list, all_sprite_list, craft.rect.x, craft.rect.y)
                spawn_time -= 50
                pygame.time.set_timer(spawn_more, int(spawn_time))
            elif event.type == powerup_spawn:
                if len(powerup_list) == 0:
                    spawnpowerup(powerup_list, all_sprite_list)
                    pygame.time.set_timer(powerup_spawn, powerup_time)

            ###############################
        #######################################
        all_sprite_list.update()

        laser_hit_list = pygame.sprite.spritecollide(craft, laser_list, True)
        for hit in laser_hit_list:
            hurtsound.play()
            laser_list.remove(hit)
            all_sprite_list.remove(hit)
            if craftchoice == 'fast':
                craft.integrity -= 15 * difficulty
            elif craftchoice == 'mid':
                craft.integrity -= 10 * difficulty
            elif craftchoice == 'tank':
                craft.integrity -= 5 * difficulty
            spawn(laser_list, all_sprite_list, craft.rect.x, craft.rect.y)
            # print(craft.integrity)
        for laser in laser_list:
            if laser.rect.x < -50:
                total_obs += 1
                if craft.boost < 100:
                    if craftchoice == 'fast':
                        craft.boost += 15
                        if craft.boost > 100:
                            craft.boost == 100
                    elif craftchoice == 'mid':
                        craft.boost += 10
                    elif craftchoice == 'tank':
                        craft.boost += 5
                laser.reset_pos()
            elif laser.rect.y > 860:
                total_obs += 1
                if craft.boost < 100:
                    if craftchoice == 'fast':
                        craft.boost += 15
                        if craft.boost > 100:
                            craft.boost == 100
                    elif craftchoice == 'mid':
                        craft.boost += 10
                    elif craftchoice == 'tank':
                        craft.boost += 5
                laser.reset_pos()
            elif laser.rect.y < -100:
                total_obs += 1
                if craft.boost < 100:
                    if craftchoice == 'fast':
                        craft.boost += 15
                        if craft.boost > 100:
                            craft.boost == 100
                    elif craftchoice == 'mid':
                        craft.boost += 10
                    elif craftchoice == 'tank':
                        craft.boost += 5
                laser.reset_pos()

        powerup_hit_list = pygame.sprite.spritecollide(craft, powerup_list, True)
        for hit in powerup_hit_list:
            powerupsound.play()
            if hit.integrityup == 100:
                if craft.integrity < 100:
                    full = 100 - craft.integrity
                    craft.integrity += full
            else:
                if craft.boost < 100:
                    full = 100 - craft.boost
                    craft.boost += full
            powerup_list.remove(hit)
            all_sprite_list.remove(hit)
        screen.blit(background, (0, 0))

        if craft.integrity <= 0:
            return 'over', total_time
        if total_obs > 100:
            return 'continue', total_time

        all_sprite_list.draw(screen)
        display_time(total_time)
        integritybar(craft.integrity)
        progression(total_obs)
        boostbar(craft.boost)
        # print(total_time)
        pygame.display.update()
        fps_clock.tick(fps)


def runlevel2(difficulty, craftchoice):
    """Level 2 contained here, will use the difficulty and craftchoice params to draw and play out accordingly.

    Args:
        difficulty (int): 1, 2, or 3, difficulty of choice dictated by player in prior screen

        craftchoice (str): fast, mid, tank, craft of choice dictated by player in prior screen

    Returns:
        str: 'over' or 'continue', for game over screen or continuation screen respectively.
    """
    global pause
    # laser_timing = USEREVENT + 1
    count_up = USEREVENT + 2
    spawn_more = USEREVENT + 3
    powerup_spawn = USEREVENT + 4
    spawn_time = 5000
    if difficulty == 1:
        spawn_time *= 1
    elif difficulty == 2:
        spawn_time *= 0.60
    elif difficulty == 3:
        spawn_time *= 0.25
    pygame.time.set_timer(spawn_more, int(spawn_time))
    powerup_time = randint(5000, 7000)
    total_time = 0
    total_obs = 0
    display_time(total_time)
    pygame.time.set_timer(count_up, 1000)
    pygame.time.set_timer(powerup_spawn, powerup_time)
    # Sprite Stuff
    all_sprite_list = pygame.sprite.Group()
    laser_list = pygame.sprite.Group()
    powerup_list = pygame.sprite.Group()
    ###########################################
    # Backgroud List
    # laser_list, grid_canvas = createlasers(40, 40)

    # laser = BackgroundTest.Laser(40, 40, pygame.Color(0, 255, 204))
    for x in range(0, 3 * difficulty, 1):
        spawn(laser_list, all_sprite_list, randint(200, 600), randint(-10, 10))
    # obstacles = startsquares(400)
    # circ = onecirclaser(400)
    # # laser_list.add(laser)
    # laser_list.add(obstacles)
    # laser_list.add(circ)
    # all_sprite_list.add(obstacles)
    # all_sprite_list.add(circ)
    ###########################################
    # Walls
    wall_list = pygame.sprite.Group()
    leftwall = Wall(-1, 0, 1, 800)
    topwall = Wall(0, -1, 800, 1)
    rightwall = Wall(799, 0, 1, 800)
    bottomwall = Wall(0, 799, 800, 1)

    wall_list.add(leftwall)
    wall_list.add(topwall)
    wall_list.add(rightwall)
    wall_list.add(bottomwall)
    all_sprite_list.add(leftwall)
    all_sprite_list.add(rightwall)
    all_sprite_list.add(topwall)
    all_sprite_list.add(bottomwall)
    ###########################################
    # Craft Stuff
    # boostimg = pygame.image.load('gameassets/1430802008.png')
    if craftchoice == 'fast':
        craft = FastCraft.Craft(10, 10)
    elif craftchoice == 'mid':
        craft = MidCraft.Craft(10, 10)
    elif craftchoice == 'tank':
        craft = TankCraft.Craft(10, 10)
    craft.walls = wall_list
    all_sprite_list.add(craft)

    # sounds
    errorsound = pygame.mixer.Sound('gameassets/error.ogg')
    powerupsound = pygame.mixer.Sound('gameassets/vgbeep.ogg')
    boostsound = pygame.mixer.Sound('gameassets/boost.ogg')
    hurtsound = pygame.mixer.Sound('gameassets/hurt.ogg')
    ##########################################
    while True:  # <--- main game loop
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()
            ################################
            elif event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    craft.changespeed(-15, 0)
                elif event.key == pygame.K_RIGHT:
                    craft.changespeed(15, 0)
                elif event.key == pygame.K_UP:
                    craft.changespeed(0, -15)
                elif event.key == pygame.K_DOWN:
                    craft.changespeed(0, 15)
                elif event.key == K_SPACE:
                    if craft.boost > 0:
                        boostsound.play()
                        craft.boost -= 10
                        for laser in laser_list:
                            laser.update(4)
                    else:
                        errorsound.play()
                elif event.key == K_p:
                    pause = True
                    paused()
            elif event.type == KEYUP:
                if event.key == pygame.K_LEFT:
                    craft.changespeed(15, 0)
                elif event.key == pygame.K_RIGHT:
                    craft.changespeed(-15, 0)
                elif event.key == pygame.K_UP:
                    craft.changespeed(0, 15)
                elif event.key == pygame.K_DOWN:
                    craft.changespeed(0, -15)

            elif event.type == count_up:
                total_time += 1
            elif event.type == spawn_more:
                spawn(laser_list, all_sprite_list, craft.rect.x, craft.rect.y)
                spawn_time -= 50
                pygame.time.set_timer(spawn_more, int(spawn_time))
            elif event.type == powerup_spawn:
                if len(powerup_list) == 0:
                    spawnpowerup(powerup_list, all_sprite_list)
                    pygame.time.set_timer(powerup_spawn, powerup_time)

            ###############################
        #######################################
        all_sprite_list.update()

        laser_hit_list = pygame.sprite.spritecollide(craft, laser_list, True)
        for hit in laser_hit_list:
            hurtsound.play()
            laser_list.remove(hit)
            all_sprite_list.remove(hit)
            if craftchoice == 'fast':
                craft.integrity -= 15 * difficulty
            elif craftchoice == 'mid':
                craft.integrity -= 10 * difficulty
            elif craftchoice == 'tank':
                craft.integrity -= 5 * difficulty
            spawn(laser_list, all_sprite_list, craft.rect.x, craft.rect.y)
            # print(craft.integrity)
        for laser in laser_list:
            if laser.rect.x < -50:
                total_obs += 1
                if craft.boost < 100:
                    if craftchoice == 'fast':
                        craft.boost += 15
                        if craft.boost > 100:
                            craft.boost == 100
                    elif craftchoice == 'mid':
                        craft.boost += 10
                    elif craftchoice == 'tank':
                        craft.boost += 5
                laser.reset_pos()
            elif laser.rect.y > 860:
                total_obs += 1
                if craft.boost < 100:
                    if craftchoice == 'fast':
                        craft.boost += 15
                        if craft.boost > 100:
                            craft.boost == 100
                    elif craftchoice == 'mid':
                        craft.boost += 10
                    elif craftchoice == 'tank':
                        craft.boost += 5
                laser.reset_pos()
            elif laser.rect.y < -100:
                total_obs += 1
                if craft.boost < 100:
                    if craftchoice == 'fast':
                        craft.boost += 15
                        if craft.boost > 100:
                            craft.boost == 100
                    elif craftchoice == 'mid':
                        craft.boost += 10
                    elif craftchoice == 'tank':
                        craft.boost += 5
                laser.reset_pos()

        powerup_hit_list = pygame.sprite.spritecollide(craft, powerup_list, True)
        for hit in powerup_hit_list:
            powerupsound.play()
            if hit.integrityup == 100:
                if craft.integrity < 100:
                    full = 100 - craft.integrity
                    craft.integrity += full
            else:
                if craft.boost < 100:
                    full = 100 - craft.boost
                    craft.boost += full
            powerup_list.remove(hit)
            all_sprite_list.remove(hit)
        screen.blit(background, (0, 0))

        if craft.integrity <= 0:
            return 'over', total_time
        if total_obs > 100:
            return 'gameover', total_time

        all_sprite_list.draw(screen)
        display_time(total_time)
        integritybar(craft.integrity)
        progression(total_obs)
        boostbar(craft.boost)
        # print(total_time)
        pygame.display.update()
        fps_clock.tick(fps)


def grats(cond, time, ship):
    """Continuation screen, outputs changing whether level passed or not.

    Will show user their total time, the ship they used, and options to continue or restart if they
    passed the level or lost the game.

    Args:
        cond (str): The condition of the game, 'over' if the player lost their integrity, and 'continue' if they passed
        the level.

        time (int): The total time it took the player to crash and burn, or to complete the level.

        ship (str): The ship the player choose to use
    """
    sfont = pygame.font.SysFont('gameassets/Anonymous Pro.tff', 50, False, False)
    choice_sprite_list = pygame.sprite.Group()
    sound_time = USEREVENT + 1
    timeforsound = 1000
    badsound = pygame.mixer.Sound('gameassets/gameover.ogg')
    goodsound = pygame.mixer.Sound('gameassets/success.ogg ')
    if cond == 'over':
        badsound.play()
    elif cond == 'continue':
        goodsound.play()
    if ship == 'fast':
        ship1 = FastCraft.Craft(380, 210)
        choice_sprite_list.add(ship1)
    elif ship == 'mid':
        ship2 = MidCraft.Craft(380, 210)
        choice_sprite_list.add(ship2)
    elif ship == 'tank':
        ship3 = TankCraft.Craft(380, 210)
        choice_sprite_list.add(ship3)
    pygame.time.set_timer(sound_time, timeforsound)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT event to exit the game
                pygame.quit()
                sys.exit()

            ################################

            elif event.type == KEYDOWN:
                if event.key == K_1 or event.key == K_KP1:
                    return 'fast'
                elif event.key == K_2 or event.key == K_KP2:
                    return 'mid'
                elif event.key == K_3 or event.key == K_KP3:
                    return 'tank'
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                        pygame.quit()
                        sys.exit()
                elif event.key == K_SPACE:
                    if cond == 'continue':
                        return 'level2'
                    else:
                        main()
            elif event.type == sound_time:
                if cond == 'over':
                    pass
            ###############################
        screen.blit(background, (0, 0))
        choice_sprite_list.draw(screen)
        if cond == 'continue':
            if time < 30:
                text = 'Wow, Pretty Fast! Lvl 1 complete'
                screen.blit(sfont.render(text, True, white), (150, 300))
            elif time > 90:
                text = 'Pretty Slow There. Lvl 1 complete'
                screen.blit(sfont.render(text, True, white), (150, 300))
            else:
                text = 'Lvl 1 complete'
                screen.blit(sfont.render(text, True, white), (150, 300))

            cont = 'Press Space to continue'
            exitbut = 'Press Enter to Quit'
            screen.blit(sfont.render(cont, True, white), (150, 400))
            screen.blit(sfont.render(exitbut, True, white), (150, 500))
        elif cond == 'over':
            text = 'You Died, Too Bad'
            over = 'Press Space to Restart'
            retry = 'Press Enter to Quit'
            screen.blit(sfont.render(text, True, white), (150, 300))
            screen.blit(sfont.render(over, True, white), (150, 400))
            screen.blit(sfont.render(retry, True, white), (150, 500))
        elif cond == 'gameover':
            text = 'You Beat the Game'
            over = 'Press Space to Restart'
            retry = 'Press Enter to Quit'
            screen.blit(sfont.render(text, True, white), (150, 300))
            screen.blit(sfont.render(over, True, white), (150, 400))
            screen.blit(sfont.render(retry, True, white), (150, 500))
        display_time(time, 150, 200)
        pygame.display.update()


# def scoresave(level, ship, time, difficulty):
#     score_file = open('gamedata/score.dat', 'wb')
#     score_list = [level, ship, time, difficulty]
#     pickle.dump(score_list, score_file)
#     score_file.close()
#
#
# def scoreload():
#     score_file = open('gamedata/score.dat', 'rb')
#     score_list = pickle.load(score_file)
#     score_file.close()
#     return score_list


def unpause():
    """ Simply changes global value of pause to False, to facilitate unpausing game

    """
    global pause
    pause = False


def paused():
    """ Pauses game, and blits the word 'Paused' onto game screen

    The method will pause the action and music, play the pause menu sound, and wait for the player to unpause by
        pressing the letter P. Then it will unpause both music and game.

    """
    pfont = pygame.font.SysFont('gameassets/Anonymous Pro.tff', 50, False, False)
    pausesound = pygame.mixer.Sound('gameassets/pause.ogg')
    unpausesound = pygame.mixer.Sound('gameassets/unpause.ogg')
    pygame.mixer.music.pause()
    pausesound.play()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    unpausesound.play()
                    pygame.mixer.music.unpause()
                    unpause()
        screen.blit(pfont.render('Paused',  True, white), (360, 400))
        pygame.display.update()
        fps_clock.tick(15)


def display_time(time, x=50, y=50):
    """Method to display the current time elapsed, in a more pleasant way than just outputting seconds.

    Args:
        time (int): The time pygame has calculated to have elapsed, in seconds.

        x (int): desired x coordinate to draw time onto, 50 is default.

        y (int): desired y coordinate to draw time onto, 50 is default.
    """
    timstr = 0
    if time < 60:
        timstr = '0:0' + str(time)
        if time > 9:
            timstr = '0:' + str(time)
    else:
        if time < 120:
            timstr = '1:0' + str(time % 60)
            if time > 69:
                timstr = '1:' + str(time % 60)
        elif time < 180:
            timstr = '2:0' + str(time % 120)
            if time > 129:
                timstr = '2:' + str(time % 60)
        elif time < 240:
            timstr = '3:0' + str(time % 180)
            if time > 189:
                timstr = '3:' + str(time % 60)

    time_left_txt = 'Total Time: ' + timstr
    screen.blit(font.render(time_left_txt, True, teal), (x, y))


def integritybar(integrity):
    """Bar drawn onto main screen that shows the craft's integrity

    Bar will be update with the screen, so will show an up-to-date value. Changes color based on total integrity.

    Args:
        integrity (int): Craft's integrity, goes down and up depending on whether a powerup or a enemy collided with
        player.

    """
    integ = int(integrity)
    # font = pygame.font.SysFont('Consolas', 20, False, False)
    # screen.blit(font.render(integ, True, Color(102, 51, 0)), (750, 50))
    pygame.draw.rect(screen, white, [680, 50, 102, 20], 2)
    if integ > 70:
            pygame.draw.rect(screen, green, [682, 52, integ, 17])
    elif integ > 40:
        pygame.draw.rect(screen, yellow, [682, 52, integ, 17])
    elif integ > 0:
        pygame.draw.rect(screen, red, [682, 52, integ, 17])


def boostbar(boost):
    """Boost bar drawn onto screen, that updates as the game plays.

    Args:
        boost (int): The current boost value associated to the player

    """
    boo = int(boost)
    pygame.draw.rect(screen, white, [680, 75, 102, 20], 2)
    if boo > 0:
        pygame.draw.rect(screen, blue, [682, 77, boo, 17])


def startsquares(xpos):
    """Creates a group of enemy sprites with a designated x coordinate.

    Args:
        xpos (int): Designated x coordinate for use by Sprite, if method is used during gameplay, it will use the
            player's x coordinate.

    Returns:
        laser_list (pygame.sprite.Group()): A group of 3 sprites

    """
    laser_list = pygame.sprite.Group()
    for x in range(0, 3, 1):
        cur_laser = EnemySprite1.Laser(xpos)
        laser_list.add(cur_laser)
    return laser_list


# def onesqlaser(xpos):
#     laser = EnemySprite1.Laser(xpos)
#     return laser
# def onecirclaser(xpos):
#     laser = EnemySprite3.Laser(xpos)
#     return laser
# def onetrilaser(xpos):
#     laser = EnemySprite2.Laser(xpos)
#     return laser
# def fireball():
#     laser = EnemySprite4.Laser()
#     return laser


def spawn(laser_list, all_sprites_list, xpos, ypos):
    """Method to spawn a random enemy given the laser_list and all_sprite_list

    Will spawn enemies, some will receive the player's current x or y coordinate to prevent them from staying in one
        place.

    Args:
        laser_list (sprite group): sprite group of all the enemies on screen
        all_sprites_list (sprite group): sprite group of all the elements in the game
        xpos (int): current x coordinate of the player
        ypos (int): current y coordinate of the player

    """
    tots_rand = randint(0, 4)
    if tots_rand == 0:
        laser = EnemySprite1.Laser(ypos)
        laser_list.add(laser)
        all_sprites_list.add(laser)
    elif tots_rand == 1:
        laser = EnemySprite2.Laser(xpos)
        laser_list.add(laser)
        all_sprites_list.add(laser)
    elif tots_rand == 2:
        laser = EnemySprite3.Laser(xpos)
        laser_list.add(laser)
        all_sprites_list.add(laser)
    elif tots_rand == 3:
        laser = EnemySprite4.Laser()
        laser_list.add(laser)
        all_sprites_list.add(laser)


def spawnpowerup(powerup_list, all_sprite_list):
    """Method to spawn a random powerup

    Will spawn powerups for the player to pick up

    Args:
        powerup_list (sprite group): sprite group of all the powerups on screen
        all_sprites_list (sprite group): sprite group of all the elements in the game
        xpos (int): current x coordinate of the player
        ypos (int): current y coordinate of the player

    """
    tots_rand = randint(0, 1)
    if tots_rand == 0:
        powerup = HealthPower.Health()
        powerup_list.add(powerup)
        all_sprite_list.add(powerup)
    elif tots_rand == 1:
        powerup = BoostPower.Boost()
        powerup_list.add(powerup)
        all_sprite_list.add(powerup)


def progression(total):
    """Progress bar drawn onto screen.

    Provided with total obstacles avoided, will draw a progress bar as the game plays out.

    Args:
        total (int): Total number of obstacles avoided.

    """
    percentage = total*6

    if percentage < 600:
        pygame.draw.rect(screen, yellow, [100, 787, percentage, 8])
    else:
        pygame.draw.rect(screen, yellow, [100, 787, 600, 8])

    pygame.draw.rect(screen, white, [100, 785, 600, 10], 2)


if __name__ == '__main__':
    main()
    doctest.testmod()
