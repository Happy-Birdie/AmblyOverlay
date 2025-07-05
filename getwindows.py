import pygetwindow as gw

#SET-UP FOR UI

#get windows
def get_open_windows():
    return gw.getAllTitles()

if __name__ == "__main__":
    open_windows = get_open_windows()
    list = None
    if open_windows:
        print("Open windows:")
        for window in open_windows:
            if ((window == "Settings") or
                (window == "Windows Input Experience") or
                (window == "Program Manager") or
                (window == "")):
                continue
            else:
                print(window)
    else:
        print("No open windows found.")


#minimize maximize
def selecting_window(title):
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        print(f"Window '{title}' not found. Please ensure it is open.")
        return
    
    window = windows[0]  #take the first matching window
    try:
        window.maximize()
        print(f"Maximized window: {title}")
    except Exception as e:
        print(f"Failed to maximize window '{title}': {e}")
 
'''
window.minimize()
print("Window minimized.")

window.maximize()
print("Window maximized.")

window.restore()  # Opens a minimized window or returns a maximized window to its previous size
print("Window restored to its previous state.")
'''