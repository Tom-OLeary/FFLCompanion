import os
import re
import shlex
import sys
from subprocess import Popen, PIPE
from git import GitCommandError, Repo


def execute(command, raw_output=False, decode=True):
    p = Popen(shlex.split(command), stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()

    if hasattr(out, "decode"):
        if decode:
            out = out.decode()

    if hasattr(err, "decode"):
        if decode:
            err = err.decode()

    if not raw_output:
        out = [l.strip() for l in out.splitlines()]
        err = [l.strip() for l in err.splitlines()]

    return p.returncode, out, err


def get_modified_files() -> list[str]:
    repo = Repo(".")
    return [diff.b_path for diff in repo.index.diff(repo.head.commit, R=True, diff_filter="d")]


def main():
    files = [fn for fn in get_modified_files() if fn.endswith(".py")]
    if not files:
        return

    try:
        return_code, out, err = execute(f"autoflake --in-place --remove-all-unused-imports {' '.join(files)}")
    except OSError:
        print("Autoflake not installed", file=sys.stderr)
        sys.exit(-1)

    if return_code != 0:
        print("Autoflake failed", file=sys.stderr)
        if out:
            for line in out:
                print(line)
        if err:
            for line in err:
                print(line, file=sys.stderr)
        sys.exit(-1)


if __name__ == "__main__":
    main()