import sympy as sp
from tkinter import messagebox

class MathSolver:
    def __init__(self):
        print("Math Solver started!") # не знаю что тут сделать

    def solve_equation(self, eq, show_only_real):
        if not eq:
            messagebox.showwarning("Помилка", "Введіть рівняння!")
            return

        try:
            if "=" in eq:
                left, right = eq.split("=", 1)
                expr = sp.parse_expr(left.strip()) - sp.parse_expr(right.strip())
            else:
                expr = sp.parse_expr(eq)

            x = sp.symbols("x")
            solutions = sp.solve(expr, x)

            result = f"Рівняння: {eq}\n\n"

            real_roots = []
            complex_roots = []

            for sol in solutions:
                if sol.is_real:
                    real_roots.append(sol)
                else:
                    complex_roots.append(sol)

            if show_only_real:
                result += f"✅ Реальні корені ({len(real_roots)}):\n"
                for sol in real_roots:
                    result += f"   x = {sol}\n"

                if complex_roots:
                    result += f"\n❎ Комплексних коренів не показано: {len(complex_roots)}\n"
            else:
                result += f"Всі корені ({len(solutions)}):\n"
                for sol in solutions:
                    if sol.is_real:
                        result += f"   x = {sol}  (реальний)\n"
                    else:
                        result += f"   x = {sol}  (комплексний)\n"

            return result

        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося вирішити рівняння:\n{str(e)}")
