import pyautogui
import random
import string
import time


# Function to generate random string of characters
def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


# Main loop
while True:
    # Generate random mouse movement
    x, y = random.randint(270, 1200), random.randint(200, 455)
    pyautogui.moveTo(x, y, duration=0.5)

    # Generate random string and type it
    random_text = random_string(random.randint(1, 20))
    pyautogui.typewrite(random_text)
    univorm = random.uniform(0, 2)
    print(univorm)

    # Generate random scroll action (up or down)
    scroll_direction = random.choice(["up", "down"])
    scroll_amount = random.randint(50, 200)  # Adjust scroll amount as needed
    if scroll_direction == "up":
        pyautogui.scroll(scroll_amount)
    else:
        pyautogui.scroll(-scroll_amount)

    # Wait for a random duration before the next iteration
    time.sleep(random.uniform(0, 2))
