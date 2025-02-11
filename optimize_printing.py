from typing import List, Dict
from dataclasses import dataclass
from colorama import Fore, Style


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    print_jobs = sorted(print_jobs, key=lambda x: (x["priority"], -x["volume"]))

    print_order = []
    total_time = 0
    queue = []
    current_volume = 0

    for job in print_jobs:
        if (
            len(queue) < constraints["max_items"]
            and current_volume + job["volume"] <= constraints["max_volume"]
        ):
            queue.append(job)
            current_volume += job["volume"]
        else:
            if queue:
                total_time += max(j["print_time"] for j in queue)
                print_order.extend(j["id"] for j in queue)
            queue = [job]
            current_volume = job["volume"]

    if queue:
        total_time += max(j["print_time"] for j in queue)
        print_order.extend(j["id"] for j in queue)

    return {"print_order": print_order, "total_time": total_time}


# Тестування
def test_printing_optimization():
    constraints = {"max_volume": 300, "max_items": 2}

    tests = [
        {
            "name": "Тест 1 (однаковий пріоритет)",
            "jobs": [
                {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
                {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
                {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
            ],
        },
        {
            "name": "Тест 2 (різні пріоритети)",
            "jobs": [
                {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
                {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
                {"id": "M3", "volume": 120, "priority": 3, "print_time": 150},
            ],
        },
        {
            "name": "Тест 3 (перевищення обмежень)",
            "jobs": [
                {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
                {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
                {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
            ],
        },
    ]

    for test in tests:
        print(Fore.CYAN + test["name"] + Style.RESET_ALL)
        result = optimize_printing(test["jobs"], constraints)
        print(Fore.GREEN + f"Порядок друку: {result['print_order']}" + Style.RESET_ALL)
        print(
            Fore.YELLOW
            + f"Загальний час: {result['total_time']} хвилин"
            + Style.RESET_ALL
        )
        print("-" * 50)


if __name__ == "__main__":
    test_printing_optimization()
