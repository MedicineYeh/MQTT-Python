import tkinter as tk
from functools import partial
from collections import defaultdict

from logzero import logger

# This is a code snippit from
# https://www.reddit.com/r/Python/comments/27crqg/making_defaultdict_create_defaults_that_are_a/
class key_dependent_dict(defaultdict):
    def __init__(self,f_of_x):
        super().__init__(None) # base class doesn't get a factory
        self.f_of_x = f_of_x # save f(x)
    def __missing__(self, key): # called when a default needed
        ret = self.f_of_x(key) # calculate default value
        self[key] = ret # and install it in the dict
        return ret

class TkinterGUI():
    def __init__(self, config = {}):
        # Config default values
        self.config = {
                    'TITLE': 'MQTT',
                    'GEOMETRY': '580x240',
                }
        # Merge two dicts
        self.config = {**self.config, **config}
        self.callback = key_dependent_dict(lambda key: self._dummy_event_handler(key))
        self._on_update = None

    def _exit_handler(self):
        self.root.quit()
        if self._exit_callback is not None:
            self._exit_callback()

    def _dummy_event_handler(self, name):
        def _f(name):
            logger.error('Event "{}" is not implemented yet!'.format(name))
        return partial(_f, name)

    def on_event(self, event_name):
        # type: (string) -> Callable
        """ A decorator function to register the event with one argument to specify interval """
        def _f(func, event_name):
            # type: (Callable) -> Callable
            self.callback[event_name] = func
        return partial(_f, event_name = event_name)

    def on_exit(self):
        # type: () -> Callable
        """ A decorator function to register the event with one argument to specify interval """
        def wrap_exit(func):
            # type: (Callable) -> Callable
            self._exit_callback = func
        return wrap_exit

    def init(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self._exit_handler)

        self.root.title(self.config.get('TITLE'))
        self.root.geometry(self.config.get('GEOMETRY'))
        # Config all custom GUI interfaces here (hand-coded/fixed GUI without config)
        tk.Label(self.root, text='Hello World').pack()
        tk.Button(self.root,
            text='hit me',
            width=15, height=2,
            command=self.callback['btn_hit']).pack()
        tk.Button(self.root,
            text='This callback is not implemented',
            width=25, height=2,
            command=self.callback['btn_hit_no_impl_example']).pack()
        # Connection status
        self.status = tk.StringVar()
        self.status.set('Disconnected')
        tk.Label(self.root, textvariable = self.status, bg = '#C0C0C0').pack()
        # Connection status 2
        self.status2 = tk.StringVar()
        self.status2.set('Disconnected')
        tk.Label(self.root, textvariable = self.status2, bg = '#C0C0C0').pack()

    def update(self):
        if self._on_update:
            self._on_update()
        # This is a single step update function (non-blocking)
        self.root.update()

    def on_update(self):
        # type: () -> Callable
        """ A decorator function to register the event """

        def _decorator(func):
            # type: (Callable) -> Callable
            self._on_update = func
        return _decorator

