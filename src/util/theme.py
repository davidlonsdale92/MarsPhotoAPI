from blessed import Terminal
from inquirer.themes import Default


class CustomTheme(Default):
    def __init__(self):
        super().__init__()
        self.term = Terminal()
        self.List.selection_color = self.term.on_red
