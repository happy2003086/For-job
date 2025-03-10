import random, re, pygame, sys
from pygame import gfxdraw

# ===============================================#
#       TODO: improve performance of ai         #
# ===============================================#

WIDTH = 1000 # window dimensions
HEIGHT = 1000
BOARD_SIZE = min(WIDTH, HEIGHT)

classic, big, mega = 13, 20, 32

SIZE = classic  # board dimensions: classic is 13, big is 20, mega is 32
sq_w = (BOARD_SIZE - 1) // SIZE  # this is for simplicity later on
text_size = (BOARD_SIZE - 1) // 8
ts1 = 0.01
ts2 = 0.005
ts3 = 0.003
ts4 = 0.003

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BOARD = (50, 190, 67)
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("GAME")
screen.fill(BOARD)
pygame.display.flip()

scoreing_dic = {
	'_XX(?=(_))': -4, '_XX(?=(O))': -2, 'OXX(?=(_))': -2, 'OXX(?=(O))': -1, '__XXX(?=(_))': -100, '_XXX(?=(__))': -100,
	'_XX_X(?=(_))': -100, '_X_XX(?=(_))': -100, 'XXXX(?=(_))': -400,
	'XXX_X': -400, 'XX_XX': -400, 'X_XXX': -400, '_XXXX': -400, 'XXXXX': -1600, '_OO(?=(_))': 3, '_OO(?=(X))': 2,
	'XOO(?=(_))': 2, 'XOO(?=(X))': 1, '__OOO(?=(_))': 15, '_OOO(?=(__))': 15,
	'_OO_O(?=(_))': 12, '_O_OO(?=(_))': 12, 'OOOO(?=(_))': 155, 'OOO_O': 150, 'OO_OO': 150, 'O_OOO': 150, '_OOOO': 155,
	'OOOOO': 2000, 'OX': 1, 'XO': 1
}

# function to write words on screen
font_name = pygame.font.match_font('Arial')


def draw_text(surf, text, size, x, y, color=WHITE):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (int(x), int(y))
	surf.blit(text_surface, text_rect)


# helper functions for array manipulations

def get_columns(arr):
	return [[j[i] for j in arr] for i in range(len(arr[0]))]


def empty_arr(l, w, fill=0):
	res = []
	for i in range(l):
		res.append([])
		for j in range(w):
			res[i].append(fill)
	return res


def get_diagonals(arr, od=False):
	if od:
		arr = [list(reversed(i)) for i in arr]
	n = len(arr) + len(arr[0]) - 1
	res = []
	for i in range(n):
		l = []
		x = i
		while x >= 0:
			try:
				l.append(arr[x][i - x])
			except(IndexError):
				pass
			finally:
				x -= 1
		if od:
			l.reverse()
		res.append(l)
	return res


def ai(board):  # function that lets the computer make good moves
	if board.rows == empty_arr(SIZE, SIZE, '_'):
		board.set((SIZE // 2, SIZE // 2), 'O')
		return board
	arr = board.rows
	maxed_boards = []
	max_score = float('-inf')
	for i in range(SIZE):  # for each cell in the board
		for j in range(SIZE):
			has_neighbors = False
			for dx in [-2, -1, 0, 1, 2]:  # checks to see if this cell has a non-empty neighbor in a radius of two cells
				for dy in [-2, -1, 0, 1, 2]:
					x = i + dx
					y = j + dy
					if x not in list(range(SIZE)) or y not in list(range(SIZE)):
						continue
					if arr[x][y] != '_':
						has_neighbors = True
			if not has_neighbors or board.rows[i][
				j] != '_':  # if no neighbors or if the cell is already occupied, skip this cell
				continue
			pos = (i, j)
			board.set(pos, 'O')  # sets cell to 'O'
			score = board.score()
			if (score > max_score) or not maxed_boards:  # if a better board was found, reset the list of 'best boards'
				maxed_boards = [pos]
				max_score = score
			elif score == max_score:  # otherwise if the scores are the same, add it to the list
				maxed_boards.append(pos)
			board.set(pos, '_')  # sets cell back to '_'
	pos = (0, 0)
	try:  # try to find a random board from the best boards
		pos = maxed_boards[random.randint(0, len(maxed_boards) - 1)]
		board.set(pos, 'O')
	except:  # otherwise if they are all equal find a random move
		pos = (random.randint(0, SIZE), random.randint(0, SIZE))
		board.set(pos, 'O')
	return pos


# game board class
class Board:
	def __init__(self, size):
		self.rows = empty_arr(size, size, '_')
		self.columns = get_columns(self.rows)
		self.diagonal_1 = get_diagonals(self.rows)
		self.diagonal_2 = get_diagonals(self.rows, True)
		self.size = size

	def update(self):  # updates columns and diagonals
		self.diagonal_1 = get_diagonals(self.rows)
		self.diagonal_2 = get_diagonals(self.rows, True)

	def set(self, pos, color):  # lets player or computer make a move
		self.rows[pos[0]][pos[1]] = color
		self.columns[pos[1]][pos[0]] = color
		self.update()

	def check(self):  # checks for wins
		draw = True
		for i in self.rows:
			if '_' in i: draw = False
		if draw: return '?'
		for orientation in [self.rows, self.columns, self.diagonal_1, self.diagonal_2]:
			for line in orientation:
				if 'XXXXX' in ''.join(line):
					return 'X'
				elif 'OOOOO' in ''.join(line):
					return 'O'
		return None

	def score(self):  # helper function for the ai
		dic = scoreing_dic
		score = 0
		for orientation in [self.rows, self.columns, self.diagonal_1, self.diagonal_2]:  # calculates score
			for line in orientation:
				strng = ''.join(line)
				for pattern in dic.keys():
					score += dic[pattern] * len(re.findall(pattern, strng))
		return score


prev_move = None


def render(b):  # draws board
	screen.fill(BLACK)
	rect = pygame.Surface((sq_w - 1, sq_w - 1)).get_rect()
	for i in range(SIZE):
		for j in range(SIZE):
			center = (int(i * BOARD_SIZE / SIZE) + sq_w // 2 + (WIDTH - BOARD_SIZE) // 2,
					int(j * BOARD_SIZE / SIZE) + sq_w // 2 + (HEIGHT - BOARD_SIZE) // 2)
			rect.center = center
			color = b.rows[i][j]
			pygame.draw.rect(screen, BOARD, rect)
			if color == 'O':
				if prev_move == (i, j):
					gfxdraw.filled_circle(screen, center[0], center[1], int(sq_w * 0.4), BLACK)
					gfxdraw.aacircle(screen, center[0], center[1], int(sq_w * 0.4), BLUE)
				else:
					gfxdraw.filled_circle(screen, center[0], center[1], int(sq_w * 0.4), BLACK)
					gfxdraw.aacircle(screen, center[0], center[1], int(sq_w * 0.4), BLACK)
			if color == 'X':
				gfxdraw.filled_circle(screen, center[0], center[1], int(sq_w * 0.4), WHITE)
				gfxdraw.aacircle(screen, center[0], center[1], int(sq_w * 0.4), WHITE)
	pygame.display.flip()


def game_over(winner, moves):
	text = ''
	# decides winner
	if winner == 'X':
		text = 'You won in ' + str(moves) + ' moves'
	elif winner == 'O':
		text = 'Computer won in ' + str(moves) + ' moves'
	elif winner == 'p':
		text = 'You stopped after ' + str(moves) + ' turns'
	else:
		text = 'DRAW!'
	# shows info
	shadowed_text('GAME OVER', 1.3 * text_size, min(WIDTH, 800) * ts1, -1.6 * text_size)
	shadowed_text(text, 0.6 * text_size, min(WIDTH, 800) * ts2, -0.4 * text_size)
	shadowed_text('Click to play again', 0.4 * text_size, min(WIDTH, 800) * ts3, 0.2 * text_size)
	shadowed_text('OR', 0.5 * text_size, min(WIDTH, 800) * ts2, 0.6 * text_size)
	shadowed_text('Press c for classic board size (13X13)', 0.4 * text_size, min(WIDTH, 800) * ts3, 1.2 * text_size)
	shadowed_text('Press b for big board size (20X20)', 0.4 * text_size, min(WIDTH, 800) * ts3, 1.6 * text_size)
	shadowed_text('Press m for mega board size (32X32)', 0.4 * text_size, min(WIDTH, 800) * ts3, 2.0 * text_size)


def shadowed_text(text, size, shadow, offset=0, reversed=False):  # function for drawing shadowed text
	size = int(size)
	shadow = int(shadow)
	offset = int(offset)
	if not reversed:
		#draw_text(screen, text, size, WIDTH / 2 + shadow, HEIGHT / 2 + offset, (30, 10, 230))
		draw_text(screen, text, size, WIDTH / 2, HEIGHT / 2 + offset, (150, 10, 150))
		#draw_text(screen, text, size, WIDTH / 2 - shadow, HEIGHT / 2 + offset, (230, 10, 30))
	else:
		#draw_text(screen, text, size, WIDTH / 2 + shadow, HEIGHT / 2 + offset, (230, 10, 30))
		draw_text(screen, text, size, WIDTH / 2, HEIGHT / 2 + offset, (150, 10, 150))
		#draw_text(screen, text, size, WIDTH / 2 - shadow, HEIGHT / 2 + offset, (30, 10, 230))


b = Board(SIZE)
render(b)

moves = 0
running = True


def resize(event):
	surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
	WIDTH = event.w
	HEIGHT = event.h
	BOARD_SIZE = min(WIDTH, HEIGHT)
	sq_w = (BOARD_SIZE) // SIZE
	text_size = (BOARD_SIZE - 1) // 8
	render(b)
	game_over('p', moves)
	pygame.display.flip()


while running:  # game loop
	waiting = True
	restart_game = False
	while waiting:  # waiting for player to make move
		for event in pygame.event.get():  # checks for events, including player making move
			if event.type == pygame.QUIT:  # close screen
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:  # player move
				inp = pygame.mouse.get_pos()
				inp = [int((inp[0] - (WIDTH - BOARD_SIZE) / 2) / BOARD_SIZE * SIZE),
					int((inp[1] - (HEIGHT - BOARD_SIZE) / 2) / BOARD_SIZE * SIZE)]
				try:  # if its a valid move, record it and move on
					if inp[0] < 0 or inp[1] < 0 or b.rows[inp[0]][
						inp[1]] != '_': raise ValueError  # if the input is invalid, raise an error
					b.set(inp, 'X')  # records move
					render(b)  # draws board
					waiting = False  # moves on
				except:
					pass  # otherwise retry
			if event.type == pygame.VIDEORESIZE:  # screen resizing
				surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
				WIDTH = event.w
				HEIGHT = event.h
				BOARD_SIZE = min(WIDTH, HEIGHT)
				sq_w = (BOARD_SIZE) // SIZE
				text_size = (BOARD_SIZE - 1) // 8
				render(b)
	
	if restart_game: continue

	result = b.check()  # finds out if player won
	moves += 1
	if result is not None:  # if player won, display some text and wait for click, then reset board and move on
		render(b)
		game_over(result, moves)
		pygame.display.flip()
		waiting = True
		render_text = True
		while waiting:  # waits for input
			space_pressed = False
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						SIZE = classic
						waiting = False
					elif event.key == pygame.K_b:
						SIZE = big
						waiting = False
					elif event.key == pygame.K_m:
						SIZE = mega
						waiting = False
					elif event.key == pygame.K_SPACE:
						space_pressed = True
				if event.type == pygame.QUIT:
					running = False
					waiting = False
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					waiting = False
				if event.type == pygame.VIDEORESIZE:  # screen resizing
					resize(event)
			if space_pressed:
				render_text = not render_text
				if render_text:
					game_over(result, moves)
					pygame.display.flip()
				else:
					render(b)
		b = Board(SIZE)
		sq_w = (BOARD_SIZE - 1) // SIZE
		moves = 0
		prev_move = None

	prev_move = ai(b)  # computer move
	result = b.check()  # finds out if computer won

	if result is not None:  # if computer won,  display some text and wait for click, then reset board and move on
		moves += 1
		render(b)  # redraw the board
		game_over(result, moves)
		pygame.display.flip()  # refreshes screen
		waiting = True

		render_text = True
		while waiting:  # waits for input
			space_pressed = False
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_c:
						SIZE = classic
						waiting = False
					elif event.key == pygame.K_b:
						SIZE = big
						waiting = False
					elif event.key == pygame.K_m:
						SIZE = mega
						waiting = False
					elif event.key == pygame.K_SPACE:
						space_pressed = True
				if event.type == pygame.QUIT:  # close screen
					running = False
					waiting = False
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:  # stops waiting
					waiting = False
				if event.type == pygame.VIDEORESIZE:  # screen resizing
					resize(event)
			if space_pressed:
				render_text = not render_text
				if render_text:
					game_over(result, moves)
					pygame.display.flip()
				else:
					render(b)
		b = Board(SIZE)  # resets board
		sq_w = (BOARD_SIZE - 1) // SIZE
		moves = 0  # resets moves
		prev_move = None
	else:
		moves += 1
	render(b)  # redraw the board
pygame.quit()