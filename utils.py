import sympy as sp
from tkinter import messagebox

class Utils:
    def __init__(self):
        pass

    def calculate_derivative(self, expr_str: str):
        if not expr_str:
            messagebox.showwarning("Помилка", "Введіть функцію!")
            return None

        try:
            x = sp.symbols('x')
            expr = sp.parse_expr(expr_str)
            derivative = sp.diff(expr, x)
            return f"Похідна:\n   f'(x) = {derivative}"
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося знайти похідну:\n{str(e)}")
            return None

    def calculate_integer(self, expr_str: str, definite=False, lower_limit=None, upper_limit=None):
        if not expr_str:
            messagebox.showwarning("Помилка", "Введіть функцію!")
            return None

        try:
            x = sp.symbols('x')
            expr = sp.parse_expr(expr_str)

            if definite and lower_limit is not None and upper_limit is not None:
                integral = sp.integrate(expr, (x, lower_limit, upper_limit))
                return f"Визначений інтеграл від {lower_limit} до {upper_limit}:\n   ∫ {expr} dx = {integral}"
            else:
                integral = sp.integrate(expr, x)
                return f"Невизначений інтеграл:\n   ∫ {expr} dx = {integral} + C"
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося обчислити інтеграл:\n{str(e)}")
            return None
