

import time
import webbrowser
import urllib.parse
import sys
import os

import pyautogui
import pyperclip

# ---------------- CONFIG ----------------
QUERY = "Coolie movie total collection"
SEARCH_URL = "https://www.google.com/search?q=" + urllib.parse.quote_plus(QUERY)
OUTPUT_TXT = "coolie.txt"

# Tuning (increase if your machine/browser is slow)
WAIT_AFTER_OPEN = 6         # seconds to wait after opening search results
WAIT_AFTER_CLICK = 6        # seconds to wait after clicking the first result (page load)
TAB_FALLBACK_COUNT = 10     # how many tab presses to try (if positional click fails)
# Positional click uses these relative coordinates (fractions of screen width/height)
FIRST_RESULT_REL_X = 0.50   # center horizontally
FIRST_RESULT_REL_Y = 0.32   # near top third of the page (adjust if needed)

# ----------------------------------------

# Auto-detect command key (mac) vs ctrl (win/linux)
IS_MAC = sys.platform == "darwin"
MOD_KEY = "command" if IS_MAC else "ctrl"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.25

def open_search_page():
    print(f"Opening search page for: {QUERY}")
    webbrowser.open(SEARCH_URL)
    time.sleep(WAIT_AFTER_OPEN)

def focus_browser_window():
    # Click near center to make sure browser has focus
    w, h = pyautogui.size()
    pyautogui.click(int(w/2), int(h/2))
    time.sleep(0.4)

def try_click_first_result_by_position():
    w, h = pyautogui.size()
    x = int(w * FIRST_RESULT_REL_X)
    y = int(h * FIRST_RESULT_REL_Y)
    print(f"Trying positional click at ({x},{y}) - relative ({FIRST_RESULT_REL_X},{FIRST_RESULT_REL_Y})")
    pyautogui.moveTo(x, y, duration=0.35)
    pyautogui.click()
    time.sleep(0.4)

def try_click_first_result_by_tab():
    print(f"Attempting tab-navigation fallback ({TAB_FALLBACK_COUNT} tabs then Enter).")
    # Sometimes cookie banners or search-box focus can change how many tabs are required.
    for i in range(TAB_FALLBACK_COUNT):
        pyautogui.press('tab')
        time.sleep(0.12)
    pyautogui.press('enter')
    time.sleep(0.4)

def copy_visible_page_text():
    print("Selecting all and copying page content to clipboard...")
    pyautogui.hotkey(MOD_KEY, 'a')
    time.sleep(0.15)
    pyautogui.hotkey(MOD_KEY, 'c')
    time.sleep(0.6)
    text = pyperclip.paste()
    return text

def save_text_to_file(text):
    if not text:
        print("Warning: clipboard empty or copy failed. Saving placeholder text.")
        text = "(No text captured — clipboard empty.)"
    path = os.path.join(os.getcwd(), OUTPUT_TXT)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved captured text to: {path}")

def main():
    open_search_page()
    focus_browser_window()

    # Try positional click first, then fallback to tab-navigation
    try:
        try_click_first_result_by_position()
        print(f"Waiting {WAIT_AFTER_CLICK}s for the target page to load...")
        time.sleep(WAIT_AFTER_CLICK)
    except Exception as e:
        print("Positional click raised an exception:", e)

    # After positional attempt, check clipboard after selecting the page content.
    # If the positional click didn't open the page, try the tab fallback and try again.
    text = ""
    try:
        text = copy_visible_page_text()
        if not text.strip():
            # seems we didn't land on an article page or copy failed; try tab fallback
            print("Initial copy returned empty. Trying tab-navigation fallback to open first result...")
            try_click_first_result_by_tab()
            print(f"Waiting {WAIT_AFTER_CLICK}s for the target page to load (after fallback)...")
            time.sleep(WAIT_AFTER_CLICK)
            text = copy_visible_page_text()
    except Exception as e:
        print("Error during copy attempt:", e)
        # try fallback then copy
        try:
            try_click_first_result_by_tab()
            time.sleep(WAIT_AFTER_CLICK)
            text = copy_visible_page_text()
        except Exception as e2:
            print("Fallback also failed:", e2)

    save_text_to_file(text)
    print("Done. If the result isn't what you expected, read the troubleshooting tips below.")

if __name__ == "__main__":
    main()
