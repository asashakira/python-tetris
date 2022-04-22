from __future__ import annotations

import pkg_resources


def minos() -> list[list[list[str]]]:
    minos_: list[list[list[str]]] = [
        [["" for k in range(4)] for j in range(4)] for i in range(7)
    ]
    with open(pkg_resources.resource_filename(__name__, "ars")) as f:
        for i in range(7):
            for j in range(4):
                for k in range(4):
                    line = f.readline().rstrip()
                    minos_[i][j][k] = line
    return minos_


if __name__ == "__main__":
    s = minos()
    for j in range(4):
        for k in range(4):
            print(s[1][j][k])
    pass
