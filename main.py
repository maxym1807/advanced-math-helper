from tkinter import messagebox

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from history import HistoryManager
from math_solver import MathSolver
from plotter import Plotter
from utils import Utils

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MathHelperApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Advanced Math Helper")
        self.geometry("740x780")
        self.resizable(True, True)

        self.history_manager = HistoryManager()
        self.math_solver = MathSolver()
        self.plotter = Plotter()
        self.utils = Utils()

        self.current_equation = ctk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        title = ctk.CTkLabel(self, text="Advanced Math Helper",
                             font=ctk.CTkFont(size=32, weight="bold"))
        title.pack(pady=(15, 5))

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabview.add("Розв'язувач рівнянь")
        self.tabview.add("Побудова графіків")
        self.tabview.add("Похідні / Інтеграли")
        self.tabview.add("Історія")

        self.create_solver_tab()
        self.create_plot_tab()
        self.create_deriv_tab()
        self.create_history_tab()

    def create_input_section(self, tab):
        frame = ctk.CTkFrame(tab)
        frame.pack(fill="x", padx=20)

        ctk.CTkLabel(frame, text="Введіть функцію або рівняння:",
                     font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(0, 5))

        entry = ctk.CTkEntry(frame, textvariable=self.current_equation,
                             placeholder_text="Наприклад: x**2 - 5*x + 6 або sin(x)",
                             height=40, font=ctk.CTkFont(size=14))
        entry.pack(fill="x", padx=5)
        return entry

    def create_solver_tab(self):
        tab = self.tabview.tab("Розв'язувач рівнянь")
        self.create_input_section(tab)

        self.real_switch = ctk.CTkSwitch(tab, text="Тільки дійсні корені",
                                         variable=ctk.BooleanVar(value=True))
        self.real_switch.pack(pady=8)

        ctk.CTkButton(tab, text="Розв'язати рівняння", command=self.solve_equation,
                      width=240, height=45).pack(pady=(0, 10))

        self.result_text = ctk.CTkTextbox(tab, height=320, font=ctk.CTkFont(size=14))
        self.result_text.pack(fill="both", expand=True, padx=20, pady=10)

    def create_plot_tab(self):
        tab = self.tabview.tab("Побудова графіків")

        self.create_input_section(tab)

        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack()

        ctk.CTkButton(btn_frame, text="Побудувати графік", command=self.plot_function,
                      width=240, height=45, fg_color="#1f8c4f", hover_color="#17693b").pack(side="left", padx=(0, 10),
                                                                                            pady=8)

        ctk.CTkButton(btn_frame, text="Очистити графік", command=self.clear_plot,
                      width=180, height=45).pack(side="left", pady=8)

        # Область для графіка
        self.plot_frame = ctk.CTkFrame(tab)
        self.plot_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def plot_function(self):
        try:
            self.clear_plot()
        except Exception as e:
            pass

        expr_str = self.current_equation.get().strip()
        fig = self.plotter.plot_expr(expr_str)
        if fig:
            canvas = FigureCanvasTkAgg(fig, self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

    def clear_plot(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

    # Розв'язання рівняння
    def solve_equation(self):
        expr_str = self.current_equation.get().strip()
        only_real = self.real_switch.get()
        result = self.math_solver.solve_equation(expr_str, only_real)

        if result:
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", result)

            self.history_manager.save_to_history(result)
            self.update_history()

    def create_deriv_tab(self):
        tab = self.tabview.tab("Похідні / Інтеграли")

        self.create_input_section(tab)

        # Перемикач режиму
        self.operation_var = ctk.StringVar(value="derivative")
        radio_frame = ctk.CTkFrame(tab)
        radio_frame.pack(pady=10)

        ctk.CTkRadioButton(radio_frame, text="Похідна", variable=self.operation_var,
                           value="derivative").pack(side="left", padx=20)
        ctk.CTkRadioButton(radio_frame, text="Невизначений інтеграл", variable=self.operation_var,
                           value="indefinite").pack(side="left", padx=20)
        ctk.CTkRadioButton(radio_frame, text="Визначений інтеграл", variable=self.operation_var,
                           value="definite").pack(side="left", padx=20)

        # Поля для визначеного інтеграла
        self.limit_frame = ctk.CTkFrame(tab)
        self.limit_frame.pack(pady=8)

        ctk.CTkLabel(self.limit_frame, text="Від:").pack(side="left", padx=5)
        self.lower_limit = ctk.CTkEntry(self.limit_frame, width=80, placeholder_text="0")
        self.lower_limit.pack(side="left", padx=5)

        ctk.CTkLabel(self.limit_frame, text="До:").pack(side="left", padx=5)
        self.upper_limit = ctk.CTkEntry(self.limit_frame, width=80, placeholder_text="1")
        self.upper_limit.pack(side="left", padx=5)

        ctk.CTkButton(tab, text="Обчислити", command=self.calculate_deriv_integral,
                      width=240, height=45, fg_color="#9f46e8").pack(pady=15)

        self.deriv_result = ctk.CTkTextbox(tab, height=320, font=ctk.CTkFont(size=14))
        self.deriv_result.pack(fill="both", expand=True, padx=20, pady=10)

    def calculate_deriv_integral(self):
        expr = self.current_equation.get().strip()
        if not expr:
            messagebox.showwarning("Помилка", "Введіть функцію!")
            return

        operation = self.operation_var.get()

        if operation == "derivative":
            result = self.utils.calculate_derivative(expr)
        elif operation == "indefinite":
            result = self.utils.calculate_integer(expr, definite=False)
        else:  # definite
            try:
                a = float(self.lower_limit.get())
                b = float(self.upper_limit.get())
                result = self.utils.calculate_integer(expr, definite=True, lower_limit=a, upper_limit=b)
            except:
                messagebox.showerror("Помилка", "Введіть коректні межі інтегрування!")
                return

        if result:
            self.deriv_result.delete("0.0", "end")
            self.deriv_result.insert("0.0", result)

            # Зберігаємо в історію
            self.history_manager.save_to_history(result)
            self.update_history()

    def create_history_tab(self):
        tab = self.tabview.tab("Історія")
        ctk.CTkLabel(tab, text="Історія рішень", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 5))

        self.history_text = ctk.CTkTextbox(tab, font=ctk.CTkFont(size=13))
        self.history_text.pack(fill="both", expand=True, padx=20, pady=10)

        self.update_history()

    def update_history(self):
        self.history_text.delete("0.0", "end")
        entries = self.history_manager.get_last_entries(15)

        if not entries:
            self.history_text.insert("0.0", "Історія поки що порожня.\nРозв'яжіть кілька рівнянь!")
            return

        text = ""
        for entry in entries:
            text += f"📅 {entry["date"]}\n"
            text += f"{entry["solution"]}\n"
            text += "-" * 70 + "\n\n"

        self.history_text.insert("0.0", text)


if __name__ == "__main__":
    app = MathHelperApp()
    app.mainloop()
