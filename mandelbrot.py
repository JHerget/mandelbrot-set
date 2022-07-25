from PIL import Image, ImageTk
from matplotlib import cm, colors
import numpy as np

class Mandelbrot:
    def __init__(self, width, height, res):
        self.width = width
        self.height = height
        self.res = res
        self.zoom = 2
        self.center = (-0.5, 0)
        self.max_iterations = 200

        self.ROW = self.height // self.res
        self.COL = self.width // self.res

        self.range_x = (self.center[0] - self.zoom / 2, self.center[0] + self.zoom / 2)
        self.range_y = (self.center[1] - self.zoom / 2, self.center[1] + self.zoom / 2)

        self.escape_values = np.zeros((self.ROW, self.COL), dtype=np.uint8)
        self.color_values = np.zeros((self.width, self.height, 3), dtype=np.uint8)
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.color_values))

        self.color_mapper = cm.get_cmap("hsv", self.max_iterations)

    @staticmethod
    def map_range(num, num_lower, num_higher, new_lower, new_higher):
        return (num - num_lower) * (new_higher - new_lower) / (num_higher - num_lower) + new_lower

    @staticmethod
    def f(Z, C):
        return Z ** 2 + C

    def calc_f(self, row_col_elem):
        self.status += 1 / (self.ROW * self.COL)
        print(f"Screen status: {round(self.status * 100, 2)}%")

        (row, col), elem = row_col_elem
        C_real = Mandelbrot.map_range(col, 0, self.COL - 1, self.range_x[0], self.range_x[1])
        C_imag = Mandelbrot.map_range(row, 0, self.ROW - 1, self.range_y[0], self.range_y[1])
        Z, C = complex(0, 0), complex(C_real, C_imag)
        infinity = 10

        value = Mandelbrot.f(Z, C)
        for iteration in range(self.max_iterations):
            value = Mandelbrot.f(value, C)

            if abs(value) > infinity:
                return iteration

        return -1

    def calculate_escape_values(self):
        self.status = 0
        self.escape_values = np.reshape(list(map(self.calc_f, np.ndenumerate(self.escape_values))), (self.ROW, self.COL))

    def translate_display(self, x, y):
        _x = Mandelbrot.map_range(x, 0, self.width, self.range_x[0], self.range_x[1])
        _y = Mandelbrot.map_range(y, 0, self.height, self.range_y[0], self.range_y[1])

        self.center = (_x, _y)
        self.update_range()

    def colorize_display(self):
        for j, row in enumerate(self.escape_values):
            for i, col in enumerate(row):
                escape_value = self.escape_values[j][i]

                if escape_value > -1:
                    color = self.color_mapper(escape_value % self.max_iterations)
                else:
                    color = [0, 0, 0]

                for k in range(self.res):
                    self.color_values[j * self.res + k][i * self.res:(i + 1) * self.res] = np.array([color[0]*255, color[1]*255, color[2]*255], dtype=np.uint8)

        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.color_values))
        return self.image

    def set_zoom(self, zoom):
        self.zoom = zoom
        self.update_range()

    def update_range(self):
        self.range_x = (self.center[0] - self.zoom / 2, self.center[0] + self.zoom / 2)
        self.range_y = (self.center[1] - self.zoom / 2, self.center[1] + self.zoom / 2)

    def set_resolution(self, res):
        self.res = res
        self.ROW = self.height // self.res
        self.COL = self.width // self.res
        self.escape_values = np.zeros((self.ROW, self.COL), dtype=np.uint8)