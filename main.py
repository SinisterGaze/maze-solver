from types import CellType
import numpy as np
from numpy.lib.histograms import histogram_bin_edges
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Maze:
    def __init__(self, n, m, p = .4, q = .3, cellsize = 20):
        self.n = n
        self.m = m

        self.p = p
        self.q = q
        
        self.cellsize = cellsize
        self.vertical_walls = np.random.rand(self.n, self.m-1)
        self.horizontal_walls = np.random.rand(self.n-1, self.m)
        self.vertical_walls = self.vertical_walls < self.p
        self.horizontal_walls = self.horizontal_walls < self.q

        self.width = self.m*self.cellsize
        self.height = self.n*self.cellsize
        assert self.width <= WIDTH and self.height <= HEIGHT

        self.xleft = (WIDTH-self.width)/2
        self.ytop = (HEIGHT-self.height)/2

        self.winningpath = []

        
    def show(self, surface):
        for i in range(self.n):
            for j in range(self.m):
                if j == 0:
                    self.draw_vline(surface, i, j)
                elif j == self.m-1:
                    self.draw_vline(surface, i, j+1)
                if i == 0:
                    self.draw_hline(surface, i, j)
                elif i == self.n-1:
                    self.draw_hline(surface, i+1, j)
                if j < self.m-1 and self.vertical_walls[i, j]:
                    self.draw_vline(surface, i, j+1)
                if i < self.n-1 and self.horizontal_walls[i, j]:
                    self.draw_hline(surface, i+1, j)

    def draw_vline(self, surface, i, j):
        x = self.xleft + j * self.cellsize
        y = self.ytop + i * self.cellsize

        start_pos = (x, y)
        end_pos = (x, y + self.cellsize)

        pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, width = 1)

    def draw_hline(self, surface, i, j):
        x = self.xleft + j * self.cellsize
        y = self.ytop + i * self.cellsize

        start_pos = (x, y)
        end_pos = (x + self.cellsize, y)

        pygame.draw.line(surface, (0, 0, 0), start_pos, end_pos, width = 1)
   
    def get_neighbors(self, cell):
        i, j = cell
        assert (0 <= i <= self.n-1) and (0 <= j <= self.m-1)
        neighbors = []
        if i > 0 and not self.horizontal_walls[i-1,j]: 
            neighbors.append((i-1, j))
        if j > 0 and not self.vertical_walls[i,j-1]:
            neighbors.append((i, j-1))
        if i < self.n-1 and not self.horizontal_walls[i,j]:
            neighbors.append((i+1,j))
        if j < self.m-1 and not self.vertical_walls[i,j]:
            neighbors.append((i, j+1))
        
        return neighbors
    
    def draw_cell(self, surface, cell, color):
        i, j = cell
        x = self.xleft + (j + 0.5) * self.cellsize
        y = self.ytop + (i +  0.5) * self.cellsize
        pygame.draw.circle(surface, color, (x,y), 0.4*self.cellsize)

    def breadth_first_search(self):
        start_point = (0, np.random.randint(self.m))
        self.start_point = start_point
        end_row = self.n-1

        to_visit = [start_point]
        visited = []

        score = np.matrix(np.ones((self.n, self.m)) * np.inf)
        score[start_point] = 0

        from_point = start_point

        winner = (-1, -1) 
        best_score = np.inf
        while to_visit:
            current = to_visit[0]

            i, _ = current

            if i == end_row:
                winner = current if score[current] < best_score else winner
                best_score = min(best_score, score[current])
            
            if winner == (-1, -1) or score[current] < best_score:
                queue = self.get_neighbors(current)
                for point in queue:
                    score[point] = min(score[point], score[current] + 1)
                    if point not in visited:
                        to_visit.append(point)
            
            visited.append(current)
            to_visit=to_visit[1:]

        if winner != (-1, -1):
            self.winningpath = self.get_path(winner, score)
            
        return start_point, winner, score

    def draw_winning_path(self, surface):
        path = self.winningpath
        if path:
            winner = path[0]
            p1 = path[0]
            path = path[1:]
            while path:
                p2 = path[0]
                self.draw_line(surface, p1, p2)
                p1 = p2
                path = path[1:]

            self.draw_cell(surface, winner, (0,255,0))  
        self.draw_cell(screen, self.start_point, (0,255, 255))
    
    def get_path(self, point, score):
        if point != (-1, -1):
            current = point
            path = [current]
            while score[current] > 0:
                for point in self.get_neighbors(current):
                    if score[point] == score[current] - 1:
                        path.append(point)
                        current = point
                        continue
            return path
        else:
            return []

    def draw_line(self, surface, from_point, to_point, color = (255,0,0), width = 2):
        x1 = self.xleft + self.cellsize * (from_point[1] + 0.5)
        y1 = self.ytop + self.cellsize * (from_point[0] + 0.5)
        x2 = self.xleft + self.cellsize * (to_point[1] + 0.5)
        y2 = self.ytop + self.cellsize * (to_point[0] + 0.5)

        start_pos = (x1,y1)
        end_pos = (x2,y2)
        pygame.draw.line(surface, color, start_pos, end_pos, width = width)

def main():
    done = False
    clock = pygame.time.Clock()
    M = Maze(30, 30)
    start_point, winner, score = M.breadth_first_search()
    while not done:

        dt = clock.tick(144)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            continue
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((255,255,255))
        
        M.show(screen)
        M.draw_winning_path(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
