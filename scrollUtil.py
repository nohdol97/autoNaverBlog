import time, random

def smooth_scroll_to_element(driver, element, offset=-150, steps=50, delay=0.01):
    element_location = element.location['y'] + offset
    current_position = driver.execute_script("return window.pageYOffset;")
    delta = element_location - current_position
    step_size = delta / steps

    for _ in range(steps):
        current_position += step_size
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(delay + random.uniform(0, delay))