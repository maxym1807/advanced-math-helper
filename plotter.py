import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
from tkinter import messagebox

class Plotter:
    def __init__(self):
        print("Plotter started!") # не знаю что тут сделать

    def plot_expr(self, expr_str):
        if not expr_str:
            messagebox.showwarning("Помилка", "Введіть рівняння або функцію!")
            return

        try:
            x = sp.symbols('x')

            # Якщо рівняння містить знак «=», будуємо left - right
            if '=' in expr_str:
                left, right = expr_str.split('=', 1)
                expr = sp.parse_expr(left.strip()) - sp.parse_expr(right.strip())
            else:
                expr = sp.parse_expr(expr_str)

            f = sp.lambdify(x, expr, 'numpy')

            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)

            # Будуємо графік
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(x_vals, y_vals, linewidth=3, color='#1c90ba', label=f'f(x) = {expr}')
            ax.grid(True, linestyle='--', alpha=0.7)
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.set_title(f'Графік: {expr_str}', fontsize=14)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.legend()

            roots = sp.solve(expr, x)
            for root in roots:
                if root.is_real:
                    plt.scatter([root], [0], color='red', s=50, zorder=5)

            fig.tight_layout()
            return fig

        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося побудувати графік:\n{str(e)}")
