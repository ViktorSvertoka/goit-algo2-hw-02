from typing import List, Dict
from colorama import Fore, Style, init

# Ініціалізація colorama для коректного відображення на всіх платформах
init(autoreset=True)


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    from functools import lru_cache

    @lru_cache(None)
    def dp(n):
        if n == 0:
            return 0, []

        max_profit, best_cut = 0, []
        for i in range(1, n + 1):
            if i <= len(prices):
                profit, cuts = dp(n - i)
                profit += prices[i - 1]
                if profit > max_profit:
                    max_profit = profit
                    best_cut = [i] + cuts

        return max_profit, best_cut

    max_profit, cuts = dp(length)
    return {"max_profit": max_profit, "cuts": cuts, "number_of_cuts": len(cuts) - 1}


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    dp = [0] * (length + 1)
    cuts_record = [[] for _ in range(length + 1)]

    for n in range(1, length + 1):
        for i in range(1, n + 1):
            if i <= len(prices):
                if dp[n] < dp[n - i] + prices[i - 1]:
                    dp[n] = dp[n - i] + prices[i - 1]
                    cuts_record[n] = [i] + cuts_record[n - i]

    return {
        "max_profit": dp[length],
        "cuts": cuts_record[length],
        "number_of_cuts": len(cuts_record[length]) - 1,
    }


def run_tests():
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"},
    ]

    for test in test_cases:
        print(f"\n{Fore.CYAN}Тест: {test['name']}")
        print(f"{Fore.GREEN}Довжина стрижня: {test['length']}")
        print(f"{Fore.YELLOW}Ціни: {test['prices']}")

        memo_result = rod_cutting_memo(test["length"], test["prices"])
        print(f"\n{Fore.MAGENTA}Результат мемоізації:")
        print(f"{Fore.LIGHTGREEN_EX}Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        table_result = rod_cutting_table(test["length"], test["prices"])
        print(f"\n{Fore.MAGENTA}Результат табуляції:")
        print(
            f"{Fore.LIGHTGREEN_EX}Максимальний прибуток: {table_result['max_profit']}"
        )
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print(f"\n{Fore.GREEN}Перевірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
