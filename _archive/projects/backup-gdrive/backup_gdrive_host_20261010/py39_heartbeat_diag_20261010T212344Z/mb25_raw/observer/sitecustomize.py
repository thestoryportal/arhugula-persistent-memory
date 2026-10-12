import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

trace_path = os.environ["PY39_TRACE"]
target = os.path.realpath(os.environ["PY39_TARGET_STATUS"])

def emit(event, **fields):
    record = dict(event=event, pid=os.getpid(), ppid=os.getppid(), **fields)
    fd = os.open(trace_path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.write(fd, (json.dumps(record, sort_keys=True)+"\n").encode())
    finally:
        os.close(fd)

emit("python_start", executable=sys.executable, version=sys.version, argv=sys.argv,
     dont_write_bytecode=sys.flags.dont_write_bytecode)
seen = set()
def profile(frame, event, arg):
    if event != "call" or frame.f_code.co_filename != target:
        return
    name = frame.f_code.co_name
    if name not in {"main", "record", "classify", "preflight", "recover", "health"} or name in seen:
        return
    seen.add(name)
    tool_sys = frame.f_globals["sys"]
    record = dict(event="tool_version", pid=os.getpid(), ppid=os.getppid(), function=name,
                  file=frame.f_code.co_filename, line=frame.f_code.co_firstlineno,
                  executable=tool_sys.executable, version=tool_sys.version, argv=tool_sys.argv,
                  dont_write_bytecode=tool_sys.flags.dont_write_bytecode)
    # Print from the executing tool's globals into its separate version log.
    with open(trace_path, "a") as stream:
        print(json.dumps(record, sort_keys=True), file=stream)
sys.setprofile(profile)

original_popen_init = subprocess.Popen.__init__
def observe_popen(self, *args, **kwargs):
    original_popen_init(self, *args, **kwargs)
    command = kwargs.get("args", args[0] if args else [])
    first = command[0] if isinstance(command, (list, tuple)) and command else str(command)
    emit("popen", child_pid=self.pid, executable=str(first))
subprocess.Popen.__init__ = observe_popen

original_cleanup = tempfile.TemporaryDirectory.cleanup
def observe_cleanup(self):
    root = Path(self.name)
    for path in root.rglob("rclone.pid"):
        text = path.read_text().strip()
        if text.isdigit() and int(text) > 0:
            emit("owned_sync_child", child_pid=int(text), evidence=str(path))
        elif text:
            emit("pid_observation_invalid", evidence=str(path), text=text)
    original_cleanup(self)
tempfile.TemporaryDirectory.cleanup = observe_cleanup
