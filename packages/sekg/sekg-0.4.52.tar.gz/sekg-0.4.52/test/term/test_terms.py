#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sekg.term.fusion import Fusion
from pathlib import Path

if __name__ == "__main__":
    fusion = Fusion()

    print(fusion.check_synonym("edit mode", "editmode"))
    print(fusion.check_abbr("byte order mask", "bom"))

    with (Path(__file__).parent / "terms.txt").open("r", encoding="utf-8") as f:
        terms = {line.strip() for line in f}
    synsets = fusion.fuse(terms)
    with (Path(__file__).parent / "synsets.txt").open("w", encoding="utf-8") as f:
        f.write("\n".join([str(synset) for synset in synsets]))
