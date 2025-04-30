import streamlit as st
import numpy as np
import random

# Constants
ROWS, COLUMNS = 20, 10
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
]
COLORS = ['🟥', '🟩', '🟦', '🟨', '🟧', '🟪', '🟫']
EMPTY = '⬛'

# Initialize session state
if "grid" not in st.session_state:
    st.session_state.grid = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
    st.session_state.shape = random.choice(SHAPES)
    st.session_state.color = random.choice(COLORS)
    st.session_state.x = COLUMNS // 2 - len(st.session_state.shape[0]) // 2
    st.session_state.y = 0

def draw_grid():
    grid_copy = [row.copy() for row in st.session_state.grid]
    shape = st.session_state.shape
    color = st.session_state.color
    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c]:
                y = st.session_state.y + r
                x = st.session_state.x + c
                if 0 <= y < ROWS and 0 <= x < COLUMNS:
                    grid_copy[y][x] = color
    for row in grid_copy:
        st.write(''.join(row))

def can_move(dx, dy):
    shape = st.session_state.shape
    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c]:
                new_x = st.session_state.x + c + dx
                new_y = st.session_state.y + r + dy
                if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                    return False
                if new_y >= 0 and st.session_state.grid[new_y][new_x] != EMPTY:
                    return False
    return True

def lock_piece():
    shape = st.session_state.shape
    color = st.session_state.color
    for r in range(len(shape)):
        for c in range(len(shape[0])):
            if shape[r][c]:
                x = st.session_state.x + c
                y = st.session_state.y + r
                if 0 <= y < ROWS and 0 <= x < COLUMNS:
                    st.session_state.grid[y][x] = color
    spawn_new_piece()

def spawn_new_piece():
    st.session_state.shape = random.choice(SHAPES)
    st.session_state.color = random.choice(COLORS)
    st.session_state.x = COLUMNS // 2 - len(st.session_state.shape[0]) // 2
    st.session_state.y = 0
    if not can_move(0, 0):
        st.error("Game Over!")
        st.session_state.grid = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]

def rotate():
    shape = st.session_state.shape
    rotated = [list(row) for row in zip(*shape[::-1])]
    original_shape = st.session_state.shape
    st.session_state.shape = rotated
    if not can_move(0, 0):
        st.session_state.shape = original_shape

# Draw controls
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⬅️"):
        if can_move(-1, 0):
            st.session_state.x -= 1
with col2:
    if st.button("⬇️"):
        if can_move(0, 1):
            st.session_state.y += 1
        else:
            lock_piece()
with col3:
    if st.button("➡️"):
        if can_move(1, 0):
            st.session_state.x += 1
with col4:
    if st.button("🔄 Rotate"):
        rotate()

draw_grid()

