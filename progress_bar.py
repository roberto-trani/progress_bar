from time import time
import ipywidgets
from IPython.display import display
from labeling import get_custom_labeling_fun

_default_labeling_fun = get_custom_labeling_fun()


class ProgressBar(object):
    def __init__(
        self,
        every=None,
        size=None,
        labeling_fun=_default_labeling_fun,
        display=True
    ):
    """
    :param every: the number of iterations to wait between two updates or None for dynamic behaviour
    :type every: int
    :param size: the total number of iterations or None if not available
    :type size: int
    :param labeling_fun: A function that given the current iteration, the total number of iterations, and the elapsed time returns the labeling string
    :type labeling_fun: (int, int, int) -> str
    :param display: a boolean indicating if the progress bar should be displayed
    :type display: bool
    """
        self._counter = 0
        self._adaptive = True
        self._every = None
        self._size = None
        self._labeling_fun = None
        self._stopped = False
        self._visible = False
        self._start_time = time()
        self._last_time = self._start_time

        # shortcut to set the labeling fun
        if isinstance(labeling_fun, dict):
            labeling_fun = get_custom_labeling_fun(**labeling_fun)

        # init the box with the label and the progress bar
        self._label = ipywidgets.HTML()
        self._progress = ipywidgets.IntProgress(min=0, max=1, value=1)
        self._box = ipywidgets.VBox(children=([self._label, self._progress]))

        # adjust the fields using the properties
        self.every = every
        self.size = size
        # NOTE: this property must be the last one to be set !
        self.labeling_fun = labeling_fun

        # auto display
        if display:
            self.display()

    def _ipython_display_(self, **kwargs):
        if not self._visible:
            self._visible = True
        self.update()
        return self._box._ipython_display_(**kwargs)

    def display(self):
        display(self)
        return self

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        assert not self._stopped and isinstance(value, (int, long)) and value > 0
        # set the field
        self._counter = value
        # update the status
        self.update()

    @property
    def every(self):
        return None if self._adaptive else self._every

    @every.setter
    def every(self, value):
        assert (value is None) or (isinstance(value, (int, long)) and value > 0)
        # set the field
        self._adaptive = value is None
        self._every = value or 1

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        assert (value is None) or (isinstance(value, (int, long)) and value > 0)
        # set the field
        self._size = value
        # update the progress bar
        if self._size is None:
            self._progress.max = 1
            self._progress.value = 1
            self._progress.bar_style = 'info'
        else:
            self._progress.max = self._size
            self._progress.value = self._counter
            self._progress.bar_style = ''
        # update the status
        self.update()

    @property
    def labeling_fun(self):
        return self._labeling_fun

    @labeling_fun.setter
    def labeling_fun(self, value):
        assert value is None or callable(value)
        # set the field
        self._labeling_fun = value
        # update the status
        self.update()

    def increase(self):
        assert not self._stopped
        self._counter += 1
        if self._counter % self._every == 0:
            self.update()

    def increase_many(self, how_many):
        assert not self._stopped and isinstance(how_many, (int, long)) and how_many > 0
        self._counter += how_many
        # update the bar if the increase is bigger than 'every' or if the increase jump over the update point
        if how_many >= self._every or (self._counter % self._every) <= ((self._counter - how_many) % self._every):
            self.update()

    def stop(self, success=True):
        assert not self._stopped
        self._stopped = True
        self._progress.bar_style = 'success' if success else 'danger'
        self.update()

    def close(self, success=True):
        self._box.close()

    def hide_label(self):
        assert self._labeling_fun is not None
        self._label.add_class("hide")
        return self

    def unhide_label(self):
        assert self._labeling_fun is not None
        self._label.remove_class("hide")
        return self

    def hide_bar(self):
        self._progress.add_class("hide")
        return self

    def unhide_bar(self):
        self._progress.remove_class("hide")
        return self

    def hide(self, success=True):
        self._box.add_class("hide")
        return self

    def unhide(self, success=True):
        self._box.remove_class("hide")
        return self

    def update(self):
        # update the status only if it is visible
        if not self._visible:
            return self
        count = self._counter

        if not self._stopped:
            self._last_time = time()

        elapsed_time = self._last_time - self._start_time

        if self._adaptive:
            # try to perform an update every half second
            self._every = (int(count / (elapsed_time * 2)) or 1) if elapsed_time > 0 else 1

        # update the progress bar
        self._progress.value = count
        # update the label
        if self._labeling_fun:
            self._label.value = self._labeling_fun(count, self._size, elapsed_time)
        return self
