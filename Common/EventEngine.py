from logzero import logger
from circuits import Component, Event, Timer
from circuits.tools import graph

from Common.Events import PeriodicEvents

class stop_timers(Event):
    """ Timer stop event"""

class start_timers(Event):
    """ Timer start event"""

class Scheduler(Component):
    def stop_timers(self):
        logger.info("Stop timers")
        for t in self.timers:
            t.unregister()

    def start_timers(self):
        logger.info("Start timers")
        for t in self.timers:
            t.register(self)

    def init(self, events, gui = None):
        self.timers = []
        # Create and register all the events defined in PeriodicEvents
        events.register(self)
        # Construct the list of timer handlers for all events iff interval[e] is defined/registered
        self.timers = [ Timer(events.interval[e], Event.create(e), persist=True).register(self)
                        for e in events.event_names if events.interval.get(e) ]
        # Set up GUI handler for updating
        if gui is not None:
            self.gui = gui
            Timer(0.01, Event.create('update_gui'), persist=True).register(self)

    def update_gui(self):
        if self.gui is not None:
            self.gui.update()

    def started(self, component):
        """Started Event Handler

        This is fired internally when your application starts up and can be used to
        trigger events that only occur once during startup.
        """
        logger.debug(graph(self.root))

        # The following codes are just a demo on how to stop/start timers with timmer
        # Timer(1, Event.create("stop_timers")).register(self)
        # Timer(2, Event.create("start_timers")).register(self)

