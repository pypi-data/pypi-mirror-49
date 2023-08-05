from catalyst.dl.callbacks import VerboseLogger

from catalyst.dl.state import RunnerState
from mlcomp.utils.misc import now

from mlcomp.db.providers import ReportSeriesProvider
from mlcomp.db.models import ReportSeries
from mlcomp.utils.config import Config
from mlcomp.worker.executors.base import Executor
from pathlib import Path
from catalyst.utils.config import parse_args_uargs
from catalyst.dl.scripts.utils import import_experiment_and_runner
from catalyst.dl.experiments.runner import Runner
from mlcomp.db.misc.report_info import *
from mlcomp.worker.executors.catalyst.precision_recall import PrecisionRecallCallback
from mlcomp.worker.executors.catalyst.f1 import F1Callback
from catalyst.dl.callbacks.core import Callback
from mlcomp.worker.executors.catalyst.img_classify import ImgClassifyCallback
from catalyst.utils.misc import set_global_seed

class Args:
    baselogdir = None
    batch_size = None
    check = False
    config = None
    configs = []
    expdir = None
    logdir = None
    num_epochs = None
    num_workers = None
    resume = None
    seed = 42
    verbose = True

    def _get_kwargs(self):
        return [(k, v) for k, v in self.__dict__.items() if not k.startswith('_')]


# noinspection PyTypeChecker
@Executor.register
class Catalyst(Executor, Callback):
    def __init__(self, args: Args, report: ReportSchemeInfo):
        self.args = args
        self.report = report
        self.experiment = None
        self.runner = None
        self.series_provider = ReportSeriesProvider()

    def callbacks(self):
        result = [self]
        for items, cls in [
            [self.report.precision_recall, PrecisionRecallCallback],
            [self.report.f1, F1Callback],
            [self.report.img_classify, ImgClassifyCallback],
        ]:
            for item in items:
                result.append(cls(self.experiment, self.task, self.dag, item))
        return result

    def on_epoch_end(self, state: RunnerState):
        for s in self.report.series:
            train = state.metrics.epoch_values['train'][s.key]
            val = state.metrics.epoch_values['valid'][s.key]

            train = ReportSeries(part='train', name=s.key, epoch=state.epoch, task=self.task.id, value=train, time=now())
            val = ReportSeries(part='valid', name=s.key, epoch=state.epoch, task=self.task.id, value=val, time=now())

            self.series_provider.add(train)
            self.series_provider.add(val)

    def on_stage_start(self, state: RunnerState):
        state.loggers = [VerboseLogger()]

    @classmethod
    def _from_config(cls, executor: dict, config: Config, additional_info: dict):
        args = Args()
        for k, v in executor['args'].items():
            if v in ['False', 'True']:
                v = v == 'True'
            elif v.isnumeric():
                v = int(v)

            setattr(args, k, v)

        report = ReportSchemeInfo(additional_info.get('report_config', dict()))
        if len(args.configs)==0:
            args.configs = [args.config]
        return cls(args=args, report=report)

    def work(self):
        args, config = parse_args_uargs(self.args, [])
        # set_global_seed(args.seed)

        Experiment, R = import_experiment_and_runner(Path(args.expdir))

        experiment = Experiment(config)
        runner: Runner = R()

        self.experiment = experiment
        self.runner = runner

        _get_callbacks = experiment.get_callbacks

        def get_callbacks(stage):
            return _get_callbacks(stage) + self.callbacks()

        experiment.get_callbacks = get_callbacks

        runner.run_experiment(
            experiment,
            check=args.check
        )
