import random
from collections import Counter
import matplotlib.pyplot as plt

# аналітичні ймовірності (2..12) для двох ідеальних d6 ---
ANALYTIC_COUNTS = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:5, 9:4, 10:3, 11:2, 12:1}
ANALYTIC_PROB = {s: c/36 for s, c in ANALYTIC_COUNTS.items()}


def simulate_rolls(n_rolls: int, seed: int | None = 42) -> dict[int, float]:
    """Монте-Карло: повертає ймовірності сум 2..12 після n_rolls кидків двох кубиків."""
    if seed is not None:
        random.seed(seed)
    cnt = Counter()
    for _ in range(n_rolls):
        s = random.randint(1, 6) + random.randint(1, 6)
        cnt[s] += 1
    return {s: cnt.get(s, 0) / n_rolls for s in range(2, 13)}


def print_table(mc_prob: dict[int, float]) -> None:
    """Друк таблиці: сума | Монте-Карло | аналітика | похибка."""
    print(f"{'Сума':>4} | {'Монте-Карло':>12} | {'Аналітика':>10} | {'Δ абс.':>6}")
    print("-" * 44)
    mae = 0.0
    for s in range(2, 13):
        p_mc = mc_prob[s]
        p_an = ANALYTIC_PROB[s]
        err  = abs(p_mc - p_an)
        mae += err
        print(f"{s:>4} | {p_mc*100:10.2f}% | {p_an*100:8.2f}% | {err*100:6.2f}%")
    mae /= 11
    print("-" * 44)
    print(f"Середня абсолютна похибка (MAE): {mae*100:.2f}%")


def plot_probs(mc_prob: dict[int, float], title="Ймовірності сум (Монте-Карло vs аналітика)"):
    xs = list(range(2, 13))
    y_mc = [mc_prob[s] for s in xs]
    y_an = [ANALYTIC_PROB[s] for s in xs]

    plt.figure(figsize=(9, 5))
    plt.bar(xs, [p*100 for p in y_mc], width=0.6, label="Монте-Карло")
    plt.plot(xs, [p*100 for p in y_an], marker="o", linewidth=2, label="Аналітика")
    plt.xticks(xs)
    plt.ylabel("Ймовірність, %")
    plt.xlabel("Сума на двох кубиках")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()


def chi_square(mc_prob: dict[int, float], n_rolls: int) -> float:
    """Хі-квадрат статистика (добре, коли близько до 0; df=10)."""
    chi = 0.0
    for s in range(2, 13):
        obs = mc_prob[s] * n_rolls
        exp = ANALYTIC_PROB[s] * n_rolls
        chi += (obs - exp) ** 2 / exp
    return chi


def print_conclusions(mc_prob: dict[int, float], n_rolls: int) -> None:
    """Підсумкові висновки по емпіричним результатам."""
    mae_val = sum(abs(mc_prob[s] - ANALYTIC_PROB[s]) for s in range(2, 13)) / 11 * 100.0
    # χ² і критичне значення для df=10, alpha=0.05
    chi = chi_square(mc_prob, n_rolls)
    chi_crit = 18.31

    verdict = (
        "не відхиляємо H0 (узгоджено з аналітикою)"
        if chi < chi_crit else
        "є підстави сумніватись у моделі (χ² > 18.31)"
    )

    print("\nВисновки:")
    print(f"- Найімовірніша сума: 7 (~{mc_prob[7]*100:.2f}%), найрідші: 2 та 12.")
    print(f"- Середня абсолютна похибка (MAE): {mae_val:.2f}% при N={n_rolls:,}.")
    print(f"- Статистика χ² = {chi:.2f} (df=10), критичне 18.31 → {verdict}.")


if __name__ == "__main__":
    N = 1_000_000
    mc = simulate_rolls(N, seed=123)

    print(f"Результати Монте-Карло для {N:,} кидків двох d6\n")
    print_table(mc)
    print(f"\nСтатистика χ²: {chi_square(mc, N):.2f} (df=10)")

    print_conclusions(mc, N)
    plot_probs(mc, title=f"Монте-Карло (N={N:,}) vs аналітика")
