from typing import Dict, List, Tuple

items = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}


def greedy_algorithm(items: Dict[str, Dict[str, int]], budget: int) -> List[str]:
    """
    Жадібний підхід: сортуємо за ratio = calories / cost (спадаюче),
    беремо поки вистачає бюджету. Дає швидке наближення, але не гарантує оптимум.
    """
    data = []
    for name, v in items.items():
        c, cal = v["cost"], v["calories"]
        if c <= 0:
            continue
        data.append((name, c, cal, cal / c))
    data.sort(key=lambda x: x[3], reverse=True)

    chosen = []
    remaining = budget
    for name, cost, cal, ratio in data:
        if cost <= remaining:
            chosen.append(name)
            remaining -= cost
    return chosen


def dynamic_programming(items: Dict[str, Dict[str, int]], budget: int) -> List[str]:
    """
    0/1 Knapsack (кожну страву можна взяти не більше одного разу).
    Оптимально максимізує калорії при обмеженні вартості (<= budget).
    Час: O(N * budget), пам'ять: O(N * budget) для простоти; вміє відновлювати вибір.
    """
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    cals  = [items[n]["calories"] for n in names]
    n = len(names)

    # dp[i][w] = макс. калорій із перших i предметів при бюджеті w
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # заповнення
    for i in range(1, n + 1):
        ci, vi = costs[i - 1], cals[i - 1]
        for w in range(budget + 1):
            dp[i][w] = dp[i - 1][w]
            if ci <= w:
                cand = dp[i - 1][w - ci] + vi
                if cand > dp[i][w]:
                    dp[i][w] = cand

    res: List[str] = []
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            res.append(names[i - 1])
            w -= costs[i - 1]
    res.reverse()
    return res


if __name__ == "__main__":
    for B in (40, 50, 65, 75, 90):
        g = greedy_algorithm(items, B)
        d = dynamic_programming(items, B)

        def total(lst: List[str]) -> Tuple[int, int]:
            cost = sum(items[x]["cost"] for x in lst)
            cal  = sum(items[x]["calories"] for x in lst)
            return cost, cal

        g_cost, g_cal = total(g)
        d_cost, d_cal = total(d)

        print(f"Бюджет = {B}")
        print(f"  Greedy:   {g} | вартість={g_cost}, калорій={g_cal}")
        print(f"  DP оптим.: {d} | вартість={d_cost}, калорій={d_cal}")
        print("-" * 60)
