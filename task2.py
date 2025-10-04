import math
import time
import turtle
from typing import Optional, Any


def pythagoras_tree(
    t: turtle.Turtle,
    x: float,
    y: float,
    length: float,
    angle: float,
    level: int,
    k: float = math.sqrt(2) / 2,
    animate: bool = True,
    pause: float = 0.01,
    screen: Optional[Any] = None,
) -> None:
    if level == 0 or length <= 0:
        return

    x2 = x + length * math.cos(math.radians(angle))
    y2 = y + length * math.sin(math.radians(angle))

    t.penup()
    t.goto(x, y)
    t.pendown()
    t.goto(x2, y2)

    if animate and screen is not None:
        screen.update()
        if pause > 0:
            time.sleep(pause)

    new_len = length * k
    pythagoras_tree(t, x2, y2, new_len, angle + 45, level - 1, k, animate, pause, screen)
    pythagoras_tree(t, x2, y2, new_len, angle - 45, level - 1, k, animate, pause, screen)


def ask_level(default_level: int = 10) -> int:
    try:
        s = input(f"Введіть рівень рекурсії (8–12) [{default_level}]: ").strip()
        return default_level if not s else max(int(s), 0)
    except Exception:
        return default_level


def main() -> None:
    SCREEN_W, SCREEN_H = 1400, 900
    level = ask_level(10)

    screen = turtle.Screen()
    screen.setup(width=SCREEN_W, height=SCREEN_H)
    screen.bgcolor("white")
    screen.title(f"Дерево Піфагора (рівень {level})")
    screen.tracer(0, 0)

    t = turtle.Turtle(visible=False)
    t.speed(0)
    t.color("#B8474C")
    t.pensize(1)

    k = math.sqrt(2) / 2
    canopy_ratio = 0.80
    desired_canopy = SCREEN_H * canopy_ratio
    geom_sum = (1 - k**level) / (1 - k) if level > 0 else 0.0
    first_branch = desired_canopy / geom_sum if geom_sum > 0 else 0.0
    trunk_length = first_branch * 0.30

    start_x, start_y = 0, -SCREEN_H * 0.30

    t.penup(); t.goto(start_x, start_y); t.pendown()
    t.goto(start_x, start_y + trunk_length)
    screen.update()

    pythagoras_tree(
        t,
        start_x,
        start_y + trunk_length,
        first_branch,
        90,
        level,
        k,
        animate=True,     # ← покрокова анімація (True/False)
        pause=0.01,
        screen=screen,
    )

    screen.update()
    print(f"Готово. Рівень: {level}, перша гілка: {first_branch:.1f}px, стовбур: {trunk_length:.1f}px.")
    screen.mainloop()


if __name__ == "__main__":
    main()
