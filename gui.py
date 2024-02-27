import pygame
import random

class Land:
    def __init__(self, rows, cols, mine_qty, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.mine_qty = mine_qty
        self.width = width
        self.height = height
        self.screen = screen
        self.title = "MINESWEEPER"
        self.status_play = 0 # 0 - not start, 1 - playing, 2 - win, 3 - lose
        self.time_play = 0
        self.openned = rows * cols - mine_qty
        self.mines_area = [[[0, 0] for _ in range(cols)] for _ in range(rows)]
        self.mines_loc = []
        self.drop_mine()
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def drop_mine(self):
        total = self.rows * self.cols
        self.mines_loc = []

        while len(self.mines_loc) < self.mine_qty:
            loc = int(random.random() * total) 
            if loc not in self.mines_loc:
                self.mines_loc.append(loc)
                x, y = [loc%self.cols, loc//self.cols]
                self.mines_area[y][x][0] = "*"
                for xd, yd in diag:
                    if 0 <= x + xd < self.cols and 0 <= y + yd < self.rows and self.mines_area[y + yd][x + xd][0] != "*":
                        self.mines_area[y + yd][x + xd][0] += 1

    def redrop_mine(self):
        self.mines_area = [[[0, 0] for _ in range(self.cols)] for _ in range(self.rows)]
        self.drop_mine()
    
    def draw(self):
        # TEXT
        text_quit = pygame.font.Font("freesansbold.ttf", 20).render("<back", True, (0, 0, 0))
        self.screen.blit(text_quit, (30, 30))
        
        text_title = pygame.font.Font("freesansbold.ttf", 50).render(self.title, True, (0, 0, 0))
        text_title_rect = text_title.get_rect()
        text_title_rect.center = (self.screen.get_rect().center[0], 45)
        self.screen.blit(text_title, text_title_rect)

        font_game = pygame.font.Font("freesansbold.ttf", 40)
        text_mines = font_game.render(f"{self.mine_qty:03d}", True, (0, 0, 0))
        self.screen.blit(text_mines, (200, 75))
        text_time = font_game.render(f"{self.time_play:03d}", True, (0, 0, 0))
        self.screen.blit(text_time, (450, 75))

        self.gap = min((self.height - 116) / self.rows, self.width / self.cols)
        self.margin = (self.width - (self.gap * self.cols)) / 2
        
        # LINE
        for i in range(self.cols+1): # vertical
            pygame.draw.line(self.screen, (0, 0, 0), (self.margin + i*self.gap, 116), (self.margin + i*self.gap, self.height), 2)
        for i in range(self.rows+1): # horizontal
            pygame.draw.line(self.screen, (0, 0, 0), (self.margin, 116 + i*self.gap), (self.width - self.margin, 116 + i*self.gap), 2)
        
        # BOX AND NUMBER
        font_mine = pygame.font.Font("freesansbold.ttf", int(self.gap-5))
        for r in range(self.rows):
            for c in range(self.cols):
                is_openned = self.mines_area[r][c][1]
                if is_openned == 1:
                    val = self.mines_area[r][c][0]
                    text = font_mine.render(str(val if val else ""), True, (0, 0, 0))
                    self.screen.blit(text, (self.margin + (c+0.55)*self.gap - text.get_width()/2, 116 + (r+0.55)*self.gap - text.get_height()/2))
                else:
                    if is_openned == 0:
                        color = (255, 255, 255)
                    if is_openned == 2:
                        color = (250, 250, 40)
                    if is_openned == 3:
                        color = (250, 20, 20)
                    if is_openned == 4:
                        color = (0, 0, 0)
                    pygame.draw.rect(self.screen, color, (self.margin + 2 + c*self.gap, 118 + r*self.gap, self.gap - 5, self.gap - 5), int(self.gap))

    def popup(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols and self.mines_area[r][c][1] != 1:
            self.mines_area[r][c][1] = 1
            self.openned -= 1
            if not self.mines_area[r][c][0]:
                for rd, cd in diag:
                    self.popup(r+rd, c+cd)

    def click(self, pos, btn):
        if self.margin < pos[0] < self.width - self.margin and 116 < pos[1] < self.height:
            x = int((pos[0] - self.margin) // self.gap)
            y = int((pos[1] - 116) // self.gap)
            mine = self.mines_area[y][x]

            if btn == 3:
                if mine[1] == 2:
                    mine[1] = 0
                    self.mine_qty += 1
                elif mine[1] == 0:
                    if self.status_play == 0:
                        self.status_play = 1
                    mine[1] = 2
                    self.mine_qty -= 1
            elif btn == 1:
                if mine[1] == 0:
                    if mine[0] == "*":
                        if self.status_play == 0:
                            while mine[0] == "*":
                                self.redrop_mine()
                            self.click(pos, btn)
                        else:
                            for loc in self.mines_loc:
                                c, r = [loc%self.cols, loc//self.cols]
                                self.mines_area[r][c][1] = 3
                            mine[1] = 4
                            self.title = "BOOOMMMMM"
                            self.status_play = 3
                    else:
                        if self.status_play < 2:
                            if self.status_play == 0:
                                self.status_play = 1
                            self.popup(y, x)
                            if self.openned == 0:
                                self.title = "WIINNNN!"
                                self.status_play = 2

diag = [[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]]
difficulties = [[9,9,10], [16,16,40], [16,30,99]]

def main():
    pygame.init()
    width, height = 720, 500
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    scr_centerX, scr_centerY = screen.get_rect().center
    pygame.display.set_caption("Minesweeper")
    running = True
    difficulty = -1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if board_game.status_play == 1:
                    board_game.time_play += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if difficulty == -1:
                    if 260 <= mouse[0] <= 460 and (125 <= mouse[1] <= 175 or 225 <= mouse[1] <= 275 or 325 <= mouse[1] <= 375):
                        if 125 <= mouse[1] <= 175:
                            difficulty = 0
                        if 225 <= mouse[1] <= 275:
                            difficulty = 1
                        if 325 <= mouse[1] <= 375:
                            difficulty = 2
                        r, c, mine_qty = difficulties[difficulty]
                        board_game = Land(r, c, mine_qty, width, height, screen)
                else:
                    if 30 < mouse[1] <= 50 and event.button == 1:
                        if 30 < mouse[0] <= 87:
                            difficulty = -1
                    else:
                        board_game.click(mouse, event.button)
                    

        screen.fill((198, 198, 198))
        mouse = pygame.mouse.get_pos()

        if difficulty == -1:
            rectangle = pygame.Rect(0, 0, 200, 50)
            font = pygame.font.Font("freesansbold.ttf",20)
            
            for y, diff_text in [[-100, "Beginner"], [0, "Intermediate"], [100, "Expert"]]:
                rectangle.center = (scr_centerX, scr_centerY + y)
                text = font.render(diff_text, True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = rectangle.center
                pygame.draw.rect(screen, (75, 75, 250), rectangle, 0, 10)
                screen.blit(text, textRect)     
        else:
            board_game.draw()
        
        clock.tick(60)
        pygame.display.update()

main()
pygame.quit()
