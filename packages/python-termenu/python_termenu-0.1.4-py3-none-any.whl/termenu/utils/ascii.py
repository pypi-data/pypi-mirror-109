# Modules
import os
import colorama
import subprocess

# Text holder
colorama.init()
class AsciiHolder(object):
    """Takes ascii text and converts it using colorama"""

    def not_active(self, text):
        return text

    def is_active(self, text):
        return colorama.Back.LIGHTBLACK_EX + text + colorama.Back.RESET

# Clear function
def clear():
    subprocess.run(["clear" if os.name != "nt" else "cls"], shell = True)
