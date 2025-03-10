import chess
import random

def main():
    board = chess.Board()  # 建立初始棋局
    print("開始國際象棋遊戲！你是白棋。")
    print("請用UCI格式輸入走法，例如 e2e4")
    print("--------------------------------------------------")
    
    while not board.is_game_over():
        # 顯示棋盤
        print(board)
        print()
        
        if board.turn == chess.WHITE:
            # 玩家回合
            move_input = input("你的走法: ").strip()
            try:
                move = chess.Move.from_uci(move_input)
            except ValueError:
                print("走法格式錯誤，請使用UCI格式（例如 e2e4）")
                continue
            if move in board.legal_moves:
                board.push(move)
            else:
                print("非法走法，請重新輸入！")
                continue
        else:
            # AI回合：隨機走法
            valid_moves = list(board.legal_moves)
            move = random.choice(valid_moves)
            board.push(move)
            print("AI走了:", board.san(move))
        
        print("--------------------------------------------------")
    
    # 遊戲結束
    print(board)
    print("遊戲結束，結果:", board.result())

if __name__ == "__main__":
    main()
#