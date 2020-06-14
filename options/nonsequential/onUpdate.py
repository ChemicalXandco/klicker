from options.nonsequential.abstract.onEvent import OnEvent


class Widget(OnEvent):
    def __init__(self, *args):
        super().__init__(*args)

    def update(self):
        self.optionManger.runOptions()
