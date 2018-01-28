import sys, pygame, random
from ww import *
pygame.init()
pygame.key.set_repeat(100, 50) # keyboard repeat behaviour. (delay, interval) unit: millisecond.

ww=Stage(20, 20, 24)
ww.set_player(KeyboardPlayer("icons/face-cool-24-up.png", ww))
ww.add_actor(Wall("icons/wall.jpg", ww, 3, 4))
ww.add_actor(ExplodingMonster("icons/face-angry.png", ww, 0, 3, 1, 20))
ww.add_actor(ExplodingMonster("icons/face-angry.png", ww, 7, 4, 1, 20))
ww.add_actor(NormalMonster("icons/face-devil-grin-24.png", ww, 4, 10, 3))
ww.add_actor(NormalMonster("icons/face-devil-grin-24.png", ww, 5, 20, 2))
ww.add_actor(EzMonster("icons/face-sick.png", ww, 2, 4, 3))
# the greater the value of delay, the slower the monster will move.
# if the EzMonster touch Player, Player will die.
# the forth value of ExplodingMonster is delay time of explotion.

# YOUR COMMENT GOES HERE. BRIEFLY DESCRIBE WHAT THE FOLLOWING LOOP DOES.
num_boxes=0
while num_boxes<90:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(Box("icons/emblem-package-2-24.png", ww, x, y))
        num_boxes+=1

num_sticky_boxes=0
while num_sticky_boxes<10:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(StickyBox("icons/applications.ico", ww, x, y)) #TODO: find an special icon for sticky boxes.
        num_sticky_boxes+=1

pygame.mixer.music.load('background.mid')
pygame.mixer.music.play(-1, 0.0)

# YOUR COMMENT GOES HERE. BRIEFLY DESCRIBE WHAT THE FOLLOWING LOOP DOES.
while True:
    pygame.time.wait(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
                ww.player_event(event.key)
    ww.step()
    ww.draw()