from catalyst.dl.experiments import Experiment
from catalyst.dl.state import RunnerState

from mlcomp.db.providers import ReportImgProvider
from mlcomp.db.misc.report_info import ReportSchemeItem
from mlcomp.db.models import Task, Dag
from catalyst.dl.callbacks.core import Callback
from collections import defaultdict


class BaseCallback(Callback):
    def __init__(self, experiment: Experiment, task: Task, dag: Dag, info: ReportSchemeItem):
        self.info = info
        self.task = task
        self.dag = dag
        self.img_provider = ReportImgProvider()
        self.experiment = experiment
        self.is_best = False
        self.data = defaultdict(lambda: defaultdict(list))
        self.added = defaultdict(lambda: defaultdict(int))

    def on_epoch_end(self, state: RunnerState):
        self.is_best = state.metrics.is_best
        self.data = defaultdict(lambda: defaultdict(list))
        self.added = defaultdict(lambda: defaultdict(int))