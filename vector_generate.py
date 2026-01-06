import svgwrite

def generate_grid_svg(filename="grid.svg", size=10000, cell_size=50, grid_color="gray", bg_color="none", axes=False, axes_color="gray"):
    dwg = svgwrite.Drawing(filename, size=(size, size))

    if bg_color != "none": dwg.add(dwg.rect(insert=(0, 0), size=(size, size), fill=bg_color))

    for x in range(0, size + cell_size, cell_size): dwg.add(dwg.line(start=(x, 0), end=(x, size), stroke=grid_color))
    for y in range(0, size + cell_size, cell_size): dwg.add(dwg.line(start=(0, y), end=(size, y), stroke=grid_color))

    if axes:
        dwg.add(dwg.line(start=(size / 2, 0), end=(size / 2, size), stroke=axes_color))
        dwg.add(dwg.line(start=(0, size / 2), end=(size, size / 2), stroke=axes_color))

    dwg.save()
    print(f"Grid SVG saved as {filename}")

generate_grid_svg(filename="grid.svg", bg_color="black")
generate_grid_svg(filename="blue_grid.svg", grid_color="#456789", bg_color="black")
generate_grid_svg(filename="blue_grid_with_axes.svg", grid_color="#456789", bg_color='none', axes=True)
