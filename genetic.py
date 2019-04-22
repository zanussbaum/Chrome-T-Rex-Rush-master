from individual import Individual
from main import *
from pynput.keyboard import Key, Controller


def det_testers(individuals):
    max_diff = 100
    species1 = None
    species2 = None
    for ind1 in individuals:
        for ind2 in individuals:
            if ind1 != ind2:
                sim = ind1.similarity(ind2)
                if sim < max_diff:
                    max_diff = sim
                    species1 = ind1
                    species2 = ind2
    return species1, species2


def det_closest(cacti, pteras, dino):
    min = 1000
    for c in cacti:
        distance = c.rect.left - dino.rect.right
        if distance < min:
            min = distance
    for p in pteras:
        distance = p.rect.left - dino.rect.right
        if distance < min:
            min = distance
    return min


def act_on_scenario(species, cacti, pteras, dino, scenario):
    reaction = species[scenario]
    closest = det_closest(cacti, pteras, dino)
    if closest <= abs(reaction):
        keyboard = Controller()
        if reaction > 0:
            keyboard.press(Key.up)
        else:
            keyboard.press(Key.down)


def calc_offset(dino, container):
    offset = 0
    # Ignore those past us already
    for c in container:
        if c.rect.right < dino.rect.left:
            offset += 1
    return offset


def select_scenario(cacti, pteras, dino):
    offset_cactus = calc_offset(dino, cacti)
    cacti_amt = len(cacti) - offset_cactus
    offset_ptera = calc_offset(dino, pteras)
    ptera_amt = len(pteras) - offset_ptera
    if cacti_amt == 1:
        if ptera_amt == 0:
            return 0
        elif ptera_amt == 1:
            return 1
        elif ptera_amt == 2:
            return 2
        else:
            print("We had 1 cactus and more than 2 Birds")
            exit(-1)
    elif cacti_amt == 2:
        if ptera_amt == 0:
            return 3
        elif ptera_amt == 1:
            return 4
        elif ptera_amt == 2:
            return 5
        else:
            print("We had 2 cacti and more than 2 Birds")
            exit(-1)
    elif cacti_amt == 0:
        if ptera_amt == 0:
            return 6
        elif ptera_amt == 1:
            return 7
        elif ptera_amt == 2:
            return 8
        else:
            print("We had no cacti and more than 2 Birds")
            exit(-1)
    else:
        print("We had more than 2 cacti")
        exit(-1)


def run_game(species):
    global high_score
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    playerDino = Dino(44, 47)
    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image, retbutton_rect = load_image('replay_button.png', 35, 31, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 190, 11, -1)

    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
    HI_image = pygame.Surface((22, int(11 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.1
    HI_rect.left = width * 0.73

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                # This seems to process the input and is NOT correlated to game events
                # Right here seems the best place to decide on movements
                scenario = select_scenario(cacti, pteras, playerDino)
                act_on_scenario(species.strategy, cacti, pteras, playerDino, scenario)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if playerDino.rect.bottom == int(0.98 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() is not None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

            if not move(cacti, playerDino, gamespeed):
                gameQuit = True
                species.fitness = high_score
            if not move(pteras, playerDino, gamespeed):
                gameQuit = True
                species.fitness = high_score
            add_cactus(last_obstacle, gamespeed, cacti)
            add_ptera(last_obstacle, gamespeed, pteras, counter)

            if len(clouds) < 5 and random.randrange(0, 300) == 10:
                Cloud(width, random.randrange(height / 5, height / 2))

            playerDino.update()
            cacti.update()
            pteras.update()
            clouds.update()
            new_ground.update()
            scb.update(playerDino.score)
            highsc.update(high_score)

            #draw updated
            if pygame.display.get_surface() is not None:
                screen.fill(background_col)
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                cacti.draw(screen)
                pteras.draw(screen)
                playerDino.draw()
                pygame.display.update()
            clock.tick(FPS)

            if playerDino.isDead:
                gameOver = True
                if playerDino.score > high_score:
                    high_score = playerDino.score

            if counter % 700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        if gameQuit:
            break

        #Game Over loop, Since we never replay can maybe cut this entirely
        while gameOver:
            if pygame.display.get_surface() is None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameplay()
            highsc.update(high_score)
            if pygame.display.get_surface() is not None:
                disp_gameOver_msg(retbutton_image, gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


def main():
    population = 20
    individuals = [population]
    for spec in range(population):
        individuals[spec] = Individual()
    species1, species2 = det_testers(individuals)
    run_game(species1)
    run_game(species2)
    for ind in individuals:
        if ind != species1 and ind != species2:
            ind.fitness = (ind.fitness_approx(species1) + ind.fitness_approx(species2)) / 2
    # Crossover and Mutation


if __name__ == "__main__":
    main()
