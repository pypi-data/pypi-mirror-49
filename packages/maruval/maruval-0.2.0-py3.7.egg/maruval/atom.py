import os
import shutil
import subprocess


def configure():
    """
    python -m maruval.atom
    """
    target = os.path.dirname(os.path.dirname(__file__))
    target = os.path.join(target, "schemata", "process-palette.json")
    assert os.path.isfile(target), "Does not exist: {}".format(target)
    shutil.copyfile(target, os.path.expanduser("~/.atom/process-palette.json"))
    subprocess.call("apm install process-palette".split())
    msg = "maruval for atom configured. "
    msg += "restart atom and type 'maruval' in command palette..."
    print(msg)


if __name__ == "__main__":
    configure()
