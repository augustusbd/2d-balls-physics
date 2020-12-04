
# Python imports
from random import randint
from math import sqrt

# Library imports
import pygame
from pygame.key import *
from pygame.locals import *
from pygame.color import *

# pymunk imports
import pymunk
import pymunk.pygame_util



class BallPhysics(object):
    """
    This class implements a simple scene in which there is a static box
    (made up of a couple lines) that don't move. Two balls will interact with
    the environment.
    """
    def __init__(self):
        self._size = 300

        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 0.0)

        # Physics
        # Time step
        self._dt = 1.0 / 60.0
        # Number of physics per screen frame
        self._physics_steps_per_frame = 1

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode((self._size, self._size))
        self._clock = pygame.time.Clock()

        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        # Balls that exist in the world
        self._balls = []
        self._max_balls = 2
        # positions of mouse events for creation of balls
        self.pos1, self.pos2 = None, None

        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks = 10

    def run(self):
        """
        The main looop of the game.
        :return: None
        """
        # Main loop
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)

            self._process_events()
            self._clear_screen()
            self._draw_objects()
            pygame.display.flip()

            # Delay fixed time between frames
            self._clock.tick(50)
            pygame.display.set_caption(f"fps: {str(self._clock.get_fps())}")

    def _add_static_scenery(self):
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_box = [pymunk.Segment(static_body, (5.0, 5.0), (5.0, self._size-5), 1.0),
                      pymunk.Segment(static_body, (5.0, 5.0), (self._size-5, 5.0), 1.0),
                      pymunk.Segment(static_body, (5.0, self._size-5), (self._size-5, self._size-5), 1.0),
                      pymunk.Segment(static_body, (self._size-5, 5.0), (self._size-5, self._size-5), 1.0)]

        for edge in static_box:
            edge.elasticity = 0.999
            edge.friction = 0.2
        self._space.add(static_box)

    def _process_events(self):
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self._running = False

            # Creating Balls
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.pos1 = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.pos2 = pygame.mouse.get_pos()
                self._update_balls()

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self._running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")
                print("Saved image: bouncing_balls.png")

    def _update_balls(self):
        """
        Create a ball.
        :return:
        """
        # Create Ball if < self._max_balls and there are positions 1 & 2
        if (self.pos1, self.pos2) != (None, None) and len(self._balls) < self._max_balls:
            pos1_x, pos1_y = self.pos1
            pos2_x, pos2_y = self.pos2
            initial_position = self.pos1

            # x & y components of initial velocity
            v_x = pos2_x - pos1_x
            v_y = pos2_y - pos1_y
            initial_velocity = (v_x, v_y)

            self._create_ball(initial_position, initial_velocity)
            self.pos1, self.pos2 = None, None

    def _create_ball(self, initial_position, initial_velocity):
        """
        Create a ball.
        Coordinate system
        :return:
        """
        mass =  10
        radius = 5
        offset = (0, 0)
        inertia = pymunk.moment_for_circle(mass, 0, radius, offset)
        x, y = self._change_coordinates(initial_position)
        v_x, v_y = initial_velocity

        body = pymunk.Body(mass, inertia)
        body.position = x, y
        # velocity in y-direction is opposite because of coordinates in pymunk
        body.velocity = v_x, -v_y

        shape = pymunk.Circle(body, radius, offset)
        shape.elasticity = 0.999
        shape.friction = 0.1

        self._space.add(body, shape)
        self._balls.append(shape)

    def _change_coordinates(self, coords):
        """
        Change coordinates so ball starts where MOUSEBUTTONDOWN activates.
        The x position is the same.
        The y position needs to be changed.
        :return:
        """
        x, y = coords
        new_y = self._size - y
        new_coords = (x, new_y)
        return new_coords

    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(THECOLORS["white"])

    def _draw_objects(self):
        """
        Draw the objects.
        :return: None
        """
        self._space.debug_draw(self._draw_options)


if __name__ == '__main__':
    game = BallPhysics()
    game.run()
