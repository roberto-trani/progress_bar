from progress_bar import ProgressBar, _default_labeling_fun


def get_progress_bar_iterator(iterator, every=None, size=None, labeling_fun=_default_labeling_fun, display=True, hide_bar_on_success=False, hide_on_success=False):
    if size is None:
        try:
            size = len(iterator)
        except (AttributeError, TypeError):
            pass

    pb = ProgressBar(every=every, size=size, labeling_fun=labeling_fun, display=display)

    def _iter():
        try:
            for item in iterator:
                yield item
                pb.increase()
            pb.stop(True)
            if hide_bar_on_success:
                pb.hide_bar()
            if hide_on_success:
                pb.hide()
        except:
            pb.stop(False)
            raise
        finally:
            pb.update()
    return pb, _iter()


def iter_progress(iterator, every=None, size=None, labeling_fun=_default_labeling_fun, hide_bar_on_success=False, hide_on_success=False):
    pb, _iter = get_progress_bar_iterator(iterator=iterator, every=every, size=size, labeling_fun=labeling_fun, display=True, hide_bar_on_success=hide_bar_on_success, hide_on_success=hide_on_success)
    return _iter


def iteritems_progress(dict_object, every=None, labeling_fun=_default_labeling_fun, hide_bar_on_success=False, hide_on_success=False):
    assert isinstance(dict_object, dict)
    return iter_progress(iterator=dict_object.iteritems(), every=every, size=len(dict_object), labeling_fun=labeling_fun, hide_bar_on_success=hide_bar_on_success, hide_on_success=hide_on_success)


def itervalues_progress(dict_object, every=None, labeling_fun=_default_labeling_fun, hide_bar_on_success=False, hide_on_success=False):
    assert isinstance(dict_object, dict)
    return iter_progress(iterator=dict_object.itervalues(), every=every, size=len(dict_object), labeling_fun=labeling_fun, hide_bar_on_success=hide_bar_on_success, hide_on_success=hide_on_success)
