# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "matplotlib",
#   "slint",
# ]
# [tool.uv.sources]
# slint = { git = "https://github.com/slint-ui/slint", subdirectory = "api/python/slint" }
# ///

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time
import slint
import asyncio

class AppWindow(slint.loader.app_window.AppWindow):
    def __init__(self):
        super().__init__()
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvas(self.fig)
        self.ax.set_facecolor("#f9f9f9")
        self.ax.set_title("Data Stream", fontsize=14)
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Signal Amplitude")

        self.start_time = time.time()
        self.x_data = np.linspace(0, 10, 200)
        self.y_data = np.zeros_like(self.x_data)
        (self.line,) = self.ax.plot(self.x_data, self.y_data, color="#0047AB", lw=2)

        self.default_xlim = (0, 10)
        self.default_ylim = (-2, 2)

    def _update_signal(self, t_offset):
        x = np.linspace(t_offset, t_offset + 10, 200)
        y = np.sin(x) + 0.3 * np.sin(3 * x) + 0.2 * np.random.randn(200)
        self.x_data = x
        self.y_data = y
        # Instead of feeding the data into a slint model and then back into
        # Python, just bump the serial number property, which will trigger a
        # re-evaluation of the binding to the Image's source property and call
        # render_plot() again.
        self.data_serial += 1

    @slint.callback()
    def render_plot(self, zoom: float, pan: float, data_serial: int) -> slint.Image:
        x = self.x_data
        y = self.y_data

        self.line.set_data(x, y)

        base_xmin, base_xmax = x[0], x[-1]
        span = (base_xmax - base_xmin) / zoom
        center = base_xmin + (base_xmax - base_xmin) / 2 + pan
        self.ax.set_xlim(center - span / 2, center + span / 2)

        self.ax.set_ylim(self.default_ylim)

        self.canvas.draw()

        img = np.asarray(self.canvas.buffer_rgba())
        return slint.Image.load_from_array(img)

    async def simulate(self):
        while True:
            self._update_signal(time.time() - self.start_time)
            await asyncio.sleep(1)

async def main():
    app = AppWindow()
    app.show()
    await app.simulate()

slint.run_event_loop(main())
