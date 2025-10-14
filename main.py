import slint
from dataclasses import dataclass
import typing
import random
import asyncio


@dataclass
class DataPoint:
    time: float  # between 0 and 1
    value: float  # between 0 and 1


def generate_commands(points: typing.List[DataPoint]) -> str:
    commands = "M 0,1"  # bottom left
    for point in points:
        commands += f"L {point.time},{point.value}"
    return commands


class App(slint.loader.app_window.AppWindow):  # type: ignore
    def __init__(self):
        super().__init__()

    def update_points(self, points: typing.List[DataPoint]) -> None:
        self.path_commands = generate_commands(points)


async def main():
    instance = App()
    instance.show()

    points = [DataPoint(time=t / 100, value=random.uniform(0, 1)) for t in range(0, 100)]

    while True:
        instance.update_points(points)
        await asyncio.sleep(1)
        points = [DataPoint(time=t / 100, value=random.uniform(0, 1)) for t in range(0, 100)]


slint.run_event_loop(main())
