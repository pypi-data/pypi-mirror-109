from pathlib import Path
from utils import randomLine

igbo_names = Path("../data/igbo_names.txt")
yoruba_names = Path("../data/yoruba_names.txt")
hausa_names = Path("../data/hausa_names.txt")


def igbo_name():
    return randomLine(igbo_names)


def yoruba_name():
    return randomLine(yoruba_names)


def hausa_name():
    return randomLine(hausa_names)


print(hausa_name())
