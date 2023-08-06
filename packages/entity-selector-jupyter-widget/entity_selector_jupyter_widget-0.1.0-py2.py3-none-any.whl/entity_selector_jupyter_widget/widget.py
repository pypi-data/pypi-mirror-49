from __future__ import print_function, absolute_import

from .entity_selector import EntitySelector
from ipywidgets import Button, jslink, VBox, Widget, Output


class widget:
    txt = Button(
        # button_style='info',
        description='Confirm',
        icon='check'
    )

    def __init__(self, str_1, str_2):
        super().__init__()
        self.es = EntitySelector(str_1, str_2)
        self.link = jslink((self.es, 'res'), (self.txt, 'tooltip'))
        self.txt._click_handlers.callbacks = []
        self.txt.on_click(self.hook, remove=True)
        self.txt.on_click(self.hook)


    def __repr__(self):
        display(VBox((self.es, self.txt)))
        return ''

    def hook(self, btn):
        print(self.es.res)
        # print(btn.description)
