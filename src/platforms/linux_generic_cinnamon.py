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

    set_terminal_colors(mode)

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


def set_terminal_colors(mode):
    # Theme: Tango light / dark
    light_bg = "'#EEEEEC'"
    light_txt = "'#2E3436'"
    dark_bg = "'#2E3436'"
    dark_txt = "'#D3D7CF'"

    # The Profile ID may vary
    # Leftclick in the Terminal > Preferences > Profiles > Text ---> Look at the botton right corner
    default_profile = "/org/gnome/terminal/legacy/profiles:/:b1dcc9dd-5262-4d8d-a863-c897e6d979b9"

    if mode == "dark":
        background_color = dark_bg
        foreground_color = dark_txt
    elif mode == "light":
        background_color = light_bg
        foreground_color = light_txt
    else:
        raise ValueError("there can only be dark or light mode")

    subprocess.run(["dconf", "write", default_profile + "/background-color", background_color], check=True)
    subprocess.run(["dconf", "write", default_profile + "/foreground-color", foreground_color], check=True)


if __name__ == "__main__":
    import sys

    if sys.argv[1] == "dark":
        change_mode("dark")
    elif sys.argv[1] == "light":
        change_mode("light")
    else:
        raise ValueError("there can only be dark or light mode")