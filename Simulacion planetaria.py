import pygame
import math
pygame.init()

width, heigth = 800, 800
win =  pygame.display.set_mode((width, heigth))
pygame.display.set_caption("Simulacion planetaria")

#Colores
white = (255, 255, 255)
yellow = (255, 255, 0)
blue = (100, 149, 237)
red = (188, 39, 50)
dark_gray = (80, 78, 81)
black = (0, 0, 0)
orange = (254, 80, 0)
gold = (239, 184, 16)
light_blue = (12, 183, 242)
dark_blue = (37, 40, 80)


font = pygame.font.SysFont("comicsans", 16)

class Planet: 
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    Scale = 150 / AU #1 Au = 100 px 
    #Dejar la escala en 150 si solo se quieren ver los primeros 4 planetas (mercurio, venus, tierra y marte)
    #bajar la escala a 10 para ver los otros 4 planetas (jupiter, saturno, urano y neptuno)
    TimeStep = 3600*24 #1 dia

    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []    
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):		
        x = self.x * self.Scale + width / 2		
        y = self.y * self.Scale + heigth / 2

		
        if len(self.orbit) > 2:			
            updated_points = []			
            for point in self.orbit:				
                x, y = point				
                x = x * self.Scale + width / 2				
                y = y * self.Scale + heigth / 2				
                updated_points.append((x, y))
			
            pygame.draw.lines(win, self.color, False, updated_points, 2)
		
        pygame.draw.circle(win, self.color, (x, y), self.radius)
				
        if not self.sun:
                distance_text = font.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, white)
                win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

        
    def attraction(self, other):
        other_x, other_y = other.x, other.y		
        distance_x = other_x - self.x		
        distance_y = other_y - self.y		
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		
        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2		
        theta = math.atan2(distance_y, distance_x)		
        force_x = math.cos(theta) * force		
        force_y = math.sin(theta) * force		
        return force_x, force_y
    
    def update_pos(self, planets): 
        total_fx = total_fy = 0
        for planet in planets: 
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx 
            total_fy+= fy

        self.x_vel += total_fx / self.mass * self.TimeStep
        self.y_vel += total_fy / self.mass * self.TimeStep

        self.x += self.x_vel * self.TimeStep
        self.y += self.y_vel * self.TimeStep
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    #Planetas
    sun = Planet(0, 0, 30, yellow, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, blue, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    
    mars = Planet(-1.524 * Planet.AU, 0, 12, red, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, dark_gray, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14,  white, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(Planet.AU * 5.203, 0, 26, orange, 1.898 * 10**27)
    jupiter.y_vel = -13.06 * 1000   

    saturn = Planet(Planet.AU * 9.58, 0, 22, gold, 5.683 * 10**26)
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(Planet.AU * 19.22, 0, 18, light_blue, 8.681 * 10**25)
    uranus.y_vel = -6.81 * 1000

    neptune = Planet(Planet.AU * 30.05, 0, 20, dark_blue, 1.024 * 10**26)
    neptune.y_vel = -5.43 * 1000


    #array de planetas
    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run: 
        clock.tick(60)
        win.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets: 
            planet.update_pos(planets)
            planet.draw(win)

        pygame.display.update()

    pygame.quit()

main()