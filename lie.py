#  Enum qo'shish create-order (payment uchun)
# — Payment link olib kelish
# — Payment ga endpointlar berish
# — PreOrder delete method
# — PreOrderDetail, OrderDetail, OrderHistory  da driver haqida: ismi, rasmi, gosnomer kerak
# — OrderHistory ga category name kerak
# — category preorderda null boʻlishi kerak


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
    # Wait for 10 seconds before the next iteration
    time.sleep(univorm)
