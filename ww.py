import pygame

class Actor:
    '''
    Represents an Actor in the game. Can be the Player, a Monster, boxes, wall.
    Any object in the game's grid that appears on the stage, and has an
    x- and y-coordinate.
    '''
    
    def __init__(self, icon_file, stage, x, y, delay=5):
        '''
        (Actor, str, Stage, int, int, int) -> None
        Given the name of an icon file (with the image for this Actor),
        the stage on which this Actor should appear, the x- and y-coordinates
        that it should appear on, and the speed with which it should
        update, construct an Actor object.
        '''
        
        self._icon = pygame.image.load(icon_file) # the image image to display of self
        self.set_position(x, y) # self's location on the stage
        self._stage = stage # the stage that self is on

        # the following can be used to change this Actors 'speed' relative to other
        # actors speed. See the delay method.
        self._delay = delay
        self._delay_count = 0
        self.life = 5
    
    def set_position(self, x, y):
        '''
        (Actor, int, int) -> None
        Set the position of this Actor to the given x- and y-coordinates.
        '''
        
        (self._x, self._y) = (x, y)

    def get_position(self):
        '''
        (Actor) -> tuple of two ints
        Return this Actor's x and y coordinates as a tuple.
        '''
        
        return (self._x, self._y)

    def get_icon(self):
        '''
        (Actor) -> pygame.Surface
        Return the image associated with this Actor.
        '''
        
        return self._icon

    def is_dead(self):
        '''
        (Actor) -> bool
        Return True iff this Actor is not alive.
        '''
        if self.life == 0:
            return True
        return False

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool

        Other is an Actor telling us to move in direction (dx, dy). In this case, we just move.
        (dx,dy) is in {(1,1), (1,0), (1,-1), (0,1), (0,0), (0,-1), (-1,1), (-1,0), (-1,-1)}
    
        In the more general case, in subclasses, self will determine 
        if they will listen to other, and if so, will try to move in
        the specified direction. If the target space is occupied, then we 
        may have to ask the occupier to move.
        '''

        self.set_position(self._x + dx, self._y + dy)
        return True

    def delay(self):
        '''
        (Actor) -> bool
        Manage self's speed relative to other Actors. 
        Each time we get a chance to take a step, we delay. If our count wraps around to 0
        then we actually do something. Otherwise, we simply return from the step method.
        '''

        self._delay_count = (self._delay_count+1) % self._delay
        return self._delay_count == 0

    def step(self):
        '''
        (Actor) -> None
        Make the Actor take a single step in the animation of the game.
        self can ask the stage to help as well as ask other Actors
        to help us get our job done.
        '''

        if self.is_dead():
            self._stage.remove_actor(self)  #Actor is dead


class Player(Actor):
    '''
    A Player is an Actor that can handle events. These typically come
    from the user, for example, key presses etc.
    '''

    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Player, str, Stage, int, int) -> None
        Construct a Player with given image, on the given stage, at
        x- and y- position.
        '''
        
        Actor.__init__(self, icon_file, stage, x, y)
    
    def handle_event(self, event):
        '''
        Used to register the occurrence of an event with self.
        '''
        
        pass


class KeyboardPlayer(Player):
    '''
    A KeyboardPlayer is a Player that can handle keypress events.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        Construct a KeyboardPlayer. Other than the given Player information,
        a KeyboardPlayer also keeps track of the last key event that took place.
        '''
        
        Player.__init__(self, icon_file, stage, x, y)
        self._last_event = None # we are only interested in the last event
        self.dead = False
    
    def handle_event(self, event):
        '''
        (KeyboardPlayer, int) -> None
        Record the last event directed at this KeyboardPlayer.
        All previous events are ignored.
        '''

        self._last_event = event

    def is_dead(self):
        if self.life == 0 and not self.dead:
            pygame.mixer.music.stop()
            pygame.mixer.Sound('game_over.wav').play()
            self.dead = True
            return True
        elif self.life == 0:
            return True
        return False

    def step(self):
        '''
        (KeyboardPlayer) -> None
        Take a single step in the animation. 
        For example: if the user asked us to move right, then we do that.
        '''
        if self._last_event is not None:
            dx, dy = None, None
            if self._last_event == pygame.K_DOWN or self._last_event == pygame.K_KP5:
                dx, dy = 0,1
                self._icon = pygame.image.load("icons/face-cool-24-down.png")
            if self._last_event == pygame.K_LEFT or self._last_event == pygame.K_KP4:
                dx, dy = -1,0
                self._icon = pygame.image.load("icons/face-cool-24-left.png")
            if self._last_event == pygame.K_RIGHT or self._last_event == pygame.K_KP6:
                dx, dy = 1,0
                self._icon = pygame.image.load("icons/face-cool-24-right.png")
            if self._last_event == pygame.K_UP  or self._last_event == pygame.K_KP8:
                dx, dy = 0,-1
                self._icon = pygame.image.load("icons/face-cool-24-up.png")
            if self._last_event == pygame.K_KP7:
                dx, dy = -1,-1
            if self._last_event == pygame.K_KP9:
                dx, dy = 1,-1
            if self._last_event == pygame.K_KP1:
                dx, dy = -1,1
            if self._last_event == pygame.K_KP3:
                dx, dy = 1,1
            if dx is not None and dy is not None:
                self.move(self, dx, dy) # we are asking ourself to move

            self._last_event = None

        if self.is_dead():
            self._stage.remove_actor(self)

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        # Where we are supposed to move. 
        new_x = self._x + dx
        new_y = self._y + dy        

        # FIX THIS ACCORDING TO LAB INSTRUCTIONS IN PART 1
        # Check if (new_x, new_y) is on the stage.
        # If it is, then determine if another Actor is occupying that spot. If so,
        # self asks them to move. If they moved, then we can occupy the spot. Otherwise
        # we can't move. We return True if we moved and False otherwise.
        if self._stage.is_in_bounds(new_x, new_y):
            if self._stage.get_actor(new_x, new_y) != None and not isinstance(self._stage.get_actor(new_x, new_y), Monster):
                if self._stage.get_actor(new_x, new_y).move(self, dx, dy) == True:
                    return Actor.move(self, other, dx, dy)
            elif isinstance(self._stage.get_actor(new_x, new_y), NormalMonster):
                self.life = 0
                return False
            elif isinstance(self._stage.get_actor(new_x, new_y), EzMonster):
                self._stage.get_actor(new_x, new_y).life = 0
                Actor.move(self, other, dx, dy)
                return True
            elif isinstance(self._stage.get_actor(new_x, new_y), Flame):
                self.life = 0
                return False
            else:
                return Actor.move(self, other, dx, dy)
        else:
            return False


class Box(Actor):
    '''
    A Box Actor.
    '''
    
    def __init__(self, icon_file, stage, x=0, y=0):
        '''
        (Actor, str, Stage, int, int) -> None
        Construct a Box on the given stage, at given position.
        '''
        
        Actor.__init__(self, icon_file, stage, x, y)

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        new_x = self._x + dx
        new_y = self._y + dy

        # FIX THIS ACCORDING TO LAB INSTRUCTIONS IN PART 1
        # If (new_x, new_y) is on the stage, and is empty, then
        # we simply move there. Otherwise, we ask whomever is at (new_x, new_y)
        # to move, also the same direction. If they moved, the space is now
        # empty, so we now move into (new_x, new_y). If we successfully
        # moved, then we return True, otherwise, we return False. '''

        if self._stage.is_in_bounds(new_x, new_y):
            if self._stage.get_actor(new_x, new_y) != None:
                if self._stage.get_actor(new_x, new_y).move(self, dx, dy) == True:
                    return Actor.move(self, other, dx, dy)
            else:
                return Actor.move(self, other, dx, dy)
        else:
            return False


class StickyBox(Box):
    '''
    A Box Actor.
    '''


    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, ask that Actor to move to make space, and then
        move to that spot, if possible.
        If a move is not possible, then return False.
        '''

        new_x = self._x + dx
        new_y = self._y + dy

        # FIX THIS ACCORDING TO LAB INSTRUCTIONS IN PART 1
        # If (new_x, new_y) is on the stage, and is empty, then
        # we simply move there. Otherwise, we ask whomever is at (new_x, new_y)
        # to move, also the same direction. If they moved, the space is now
        # empty, so we now move into (new_x, new_y). If we successfully
        # moved, then we return True, otherwise, we return False. '''

        if self._stage.is_in_bounds(new_x, new_y):
            if self._stage.get_actor(new_x, new_y) != None:
                if isinstance(self._stage.get_actor(new_x, new_y), Monster):
                    self._stage.get_actor(new_x, new_y).stuck = True
                    self._stage.get_actor(new_x, new_y).stick_with = self
                if self._stage.get_actor(new_x, new_y).move(self, dx, dy) == True:
                    return Actor.move(self, other, dx, dy)
            else:
                return Actor.move(self, other, dx, dy)
        else:
            return False



# COMPLETE THIS CLASS FOR PART 2 OF LAB
class Wall(Actor):

    def __init__(self, icon_file, stage, x=0, y=0):
        Actor.__init__(self, icon_file, stage, x, y)

    def move(self, other, dx, dy):
        return False


class Monster(Actor):
    '''A Monster class.'''

    def __init__(self, icon_file, stage, x=0, y=0, delay=5):
        '''Construct a Monster.'''

        Actor.__init__(self, icon_file, stage, x, y, delay)
        self._dx = 1
        self._dy = 1
        self.trapped = False
        self.stuck = False
        self.stick_with = None
        self.stick_position = None

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''
        if self.is_dead():
            self._stage.remove_actor(self)
        if self.is_trapped():
            self.life -= 1
        elif not self.is_trapped():
            self.life = 5
        if self.stuck:
            if self._stage.get_actor(self.stick_position[0], self.stick_position[1]) == self.stick_with:
                return None
            else:
                self.stick_with = None
                self.stuck = False
                self.stick_position = None
        if not self.delay():
            return None
        self.move(self, self._dx, self._dy)
        return True

    def move(self, other, dx, dy):
        '''
        (Actor, Actor, int, int) -> bool
        Move this Actor by dx and dy, if possible. other is the Actor that asked to make this move.
        If a move is possible (a space is available) then move to it and return True.
        If another Actor is occupying that space, or if that space is out of bounds,
        bounce back in the opposite direction.
        If a bounce back happened, then return False.
        '''

        if other != self:  # Noone pushes me around
            return False

        bounce_off_edge = False

        new_x = self._x + self._dx
        new_y = self._y + self._dy

        if not self._stage.is_in_bounds_x(new_x):
            self._dx = -self._dx
            bounce_off_edge = True

        if not self._stage.is_in_bounds_y(new_y):
            self._dy = - self._dy
            bounce_off_edge = True

        if bounce_off_edge:
            return False

        # FIX THIS FOR PART 3 OF THE LAB
        # MONSTERS SHOULD BOUNCE BACK FROM BOXES AND OTHER MONSTERS
        # HINT: Use actor = self._stage.get_actor(new_x,new_y)
        # YOUR CODE HERE
        #if self._stage.get_actor(new_x, new_y) != None:
        if self._stage.is_in_bounds(new_x, new_y):
            actor = self._stage.get_actor(new_x, new_y)
            if actor == None:
                return Actor.move(self, other, dx, dy)
            elif isinstance(actor, KeyboardPlayer):
                self._stage.get_actor(new_x, new_y).life = 0
                return False
            elif isinstance(actor, StickyBox):
                self.stuck = True
                self.stick_with = actor
                self.stick_position = actor.get_position()
            else:
                self._dx, self._dy = -self._dx, -self._dy
                return False
        else:
            return not Actor.move(self, other, dx, dy)

    def is_trapped(self):
        x, y  = self._x, self._y
        range_x = [x-1, x, x+1]
        range_y = [y-1, y, y+1]
        for dx in range_x:
            for dy in range_y:
                if not(isinstance(self._stage.get_actor(dx,dy), Box) or isinstance(self._stage.get_actor(dx,dy), Monster) or not self._stage.is_in_bounds(dx, dy)):
                    return False
        return True


class NormalMonster(Monster):

    pass


class EzMonster(Monster):

    pass


class ExplodingMonster(Monster):

    def __init__(self, icon_file, stage, x=0, y=0, delay=5, exploding_delay = 0):
        '''Construct a Monster.'''
        super().__init__(icon_file, stage, x, y, delay=5)
        self.life = 10 + exploding_delay

    def step(self):
        '''
        Take one step in the animation (this Monster moves by one space).
        If it's being delayed, return None. Else, return True.
        '''
        if self.is_trapped():
            self.life -= 1
        self.life -= 1
        if self.is_dead():
            self._stage.remove_actor(self)
            self.explode()
        if not self.delay():
            return None
        self.move(self, self._dx, self._dy)
        return True

    def explode(self):
        x, y  = self._x, self._y
        range_x = [x-1, x, x+1]
        range_y = [y-1, y, y+1]
        for dx in range_x:
            for dy in range_y:
                if self._stage.is_in_bounds(dx, dy):
                    if isinstance(self._stage.get_actor(dx, dy), KeyboardPlayer):
                        self._stage.get_actor(dx, dy).life = 0
                    if self._stage.get_actor(dx, dy) != None:
                        self._stage.remove_actor(self._stage.get_actor(dx, dy))
                    self._stage.add_actor(Flame("icons/block-sign.ico", self._stage, dx, dy, 1)) #TODO: add flame icon here!
        return True


class Flame(Monster):

    def __init__(self, icon_file, stage, x, y, delay=1):
        super().__init__(icon_file, stage, x, y, delay=1)
        self.life = 10

    def step(self):
        self.life -= 1
        if self.is_dead():
            self._stage.remove_actor(self)

    def move(self, other, dx, dy):
        pass


class Stage:
    '''
    A Stage that holds all the game's Actors (Player, monsters, boxes, etc.).
    '''
    
    def __init__(self, width, height, icon_dimension):
        '''Construct a Stage with the given dimensions.'''


        self._actors = [] # all actors on this stage (monsters, player, boxes, ...)
        self._player = None # a special actor, the player

        # the logical width and height of the stage
        self._width, self._height = width, height

        self._icon_dimension=icon_dimension # the pixel dimension of all actors
        # the pixel dimensions of the whole stage
        self._pixel_width = self._icon_dimension * self._width
        self._pixel_height = self._icon_dimension * self._height
        self._pixel_size = self._pixel_width, self._pixel_height

        # get a screen of the appropriate dimension to draw on
        self._screen = pygame.display.set_mode(self._pixel_size)

        fontObj = pygame.font.Font('freesansbold.ttf', 32) # the first parameter is font of text, the second parameter is the size of text.
        self.textSurfaceObj = fontObj.render('You are dead!', True, (0, 255, 0), (0, 0, 128)) # the first tuple is font color, the second tuple is background color.
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (240, 240)



    def is_in_bounds(self, x, y):
        '''
        (Stage, int, int) -> bool
        Return True iff the position (x, y) falls within the dimensions of this Stage.'''
        
        return self.is_in_bounds_x(x) and self.is_in_bounds_y(y)

    def is_in_bounds_x(self, x):
        '''
        (Stage, int) -> bool
        Return True iff the x-coordinate given falls within the width of this Stage.
        '''
        
        return 0 <= x and x < self._width

    def is_in_bounds_y(self, y):
        '''
        (Stage, int) -> bool
        Return True iff the y-coordinate given falls within the height of this Stage.
        '''

        return 0 <= y and y < self._height

    def get_width(self):
        '''
        (Stage) -> int
        Return width of Stage.
        '''

        return self._width

    def get_height(self):
        '''
        (Stage) -> int
        Return height of Stage.
        '''
        
        return self._height

    def set_player(self, player):
        '''
        (Stage, Player) -> None
        A Player is a special actor, store a reference to this Player in the attribute
        self._player, and add the Player to the list of Actors.
        '''
        
        self._player=player
        self.add_actor(self._player)

    def remove_player(self):
        '''
        (Stage) -> None
        Remove the Player from the Stage.
        '''
        
        self.remove_actor(self._player)
        self._player=None

    def player_event(self, event):
        '''
        (Stage, int) -> None
        Send a user event to the player (this is a special Actor).
        '''
        
        self._player.handle_event(event)

    def add_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Add the given actor to the Stage.
        '''

        self._actors.append(actor)

    def remove_actor(self, actor):
        '''
        (Stage, Actor) -> None
        Remove the given actor from the Stage.
        '''
        
        self._actors.remove(actor)

    def step(self):
        '''
        (Stage) -> None
        Take one step in the animation of the game. 
        Do this by asking each of the actors on this Stage to take a single step.
        '''

        for a in self._actors:
            a.step()

    def get_actors(self):
        '''
        (Stage) -> None
        Return the list of Actors on this Stage.
        '''
        
        return self._actors

    def get_actor(self, x, y):
        '''
        (Stage, int, int) -> Actor or None
        Return the first actor at coordinates (x,y).
        Or, return None if there is no Actor in that position.
        '''
        
        for a in self._actors:
            if a.get_position() == (x,y):
                return a
        return None

    def draw(self):
        '''
        (Stage) -> None
        Draw all Actors that are part of this Stage to the screen.
        '''
        
        self._screen.fill((0,0,0)) # (0,0,0)=(r,g,b)=black
        for a in self._actors:
            icon = a.get_icon()
            (x,y) = a.get_position()
            d = self._icon_dimension
            rect = pygame.Rect(x*d, y*d, d, d)
            self._screen.blit(icon, rect)
        if self._player.is_dead():
            self._screen.blit(self.textSurfaceObj, self.textRectObj)
        pygame.display.flip()

