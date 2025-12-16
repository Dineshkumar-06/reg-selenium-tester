import json
from automation.src.config import DATA_JSON

from automation.src.single_dropdown import run_single_dropdown
from automation.src.dependent_dropdown import run_dependent_dropdown
from automation.src.label import run_label


def main():
    with open(DATA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("test_single_dropdown") == "Y":
        run_single_dropdown()

    if data.get("test_dependent_dropdown") == "Y":
        run_dependent_dropdown()

    if data.get("test_label") == "Y":
        run_label()


if __name__ == "__main__":
    main()
