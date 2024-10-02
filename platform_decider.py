import platform
import os
import subprocess

def set_theme(os_id, mode):
    match os_id:
        case "windows":
            import platforms.windows1x
            platforms.windows1x.change_mode(mode)
        case "linux_generic_cinnamon":
            import platforms.linux_generic_cinnamon
            platforms.linux_generic_cinnamon.change_mode(mode)

def get_theme(os_id):
    match os_id:
        case "windows":
            import platforms.windows1x
            platforms.windows1x.get_current_theme()
        case "linux_generic_cinnamon":
            import platforms.linux_generic_cinnamon
            platforms.linux_generic_cinnamon.get_current_theme()

def get_os_id():
    os_name = detect_os()
    if os_name == "windows":
        return "windows"
    elif os_name == "linuxmint":
        denv = detect_desktop_environment()
        return "linux_generic_" + denv

def detect_os():
    os_name = platform.system()

    if os_name == "Linux":
        import distro
        return distro.id()
    elif os_name == "Windows":
        return "windows"


def detect_desktop_environment():
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP") or os.environ.get("DESKTOP_SESSION") or os.environ.get(
        "GDMSESSION")

    if desktop_env:
        match desktop_env:
            case "X-Cinnamon":
                return "cinnamon"

    try:
        output = subprocess.check_output("ps -e", shell=True).decode()
        if "gnome-shell" in output:
            return "gnome"
        elif "plasmashell" in output:
            return "plasma"
        elif "xfce4-session" in output:
            return "xfce4"
        elif "cinnamon" in output:
            return "cinnamon"
        elif "mate-session" in output:
            return "mate"
        elif "lxsession" in output:
            return "lxde"
    except subprocess.CalledProcessError:
        pass

    return "unknown"

if __name__ == "__main__":
    print(detect_os())
    print(detect_desktop_environment())