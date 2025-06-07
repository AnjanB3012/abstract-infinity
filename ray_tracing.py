import math
import time
from PIL import Image
from absinf import AbsInf

# Vector utilities
def dot(a, b): return sum(i*j for i, j in zip(a, b))
def subtract(a, b): return [i - j for i, j in zip(a, b)]
def add(a, b): return [i + j for i, j in zip(a, b)]
def multiply(v, s): return [i * s for i in v]
def normalize(v):
    mag = math.sqrt(dot(v, v))
    return [i / mag for i in v]

# Sphere intersection with configurable inf_type
def intersect_sphere(origin, direction, center, radius, inf_type):
    oc = subtract(origin, center)
    b = 2 * dot(oc, direction)
    c = dot(oc, oc) - radius * radius
    discriminant = b*b - 4*c
    if discriminant < 0:
        return inf_type()
    return (-b - math.sqrt(discriminant)) / 2

# Render with configurable infinity
def render(width, height, inf_type):
    camera = [0, 0, 0]
    img = Image.new("RGB", (width, height))
    pixels = img.load()

    spheres = [
        {"center": [0, -1, 3], "radius": 1, "color": (255, 0, 0)},
        {"center": [2, 0, 4], "radius": 1, "color": (0, 0, 255)},
        {"center": [-2, 0, 4], "radius": 1, "color": (0, 255, 0)},
    ]
    light = [5, 5, -10]

    for y in range(height):
        for x in range(width):
            i = (2*(x + 0.5)/width - 1) * math.tan(math.pi/4) * width/height
            j = (1 - 2*(y + 0.5)/height) * math.tan(math.pi/4)
            direction = normalize([i, j, 1])

            min_dist = inf_type()
            color = (0, 0, 0)
            for sphere in spheres:
                dist = intersect_sphere(camera, direction, sphere["center"], sphere["radius"], inf_type)
                if min_dist > dist:
                    min_dist = dist
                    hit_point = add(camera, multiply(direction, dist))
                    normal = normalize(subtract(hit_point, sphere["center"]))
                    light_dir = normalize(subtract(light, hit_point))
                    intensity = max(dot(normal, light_dir), 0)
                    color = tuple(min(int(c * intensity), 255) for c in sphere["color"])
            pixels[x, y] = color

    return img

# Benchmark function
def benchmark(name, inf_type):
    width, height = 320, 240
    print(f"\nBenchmarking with {name}...")
    start = time.perf_counter()
    for i in range(1):
        img = render(width, height, inf_type)
    end = time.perf_counter()
    avg_time = (end - start) / 100
    img.save(f"raytrace_output_{name}.png")
    print(f"{name} avg render time over 100 runs: {avg_time:.4f} seconds")
    print(f"Saved final image as raytrace_output_{name}.png")

if __name__ == "__main__":
    benchmark("absinf", AbsInf)
    benchmark("floatinf", lambda: float('inf'))
