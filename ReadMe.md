# Theme Switcher

This Python script detects the lighting from your webcam and sets the OS theme accordingly. 
You can run main.py *once* to test the functionality of the automatic switcher. 
If you run scheduler.py, the theme switcher logic gets triggered every 10 minutes.
This is tested on Windows 11 and Linux Mint Cinnamon.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/fabsch225/theme-switcher.git
    ```
2. Install Python Dependencies
    ```sh
    pip install opencv-python
    pip install numpy
   # on windows
   pip install winreg
   # on linux
   pip install distro
    ```
3. Navigate to the project directory:
    ```sh
    cd theme-switcher
    ```
   1. On Linux: install bindings for opencv-python
      ```shell
      sudo apt-get install python3-opencv
      ```
4. Run
    ```sh
    python3 ./scheduler.py
    ```
5. Alternatively, use the Task Manager to run the script on startup.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.
For example, one could add support for macOS or ones favourite Linux Distro / Desktop Environment

## License

This project is licensed under the MIT License.