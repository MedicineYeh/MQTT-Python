from functools import wraps, partial

from logzero import logger
from circuits import Component

class PeriodicEvents(Component):
    """ This class defines all the available interfaces for this system """

    def init(self, config = {}):
        # Set up default config
        self.config = {}
        # Merge two dicts
        self.config = {**self.config, **config}
        self.interval = {}
        self.event_names = ['heartbeat', 'dataRecover']

    # === Begin of heartbeat event handling wrapper ===
    def Heartbeat(self, interval):
        # type: () -> Callable
        """ A decorator function to register the event with one argument to specify interval """

        def _decorator(func, interval):
            # type: (Callable) -> Callable
            self._heartbeat = func
            self.interval['heartbeat'] = interval
            # This is just for tutorial purpose
            logger.debug("Using {}:{} as the heartbeat function".format(__file__, func.__name__))
        return partial(_decorator, interval = interval)

    def heartbeat(self):
        """ The wrapper implementation of the event """
        self._heartbeat()
    # === End of heartbeat event handling wrapper ===

    # === Begin of heartbeat event handling wrapper ===
    def DataRecover(self, interval):
        # type: () -> Callable
        """ A decorator function to register the event with one argument to specify interval """

        def _decorator(func, interval = interval):
            # type: (Callable) -> Callable
            self._dataRecover = func
            self.interval['dataRecover'] = interval
            # This is just for tutorial purpose
            logger.debug("Using {}:{} as the dataRecover function".format(__file__, func.__name__))
        return partial(_decorator, interval = interval)

    def dataRecover(self):
        """ The wrapper implementation of the event """
        self._dataRecover()
    # === End of dataRecover event handling wrapper ===

