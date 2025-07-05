selected_window = "None" #selected window name from drop down
overlay_window = None   #reference to the current overlay window
#img = None  #image displayed in the overlay

#normalized RGB values (0-1) or 0–255 depending on your needs
CUSTOM_RED = (255, 225, 20)   #A softer red
CUSTOM_CYAN = (80, 255, 255) #A softer cyan


WINDOW_INVALID = [
    "",  #empty title
    "Program Manager",  #desktop background shell
    "Settings",  #windows Settings (can't be captured easily)
    "Windows Shell Experience Host",
    "Search",  #Cortana or Search UI
    "Task View",
    "Windows Input Experience",  #on-screen keyboard, suggestions
    "Widgets",
    "Action center",
    "Notification Center",
    "Start",
    "Lock Screen",
    "People",
    "Touch Keyboard",
    "Snipping Tool",  #works from os, not prefereable to capture
    "Run",
    "File Explorer",  #not always a stable window to capture, also os
    "Microsoft Text Input Application",
    "Xbox Game Bar",
    "Cortana",
    "Clipboard",
    "Volume Mixer",
    "Network Connections",
    "Windows Security",
    "Credential UI Broker",
    "Focus Assist",
    "CredentialManager",
    "Ease of Access",
    #"Microsoft Store",  #if needed
]
