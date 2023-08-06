from legos.utils import camel2snake

class Plugin():
    """
    Plugin allows to add functionalities to `Learner` such as `Inspector`, `Doctor`, etc ...
    and access via `learner.<plugin_name>`.
    Plugin can also be used in standalone way without add to the Learner.

    Can be add in the same way as Callbacks.

    However, these plugins is used to analysis the current state of `Learner` and provide useful stuffs
    instead of interfering with the training loop. Each plugins can have their own running loop and may used `Callbacks`
    """
    def __init__(self, learner=None):
        self.learner = learner

    @property
    def name(self):
        return camel2snake(self.__class__.__name__)
