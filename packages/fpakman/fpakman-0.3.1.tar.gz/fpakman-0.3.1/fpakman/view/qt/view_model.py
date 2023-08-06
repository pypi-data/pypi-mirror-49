from enum import Enum

from fpakman.util import util
from fpakman.core.model import Application, ApplicationStatus, FlatpakApplication


class ApplicationViewStatus(Enum):
    LOADING = 0
    READY = 1


class ApplicationView:

    def __init__(self, model: Application, visible: bool = True):
        self.model = model
        self.update_checked = model.update
        self.visible = visible
        self.status = ApplicationViewStatus.LOADING

    def get_async_attr(self, attr: str, strip_html: bool = False, default: str = '...'):

        if isinstance(self.model, FlatpakApplication) and self.model.runtime:
            res = getattr(self.model.base_data, attr)
        else:
            res = getattr(self.model.base_data, attr) if self.model.status == ApplicationStatus.READY and getattr(self.model.base_data, attr) else default

        return util.strip_html(res) if res and strip_html else res
