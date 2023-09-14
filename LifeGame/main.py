import numpy as np
import pygame

# Set the window size and cell size
WINDOW_SIZE = 800
CELL_SIZE = 5

pygame.init()

# Create a window with the specified size
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))


def update_grid(grid, rows, cols):
    new_grid = grid.copy()

    for i in range(rows):
        for j in range(cols):
            # Get the index for this cell
            idx = i * cols + j
            neighbors = get_neighbors(grid, rows, cols, i, j)

            # Apply the rules of the Game of Life to update this cell
            if grid[idx] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[idx] = 0
            else:
                if neighbors == 3:
                    new_grid[idx] = 1

    return new_grid


def get_neighbors(grid, rows, cols, row, col):
    count = 0
    # Iterate through the 3x3 neighborhood around the cell
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            # Ignore the center cell
            if i == row and j == col: continue
            # Check if the cell is out of bounds
            if i < 0 or i >= rows or j < 0 or j >= cols: continue
            idx = i * cols + j
            # If the cell is alive, increment the count
            if grid[idx] == 1:
                count += 1

    return count


def draw_grid(grid, rows, cols):

    for i in range(rows):
        for j in range(cols):
            x = j * CELL_SIZE
            y = i * CELL_SIZE

            idx = i * cols + j

            if grid[idx] == 1:
                color = (255, 255, 255)  # White for living cells
            else:
                color = (0, 0, 0)  # Black for dead cells

            # Draw the cell
            pygame.draw.rect(screen, color, pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))


def main():
    rows, cols = 160, 160
    # if grid[idx] == 1 -> black
    grid = np.random.randint(0, 8, size=rows * cols)

    for _ in range(5000):

        # Update the grid
        grid = update_grid(grid, rows, cols)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the grid
        draw_grid(grid, rows, cols)

        # Update the display
        pygame.display.flip()

        # Wait for a short time
        pygame.time.wait(10)


if __name__ == '__main__':
    main()

