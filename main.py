from mandelbrot import Mandelbrot
from simpletk import Window

width, height = 1200, 800

root = Window(width, height, "Exploring the Mandelbrot Set")
canvas = root.add_canvas(width=height, height=height, row=0, col=0, row_span=50)
mandelbrot = Mandelbrot(height, height, res=4)
scale = 0.6

def zoom_in(event):
    zoom(event, scale)

def zoom_out(event):
    zoom(event, 1 + scale)

def zoom(event, scalefactor):
    mandelbrot.translate_display(event.x, event.y)
    mandelbrot.set_zoom(mandelbrot.zoom * scalefactor)
    set_image()

def translate(dx, dy):
    x, y = mandelbrot.center
    zoom = mandelbrot.zoom
    mandelbrot.center = (x + zoom*dx, y + zoom*dy)
    mandelbrot.update_range()
    set_image()

def set_image():
    mandelbrot.calculate_escape_values()
    image = mandelbrot.colorize_display()
    canvas.delete("all")
    canvas.create_image(mandelbrot.width // 2, mandelbrot.height // 2, image=image)

set_image()

canvas.bind("<Button-1>", zoom_in)
canvas.bind("<Button-2>", zoom_out)

canvas.bind_all("<w>", lambda event: translate(0, -0.1))
canvas.bind_all("<a>", lambda event: translate(-0.1, 0))
canvas.bind_all("<s>", lambda event: translate(0, 0.1))
canvas.bind_all("<d>", lambda event: translate(0.1, 0))

root.mainloop()