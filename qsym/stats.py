import os
import time

stats_string = """start_time        : {start_time}
last_update       : {last_update}
fuzzer_pid        : {fuzzer_pid}
cycles_done       : {cycles_done}
execs_done        : {execs_done}
execs_per_sec     : {execs_per_sec}
paths_total       : {paths_total}
paths_favored     : 0
paths_found       : {paths_found}
paths_imported    : {paths_imported}
max_depth         : 0
cur_path          : 0
pending_favs      : 0
pending_total     : 0
variable_paths    : 0
stability         : 100.00%
bitmap_cvg        : {cov_pct}
unique_crashes    : {unique_crashes}
unique_hangs      : {unique_hangs}
last_path         : {last_path}
last_crash        : {last_crash}
last_hang         : {last_hang}
execs_since_crash : 0
exec_timeout      : {exec_timeout}
afl_banner        : {banner}
afl_version       : v0.0.2
target_mode       : qsym
command_line      : {cmdline}"""


class Stats:
    def __init__(self, name, afl, cmd, out_dir, timeout):
        self.stats_filepath = os.path.join(out_dir, 'fuzzer_stats')
        now = int(time.time())
        self.start_time = now
        self.last_update = now
        self.fuzzer_pid = os.getpid()
        self.cycles_done = 0
        self.execs_done = 0
        self.execs_per_sec = 0
        self.paths_total = 0
        self.paths_found = 0
        self.paths_imported = 0
        self.unique_crashes = 0
        self.unique_hangs = 0
        self.last_path = 0
        self.last_crash = 0
        self.last_hang = 0
        self.cov_pct = '0.0%'
        self.exec_timeout = timeout
        self.banner = name
        self.cmdline = "run_qsym_afl -n {} -a {} -- {}".format(
            name,
            afl,
            ' '.join(cmd))
        self.write()

    def update(self, timeout):
        now = int(time.time())
        runtime = max(now - self.start_time, 1)
        self.last_update = now
        eps = round(float(self.execs_done) / float(runtime), 3)
        self.execs_per_sec = eps
        self.exec_timeout = timeout
        self.write()

    def write(self):
        with open(self.stats_filepath, 'w') as sf:
            sf.write(stats_string.format(**self))

    def add_path(self):
        self.paths_found += 1
        self.last_path = int(time.time())

    def add_crash(self):
        self.unique_crashes += 1
        self.last_crash = int(time.time())

    def add_hang(self):
        self.unique_hangs += 1
        self.last_hang = int(time.time())

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __iter__(self):
        return iter(self.__dict__)

    def keys(self):
        return self.__dict__.keys()

    def __repr__(self):
        return stats_string.format(**self)
