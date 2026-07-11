# Math & Pathfinding Utilities - December 2022

This repository contains two main utilities:
1. **Ray-Segment Intersection Visualizer (`finddistance.py`)**: Finds the closest line segment intersecting a ray projected from a given 2D point at a specific angle (0° to 360°).
2. **Grid Path Finder (`gridPath.py`)**: Solves 2D maze pathfinding problems using a Breadth-First Search (BFS) algorithm.


# Problem:

![image](https://user-images.githubusercontent.com/103208134/204084259-5a4defaf-4c59-4d67-af78-858a0fddfe51.png)

The Program Run and Output:
![image](https://user-images.githubusercontent.com/103208134/204084104-6b0ed8c1-fdc9-4bd5-a9c7-26a25fcd3170.png)

![image](https://user-images.githubusercontent.com/103208134/204084305-053a5833-83f2-48fd-aa44-8666f0e5657f.png)

## Math & Algorithms

The Ray-Segment Intersection Visualizer (`finddistance.py`) implements two resolver strategies:

### 1. Parametric (Vector) Method
This is the default, robust method. It models the segment and the ray parametrically:
- **Line Segment (A to B):** $P(t) = A + t \cdot (B - A)$ where $0 \le t \le 1$
- **Ray (Origin O, angle $\theta$):** $R(s) = O + s \cdot (\cos\theta, \sin\theta)$ where $s \ge 0$

To find the intersection, we solve the system of linear equations:
$$A_x + t \cdot dx = O_x + s \cdot rx$$
$$A_y + t \cdot dy = O_y + s \cdot ry$$

Using Cramer's Rule, the system is solved for $t$ (segment parameter) and $s$ (ray parameter). The intersection is valid if $0 \le t \le 1$ and $s \ge 0$.

### 2. Slope-Intercept Method
This method provides a classic linear-equations approach:
- **Ray Line:** $y = m_{\text{ray}} \cdot x + c_{\text{ray}}$ where $m_{\text{ray}} = \tan\theta$
- **Segment Line:** $y = m_{\text{seg}} \cdot x + c_{\text{seg}}$ where $m_{\text{seg}} = \frac{y_2 - y_1}{x_2 - x_1}$

Solving for intersection $(x_i, y_i)$:
$$x_i = \frac{c_{\text{ray}} - c_{\text{seg}}}{m_{\text{seg}} - m_{\text{ray}}}$$
$$y_i = m_{\text{ray}} \cdot x_i + c_{\text{ray}}$$

*Note: Special handling is implemented for vertical lines (where slopes are undefined) and parallel lines.*

---

## Maze Solver Algorithm (`gridPath.py`)

The maze solving tool finds the path from a start position `'S'` to a finish position `'F'` in a 2D grid:
- The grid consists of traversable space (`0`), walls (`1`), a start (`'S'`), and a finish (`'F'`).
- The BFS algorithm explores valid moves (Left, Right, Up, Down) queue-by-queue, guaranteeing the shortest path in an unweighted grid.

---

## Setup & Running the Code

### Prerequisites
Make sure you have Python 3 installed. The visualizer script requires `matplotlib` for plotting.

```bash
pip install matplotlib
```

### 1. Ray-Segment Visualizer (`finddistance.py`)
Run the script:
```bash
python finddistance.py
```
You can choose to input coordinates manually or load them from a text file (like [sample_input.txt](file:///d:/6.%20STUDY%20MATERIAL/CSE/Projects/Python/math_uni/sample_input.txt)).

#### File Input Format:
```text
<test_point_x>,<test_point_y>
<ray_angle_degrees>
<segment1_x1>,<segment1_y1>,<segment1_x2>,<segment1_y2>
<segment2_x1>,<segment2_y1>,<segment2_x2>,<segment2_y2>
...
```

### 2. Grid Path Finder (`gridPath.py`)
Run the script:
```bash
python gridPath.py
```
This will search for the path in the defined maze and print the grid map showing the path.
