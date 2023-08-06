# Modules
from rich import print
from iikp import readchar, keys
from ..utils.ascii import AsciiHolder, clear

# Menu class
class LeftRightMenu(object):
    """Left/Right menu class designed for multiple options per line"""

    def __init__(self, label = None):
        self.label = label
        self.index_data = {}

        self.options = []
        self.optidx = 0

        self.ascii = AsciiHolder()

    def add_option(self, values: dict, default: str):
        """Takes text and a callback and creates an option from it"""
        self.options.append({"vals": values, "def": default})
        def set_index(val: int):  # noqa
            self.index_data[len(self.options) - 1] = val

        if not default:
            return set_index(0)

        validx = 0
        for value in values:
            if default in value:

                # Change index according to default
                return set_index(validx)

            validx += 1

        return set_index(0)

    def option(self, values: dict = {}, default: str = ""):
        """Internal decorator for add_option"""

        def inner_wrapper(callback):
            return self.add_option(values, default)

        return inner_wrapper

    def after_invoke(self):
        """Calls the given function everytime a callback is invoked"""

        def inner_wrapper(callback):
            self.after = callback

        return inner_wrapper

    def dict_to_index(self, dictionary: dict, index: int):
        lidx = 0
        for key in dictionary:
            if lidx == index:
                return key

            lidx += 1

        return None

    def display(self):
        """Shows the menu on the screen once, use .mainLoop() for a repeating menu"""

        # Main loop
        while True:
            clear()

            # Handle label
            if self.label:
                print(self.label + "\n")

            # Handle printing
            lidx = 0
            for option in self.options:
                larr, rarr = "<<", ">>"
                if self.optidx == lidx:
                    larr, rarr = "[yellow]<<[/yellow]", "[yellow]>>[/yellow]"

                line_caption = self.dict_to_index(option["vals"], self.index_data[lidx])
                line_text = "{} {}[reset] {}".format(larr, line_caption, rarr)

                print(line_text)
                lidx += 1

            # Handle keypress
            key = readchar()
            if key == keys.UP:
                self.optidx -= 1
                if self.optidx < 0:
                    self.optidx = len(self.options) - 1

            elif key == keys.DOWN:
                self.optidx += 1
                if self.optidx > len(self.options) - 1:
                    self.optidx = 0

            elif key == keys.LEFT:
                option = self.options[self.optidx]
                newidx = self.index_data[self.optidx] - 1
                if newidx < 0:
                    newidx = len(option["vals"]) - 1

                self.index_data[self.optidx] = newidx

            elif key == keys.RIGHT:
                option = self.options[self.optidx]
                newidx = self.index_data[self.optidx] + 1
                if newidx > (len(option["vals"]) - 1):
                    newidx = 0

                self.index_data[self.optidx] = newidx

            elif key == keys.ENTER:
                option = self.options[self.optidx]
                values = option["vals"]

                value = self.dict_to_index(values, self.index_data[self.optidx])
                return values[value]

            elif key == keys.CTRL_C:
                raise KeyboardInterrupt
