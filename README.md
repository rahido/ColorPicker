# ColorPicker
Pick a color from the screen, program shows color values and relative colors. One-click copy values to clipboard.

## For making .exe using pyInstaller:
`pyinstaller ColorPicker.py --onefile -w`
For window icon, favicon.ico should be placed in the same folder as .py or .exe.

NOTE. If your exe from pyInstaller is flagged false-positive Trojan, you can try following f.e. this post from Plain English for manually compiling pyInstaller's bootloader:
https://plainenglish.io/blog/pyinstaller-exe-false-positive-trojan-virus-resolved-b33842bd3184
