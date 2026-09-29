import java.io.*;
import java.util.Stack;
import java.util.Random;

final int GRID_COLS = 10;
final int GRID_ROWS = 8;
final int BLOCK_SIZE = 40;
final String[] COLORS = {"RED", "GREEN", "BLUE", "YELLOW"};

// ตัวแปรระบบ
String[][] board = new String[GRID_ROWS][GRID_COLS];
String targetFinalColor = "";
int movesLeft = 12;
String gameState = "PLAYING";
String selectedColor = null;
String saveStatusMsg = "";

Random rand = new Random();

void setup() {
  size(400, 440);
  initGame();
}

// --- 1. ฟังก์ชันสร้างกระดาน ---
void initGame() {
  int y = 0;
  while (y < GRID_ROWS) {
    int x = 0;
    while (x < GRID_COLS) {
      board[y][x] = COLORS[rand.nextInt(COLORS.length)];
      x++;
    }
    y++;
  }
  
  targetFinalColor = COLORS[rand.nextInt(COLORS.length)];
  movesLeft = 12;
  gameState = "PLAYING";
  selectedColor = null;
  saveStatusMsg = "";
}

// --- ระบบเซฟ/โหลดเกม ---
void saveGame() {
  try {
    // รวมข้อมูลทั้งหมดเป็น String Array เพื่อบันทึก
    String[] lines = new String[3 + GRID_ROWS];
    lines[0] = targetFinalColor;
    lines[1] = String.valueOf(movesLeft);
    lines[2] = (selectedColor == null) ? "None" : selectedColor;
    
    int y = 0;
    while (y < GRID_ROWS) {
      String line = "";
      int x = 0;
      while (x < GRID_COLS) {
        line += board[y][x] + (x < GRID_COLS - 1 ? "," : "");
        x++;
      }
      lines[3 + y] = line;
      y++;
    }
    
    // บันทึกลงไฟล์ savegame.txt
    saveStrings("savegame.txt", lines);
    saveStatusMsg = "SAVED!";
  } catch (Exception e) {
    saveStatusMsg = "SAVE ERROR!";
  }
}

void loadGame() {
  try {
    // อ่านข้อมูลจาก savegame.txt
    String[] lines = loadStrings("savegame.txt");
    
    if (lines == null || lines.length < 3 + GRID_ROWS) {
      saveStatusMsg = "NO SAVE FILE!";
      return;
    }
    
    targetFinalColor = lines[0].trim();
    movesLeft = Integer.parseInt(lines[1].trim());
    
    String sel = lines[2].trim();
    selectedColor = sel.equals("None") ? null : sel;
    
    int y = 0;
    while (y < GRID_ROWS) {
      String[] rowColors = lines[3 + y].trim().split(",");
      int x = 0;
      while (x < GRID_COLS) {
        board[y][x] = rowColors[x];
        x++;
      }
      y++;
    }
    
    gameState = "PLAYING";
    saveStatusMsg = "LOADED!";
  } catch (Exception e) {
    saveStatusMsg = "LOAD ERROR!";
  }
}

// --- 2. ฟังก์ชันระบายสี ---
void spread(int startX, int startY, String targetColor, String newColor) {
  if (targetColor.equals(newColor)) return;
  
  Stack<int[]> stack = new Stack<int[]>();
  stack.push(new int[]{startX, startY});
  
  while (!stack.isEmpty()) {
    int[] pos = stack.pop();
    int x = pos[0];
    int y = pos[1];
    
    if (x >= 0 && x < GRID_COLS && y >= 0 && y < GRID_ROWS) {
      if (board[y][x].equals(targetColor)) {
        board[y][x] = newColor;
        stack.push(new int[]{x + 1, y});
        stack.push(new int[]{x - 1, y});
        stack.push(new int[]{x, y + 1});
        stack.push(new int[]{x, y - 1});
      }
    }
  }
}

// --- 3. ฟังก์ชันเช็คชนะ ---
boolean checkWin() {
  int y = 0;
  while (y < GRID_ROWS) {
    int x = 0;
    while (x < GRID_COLS) {
      if (!board[y][x].equals(targetFinalColor)) {
        return false;
      }
      x++;
    }
    y++;
  }
  return true;
}

void changeColour(int startX, int startY, String newColor) {
  if (!gameState.equals("PLAYING")) return;
  
  saveStatusMsg = "";
  String oldColor = board[startY][startX];
  if (!oldColor.equals(newColor)) {
    spread(startX, startY, oldColor, newColor);
    movesLeft--;
    
    if (checkWin()) {
      gameState = "WON";
    } else if (movesLeft <= 0) {
      gameState = "LOST";
    }
  }
}

// --- 4. ฟังก์ชันวาดกราฟิก ---
void getColorFill(String colour) {
  if (colour.equals("RED")) fill(255, 80, 80);
  else if (colour.equals("GREEN")) fill(80, 255, 80);
  else if (colour.equals("BLUE")) fill(80, 80, 255);
  else if (colour.equals("YELLOW")) fill(255, 255, 80);
}

void drawHUD() {
  fill(0);
  textSize(14);
  text("Moves Left: " + movesLeft, 10, 345);
  text("Target:", 135, 345);
  
  getColorFill(targetFinalColor);
  stroke(0);
  ellipse(195, 340, 20, 20);
  
  fill(80);
  textSize(12);
  text("[S] Save  [L] Load", 225, 345);
  
  fill(0, 150, 0);
  text(saveStatusMsg, 335, 345);
  
  if (gameState.equals("WON")) {
    fill(0, 200, 0);
    textSize(40);
    text("YOU WIN!", 110, 160);
  } else if (gameState.equals("LOST")) {
    fill(200, 0, 0);
    textSize(40);
    text("GAME OVER", 90, 160);
  }
}

// --- 5. การตอบสนองผู้ใช้ ---
void keyPressed() {
  if (key == 's' || key == 'S') {
    saveGame();
  } else if (key == 'l' || key == 'L') {
    loadGame();
  }
}

void mousePressed() {
  if (gameState.equals("PLAYING")) {
    boolean clickedButton = false;
    
    int i = 0;
    while (i < COLORS.length) {
      int cx = 50 + (i * 100);
      int cy = 400;
      if (abs(mouseX - cx) <= 25 && abs(mouseY - cy) <= 25) {
        selectedColor = COLORS[i];
        clickedButton = true;
        saveStatusMsg = "";
        break;
      }
      i++;
    }
    
    if (!clickedButton && selectedColor != null) {
      if (mouseX >= 0 && mouseX < 400 && mouseY >= 0 && mouseY < 320) {
        int gridX = mouseX / BLOCK_SIZE;
        int gridY = mouseY / BLOCK_SIZE;
        changeColour(gridX, gridY, selectedColor);
      }
    }
  } else {
    initGame();
  }
}

// --- 6. วงจรโปรแกรมหลัก ---
void draw() {
  background(230);
  
  // 1. วาดกระดาน (while loop)
  int y = 0;
  while (y < GRID_ROWS) {
    int x = 0;
    while (x < GRID_COLS) {
      getColorFill(board[y][x]);
      stroke(255);
      rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
      x++;
    }
    y++;
  }
  
  // 2. วาดปุ่มด้านล่าง (while loop)
  int i = 0;
  while (i < COLORS.length) {
    getColorFill(COLORS[i]);
    if (COLORS[i].equals(selectedColor)) {
      stroke(255);
      strokeWeight(3);
    } else {
      stroke(0);
      strokeWeight(1);
    }
    int cx = 50 + (i * 100);
    int cy = 400;
    ellipse(cx, cy, 50, 50);
    i++;
  }
  
  strokeWeight(1);
  drawHUD();
}
