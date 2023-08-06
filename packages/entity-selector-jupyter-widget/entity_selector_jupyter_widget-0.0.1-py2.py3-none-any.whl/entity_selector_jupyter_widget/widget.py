from __future__ import print_function, absolute_import

from entity_selector_jupyter_widget import EntitySelector
from ipywidgets import Button, jslink, VBox, Widget, Output


class widget:
    txt = Button(
        # button_style='info',
        description='Confirm'
    )

    def __init__(self, str_1, str_2):
        super().__init__()
        self.es = EntitySelector(str_1, str_2)
        self.link = jslink((self.es, 'res'), (self.txt, 'tooltip'))
        self.txt.on_click(self.th)
        # super(Widget, self).__init__()

    def __repr__(self):
        display(VBox((self.es, self.txt)))
        return ''

    def th(self, btn):
        print(self.es.res)
        # print(btn.description)
