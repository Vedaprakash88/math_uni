# importing libraries
import math
import sys
import matplotlib.pyplot as plt

class Point2D:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        
    def distance_to(self, other: 'Point2D') -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        
    def plot_point(self, color="purple", marker="x", label=None):
        plt.plot(self.x, self.y, color=color, marker=marker)
        if label:
            plt.text(self.x - 0.5, self.y - 0.9, label)
            
    def __repr__(self):
        return f"({self.x}, {self.y})"


class LineSegment:
    def __init__(self, p1: Point2D, p2: Point2D):
        self.p1 = p1
        self.p2 = p2
        
    @property
    def x1(self): return self.p1.x
    @property
    def y1(self): return self.p1.y
    @property
    def x2(self): return self.p2.x
    @property
    def y2(self): return self.p2.y
    
    def length(self) -> float:
        return self.p1.distance_to(self.p2)
        
    def contains_point(self, p: Point2D, tolerance: float = 1e-5) -> bool:
        # 1. Bounding box check
        min_x, max_x = min(self.x1, self.x2), max(self.x1, self.x2)
        min_y, max_y = min(self.y1, self.y2), max(self.y1, self.y2)
        
        if not (min_x - tolerance <= p.x <= max_x + tolerance and min_y - tolerance <= p.y <= max_y + tolerance):
            return False
            
        # 2. Check distance from point to the line containing the segment
        # Area of triangle formed by p1, p2, p
        segment_len = self.length()
        if segment_len < tolerance:
            return p.distance_to(self.p1) <= tolerance
            
        area = abs((self.y2 - self.y1) * p.x - (self.x2 - self.x1) * p.y + self.x2 * self.y1 - self.y2 * self.x1)
        dist = area / segment_len
        return dist <= tolerance

    def plot(self, color="black", marker="o"):
        plt.plot((self.x1, self.x2), (self.y1, self.y2), color=color, marker=marker)
        plt.text(self.x1, self.y1 - 0.8, f'A({self.x1},{self.y1})')
        plt.text(self.x2, self.y2 - 0.8, f'B({self.x2},{self.y2})')

    def __repr__(self):
        return f"Segment[{self.p1} to {self.p2}]"


class Ray:
    def __init__(self, origin: Point2D, angle_deg: float):
        self.origin = origin
        self.angle_deg = angle_deg % 360.0
        
    @property
    def angle_rad(self):
        return math.radians(self.angle_deg)
        
    def get_direction(self) -> tuple[float, float]:
        return math.cos(self.angle_rad), math.sin(self.angle_rad)
        
    def is_point_along_ray(self, p: Point2D, tolerance: float = 1e-5) -> bool:
        dx, dy = self.get_direction()
        proj = (p.x - self.origin.x) * dx + (p.y - self.origin.y) * dy
        return proj >= -tolerance
        
    def plot(self, color="g", linestyle="dashdot", length=100.0):
        dx, dy = self.get_direction()
        end_point_x = self.origin.x + dx * length
        end_point_y = self.origin.y + dy * length
        plt.plot([self.origin.x, end_point_x], [self.origin.y, end_point_y], color=color, linestyle=linestyle)


class SlopeInterceptIntersectionResolver:
    """
    Computes intersection between a Ray and a LineSegment using slope-intercept equations.
    Includes robust error handling and fallback logic for vertical lines.
    """
    @staticmethod
    def resolve(ray: Ray, segment: LineSegment) -> Point2D:
        # Check angle for vertical ray
        theta = ray.angle_deg
        is_ray_vertical = math.isclose(theta, 90.0) or math.isclose(theta, 270.0)
        
        # Check if segment is vertical
        is_segment_vertical = math.isclose(segment.x1, segment.x2)
        
        # Edge Cases and Error Handling
        if is_ray_vertical and is_segment_vertical:
            raise ValueError("Ray and Segment are both vertical. They are either parallel or collinear.")
            
        if is_ray_vertical:
            # Ray is vertical: equation is x = ray.origin.x
            # Segment is non-vertical: calculate slope and intercept
            m_seg = (segment.y2 - segment.y1) / (segment.x2 - segment.x1)
            xi = ray.origin.x
            yi = m_seg * (xi - segment.x1) + segment.y1
            
        elif is_segment_vertical:
            # Segment is vertical: equation is x = segment.x1
            # Ray is non-vertical: calculate slope and intercept
            m_ray = math.tan(ray.angle_rad)
            xi = segment.x1
            yi = m_ray * (xi - ray.origin.x) + ray.origin.y
            
        else:
            # Neither is vertical. Calculate slopes
            m_seg = (segment.y2 - segment.y1) / (segment.x2 - segment.x1)
            m_ray = math.tan(ray.angle_rad)
            
            # Check if parallel
            if math.isclose(m_seg, m_ray):
                raise ValueError("Ray and Segment are parallel (equal slopes). No unique intersection.")
                
            # Equations:
            # y = m_ray * (x - ray.origin.x) + ray.origin.y => y = m_ray * x + c_ray
            # y = m_seg * (x - segment.x1) + segment.y1    => y = m_seg * x + c_seg
            c_ray = ray.origin.y - m_ray * ray.origin.x
            c_seg = segment.y1 - m_seg * segment.x1
            
            # m_ray * xi + c_ray = m_seg * xi + c_seg
            xi = (c_ray - c_seg) / (m_seg - m_ray)
            yi = m_ray * xi + c_ray
            
        intersection = Point2D(xi, yi)
        
        # Verify if the intersection point lies within the segment bounds and along the ray direction
        if segment.contains_point(intersection) and ray.is_point_along_ray(intersection):
            return intersection
        return None


class ParametricIntersectionResolver:
    """
    Computes intersection between a Ray and a LineSegment using parametric/vector math.
    Extremely robust, natively handles vertical lines without special conditions or division-by-zero.
    """
    @staticmethod
    def resolve(ray: Ray, segment: LineSegment) -> Point2D:
        # Segment vector: A -> B
        dx = segment.x2 - segment.x1
        dy = segment.y2 - segment.y1
        
        # Ray direction vector
        rx, ry = ray.get_direction()
        
        # Solve system:
        # A_x + t * dx = O_x + s * rx
        # A_y + t * dy = O_y + s * ry
        #
        # Rearranging:
        # t * dx - s * rx = O_x - A_x
        # t * dy - s * ry = O_y - A_y
        
        # Matrix determinant
        det = rx * dy - ry * dx
        
        # If det is 0, the lines are parallel or collinear
        if math.isclose(det, 0.0, abs_tol=1e-9):
            return None
            
        ox = ray.origin.x - segment.x1
        oy = ray.origin.y - segment.y1
        
        # Solve for t (segment parameter) and s (ray parameter)
        # Using Cramer's rule
        t = (rx * oy - ry * ox) / det
        s = (dx * oy - dy * ox) / det
        
        # Intersection is valid if 0 <= t <= 1 and s >= 0
        # (with small tolerance for float inaccuracies)
        tol = 1e-7
        if (-tol <= t <= 1.0 + tol) and (s >= -tol):
            xi = segment.x1 + t * dx
            yi = segment.y1 + t * dy
            return Point2D(xi, yi)
            
        return None


class DistanceFinderApp:
    def __init__(self):
        self.test_point = None
        self.ray = None
        self.segments = []

    def load_from_file(self, file_path: str):
        with open(file_path, 'r') as f:
            # Filter out empty lines and strip whitespace
            lines = [line.strip() for line in f if line.strip()]
            
        if len(lines) < 3:
            raise ValueError("File must contain at least 3 lines: test point, angle, and at least one segment.")
            
        # 1. Parse test point (first line)
        try:
            coords = [float(x) for x in lines[0].split(",")]
            if len(coords) != 2:
                raise ValueError("First line must have exactly 2 coordinates (x,y)")
            self.test_point = Point2D(coords[0], coords[1])
        except Exception as e:
            raise ValueError(f"Invalid test point format on line 1: {e}")
            
        # 2. Parse angle (second line)
        try:
            inp_angle = float(lines[1])
            if not (0.0 <= inp_angle <= 360.0):
                raise ValueError("Angle must be between 0 and 360")
            self.ray = Ray(self.test_point, inp_angle)
        except Exception as e:
            raise ValueError(f"Invalid angle format on line 2: {e}")
            
        # 3. Parse segments (line 3 onwards)
        self.segments = []
        for idx, line in enumerate(lines[2:], start=3):
            try:
                coords = [float(x) for x in line.split(",")]
                if len(coords) != 4:
                    print(f"Warning: Skipping line {idx} (invalid format): '{line}'")
                    continue
                p1 = Point2D(coords[0], coords[1])
                p2 = Point2D(coords[2], coords[3])
                
                # Check for zero-length line
                if math.isclose(p1.distance_to(p2), 0.0):
                    print(f"Warning: Skipping line {idx} (zero length segment): '{line}'")
                    continue
                    
                self.segments.append(LineSegment(p1, p2))
            except Exception as e:
                print(f"Warning: Skipping line {idx} (failed to parse): '{line}' - {e}")
                
        if not self.segments:
            raise ValueError("No valid line segments found in the file.")
        
        print(f"\nSuccessfully loaded inputs from '{file_path}':")
        print(f"  Test Point: {self.test_point}")
        print(f"  Angle: {self.ray.angle_deg}°")
        print(f"  Segments Loaded: {len(self.segments)}")

    def get_user_inputs(self):
        # 1. Ask for test point
        while True:
            inp_point = input("Please enter a x,y 'Test Point' e.g. 2,3 (without brackets and spaces): ").strip()
            try:
                coords = [float(x) for x in inp_point.split(",")]
                if len(coords) != 2:
                    print("2D point must have exactly 2 coordinates.")
                    continue
                self.test_point = Point2D(coords[0], coords[1])
                break
            except ValueError:
                print("Invalid format. Please enter coordinates like '2,3'.")

        # 2. Ask for angle
        while True:
            try:
                inp_angle = float(input("Enter angle between 0 and 360: "))
                if 0.0 <= inp_angle <= 360.0:
                    self.ray = Ray(self.test_point, inp_angle)
                    break
                else:
                    print("Value must be between 0 and 360.")
            except ValueError:
                print("Please enter a valid floating-point number.")

        # 3. Ask for line segments
        print("\nEnter coordinates for line segments. Type 'done' when finished.")
        num = 0
        while True:
            inp_lines = input("Enter coordinates as x1,y1,x2,y2 (no spaces, comma-separated) or 'done': ").strip()
            
            if inp_lines.lower() == 'done':
                if num == 0:
                    print("Please enter coordinates of at least one line.")
                    continue
                break
                
            try:
                coords = [float(x) for x in inp_lines.split(",")]
                if len(coords) != 4:
                    print("Please enter exactly 4 coordinates (x1, y1, x2, y2).")
                    continue
                p1 = Point2D(coords[0], coords[1])
                p2 = Point2D(coords[2], coords[3])
                
                # Check for zero-length line
                if math.isclose(p1.distance_to(p2), 0.0):
                    print("Endpoints cannot be identical (length must be > 0).")
                    continue
                    
                self.segments.append(LineSegment(p1, p2))
                num += 1
            except ValueError:
                print("Invalid input. Please enter 4 numbers separated by commas, or 'done'.")

    def run(self):
        # Decide input method
        choice = input("Enter 'file' to load input from a text file, or press Enter to input manually: ").strip().lower()
        if choice == 'file':
            while True:
                file_path = input("Enter the path to the text file: ").strip()
                # Strip potential quotes (e.g. if user drags and drops file)
                file_path = file_path.strip('\'"')
                try:
                    self.load_from_file(file_path)
                    break
                except Exception as e:
                    print(f"Error loading file: {e}")
                    retry = input("Would you like to try another file? (y/n): ").strip().lower()
                    if retry != 'y' and retry != 'yes':
                        print("Falling back to manual input...\n")
                        self.get_user_inputs()
                        break
        else:
            self.get_user_inputs()
        
        # Setup plotting
        plt.figure(figsize=(8, 8))
        self.test_point.plot_point(color="purple", marker="x", label=f"Point({self.test_point.x},{self.test_point.y})")
        
        # Plot horizontal reference line through test point
        plt.plot(range(-100, 100), [self.test_point.y] * 200, color="b", linestyle='dashdot')
        
        # Plot the ray direction
        self.ray.plot(color="g", linestyle="dashdot", length=100)
        # Add angle text
        plt.text(self.test_point.x - 0.2, self.test_point.y + 0.6, f'θ={self.ray.angle_deg}°')
        
        dict_out = {}
        
        print("\n--- Solving Intersections ---")
        for i, segment in enumerate(self.segments):
            print(f"\nEvaluating Segment {i+1}: {segment}")
            segment.plot(color="black", marker="o")
            
            # --- Method 1: Slope-Intercept with Error Handling ---
            slope_intercept_pt = None
            try:
                slope_intercept_pt = SlopeInterceptIntersectionResolver.resolve(self.ray, segment)
                print(f"  [Slope-Intercept] Intersection: {slope_intercept_pt}")
            except Exception as e:
                print(f"  [Slope-Intercept] Error: {e}")
                
            # --- Method 2: Parametric ---
            parametric_pt = ParametricIntersectionResolver.resolve(self.ray, segment)
            print(f"  [Parametric]      Intersection: {parametric_pt}")
            
            # Verify results match when both succeed
            if slope_intercept_pt and parametric_pt:
                dist_diff = slope_intercept_pt.distance_to(parametric_pt)
                if dist_diff > 1e-4:
                    print(f"  [Warning] Solvers disagreed by {dist_diff} units!")
            
            # We use the robust parametric result for the final output
            if parametric_pt:
                # Plot the intersection
                plt.plot(parametric_pt.x, parametric_pt.y, color="r", marker="*")
                plt.text(parametric_pt.x - 0.5, parametric_pt.y - 0.9, f'Intersection at {parametric_pt.x:.2f},{parametric_pt.y:.2f}')
                
                # Calculate distance
                distance = round(self.test_point.distance_to(parametric_pt), 2)
                dict_out[distance] = segment
                print(f"  -> Ray intersects this segment at distance: {distance}")
            else:
                print("  -> Ray does not intersect this segment.")
                
        # Find nearest
        if dict_out:
            closest_dist = min(dict_out.keys())
            closest_segment = dict_out[closest_dist]
            if math.isclose(closest_dist, 0.0):
                print(f"\nRESULT: The test point {self.test_point} lies directly on the segment {closest_segment}.")
            else:
                print(f"\nRESULT: The closest segment to the test point {self.test_point} is {closest_segment}, which is {closest_dist} units away at an angle of {self.ray.angle_deg}°.")
        else:
            print("\nRESULT: No intersections found with any of the segments along this angle.")

        # Show Plot
        plt.xlim(-8, 8)
        plt.ylim(-10, 10)
        plt.xlabel("x coordinates")
        plt.ylabel("y coordinates")
        plt.grid(True)
        plt.title("Ray-Segment Intersection Visualizer")
        plt.show()


if __name__ == "__main__":
    app = DistanceFinderApp()
    app.run()
