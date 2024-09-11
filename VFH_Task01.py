import pygame
import math

pygame.init()

# Screen Setup
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulation for VFH algorithm by bilal alasha")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Robot variables
robot_radius = 15  
robot_x, robot_y = 100, 100 
robot_angle = 0
robot_speed = 2

# VFH Parameters
NumOfSectors = 36  # Number of sectors for obstacle detection
SectorAngle = 2 * math.pi / NumOfSectors  # Angle of each sector
MaxSpeed = 3
MinSpeed = 1
SonarRange = 150

# Target location
target_x, target_y = 700, 500 

# Obstacles
obstacles = [
    # [x,y,width,height]
    (50, 50, 800, 20),
    (50, 530, 700, 20),
    (50, 50, 20, 500),
    (150, 50, 20, 20),
    (730, 50, 20, 500),
    (200, 50, 20, 200),
    (300, 50, 20, 200),
    (400, 300, 20, 230),
    (400, 300, 200, 20),
    (350, 350, 340, 40),
    (600, 300, 20, 100),
    (500, 300, 20, 100),
    (650, 300, 20, 100),
]

def draw_robot(x, y, angle):
    pygame.draw.circle(screen, BLUE, (int(x), int(y)), robot_radius)
    # Draw direction line(thanks gpt)
    end_x = x + math.cos(angle) * robot_radius
    end_y = y + math.sin(angle) * robot_radius
    pygame.draw.line(screen, GREEN, (x, y), (end_x, end_y), 3)

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)

def draw_target(x, y):
    pygame.draw.circle(screen, YELLOW, (int(x), int(y)), 10)

# Sonar function 
def cast_sonar(x, y, angle):
    ray_x = x
    ray_y = y
    for i in range(SonarRange):
        ray_x += math.cos(angle)
        ray_y += math.sin(angle)
        if ray_x < 0 or ray_x > width or ray_y < 0 or ray_y > height:
            break
        # Check if ray hits any obstacles (with considering the robot's radius thanks gpt)
        for obs in obstacles:
            obs_left = obs[0] - robot_radius
            obs_right = obs[0] + obs[2] + robot_radius
            obs_top = obs[1] - robot_radius
            obs_bottom = obs[1] + obs[3] + robot_radius
            if obs_left <= ray_x <= obs_right and obs_top <= ray_y <= obs_bottom:
                pygame.draw.line(screen, GRAY, (x, y), (ray_x, ray_y), 1)  # Draw sonar ray
                return math.dist((x,y),(ray_x,ray_y))
    pygame.draw.line(screen, GRAY, (x, y), (ray_x, ray_y), 1)  # Draw sonar ray to max range
    return SonarRange

# Sector density calculation with radius consideration
def calculate_sector_densities(x, y):
    sector_densities = [0] * NumOfSectors
    for i in range(NumOfSectors):
        angle = i * SectorAngle
        distance = cast_sonar(x, y, angle)
        obstacle_density = 1 / distance  
        sector_densities[i] = obstacle_density
    return sector_densities

def find_best_sector(sector_densities, robot_x, robot_y):
    best_sector = -1
    # cool thing in pythn you can use infinite insted of using a really big number(thanks gpt)
    lowest_density = float('inf')

    # Calculate the angle to the target (thanks gpt)
    target_angle = math.atan2(target_y - robot_y, target_x - robot_x)

    # Find the closest sector to the target direction that has low obstacle density
    target_sector = int(target_angle // SectorAngle) % NumOfSectors

    # Check a range of sectors around the target sector and penalize sectors with high densities note the range of the for is just by testing no math reasin behind it
    for i in range(-5, 5):  
        sector_index = (target_sector + i) % NumOfSectors
        if sector_densities[sector_index] < lowest_density and sector_densities[sector_index] < 0.4:  # More cautious threshold (thanks gpt i have no idea what is this)
            lowest_density = sector_densities[sector_index]
            best_sector = sector_index

    # If no valid sector is found, pick the sector with the least density
    if best_sector == -1:
        for i in range(NumOfSectors):
            if sector_densities[i] < lowest_density:
                lowest_density = sector_densities[i]
                best_sector = i

    return best_sector

def calculate_speed_and_angle(best_sector):
    # Convert the sector index to an angle
    desired_angle = best_sector * SectorAngle

    # Adjust speed based on how clear the path is
    speed = MaxSpeed if desired_angle == robot_angle else MinSpeed

    return speed, desired_angle

# i was having a hard time notcing some very small collisions so this in theory should just be for testing but the code is not alwayes working with some obstacles so i will leave it
def check_collision(robot_x, robot_y):
    # Check if the robot collides with any obstacles, considering its radius
    for obs in obstacles:
        obs_left = obs[0] - robot_radius
        obs_right = obs[0] + obs[2] + robot_radius
        obs_top = obs[1] - robot_radius
        obs_bottom = obs[1] + obs[3] + robot_radius
        if obs_left <= robot_x <= obs_right and obs_top <= robot_y <= obs_bottom:
            return True
    return False

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw obstacles and target
    draw_obstacles(obstacles)
    draw_target(target_x, target_y)

    # Calculate sector densities based on sonar data and visualize sonar rays
    sector_densities = calculate_sector_densities(robot_x, robot_y)

    # Find the best sector with the lowest obstacle density, considering the target
    best_sector = find_best_sector(sector_densities, robot_x, robot_y)

    # Calculate the speed and steering angle based on the best sector
    if best_sector != -1:
        robot_speed, robot_angle = calculate_speed_and_angle(best_sector)
    else:
        robot_speed = 0  # Stop if no valid sector

    # Update robot's position
    robot_x += math.cos(robot_angle) * robot_speed
    robot_y += math.sin(robot_angle) * robot_speed

    # Keep the robot within the screen boundaries(thanls gpt)
    robot_x = max(robot_radius, min(robot_x, width - robot_radius))
    robot_y = max(robot_radius, min(robot_y, height - robot_radius))

    # Draw the robot
    draw_robot(robot_x, robot_y, robot_angle)

    # Check for collisions with obstacles
    if check_collision(robot_x, robot_y):
        print("Collision detected! Stopping the simulation.")
        running = False

    # Check if the robot has reached the target (thanks gpt the dis did not work here)
    if math.hypot(target_x - robot_x, target_y - robot_y) < 10:
        print("Target Reached!")
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
