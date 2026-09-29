import py5
import random
import os

GRID_COLS = 10
GRID_ROWS = 8
CELL_SIZE = 40
TILE_SIZE = 34 # ขนาดเล็กลงนิดนึงเพื่อเว้นช่องว่าง (Gap)
OFFSET_X = 10  # ขยับกริดออกจากขอบซ้าย
OFFSET_Y = 70  # ขยับกริดลงมาจากขอบบน

# ชุดสี Modern UI
PALETTE = {
    "RED": (255, 75, 75),      # Coral Red
    "GREEN": (0, 230, 118),    # Neon Mint
    "BLUE": (41, 121, 255),    # Azure Blue
    "YELLOW": (255, 234, 0)    # Electric Yellow
}
COLORS = list(PALETTE.keys())
BG_COLOR = (30, 30, 36)        # สีพื้นหลัง Dark Slate
UI_TEXT_COLOR = (200, 204, 212)

# ตัวแปรระบบ
board = []
target_final_color = ""
moves_left = 12
game_state = "PLAYING"
selected_color = None
save_status_msg = ""
save_status_timer = 0 # เพิ่มตัวจับเวลาให้ข้อความหายไปเอง

def setup():
    py5.size(420, 480) # ขยายหน้าจอให้พอดีกับ Layout ใหม่
    init_game()

def init_game():
    global board, target_final_color, moves_left, game_state, selected_color, save_status_msg
    board = []
    
    for y in range(GRID_ROWS):
        row = [random.choice(COLORS) for _ in range(GRID_COLS)]
        board.append(row)
        
    target_final_color = random.choice(COLORS)
    moves_left = 12
    game_state = "PLAYING"
    selected_color = None
    save_status_msg = ""

def save_game():
    global save_status_msg, save_status_timer
    try:
        with open("savegame.txt", "w") as f:
            f.write(target_final_color + "\n")
            f.write(str(moves_left) + "\n")
            f.write(str(selected_color) + "\n")
            for y in range(GRID_ROWS):
                f.write(",".join(board[y]) + "\n")
        save_status_msg = "SAVED!"
        save_status_timer = 60 # แสดงข้อความ 60 เฟรม
    except:
        save_status_msg = "SAVE ERROR!"
        save_status_timer = 60

def load_game():
    global board, target_final_color, moves_left, selected_color, game_state, save_status_msg, save_status_timer
    if not os.path.exists("savegame.txt"):
        save_status_msg = "NO SAVE!"
        save_status_timer = 60
        return
        
    try:
        with open("savegame.txt", "r") as f:
            lines = f.readlines()
        
        target_final_color = lines[0].strip()
        moves_left = int(lines[1].strip())
        
        sel = lines[2].strip()
        selected_color = None if sel == "None" else sel
        
        board = []
        for y in range(GRID_ROWS):
            board.append(lines[3 + y].strip().split(","))
            
        game_state = "PLAYING"
        save_status_msg = "LOADED!"
        save_status_timer = 60
    except:
        save_status_msg = "LOAD ERROR!"
        save_status_timer = 60

def spread(start_x, start_y, target_colour, new_colour):
    if target_colour == new_colour: return
    
    stack = [(start_x, start_y)]
    while stack:
        x, y = stack.pop()
        if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
            if board[y][x] == target_colour:
                board[y][x] = new_colour
                stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

def check_win():
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            if board[y][x] != target_final_color:
                return False 
    return True

def change_colour(start_x, start_y, new_colour):
    global moves_left, game_state, save_status_msg
    if game_state != "PLAYING": return
    
    save_status_msg = ""
    old_colour = board[start_y][start_x]
    if old_colour != new_colour:
        spread(start_x, start_y, old_colour, new_colour)
        moves_left -= 1
        
        if check_win():
            game_state = "WON"
        elif moves_left <= 0:
            game_state = "LOST"

def set_color_fill(colour, alpha=255):
    r, g, b = PALETTE[colour]
    py5.fill(r, g, b, alpha)

def draw_hud():
    global save_status_timer
    
    # วาดแถบด้านบน
    py5.fill(45, 45, 53)
    py5.no_stroke()
    py5.rect(0, 0, 420, 55)
    
    py5.fill(*UI_TEXT_COLOR)
    py5.text_size(16)
    py5.text_align(py5.LEFT, py5.CENTER)
    py5.text_font(py5.create_font("Arial Bold", 16))
    py5.text(f"MOVES: {moves_left}", 15, 27)
    
    # Target
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.text("TARGET:", 170, 27)
    set_color_fill(target_final_color)
    py5.rect(215, 12, 30, 30, 8) # เป้าหมายขอบมน
    
    # Save/Load info
    py5.fill(*UI_TEXT_COLOR)
    py5.text_size(11)
    py5.text_align(py5.RIGHT, py5.CENTER)
    py5.text("[S] SAVE   [L] LOAD", 405, 18)
    
    # Status Message
    if save_status_timer > 0:
        py5.fill(0, 230, 118)
        py5.text(save_status_msg, 405, 38)
        save_status_timer -= 1

def key_pressed():
    if py5.key in ['s', 'S']: save_game()
    elif py5.key in ['l', 'L']: load_game()

def mouse_pressed():
    global selected_color, save_status_msg
    if game_state == "PLAYING":
        clicked_button = False
        
        # เช็คการคลิกปุ่มเลือกสีด้านล่าง
        for i, color in enumerate(COLORS):
            cx = 70 + (i * 93)
            cy = 430
            if abs(py5.mouse_x - cx) <= 25 and abs(py5.mouse_y - cy) <= 25:
                selected_color = color
                clicked_button = True
                save_status_msg = ""
                break
                
        # เช็คการคลิกบนตาราง (ถ้าเลือกสีแล้ว)
        if not clicked_button and selected_color is not None:
            if OFFSET_X <= py5.mouse_x < OFFSET_X + (GRID_COLS * CELL_SIZE) and \
               OFFSET_Y <= py5.mouse_y < OFFSET_Y + (GRID_ROWS * CELL_SIZE):
                grid_x = int((py5.mouse_x - OFFSET_X) / CELL_SIZE)
                grid_y = int((py5.mouse_y - OFFSET_Y) / CELL_SIZE)
                change_colour(grid_x, grid_y, selected_color)
    else:
        init_game()

def draw():
    py5.background(*BG_COLOR)
    
    # 1. วาดตารางเกม
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            px = OFFSET_X + (x * CELL_SIZE)
            py_coord = OFFSET_Y + (y * CELL_SIZE)
            
            # วาดเงา (Shadow)
            py5.fill(15, 15, 18, 150)
            py5.no_stroke()
            py5.rect(px + 2, py_coord + 3, TILE_SIZE, TILE_SIZE, 6)
            
            # วาดบล็อกสี (ขอบมน 6px)
            set_color_fill(board[y][x])
            py5.rect(px, py_coord, TILE_SIZE, TILE_SIZE, 6)
            
    # 2. วาด HUD ด้านบน
    draw_hud()
    
    # 3. วาดปุ่มเลือกสีด้านล่าง
    for i, color in enumerate(COLORS):
        cx = 70 + (i * 93)
        cy = 430
        
        # ถ้าสีนี้ถูกเลือก ให้วาดวงแหวนสว่างด้านนอก
        if color == selected_color:
            set_color_fill(color, 80) # โปร่งแสง
            py5.ellipse(cx, cy, 60, 60)
            py5.stroke(255)
            py5.stroke_weight(3)
        else:
            py5.no_stroke()
            
        set_color_fill(color)
        py5.ellipse(cx, cy, 45, 45)
        
    # 4. วาดหน้าจอจบเกม (Overlay)
    if game_state in ["WON", "LOST"]:
        # แผ่นฟิล์มดำโปร่งแสง
        py5.fill(10, 10, 15, 210)
        py5.no_stroke()
        py5.rect(0, 0, py5.width, py5.height)
        
        py5.text_align(py5.CENTER, py5.CENTER)
        py5.text_font(py5.create_font("Arial Bold", 48))
        
        if game_state == "WON":
            py5.fill(0, 255, 150) # Neon Green
            py5.text("YOU WIN!", py5.width/2, py5.height/2 - 20)
        else:
            py5.fill(255, 75, 75) # Coral Red
            py5.text("GAME OVER", py5.width/2, py5.height/2 - 20)
            
        py5.fill(*UI_TEXT_COLOR)
        py5.text_size(16)
        py5.text("Click anywhere to restart", py5.width/2, py5.height/2 + 30)

py5.run_sketch()