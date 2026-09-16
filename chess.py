"""
Python 國際象棋 (Chess) — 約 1000 ELO（手機自適應 + 向量棋子圖像版）
"""

import tkinter as tk
from tkinter import messagebox

# ============================================================
# 常數
# ============================================================
WHITE, BLACK = 'w', 'b'
MATE = 100000
DEPTH = 3              # 搜尋深度（3 ≈ 1000~1300 ELO）

INIT_BOARD = [
    'r','n','b','q','k','b','n','r',
    'p','p','p','p','p','p','p','p',
    None,None,None,None,None,None,None,None,
    None,None,None,None,None,None,None,None,
    None,None,None,None,None,None,None,None,
    None,None,None,None,None,None,None,None,
    'P','P','P','P','P','P','P','P',
    'R','N','B','Q','K','B','N','R',
]

PIECE_VALUES = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000}

KNIGHT_OFFSETS = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
BISHOP_DIRS    = [(-1,-1),(-1,1),(1,-1),(1,1)]
ROOK_DIRS      = [(-1,0),(1,0),(0,-1),(0,1)]
KING_DIRS      = BISHOP_DIRS + ROOK_DIRS

PST = {
'P': [
     0,  0,  0,  0,  0,  0,  0,  0,  50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,   5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,   5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,   0,  0,  0,  0,  0,  0,  0,  0],
'N': [
   -50,-40,-30,-30,-30,-30,-40,-50, -40,-20,  0,  0,  0,  0,-20,-40,
   -30,  0, 10, 15, 15, 10,  0,-30, -30,  5, 15, 20, 20, 15,  5,-30,
   -30,  0, 15, 20, 20, 15,  0,-30, -30,  5, 10, 15, 15, 10,  5,-30,
   -40,-20,  0,  5,  5,  0,-20,-40, -50,-40,-30,-30,-30,-30,-40,-50],
'B': [
   -20,-10,-10,-10,-10,-10,-10,-20, -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5, 10, 10,  5,  0,-10, -10,  5,  5, 10, 10,  5,  5,-10,
   -10,  0, 10, 10, 10, 10,  0,-10, -10, 10, 10, 10, 10, 10, 10,-10,
   -10,  5,  0,  0,  0,  0,  5,-10, -20,-10,-10,-10,-10,-10,-10,-20],
'R': [
     0,  0,  0,  0,  0,  0,  0,  0,   5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,  -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,  -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,   0,  0,  0,  5,  5,  0,  0,  0],
'Q': [
   -20,-10,-10, -5, -5,-10,-10,-20, -10,  0,  0,  0,  0,  0,  0,-10,
   -10,  0,  5,  5,  5,  5,  0,-10,  -5,  0,  5,  5,  5,  5,  0, -5,
     0,  0,  5,  5,  5,  5,  0, -5, -10,  5,  5,  5,  5,  5,  0,-10,
   -10,  0,  5,  0,  0,  0,  0,-10, -20,-10,-10, -5, -5,-10,-10,-20],
'K': [
   -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
   -30,-40,-40,-50,-50,-40,-40,-30, -30,-40,-40,-50,-50,-40,-40,-30,
   -20,-30,-30,-40,-40,-30,-30,-20, -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,  20, 30, 10,  0,  0, 10, 30, 20],
}

# ============================================================
# 棋子圖像：用 Canvas 向量繪製，唔靠字體、唔靠圖檔
# ============================================================
def draw_piece(cv, s, kind, is_white):
    """喺 canvas cv 上面畫一粒棋子。s = 格仔邊長(px)，kind = 'P','N','B','R','Q','K'"""
    fill = '#FFFFFF' if is_white else '#1E1E1E'
    line = '#1E1E1E' if is_white else '#000000'
    lw   = max(1.0, s * 0.045)
    cx   = s / 2.0

    def P(*pts):
        cv.create_polygon(*pts, fill=fill, outline=line, width=lw)

    def O(x0, y0, x1, y1):
        cv.create_oval(x0, y0, x1, y1, fill=fill, outline=line, width=lw)

    def R(x0, y0, x1, y1):
        cv.create_rectangle(x0, y0, x1, y1, fill=fill, outline=line, width=lw)

    if kind == 'P':                                    # 兵
        O(cx - 0.14*s, 0.22*s, cx + 0.14*s, 0.50*s)
        P(cx - 0.11*s, 0.46*s,  cx + 0.11*s, 0.46*s,
          cx + 0.17*s, 0.72*s,  cx - 0.17*s, 0.72*s)
        R(cx - 0.23*s, 0.72*s,  cx + 0.23*s, 0.84*s)

    elif kind == 'R':                                  # 車
        for dx in (-0.16, 0.0, 0.16):
            R(cx + dx*s - 0.07*s, 0.13*s, cx + dx*s + 0.07*s, 0.26*s)
        R(cx - 0.22*s, 0.24*s, cx + 0.22*s, 0.34*s)
        P(cx - 0.17*s, 0.34*s,  cx + 0.17*s, 0.34*s,
          cx + 0.21*s, 0.72*s,  cx - 0.21*s, 0.72*s)
        R(cx - 0.25*s, 0.72*s, cx + 0.25*s, 0.84*s)

    elif kind == 'N':                                  # 馬
        P(cx - 0.16*s, 0.84*s,  cx - 0.18*s, 0.64*s,  cx - 0.12*s, 0.50*s,
          cx - 0.04*s, 0.40*s,  cx - 0.10*s, 0.32*s,  cx - 0.20*s, 0.34*s,
          cx - 0.24*s, 0.28*s,  cx - 0.16*s, 0.22*s,  cx - 0.06*s, 0.24*s,
          cx + 0.04*s, 0.30*s,  cx + 0.16*s, 0.26*s,  cx + 0.24*s, 0.34*s,
          cx + 0.24*s, 0.48*s,  cx + 0.18*s, 0.60*s,  cx + 0.16*s, 0.72*s,
          cx + 0.20*s, 0.84*s)

    elif kind == 'B':                                  # 象
        O(cx - 0.06*s, 0.13*s, cx + 0.06*s, 0.25*s)
        O(cx - 0.15*s, 0.26*s, cx + 0.15*s, 0.68*s)
        R(cx - 0.23*s, 0.68*s, cx + 0.23*s, 0.78*s)
        R(cx - 0.27*s, 0.78*s, cx + 0.27*s, 0.86*s)

    elif kind == 'Q':                                  # 后
        for dx in (-0.20, -0.10, 0.0, 0.10, 0.20):
            O(cx + dx*s - 0.045*s, 0.11*s, cx + dx*s + 0.045*s, 0.20*s)
        P(cx - 0.22*s, 0.46*s, cx - 0.20*s, 0.22*s, cx - 0.10*s, 0.36*s,
          cx,          0.18*s,
          cx + 0.10*s, 0.36*s, cx + 0.20*s, 0.22*s, cx + 0.22*s, 0.46*s)
        P(cx - 0.18*s, 0.46*s, cx + 0.18*s, 0.46*s,
          cx + 0.14*s, 0.70*s, cx - 0.14*s, 0.70*s)
        R(cx - 0.26*s, 0.70*s, cx + 0.26*s, 0.80*s)
        R(cx - 0.29*s, 0.80*s, cx + 0.29*s, 0.88*s)

    elif kind == 'K':                                  # 王
        R(cx - 0.035*s, 0.09*s, cx + 0.035*s, 0.30*s)
        R(cx - 0.10*s,  0.15*s, cx + 0.10*s,  0.23*s)
        P(cx - 0.22*s, 0.46*s, cx - 0.22*s, 0.32*s, cx - 0.10*s, 0.40*s,
          cx,          0.30*s,
          cx + 0.10*s, 0.40*s, cx + 0.22*s, 0.32*s, cx + 0.22*s, 0.46*s)
        P(cx - 0.18*s, 0.46*s, cx + 0.18*s, 0.46*s,
          cx + 0.14*s, 0.70*s, cx - 0.14*s, 0.70*s)
        R(cx - 0.26*s, 0.70*s, cx + 0.26*s, 0.80*s)
        R(cx - 0.29*s, 0.80*s, cx + 0.29*s, 0.88*s)


# ============================================================
# 棋盤類別
# ============================================================
class Board:
    def __init__(self):
        self.board = INIT_BOARD[:]
        self.turn = WHITE
        self.castling = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.ep = None
        self.halfmove = 0
        self.undo_stack = []

    def make_move(self, move):
        fr, fc, tr, tc, promo = move
        fi, ti = fr * 8 + fc, tr * 8 + tc
        piece = self.board[fi]
        is_white = piece.isupper()

        u = {'move': move, 'captured': self.board[ti], 'captured_idx': ti,
             'castling': self.castling.copy(), 'ep': self.ep,
             'halfmove': self.halfmove, 'rook_move': None}

        if piece.upper() == 'P' and fc != tc and self.board[ti] is None:
            cap_i = fr * 8 + tc
            u['captured'] = self.board[cap_i]
            u['captured_idx'] = cap_i
            self.board[cap_i] = None

        self.board[fi] = None
        self.board[ti] = piece

        if promo:
            self.board[ti] = promo if is_white else promo.lower()

        if piece.upper() == 'K' and abs(tc - fc) == 2:
            rf = fr * 8 + (7 if tc > fc else 0)
            rt = fr * 8 + (5 if tc > fc else 3)
            rook = self.board[rf]
            u['rook_move'] = (rf, rt, rook)
            self.board[rf] = None
            self.board[rt] = rook

        if piece == 'K':
            self.castling['K'] = self.castling['Q'] = False
        elif piece == 'k':
            self.castling['k'] = self.castling['q'] = False
        elif piece == 'R':
            if fr == 7 and fc == 7: self.castling['K'] = False
            if fr == 7 and fc == 0: self.castling['Q'] = False
        elif piece == 'r':
            if fr == 0 and fc == 7: self.castling['k'] = False
            if fr == 0 and fc == 0: self.castling['q'] = False

        if   ti == 63: self.castling['K'] = False
        elif ti == 56: self.castling['Q'] = False
        elif ti == 7:  self.castling['k'] = False
        elif ti == 0:  self.castling['q'] = False

        self.ep = None
        if piece.upper() == 'P' and abs(tr - fr) == 2:
            self.ep = ((fr + tr) // 2, fc)

        self.halfmove = 0 if (piece.upper() == 'P' or u['captured'] is not None) else self.halfmove + 1
        self.turn = BLACK if is_white else WHITE
        self.undo_stack.append(u)

    def unmake_move(self):
        u = self.undo_stack.pop()
        fr, fc, tr, tc, promo = u['move']
        fi, ti = fr * 8 + fc, tr * 8 + tc
        piece = self.board[ti]
        if promo: piece = 'P' if piece.isupper() else 'p'
        self.board[ti] = None
        self.board[u['captured_idx']] = u['captured']
        self.board[fi] = piece
        if u['rook_move']:
            rf, rt, rook = u['rook_move']
            self.board[rt] = None
            self.board[rf] = rook
        self.castling = u['castling']
        self.ep = u['ep']
        self.halfmove = u['halfmove']
        self.turn = BLACK if self.turn == WHITE else WHITE

    def attacked(self, r, c, by):
        b = self.board
        if by == WHITE:
            for dc in (-1, 1):
                nr, nc = r + 1, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8 and b[nr*8+nc] == 'P': return True
        else:
            for dc in (-1, 1):
                nr, nc = r - 1, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8 and b[nr*8+nc] == 'p': return True
        for dr, dc in KNIGHT_OFFSETS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                p = b[nr*8+nc]
                if p and p.upper() == 'N' and p.isupper() == (by == WHITE): return True
        for dr, dc in KING_DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                p = b[nr*8+nc]
                if p and p.upper() == 'K' and p.isupper() == (by == WHITE): return True
        for dr, dc in BISHOP_DIRS:
            nr, nc = r + dr, c + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                p = b[nr*8+nc]
                if p:
                    if p.isupper() == (by == WHITE) and p.upper() in ('B', 'Q'): return True
                    break
                nr += dr; nc += dc
        for dr, dc in ROOK_DIRS:
            nr, nc = r + dr, c + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                p = b[nr*8+nc]
                if p:
                    if p.isupper() == (by == WHITE) and p.upper() in ('R', 'Q'): return True
                    break
                nr += dr; nc += dc
        return False

    def find_king(self, side):
        t = 'K' if side == WHITE else 'k'
        for i in range(64):
            if self.board[i] == t: return i
        return -1

    def in_check(self, side):
        ki = self.find_king(side)
        if ki < 0: return False
        r, c = divmod(ki, 8)
        return self.attacked(r, c, BLACK if side == WHITE else WHITE)

    def pseudo_moves(self):
        moves = []
        side = self.turn
        b = self.board
        is_white = (side == WHITE)
        for i in range(64):
            p = b[i]
            if p is None or p.isupper() != is_white: continue
            r, c = divmod(i, 8)
            pu = p.upper()
            if pu == 'P':
                d = -1 if is_white else 1
                start = 6 if is_white else 1
                last = 0 if is_white else 7
                nr = r + d
                if 0 <= nr < 8:
                    if b[nr*8+c] is None:
                        if nr == last:
                            for pr in 'QRBN': moves.append((r, c, nr, c, pr))
                        else:
                            moves.append((r, c, nr, c, None))
                            if r == start and b[(r+2*d)*8+c] is None:
                                moves.append((r, c, r+2*d, c, None))
                    for dc in (-1, 1):
                        nc = c + dc
                        if 0 <= nc < 8:
                            tp = b[nr*8+nc]
                            if tp is not None and tp.isupper() != is_white:
                                if nr == last:
                                    for pr in 'QRBN': moves.append((r, c, nr, nc, pr))
                                else: moves.append((r, c, nr, nc, None))
                            elif self.ep == (nr, nc):
                                moves.append((r, c, nr, nc, None))
            elif pu == 'N':
                for dr, dc in KNIGHT_OFFSETS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        tp = b[nr*8+nc]
                        if tp is None or tp.isupper() != is_white:
                            moves.append((r, c, nr, nc, None))
            elif pu in ('B', 'R', 'Q'):
                dirs = []
                if pu in ('B', 'Q'): dirs += BISHOP_DIRS
                if pu in ('R', 'Q'): dirs += ROOK_DIRS
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    while 0 <= nr < 8 and 0 <= nc < 8:
                        tp = b[nr*8+nc]
                        if tp is None: moves.append((r, c, nr, nc, None))
                        else:
                            if tp.isupper() != is_white: moves.append((r, c, nr, nc, None))
                            break
                        nr += dr; nc += dc
            elif pu == 'K':
                for dr, dc in KING_DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        tp = b[nr*8+nc]
                        if tp is None or tp.isupper() != is_white:
                            moves.append((r, c, nr, nc, None))
                opp = BLACK if is_white else WHITE
                if is_white and r == 7 and c == 4:
                    if (self.castling['K'] and b[61] is None and b[62] is None and b[63] == 'R'
                            and not self.attacked(7, 4, opp) and not self.attacked(7, 5, opp) and not self.attacked(7, 6, opp)):
                        moves.append((7, 4, 7, 6, None))
                    if (self.castling['Q'] and b[59] is None and b[58] is None and b[57] is None and b[56] == 'R'
                            and not self.attacked(7, 4, opp) and not self.attacked(7, 3, opp) and not self.attacked(7, 2, opp)):
                        moves.append((7, 4, 7, 2, None))
                elif (not is_white) and r == 0 and c == 4:
                    if (self.castling['k'] and b[5] is None and b[6] is None and b[7] == 'r'
                            and not self.attacked(0, 4, opp) and not self.attacked(0, 5, opp) and not self.attacked(0, 6, opp)):
                        moves.append((0, 4, 0, 6, None))
                    if (self.castling['q'] and b[3] is None and b[2] is None and b[1] is None and b[0] == 'r'
                            and not self.attacked(0, 4, opp) and not self.attacked(0, 3, opp) and not self.attacked(0, 2, opp)):
                        moves.append((0, 4, 0, 2, None))
        return moves

    def legal_moves(self):
        side = self.turn
        result = []
        for m in self.pseudo_moves():
            self.make_move(m)
            if not self.in_check(side): result.append(m)
            self.unmake_move()
        return result

# ============================================================
# 評估與搜尋
# ============================================================
def evaluate(g):
    score = 0
    b = g.board
    for i in range(64):
        p = b[i]
        if p is None: continue
        pu = p.upper()
        v = PIECE_VALUES[pu]
        if p.isupper(): v += PST[pu][i]; score += v
        else: v += PST[pu][i ^ 56]; score -= v
    return score if g.turn == WHITE else -score

def move_score(g, m):
    fr, fc, tr, tc, promo = m
    s = 0
    if promo: s += 800
    cap = g.board[tr*8+tc]
    if cap: s += PIECE_VALUES[cap.upper()] * 10 - PIECE_VALUES[g.board[fr*8+fc].upper()]
    return s

def quiesce(g, alpha, beta, qdepth):
    stand = evaluate(g)
    if stand >= beta: return beta
    if stand > alpha: alpha = stand
    if qdepth >= 4: return alpha
    caps = [m for m in g.pseudo_moves() if g.board[m[2]*8+m[3]] is not None]
    caps.sort(key=lambda m: move_score(g, m), reverse=True)
    for m in caps:
        g.make_move(m)
        if g.in_check(BLACK if g.turn == WHITE else WHITE): g.unmake_move(); continue
        score = -quiesce(g, -beta, -alpha, qdepth + 1)
        g.unmake_move()
        if score >= beta: return beta
        if score > alpha: alpha = score
    return alpha

def negamax(g, depth, alpha, beta, ply):
    if depth <= 0: return quiesce(g, alpha, beta, 0)
    moves = g.legal_moves()
    if not moves:
        if g.in_check(g.turn): return -MATE + ply
        return 0
    moves.sort(key=lambda m: move_score(g, m), reverse=True)
    for m in moves:
        g.make_move(m)
        score = -negamax(g, depth - 1, -beta, -alpha, ply + 1)
        g.unmake_move()
        if score >= beta: return beta
        if score > alpha: alpha = score
    return alpha

def find_best_move(g, depth):
    moves = g.legal_moves()
    if not moves: return None
    moves.sort(key=lambda m: move_score(g, m), reverse=True)
    best = moves[0]
    best_score = -MATE * 2
    alpha, beta = -MATE * 2, MATE * 2
    for m in moves:
        g.make_move(m)
        score = -negamax(g, depth - 1, -beta, -alpha, 1)
        g.unmake_move()
        if score > best_score:
            best_score = score
            best = m
            if score > alpha: alpha = score
    return best

# ============================================================
# GUI（Canvas 向量棋子版）
# ============================================================
class ChessGUI:
    LIGHT = '#F0D9B5'
    DARK  = '#B58863'
    SEL   = '#85C1E9'
    MOVE  = '#A9DFBF'
    CAP   = '#F1948A'

    def __init__(self, root):
        self.root = root
        root.title("Python 國際象棋")
        root.resizable(False, False)

        # 根據屏幕寬度動態計算格仔大細
        screen_w = root.winfo_screenwidth()
        self.cell = int(max(130
        , min((screen_w - 24) // 8, 62)))

        self.status = tk.Label(root, text="你嘅回合（白方）",
                               font=('Arial', max(11, self.cell // 4)), pady=4)
        self.status.pack()

        self.board_frame = tk.Frame(root, bg='#3A3A3A')
        self.board_frame.pack(padx=4, pady=4)

        self.canvases = [[None] * 8 for _ in range(8)]
        self.selected = None
        self.legal_for_selected = []
        self.thinking = False
        self.game_over = False
        self.game = Board()

        for r in range(8):
            for c in range(8):
                cv = tk.Canvas(self.board_frame, width=self.cell, height=self.cell,
                               highlightthickness=0, bd=0, bg=self.LIGHT)
                cv.grid(row=r, column=c, padx=0, pady=0)
                cv.bind('<Button-1>', lambda e, r=r, c=c: self.on_click(r, c))
                self.canvases[r][c] = cv

        tk.Button(root, text="重新開始", font=('Arial', 12),
                  command=self.restart).pack(pady=8)
        self.draw()

    # ---------- 繪圖 ----------
    def draw(self):
        g = self.game
        s = self.cell

        for r in range(8):
            for c in range(8):
                cv = self.canvases[r][c]
                cv.delete('all')

                bg = self.LIGHT if (r + c) % 2 == 0 else self.DARK

                if self.selected == (r, c):
                    bg = self.SEL
                else:
                    for m in self.legal_for_selected:
                        if m[2] == r and m[3] == c:
                            bg = self.MOVE if g.board[r * 8 + c] is None else self.CAP
                            break

                cv.create_rectangle(0, 0, s, s, fill=bg, outline='')

                p = g.board[r * 8 + c]
                if p:
                    draw_piece(cv, s, p.upper(), p.isupper())

    # ---------- 互動 ----------
    def on_click(self, r, c):
        if self.thinking or self.game_over: return
        if self.game.turn != WHITE: return

        if self.selected:
            targets = [m for m in self.legal_for_selected if m[2] == r and m[3] == c]
            if targets:
                self.play_human(targets)
                return

        p = self.game.board[r * 8 + c]
        if p and p.isupper():
            self.selected = (r, c)
            self.legal_for_selected = [m for m in self.game.legal_moves()
                                       if m[0] == r and m[1] == c]
        else:
            self.selected = None
            self.legal_for_selected = []
        self.draw()

    def play_human(self, targets):
        if len(targets) > 1:
            promo = self.ask_promotion()
            if promo is None: return
            move = next(m for m in targets if m[4] == promo)
        else:
            move = targets[0]

        self.game.make_move(move)
        self.selected = None
        self.legal_for_selected = []
        self.draw()

        if self.check_end(): return

        self.status.config(text="電腦思考中…")
        self.thinking = True
        self.root.after(50, self.ai_move)

    def ask_promotion(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("升變")
        dlg.resizable(False, False)
        dlg.grab_set()
        result = {'v': None}
        tk.Label(dlg, text="揀升變棋子：", font=('Arial', 11)).pack(padx=12, pady=6)

        frame = tk.Frame(dlg)
        frame.pack(padx=12, pady=6)

        symbols = {'Q': '♛', 'R': '♜', 'B': '♝', 'N': '♞'}
        for ch in ('Q', 'R', 'B', 'N'):
            def cmd(x=ch):
                result['v'] = x
                dlg.destroy()
            tk.Button(frame, text=symbols[ch], font=('Arial', 20, 'bold'),
                      width=3, command=cmd).pack(side='left', padx=4)

        self.root.wait_window(dlg)
        return result['v']

    def ai_move(self):
        move = find_best_move(self.game, DEPTH)
        self.thinking = False
        if move is None:
            self.check_end(); return
        self.game.make_move(move)
        self.draw()
        if self.check_end(): return
        self.status.config(text="你嘅回合（白方）")

    def check_end(self):
        moves = self.game.legal_moves()
        if not moves:
            self.game_over = True
            if self.game.in_check(self.game.turn):
                winner = "黑方（電腦）" if self.game.turn == WHITE else "白方（你）"
                msg = f"將死！{winner}勝出！"
            else:
                msg = "和棋 — 逼和（無棋可走）"
            self.status.config(text=msg)
            messagebox.showinfo("遊戲結束", msg)
            return True
        if self.game.halfmove >= 100:
            self.game_over = True
            self.status.config(text="和棋 — 50 回合規則")
            messagebox.showinfo("遊戲結束", "和棋 — 50 回合規則")
            return True
        return False

    def restart(self):
        self.game = Board()
        self.selected = None
        self.legal_for_selected = []
        self.thinking = False
        self.game_over = False
        self.status.config(text="你嘅回合（白方）")
        self.draw()

# ============================================================
# 主程式
# ============================================================
if __name__ == '__main__':
    root = tk.Tk()
    app = ChessGUI(root)
    root.mainloop()