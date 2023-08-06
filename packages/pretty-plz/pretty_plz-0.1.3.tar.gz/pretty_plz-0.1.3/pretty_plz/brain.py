import sys

from pathlib import Path

from pretty_plz.env import Env
from pretty_plz.exceptions import CommandNotFound


runnable_extensions = (
  ".exe", ".bat", ".cmd", ".sh", ".zsh", ".bash",
)


interpreter_extensions = {
  ".py": sys.executable,
  ".js": "node",
  ".ts": "ts-node",
  ".pl": "perl",
}


class pretty_plzBrain:
  def __init__(self, command):
    self.command = Path(command)
    self.spath = Path(Env.scripts_path())

  def runnable_candidates(self):
    yield self.spath / self.command
    for ext in runnable_extensions:
      yield self.spath / (str(self.command) + ext)

  def interp_candidates(self):
    for ext, interp in interpreter_extensions.items():
      yield (self.spath / (str(self.command) + ext), interp, )

  def find_command(self):
    for item in self.runnable_candidates():
      if item.exists():
        return (str(item),)
    for item, interp in self.interp_candidates():
      if item.exists():
        return (interp, str(item), )
    raise CommandNotFound(f"Could not find command `{str(self.command)}`")
