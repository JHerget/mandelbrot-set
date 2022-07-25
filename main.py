from mandelbrot import Mandelbrot
from simpletk import Window
import datetime as dt

width, height = 1200, 800

root = Window(width, height, "Exploring the Mandelbrot Set")
canvas = root.add_canvas(width=height, height=height, row=0, col=0, row_span=50)
mandelbrot = Mandelbrot(height, height, res=4)
scale = 0.6

def set_iterations(event):
    new_max = int(iterations_slider.get())
    mandelbrot.max_iterations = new_max
    display_iterations["text"] = new_max

def set_res(event):
    new_res = int(resolution_slider.get())
    mandelbrot.set_resolution(new_res)
    display_resolution["text"] = new_res

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
    print(f"Image set {dt.datetime.now()}")

set_image()

canvas.bind("<Button-1>", zoom_in)
canvas.bind("<Button-2>", zoom_out)

canvas.bind_all("<w>", lambda event: translate(0, -0.1))
canvas.bind_all("<a>", lambda event: translate(-0.1, 0))
canvas.bind_all("<s>", lambda event: translate(0, 0.1))
canvas.bind_all("<d>", lambda event: translate(0.1, 0))

resolution_label = root.add_label(text="Resolution: ", row=0, col=50)
resolution_slider = root.add_slider(start=1, end=10, value=mandelbrot.res, length=150, row=0, col=51, command=set_res)
display_resolution = root.add_label(text=mandelbrot.res, row=0, col=52)

iterations_label = root.add_label(text="Max iterations: ", row=1, col=50)
iterations_slider = root.add_slider(start=1, end=2000, value=mandelbrot.max_iterations, length=150, row=1, col=51, command=set_iterations)
display_iterations = root.add_label(text=mandelbrot.max_iterations, row=1, col=52)

update_screen_button = root.add_button(width=10, height=1, text="Update Screen", command=set_image, row=49, col=50)

root.mainloop()