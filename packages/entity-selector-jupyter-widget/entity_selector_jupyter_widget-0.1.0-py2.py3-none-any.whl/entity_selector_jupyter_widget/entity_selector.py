from __future__ import print_function

import ipywidgets as widgets
from traitlets import Unicode


@widgets.register
class EntitySelector(widgets.DOMWidget):
    _view_name = Unicode('EntitySelectorView').tag(sync=True)
    _model_name = Unicode('EntitySelectorModel').tag(sync=True)
    _view_module = Unicode('frontend_entity_selector_jupyter_widget').tag(sync=True)
    _model_module = Unicode('frontend_entity_selector_jupyter_widget').tag(sync=True)
    _view_module_version = Unicode('^0.0.1').tag(sync=True)
    _model_module_version = Unicode('^0.0.1').tag(sync=True)
    text = Unicode('').tag(sync=True)
    search = Unicode('').tag(sync=True)
    res = Unicode('').tag(sync=True)
    input_str1 = Unicode('')
    input_str2 = Unicode('')

    def __init__(self, input_str1, input_str2):
        super().__init__()
        self.text = input_str1
        self.search = input_str2
        # super(EntitySelector, self).__init__()

