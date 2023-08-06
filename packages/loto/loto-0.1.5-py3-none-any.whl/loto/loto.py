
from threading import Lock
from functools import wraps

class LockoutTagout:
    """Function decorator for simple mutual exclusions with tags.

    This decorator takes a tag as a parameter.
    Decorated functions with the same tag will acquire a lock
    associated with that tag before they are executed.
    For example, if functions f and g are both
    decorated with @Loto('data_x'), then they will
    execute with mutual exclusion. If function
    h is decorated with @Loto('data_y') then it will
    not acquire the same mutex as f and g and can
    run simultaneously.
    """
    
    locks = {}

    def __init__(self, tag):
        self.tag = tag
        if self.tag not in LockoutTagout.locks:
            LockoutTagout.locks[self.tag] = Lock()

    def __call__(self, wrappedFunc):
        # the decorator requires args that get passed to __init__
        # so the decorated function is passed here.
        # We acquire the lock associated with this tag before calling
        # the wrapped function
        @wraps(wrappedFunc)  # make the wrapped look like original
        def lockedCall(*args, **kwargs):
            with LockoutTagout.locks[self.tag]:
                wrappedFunc(*args, **kwargs)
        lockedCall._loto_tag = self.tag
        return lockedCall
