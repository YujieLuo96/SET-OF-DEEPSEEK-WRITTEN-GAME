import numpy as np
from mayavi import mlab
import time


class FractalGenerator:
    def __init__(self, max_iterations=10, power=8, size=100, bounds=(-1.2, 1.2)):
        self.max_iterations = max_iterations
        self.power = power
        self.size = size
        self.bounds = bounds

    def generate_mandelbulb(self):
        """Generate a 3D Mandelbulb fractal"""
        # Create a 3D grid of points
        x, y, z = np.mgrid[
                  self.bounds[0]:self.bounds[1]:self.size * 1j,
                  self.bounds[0]:self.bounds[1]:self.size * 1j,
                  self.bounds[0]:self.bounds[1]:self.size * 1j
                  ]

        # Prepare arrays for calculation
        mask = np.zeros_like(x, dtype=bool)
        distance = np.zeros_like(x, dtype=float)

        # Convert to vectors for easier computation
        points = np.column_stack([x.flatten(), y.flatten(), z.flatten()])

        # Process each point to determine if it's in the fractal
        for i in range(points.shape[0]):
            point = points[i]
            c = point.copy()
            z_point = point.copy()

            # Apply mandelbulb iteration formula
            for n in range(self.max_iterations):
                # Convert to spherical coordinates
                r = np.sqrt(z_point[0] ** 2 + z_point[1] ** 2 + z_point[2] ** 2)

                if r > 2.0:
                    break

                # If r is too small, we get numerical issues - add small offset
                if r < 1e-10:
                    r = 1e-10

                # Calculate angles
                theta = np.arccos(z_point[2] / r)
                phi = np.arctan2(z_point[1], z_point[0])

                # Apply power
                r_pow = r ** self.power
                sin_theta_pow = np.sin(theta * self.power)

                # Convert back to Cartesian coordinates
                z_point[0] = r_pow * sin_theta_pow * np.cos(phi * self.power) + c[0]
                z_point[1] = r_pow * sin_theta_pow * np.sin(phi * self.power) + c[1]
                z_point[2] = r_pow * np.cos(theta * self.power) + c[2]

                # Check if this point escapes
                if n == self.max_iterations - 1:
                    mask.flat[i] = True
                    distance.flat[i] = n

        return x, y, z, mask, distance


class FractalVisualizer:
    def __init__(self, fractal_generator):
        self.generator = fractal_generator
        self.figure = None

    def visualize(self, fractal_type="mandelbulb"):
        """Visualize the fractal in an interactive 3D viewer"""
        # Generate fractal data
        if fractal_type == "mandelbulb":
            x, y, z, mask, distance = self.generator.generate_mandelbulb()
        else:
            raise ValueError(f"Unsupported fractal type: {fractal_type}")

        # Create a figure
        self.figure = mlab.figure(size=(800, 800), bgcolor=(0, 0, 0))

        # Visualize the fractal with colormap based on iteration distance
        src = mlab.pipeline.scalar_field(x, y, z, distance)
        src.image_data.point_data.get_array(0).fill(0)
        src.image_data.point_data.get_array(0).from_array(distance[mask])

        # Create the surface
        surface = mlab.pipeline.iso_surface(
            src, contours=[self.generator.max_iterations / 2],
            opacity=1.0
        )

        # Apply a colormap
        surface.module_manager.scalar_lut_manager.lut.table = self._create_colormap()

        # Add title
        mlab.title(f"3D {fractal_type.capitalize()} Fractal", size=0.4)

        # Show the visualization
        mlab.show()

    def _create_colormap(self):
        """Create a custom colormap for the fractal"""
        # Create a blue-based colormap
        ncolors = 256
        colormap = np.zeros((ncolors, 4), dtype=np.uint8)

        # Generate colors (blue to cyan to white)
        for i in range(ncolors):
            ratio = i / (ncolors - 1)
            # R component
            r = int(255 * min(1, ratio * 2))
            # G component
            g = int(255 * min(1, ratio * 1.5))
            # B component
            b = int(128 + 127 * ratio)
            # Alpha
            a = 255

            colormap[i] = np.array([r, g, b, a], dtype=np.uint8)

        return colormap

    def animation(self, fractal_type="mandelbulb", duration=10):
        """Create an animated visualization with rotating fractal"""
        # Generate fractal data
        if fractal_type == "mandelbulb":
            x, y, z, mask, distance = self.generator.generate_mandelbulb()
        else:
            raise ValueError(f"Unsupported fractal type: {fractal_type}")

        # Create a figure
        self.figure = mlab.figure(size=(800, 800), bgcolor=(0, 0, 0))

        # Visualize the fractal
        src = mlab.pipeline.scalar_field(x, y, z, distance)
        src.image_data.point_data.get_array(0).fill(0)
        src.image_data.point_data.get_array(0).from_array(distance[mask])

        # Create the surface
        surface = mlab.pipeline.iso_surface(
            src, contours=[self.generator.max_iterations / 2],
            opacity=1.0
        )

        # Apply a colormap
        surface.module_manager.scalar_lut_manager.lut.table = self._create_colormap()

        # Add title
        mlab.title(f"3D {fractal_type.capitalize()} Fractal", size=0.4)

        # Animate the visualization
        for i in range(36):  # 36 frames for 360 degrees
            # Rotate the view
            mlab.view(azimuth=i * 10, elevation=30, distance='auto')
            # Pause to create animation effect
            time.sleep(duration / 36)
            # Render the scene
            mlab.draw()

        mlab.show()


def main():
    print("3D Fractal Visualization")
    print("------------------------")
    print("1. Generate Mandelbulb Fractal")
    print("2. Generate Animated Mandelbulb")

    choice = input("Enter your choice (1-2): ")

    # Create fractal generator
    resolution = input("Enter resolution (50-150, higher is slower): ")
    try:
        resolution = int(resolution)
        if resolution < 50:
            resolution = 50
        elif resolution > 150:
            resolution = 150
    except ValueError:
        resolution = 80
        print(f"Using default resolution: {resolution}")

    iterations = input("Enter max iterations (5-20, higher is more detailed): ")
    try:
        iterations = int(iterations)
        if iterations < 5:
            iterations = 5
        elif iterations > 20:
            iterations = 20
    except ValueError:
        iterations = 10
        print(f"Using default iterations: {iterations}")

    generator = FractalGenerator(max_iterations=iterations, size=resolution)
    visualizer = FractalVisualizer(generator)

    if choice == "1":
        visualizer.visualize("mandelbulb")
    elif choice == "2":
        visualizer.animation("mandelbulb")
    else:
        print("Invalid choice. Exiting.")


if __name__ == "__main__":
    main()