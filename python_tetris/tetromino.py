""" get tetromino pieces from ars file """

from __future__ import annotations

import pkg_resources


def get_minos() -> list[list[list[str]]]:
    minos: list[list[list[str]]] = [
        [["" for _ in range(4)] for _ in range(4)] for _ in range(7)
    ]
    with open(pkg_resources.resource_filename(__name__, "ars"), encoding="utf-8") as f:
        for i in range(7):
            for j in range(4):
                for k in range(4):
                    line = f.readline().rstrip()
                    minos[i][j][k] = line
    return minos


def main():
    s = get_minos()
    for j in range(4):
        for k in range(4):
            print(s[1][j][k])


if __name__ == "__main__":
    main()
