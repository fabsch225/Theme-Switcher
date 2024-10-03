import subprocess
'''

--- dark ---

gsettings set org.cinnamon.desktop.wm.preferences theme Mint-Y-Dark-Blue
gsettings set org.cinnamon.desktop.interface gtk-theme Mint-Y-Dark-Blue
gsettings set org.cinnamon.theme name Mint-Y-Dark-Blue
gsettings set org.x.apps.portal color-scheme 'prefer-dark'

--- light ---

gsettings set org.cinnamon.desktop.wm.preferences theme Mint-L-Blue
gsettings set org.cinnamon.desktop.interface gtk-theme Mint-L-Blue
gsettings set org.cinnamon.theme name Mint-L-Blue
gsettings set org.x.apps.portal color-scheme 'prefer-light'
'''

def change_mode(mode):
    dark = "Mint-Y-Dark-Blue"
    light = "Mint-L-Blue"

    if mode == "dark":
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.wm.preferences", "theme", dark])
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", dark])
        subprocess.run(["gsettings", "set", "org.cinnamon.theme", "name", dark])
        subprocess.run(["gsettings", "set", "org.x.apps.portal", "color-scheme", "prefer-dark"])
    elif mode == "light":
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.wm.preferences", "theme", light])
        subprocess.run(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", light])
        subprocess.run(["gsettings", "set", "org.cinnamon.theme", "name", light])
        subprocess.run(["gsettings", "set", "org.x.apps.portal", "color-scheme", "prefer-light"])
    else:
        raise ValueError("there can only be dark or light mode")

def get_current_theme():
    return "unknown"

if __name__ == "__main__":
    import sys

    if sys.argv[1] == "dark":
        change_mode("dark")
    elif sys.argv[1] == "light":
        change_mode("light")
    else:
        raise ValueError("there can only be dark or light mode")