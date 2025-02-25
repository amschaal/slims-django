from collections import OrderedDict
from .models import LaneData
from .forms import RunForm, PacbioRunForm, LaneFormSet


class  RunType(object):
    id = 'Run'
    name = 'General Run'
    _run_template = 'run.html'
    _run_form_template = 'run_forms/edit_run.html'
    _run_form = RunForm
    _lane_formset = LaneFormSet
    _data_directory_templates = [{'data_path': '/share/example/run/{run.run_dir}/{lane.lane_dir}', 'repository_subpath': 'subfolder/{lane.lane_dir}'}]
    def __init__(self, run=None):
        self.run = run
    @property
    def run_template(self):
        return self._run_template
    @property
    def run_form_template(self):
        return self._run_form_template
    @property
    def run_form(self):
        # from .forms import RunForm
        # return RunForm
        return self._run_form
    @property
    def lane_formset(self):
        # from .forms import LaneFormSet
        # return LaneFormSet
        return self._lane_formset
    def generate_lane_directories(self, lane):
        directories = []
        for t in self._data_directory_templates:
            data_path = t['data_path'].format(run=self.run, lane=lane)
            if 'repository_subpath' in t:
                repository_subpath = t['repository_subpath'].format(run=self.run, lane=lane)
            else:
                repository_subpath = data_path.split('/')[-1]
            directories.append(LaneData(lane=lane, data_path=data_path, repository_subpath=repository_subpath))
        # instances = [LaneData(lane=lane, data_path=d['data_path'], repository_subpath=d.get('repository_subpath', d['data_path'].split('/')[-1])) for d in directories]
        return directories
    def create_lane_directories(self, lane):
        instances = self.generate_lane_directories(lane)
        lane.directories.exclude(status=LaneData.STATUS_COMPLETE).delete()
        return LaneData.objects.bulk_create(instances)
        # return [t.format(run=self.run, lane=lane) for t in self._data_directory_templates]


class IlluminaRun(RunType):
    id = 'Illumina'
    name = 'Illumina Run'

class PacbioRun(RunType):
    id = 'Pacbio'
    name = 'Pacbio Run'
    # _run_form_template = 'run_forms/pacbio.html'
    _run_form  = PacbioRunForm

class RunTypeRegistry:
    klasses = OrderedDict()
    @classmethod
    def register(cls, klass):
        if klass.id not in cls.klasses:
            cls.klasses[klass.id] = klass
    @classmethod
    def get(cls, id):
        return cls.klasses.get(id, RunType)
    @classmethod
    def choices(cls):
        return [(klass.id, klass.name) for id, klass in cls.klasses.items()]
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(RunTypeRegistry, cls).__new__(cls)
    #         return cls.instance
    #     def __init__(self):
    #         self.classes = OrderedDict()
    # def register(self, klass):
    #     if klass.id not in self.classes:
    #         self.classes[klass.id]

# registry = RunTypeRegistry()
run_types = [RunType, IlluminaRun, PacbioRun]
for r in run_types:
    RunTypeRegistry.register(r)