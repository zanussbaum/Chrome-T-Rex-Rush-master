from matplotlib.pyplot import plot,show
from individual import Individual
from main import *
from pynput.keyboard import Key, Controller
from random import sample, random, randrange
from operator import attrgetter
from kmeans import KMeans
from statistics import mean
   
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
    min_obj = None
    for c in cacti:
        distance = c.rect.left - dino.rect.right
        if distance < min:
            min = distance
            min_obj = c
    for p in pteras:   
        distance = p.rect.left - dino.rect.right
        if distance < min:
            min = distance
            min_obj = p
    return min, min_obj


def act_on_scenario(species, cacti, pteras, dino, scenario, duck_counter):
    reaction = species[scenario]
    closest, closest_obj = det_closest(cacti, pteras, dino)
    if closest_obj and closest_obj.processed:
        return
    keyboard = Controller()
    if closest <= abs(reaction):
        closest_obj.processed = True
        if reaction > 0:
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        else:
            if duck_counter < 0:
                keyboard.release(Key.down)
            else:
                keyboard.press(Key.down)
                keyboard.release(Key.down)


def calc_offset(dino, container):
    offset = 0
    # Ignore those past us already
    for c in container:  
        if c.rect.right < dino.rect.left:             
            offset += 1    
    return offset


# look at scenario 6
# F: Whoops true haha, probably best to just delete that one
#   Or maybe better just hard code that to be no response
# i think scenario 4 showed up incorrectly

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
            print("We had no cacti and more than 2 Birds"    )
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
    frame_counter = 0
    duck_counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
    HI_image = pygame.Surface((22, int(11 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.1
    HI_rect.left = width * 0.73
    last_scenario = 0

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
                if scenario != last_scenario:
                    last_scenario = scenario
                if duck_counter > 0:
                    duck_counter -= 1
                    playerDino.isDucking = True
                else:
                    playerDino.isDucking = False
                if not (playerDino.isJumping and playerDino.isDucking and playerDino.isDead):
                    act_on_scenario(species.strategy, cacti, pteras, playerDino, scenario, duck_counter)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if not playerDino.isDucking:
                                if playerDino.rect.bottom == int(0.98 * height):
                                    playerDino.isJumping = True
                                    if pygame.mixer.get_init() is not None:
                                        jump_sound.play()
                                    playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True
                                duck_counter = 50

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN and duck_counter <= 0:
                            playerDino.isDucking = False

            if not move(cacti, playerDino, gamespeed):
                gameQuit = True
            if not move(pteras, playerDino, gamespeed):
                gameQuit = True
            add_cactus(last_obstacle, gamespeed, cacti)
            add_ptera(last_obstacle, gamespeed, pteras, frame_counter)

            if len(clouds) < 5 and randrange(0, 300) == 10:
                Cloud(width, randrange(height / 5, height / 2))

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
            if frame_counter % 700 == 699:
                new_ground.speed -= 1
                gamespeed += 1
            frame_counter = (frame_counter + 1)
        if gameQuit:
            break
    return playerDino.score



def main():
    population = 100
    individuals = [None] * population
    
    for spec in range(population):
        individuals[spec] = Individual()

    #initial running of individuals
    centroids,labels,closest = KMeans(individuals,4).run()


    for centroid in labels.keys():
        centroid.fitness = run_game(centroid)

    for centroid in labels.keys():
        for individual in labels.get(centroid):
            individual.fitness = individual.fitness_approx(centroid)

    fittest = max(individuals,key=attrgetter('fitness'))

    avg_fitness = []
    fittest_score = []
    

    generations = 0
    while generations < 3:
        print("fittest %s: %f" %(fittest, fittest.fitness))
        fittest_score.append(fittest.fitness)

        print("average fitness is %f" %(mean([ind.fitness for ind in individuals])))
        avg_fitness.append(mean([ind.fitness for ind in individuals]))

        generations += 1
        print("generation %d" %(generations))

        new_population = []
        while len(new_population) < len(individuals):
            operator = random()

            if operator < .9:
                ran_sample = sample(individuals,5)
                first_parent = max(ran_sample, key=attrgetter('fitness'))
                ran_sample = sample(individuals,5)
                second_parent = max(ran_sample, key=attrgetter('fitness'))

                first_child, second_child = first_parent.crossover(second_parent)
                new_population.append(first_child)
                new_population.append(second_child)
            else:
                ran_sample = sample(individuals,5)
                parent = max(ran_sample, key=attrgetter('fitness'))
                mutated = parent.mutate()
                new_population.append(mutated)

        individuals = new_population

        centroids,labels,closest = KMeans(individuals,4).run()

        for centroid in labels.keys():
            print("species %s" %(centroid))
            centroid.fitness = run_game(centroid)

        for centroid in labels.keys():
            for individual in labels.get(centroid):
                individual.fitness = individual.fitness_approx(centroid)

        
        fittest = max(individuals,key=attrgetter('fitness')) if max(individuals,key=attrgetter('fitness')).fitness > fittest.fitness else fittest

    print("running fittest")
    score = run_game(fittest)
    print("fittest had a score of %d" %(score))

    pygame.quit()
    quit()

    x = [i for i in range(generations)]

    plot(x,avg_fitness, 'x--')
    plot(x, fittest_score, '+--')
    show()


if __name__ == "__main__":
    main()

