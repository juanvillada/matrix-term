#!/usr/bin/env python3
import curses
import random
import time
from curses import wrapper

def draw_peace_letters(stdscr, start_y, start_x, height, width):
    # Define the word to display
    word = "PEACE"

    # Character width and spacing
    char_width = 6
    char_spacing = 2
    total_width = (char_width + char_spacing) * len(word)

    # Calculate starting position to center the word
    pos_x = start_x + (width - total_width) // 2
    pos_y = start_y + height // 3

    # Set of positions where letters appear
    positions = set()

    # Draw each letter and track positions
    for i, letter in enumerate(word):
        x = pos_x + i * (char_width + char_spacing)
        try:
            stdscr.addstr(pos_y, x, letter, curses.color_pair(1) | curses.A_BOLD)

            # Create a larger zone around each letter that rain should avoid
            for y_offset in range(-2, 3):
                for x_offset in range(-1, char_width + 1):
                    positions.add((pos_y + y_offset, x + x_offset))
        except curses.error:
            pass

    return positions

def main(stdscr):
    # Set up colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Bright green
    curses.init_pair(2, 8, curses.COLOR_BLACK)  # Dim green (8 is a dim white)
    curses.curs_set(0)  # Hide cursor

    # Get screen dimensions
    height, width = stdscr.getmaxyx()

    # Set target density (percentage of columns that should be active)
    target_density = 0.75
    min_columns = int(width * target_density)

    # Create a list of column positions and their current y-position
    columns = []
    for i in range(width):
        if random.randint(0, 100) > 30:
            columns.append([i, -random.randint(0, height)])

    # Matrix characters
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+-=[]{}|;':\",./<>?\\~`"

    # PEACE effect variables
    show_peace = False
    peace_positions = set()
    peace_timer = 0
    peace_duration = 100  # How long to show PEACE (in frames)
    peace_interval = random.randint(300, 600)  # Random interval between showings (about 30-60 seconds)

    try:
        while True:
            # Clear the screen
            stdscr.clear()

            # Update peace effect
            peace_timer += 1
            if peace_timer >= peace_interval and not show_peace:
                show_peace = True
                peace_timer = 0
                peace_interval = random.randint(300, 600)  # Set next interval
                peace_positions = draw_peace_letters(stdscr, 0, 0, height, width)
            elif show_peace:
                peace_positions = draw_peace_letters(stdscr, 0, 0, height, width)
                peace_duration -= 1
                if peace_duration <= 0:
                    show_peace = False
                    peace_duration = 100
                    peace_positions = set()

            # Draw each column
            new_columns = []
            for col in columns:
                x, y = col

                # Skip if this position is part of the PEACE text
                if show_peace and (y, x) in peace_positions:
                    new_columns.append(col)  # Keep the column but don't draw/advance it
                    continue

                # Only render if on screen
                if 0 <= y < height and 0 <= x < width:
                    # Head character (bright green)
                    try:
                        stdscr.addch(y, x, random.choice(chars), curses.color_pair(1) | curses.A_BOLD)
                    except curses.error:
                        pass

                    # Trail characters (darker green)
                    for i in range(1, min(10, y + 1)):
                        # Skip trail character if position is part of PEACE text
                        if y - i >= 0 and not (show_peace and (y - i, x) in peace_positions):
                            try:
                                stdscr.addch(y - i, x, random.choice(chars), curses.color_pair(2))
                            except curses.error:
                                pass

                # Update position for next frame (but not if we're part of PEACE text)
                if not (show_peace and (y + 1, x) in peace_positions):
                    col[1] += 1

                # Keep the column if it's still on screen or create a new one
                if y < height:
                    new_columns.append(col)
                else:  # Always create a new column when one goes off-screen
                    # But avoid positions that are part of PEACE text
                    new_x = random.randint(0, width-1)
                    if not (show_peace and (0, new_x) in peace_positions):
                        new_columns.append([new_x, 0])
                    else:
                        new_columns.append([new_x, -5])  # Start above the screen to flow down later

            # Ensure we maintain minimum column density
            if len(new_columns) < min_columns:
                # Add columns where needed to reach minimum density
                needed = min_columns - len(new_columns)
                for _ in range(needed):
                    # Find an empty column position
                    occupied_x = [col[0] for col in new_columns]
                    available_x = [x for x in range(width) if x not in occupied_x]

                    if available_x:
                        new_x = random.choice(available_x)
                    else:
                        new_x = random.randint(0, width-1)

                    # Avoid positions that are part of PEACE text
                    if not (show_peace and any((y, new_x) in peace_positions for y in range(5))):
                        new_columns.append([new_x, -random.randint(0, 5)])

            # Randomly add extra columns for dynamic appearance
            elif random.randint(0, 100) > 90 and len(new_columns) < width:
                new_x = random.randint(0, width-1)
                if not (show_peace and any((y, new_x) in peace_positions for y in range(5))):
                    new_columns.append([new_x, -random.randint(0, 5)])

            columns = new_columns

            # Refresh the screen
            stdscr.refresh()

            # Animation speed
            time.sleep(0.08)

    except KeyboardInterrupt:
        return

# Add a wrapper function for entry_point
def main_wrapper():
    wrapper(main)

if __name__ == "__main__":
    wrapper(main)
