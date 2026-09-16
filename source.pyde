# Color Flood Puzzle ( Processing Python Mode )

GRID_SIZE = 6       # ขนาดกระดาน 6x6
CELL_SIZE = 80      # ขนาดของแต่ละช่อง (พิกเซล)
MAX_MOVES = 10      # จำนวนครั้งที่อนุญาตให้กด

# ชุดสีที่ใช้ในเกม (RGB)
COLORS = [
    (230, 80, 80),   # สีแดง
    (80, 200, 80),   # สีเขียว
    (80, 120, 230),  # สีน้ำเงิน
    (240, 200, 60),  # สีเหลือง
]

grid = []
current_color = 0
moves_left = MAX_MOVES
game_over = False
game_won = False

def setup():
    size(GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE + 80)
    reset_game()

def reset_game():
    global grid, current_color, moves_left, game_over, game_won
    moves_left = MAX_MOVES
    game_over = False
    game_won = False
    
    # สุ่มสีลงบนกระดาน
    grid = []
    for r in range(GRID_SIZE):
        row = []
        for c in range(GRID_SIZE):
            row.append(int(random(len(COLORS))))
        grid.append(row)
    
    current_color = grid[0][0]

def draw():
    background(30)
    
    # 1. วาดกระดาน
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            col_idx = grid[r][c]
            r_val, g_val, b_val = COLORS[col_idx]
            fill(r_val, g_val, b_val)
            stroke(40)
            strokeWeight(3)
            rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE, 8)
            
    # 2. วาดพาเลตปุ่มกดเลือกสีด้านล่าง
    palette_y = GRID_SIZE * CELL_SIZE + 20
    btn_w = (width - 40) / len(COLORS)
    for i in range(len(COLORS)):
        r_val, g_val, b_val = COLORS[i]
        fill(r_val, g_val, b_val)
        if i == current_color:
            stroke(255)
            strokeWeight(4)
        else:
            noStroke()
        rect(20 + i * btn_w, palette_y, btn_w - 10, 40, 8)

    # 3. แสดงสถานะเกม
    fill(255)
    textSize(18)
    textAlign(LEFT, CENTER)
    text("Moves: " + str(moves_left) + "/" + str(MAX_MOVES), 20, palette_y + 50)
    
    if game_won:
        textAlign(RIGHT, CENTER)
        fill(100, 255, 100)
        text("PUZZLE SOLVED!", width - 20, palette_y + 50)
    elif game_over:
        textAlign(RIGHT, CENTER)
        fill(255, 100, 100)
        text("GAME OVER (Click to Restart)", width - 20, palette_y + 50)

def mousePressed():
    global moves_left, game_over, game_won
    
    if game_over or game_won:
        reset_game()
        return

    palette_y = GRID_SIZE * CELL_SIZE + 20
    btn_w = (width - 40) / len(COLORS)

    # เช็คว่าคลิกปุ่มสีด้านล่างหรือไม่
    if palette_y <= mouseY <= palette_y + 40:
        for i in range(len(COLORS)):
            btn_x = 20 + i * btn_w
            if btn_x <= mouseX <= btn_x + btn_w - 10:
                if i != current_color:
                    apply_color_change(i)
                    break

def apply_color_change(new_color_idx):
    global current_color, moves_left, game_over, game_won
    
    target_color = grid[0][0]
    flood_fill(0, 0, target_color, new_color_idx)
    current_color = new_color_idx
    moves_left -= 1
    
    # ตรวจสอบว่าชนะหรือยัง
    if check_win():
        game_won = True
    elif moves_left <= 0:
        game_over = True

def flood_fill(r, c, target_color, new_color):
    """อัลกอริทึม Flood Fill เปลี่ยนสีพื้นที่ที่เชื่อมต่อกัน"""
    if target_color == new_color:
        return
    if r < 0 or r >= GRID_SIZE or c < 0 or c >= GRID_SIZE:
        return
    if grid[r][c] != target_color:
        return

    grid[r][c] = new_color

    # ขยายไปยัง 4 ทิศทาง (บน, ล่าง, ซ้าย, ขวา)
    flood_fill(r + 1, c, target_color, new_color)
    flood_fill(r - 1, c, target_color, new_color)
    flood_fill(r, c + 1, target_color, new_color)
    flood_fill(r, c - 1, target_color, new_color)

def check_win():
    first_color = grid[0][0]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] != first_color:
                return False
    return True
