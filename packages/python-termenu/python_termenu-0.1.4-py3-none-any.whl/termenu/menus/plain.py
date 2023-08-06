# Modules
from rich import print
from iikp import readchar, keys
from .options import OptionHandler
from ..utils.ascii import AsciiHolder, clear

# Menu class
class PlainMenu(object):
    """The plain Menu class to use for creating multi-choice menus"""

    def __init__(self, label = None):
        self.index = 0
        self.label = label

        self.after = None
        self.active = True

        self.ascii = AsciiHolder()
        self.options = OptionHandler()

    def add_option(self, text, callback, attrs: dict = {}):
        """Takes text and a callback and creates an option from it"""

        self.options.add(text, callback, attrs = attrs)

    def option(self, text, attrs: dict = {}):
        """Internal decorator for add_option"""

        def inner_wrapper(callback):
            return self.add_option(text, callback, attrs)

        return inner_wrapper

    def after_invoke(self):
        """Calls the given function everytime a callback is invoked"""

        def inner_wrapper(callback):
            self.after = callback

        return inner_wrapper

    def display(self):
        """Shows the menu on the screen once, use .mainLoop() for a repeating menu"""

        # Create a main loop
        while True:
            clear()

            # Handle label
            if self.label is not None:
                print(self.label + "\n")

            # Print out all of our options
            for opt in self.options:
                i = self.options.index(opt)
                if i == self.index:
                    print(self.ascii.is_active(opt["text"]))

                else:
                    print(self.ascii.not_active(opt["text"]))

            # Read character input
            r = readchar()
            if r == keys.UP:
                self.index -= 1

            if r == keys.DOWN:
                self.index += 1

            if r == keys.ENTER:
                clear()  # Fix the screen

                opt = self.options.get(self.index)
                opt["callback"]()

                # Call our after invoke
                if self.after is not None:
                    self.after()

                return

            # Fix index
            if self.index < 0:
                self.index = len(self.options.options) - 1

            if self.index + 1 > len(self.options.options):
                self.index = 0

    def close(self):
        """'Kills' the menu instance, allowing you to stop it from reoccuring.
        In the event you end up mass spamming this, just use the .display() method
        on the menu rather than .mainLoop()

        This function can also be recreated simply by using .active = False"""

        self.active = False

    def mainLoop(self):
        """Makes an infinite loop of the menu"""

        # Main loop
        self.active = True
        while self.active:
            self.display()
