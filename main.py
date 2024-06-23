import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 1440, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Modified Snake Game")

# Load sound effect
pygame.mixer.init()
eating_sound = pygame.mixer.Sound("eating-sound-effect-36186.mp3")

# Load background image and scale it
background_image = pygame.image.load('pywall1.jpg').convert()
background_image = pygame.transform.scale(background_image, (width, height))

# Colors
WHITE = (255, 255, 255)
FOOD_COLOR = (0, 125, 255)
SPECIAL_FOOD_COLOR = (255, 79, 0)
BORDER = (200, 30, 30)
BACKGROUND_COLOR = (10, 10, 10)  # Dark gray background

# Gradient colors
BLUE = (0, 125, 255)
ORANGE = (255, 79, 0)
PINK = (255, 20, 147)

# Game variables
snake_size = 20
snake_speed = 15
snake_length = 3
snake = [(width // 2, height // 2)]
snake_direction = (snake_size, 0)
level_up_shown = False

food_size = 20
food = (random.randrange(1, (width - food_size) // food_size) * food_size,
        random.randrange(1, (height - food_size) // food_size) * food_size)

special_food_size = 20
special_food = None
special_food_active = False
special_food_timer = 0
special_food_points = 3

score = 0
exp = 0
level = 1
exp_needed = 5

special_food_buff_limit = 10
speed_debuff_limit = 10

font = pygame.font.Font(None, 36)

def interpolate_color(color1, color2, t):
    return (
        int(color1[0] * (1 - t) + color2[0] * t),
        int(color1[1] * (1 - t) + color2[1] * t),
        int(color1[2] * (1 - t) + color2[2] * t)
    )

def get_snake_color(index, total_segments):
    if index < total_segments / 2:
        return interpolate_color(BLUE, ORANGE, index / (total_segments / 2))
    else:
        return interpolate_color(ORANGE, PINK, (index - total_segments / 2) / (total_segments / 2))

def draw_snake(snake):
    total_segments = len(snake)
    for i, segment in enumerate(snake):
        color = get_snake_color(i, total_segments)
        pygame.draw.rect(window, color, pygame.Rect(segment[0], segment[1], snake_size, snake_size))

def draw_food(food_pos, color):
    pygame.draw.rect(window, color, pygame.Rect(food_pos[0], food_pos[1], food_size, food_size))

def draw_score(score):
    score_text = font.render(f"Score: {score} | Level: {level} | Exp: {exp}/{exp_needed}", True, WHITE)
    window.blit(score_text, (10, 10))

def draw_level_up_screen():
    level_up_text = font.render(f"Level Up! Choose a Buff:", True, WHITE)
    speed_buff_text = font.render("Press UP for +1 SPEED", True, WHITE)
    special_food_buff_text = font.render(f"Press LEFT for +1 point in special food ({special_food_buff_limit} left)", True, WHITE)
    speed_debuff_text = font.render(f"Press RIGHT for -1 SPEED ({speed_debuff_limit} left)", True, WHITE)
    skip_text = font.render("Press DOWN to Skip", True, WHITE)

    window.blit(level_up_text, (width // 2 - 150, height // 2 - 50))
    window.blit(speed_buff_text, (width // 2 - 150, height // 2))
    window.blit(special_food_buff_text, (width // 2 - 150, height // 2 + 30))
    window.blit(speed_debuff_text, (width // 2 - 150, height // 2 + 60))
    window.blit(skip_text, (width // 2 - 150, height // 2 + 90))

def increase_speed():
    global snake_speed
    snake_speed += 2

def decrease_speed():
    global snake_speed, speed_debuff_limit
    if snake_speed > 1 and speed_debuff_limit > 0:
        snake_speed -= 1
        speed_debuff_limit -= 1

def generate_special_food():
    global special_food, special_food_active, special_food_timer
    special_food = (random.randrange(1, (width - special_food_size) // special_food_size) * special_food_size,
                    random.randrange(1, (height - special_food_size) // special_food_size) * special_food_size)
    special_food_active = True
    special_food_timer = 300  # 5 seconds

special_food_score_bonus = 3  # Initial score bonus from special food
special_food_exp_bonus = 3  # Initial exp bonus from special food
special_food_bonus_increment = 1  # Increase in bonuses each time special food is consumed

def level_up():
    global level, special_food_points, level_up_shown, exp, special_food_score_bonus, special_food_exp_bonus, score, exp_needed, special_food_buff_limit, speed_debuff_limit

    if exp >= exp_needed and not level_up_shown:
        level += 1
        exp_needed += 1  # Increase exp needed for next level
        exp = 0  # Reset exp after leveling up
        level_up_shown = True  # Set the flag to True after showing the level-up screen

        pygame.time.delay(1000)  # Delay to make the level-up screen visible
        draw_level_up_screen()
        pygame.display.flip()

        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        increase_speed()
                        paused = False
                    elif event.key == pygame.K_LEFT and special_food_buff_limit > 0:
                        special_food_score_bonus += special_food_bonus_increment  # Increment bonus
                        special_food_exp_bonus += special_food_bonus_increment  # Increment bonus
                        special_food_buff_limit -= 1
                        paused = False
                    elif event.key == pygame.K_RIGHT and speed_debuff_limit > 0:
                        decrease_speed()
                        paused = False
                    elif event.key == pygame.K_DOWN:
                        paused = False  # Skip the level up screen

        pygame.time.delay(1000)  # Delay to show the chosen buff
        window.fill(BACKGROUND_COLOR)  # Clear the screen
        pygame.display.flip()

        level_up_shown = False  # Reset the flag after showing the level-up screen

def main():
    global snake, snake_direction, food, special_food, special_food_active, special_food_timer, score, snake_length, exp, level, special_food_buff_limit

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, snake_size):
                    snake_direction = (0, -snake_size)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -snake_size):
                    snake_direction = (0, snake_size)
                elif event.key == pygame.K_LEFT and snake_direction != (snake_size, 0):
                    snake_direction = (-snake_size, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-snake_size, 0):
                    snake_direction = (snake_size, 0)

        # Update snake position
        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        # Check for collisions
        if (
            new_head[0] < 0 or new_head[0] >= width or
            new_head[1] < 0 or new_head[1] >= height or
            new_head in snake[1:]
        ):
            pygame.quit()
            sys.exit()

        # Check if snake eats food
        if new_head == food:
            score += 1
            exp += 1
            eating_sound.play()  # Play eating sound effect
            snake_length += 1
            food = (random.randrange(1, (width - food_size) // food_size) * food_size,
                    random.randrange(1, (height - food_size) // food_size) * food_size)

            # Generate special food after eating 5 regular foods
            if score % 5 == 0:
                generate_special_food()

        # Check if snake eats special food
        if special_food_active and new_head == special_food:
            score += special_food_score_bonus  # Special food gives score bonus
            exp += special_food_exp_bonus  # Special food gives exp bonus
            snake_length += 1  # Special food gives length bonus
            special_food_active = False
            eating_sound.play()  # Play eating sound effect

            # Reset special food timer
            special_food_timer = 0

        # Remove tail if snake exceeds its length
        if len(snake) > snake_length:
            snake.pop()

        # Decrease special food timer
        if special_food_active:
            special_food_timer -= 1
            if special_food_timer <= 0:
                special_food_active = False

        # Level up if exp reaches the requirement
        if exp >= exp_needed:
            level_up()

        # Draw the game window
        window.blit(background_image, (0, 0))  # Draw background image
        pygame.draw.rect(window, BORDER, pygame.Rect(0, 0, width, 10))
        pygame.draw.rect(window, BORDER, pygame.Rect(0, 0, 10, height))
        pygame.draw.rect(window, BORDER, pygame.Rect(0, height - 10, width, 10))
        pygame.draw.rect(window, BORDER, pygame.Rect(width - 10, 0, 10, height))

        # Draw snake, food, and special food
        draw_snake(snake)
        draw_food(food, FOOD_COLOR)
        if special_food_active:
            draw_food(special_food, SPECIAL_FOOD_COLOR)

        # Draw score and level
        draw_score(score)

        pygame.display.flip()

        # Control the snake's speed
        pygame.time.Clock().tick(snake_speed)

if __name__ == "__main__":
    main()