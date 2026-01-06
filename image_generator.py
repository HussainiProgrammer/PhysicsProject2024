from PIL import Image, ImageDraw

def generate_grid_image(filename="grid.png", size=10000, cell_size=50, grid_color=(128, 128, 128, 255), bg_color=(0, 0, 0, 255), axes: bool=False, axes_color=(128, 128, 128)):
    image = Image.new("RGBA", (size, size), bg_color)
    draw = ImageDraw.Draw(image)

    for x in range(0, size+cell_size, cell_size): draw.line([(x, 0), (x, size)], fill=grid_color)
    for y in range(0, size+cell_size, cell_size): draw.line([(0, y), (size, y)], fill=grid_color)

    if axes:
        draw.line([(size/2, 0), (size/2, size)], fill=axes_color)
        draw.line([(0, size/2), (size, size/2)], fill=axes_color)

    image.save(filename)

    print(f"Grid image saved as {filename}")

generate_grid_image(filename="grid.png")
generate_grid_image(filename="blue_grid.png", grid_color=(69, 103, 137, 255)) #456789
generate_grid_image(filename="blue_grid_with_axes.png", grid_color=(69, 103, 137, 255), bg_color=(0,0,0,0), axes=True) #456789