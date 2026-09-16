def draw_box(x, y, size, col_index):
    r, g, b = COLORS[col_index]
    fill(r, g, b)
    stroke(40)
    strokeWeight(2)
    rect(x, y, size, size, 8)  # วาดสี่เหลี่ยมขอบมน

def change_color(new_color):
    global current_color
    target_color = grid[0][0]
    
    # ถ้ากดเลือกสีเดิม ไม่ต้องทำงาน
    if target_color == new_color:
        return
        
    current_color = new_color
    check_spread(0, 0, target_color, new_color)

def check_spread(x, y, target_color, new_color):
    if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
        return
        
    if grid[y][x] != target_color:
        return

    grid[y][x] = new_color
