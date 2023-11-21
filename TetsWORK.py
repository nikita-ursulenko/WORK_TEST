import random
import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class CityGrid:
    def __init__(self, n, m, coverage_threshold=0.3):
        self.n = n
        self.m = m
        self.grid = [[0] * m for _ in range(n)]  # 0 represents unblocked, 1 represents blocked, 2 represents tower coverage
        self.blocked_coverage_threshold = coverage_threshold
        self.towers = []  # List to store information about towers (x, y, range, cost)

    def randomly_block_cells(self):
        for i in range(self.n):
            for j in range(self.m):
                if random.random() < self.blocked_coverage_threshold:
                    self.grid[i][j] = 1

    def place_tower(self, x, y, range_r, cost):
        for i in range(max(0, x - range_r), min(self.n, x + range_r + 1)):
            for j in range(max(0, y - range_r), min(self.m, y + range_r + 1)):
                self.grid[i][j] = 2  # 2 represents tower coverage
        self.towers.append((x, y, range_r, cost))

    def display_grid(self):
        for row in self.grid:
            print(' '.join(map(str, row)))

    def optimize_tower_placement(self, budget):
        unblocked_cells = [(i, j) for i in range(self.n) for j in range(self.m) if self.grid[i][j] == 0]
        self.towers = []  # Reset towers

        # Assuming three types of towers with different ranges and costs
        tower_types = [(1, 10), (2, 20), (3, 30)]

        while unblocked_cells and budget > 0:
            x, y = unblocked_cells.pop()

            for range_r, cost in tower_types:
                if budget >= cost:
                    self.place_tower(x, y, range_r, cost)
                    budget -= cost
                    break

    def find_most_reliable_path(self, start, end):
        # Dijkstra's algorithm with reliability as the priority
        heap = [(0, start)]  # (reliability, node)
        visited = set()

        while heap:
            current_reliability, current_node = heapq.heappop(heap)

            if current_node == end:
                return 1 / current_reliability  # Inversely proportional to the number of hops

            if current_node not in visited:
                visited.add(current_node)

                x, y = current_node
                neighbors = [(x+i, y+j) for i in range(-1, 2) for j in range(-1, 2)
                             if 0 <= x+i < self.n and 0 <= y+j < self.m and self.grid[x+i][y+j] == 2]

                for neighbor in neighbors:
                    neighbor_reliability = current_reliability + 1  # 1 represents a hop
                    heapq.heappush(heap, (1 / neighbor_reliability, neighbor))

        return float('inf')  # No path found

    def visualize_city(self):
        fig, ax = plt.subplots()

        # Plot obstructed blocks
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 1:
                    ax.add_patch(patches.Rectangle((j, self.n - i - 1), 1, 1, facecolor='black'))

        # Plot towers and their coverage areas
        for i in range(self.n):
            for j in range(self.m):
                if self.grid[i][j] == 2:
                    ax.add_patch(patches.Rectangle((j, self.n - i - 1), 1, 1, facecolor='blue', alpha=0.5))

        ax.set_xlim(0, self.m)
        ax.set_ylim(0, self.n)
        ax.set_aspect('equal', 'box')
        plt.gca().invert_yaxis()
        plt.title('City Grid Visualization')
        plt.show()

# Example usage
city = CityGrid(5, 5)
city.display_grid()
print("\nOptimizing tower placement with budget 40\n")
city.optimize_tower_placement(40)
city.display_grid()

# Visualize the city
city.visualize_city()
