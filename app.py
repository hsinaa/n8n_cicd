"""Scientific calculator GUI (Tkinter). Run with:  python app.py"""
import tkinter as tk

from calculator import CalculatorError, evaluate, format_result

BUTTONS = [
    ["DEG", "(", ")", "⌫", "C"],
    ["sin(", "cos(", "tan(", "√(", "^"],
    ["ln(", "log(", "exp(", "fact(", "%"],
    ["7", "8", "9", "÷", "π"],
    ["4", "5", "6", "×", "e"],
    ["1", "2", "3", "-", "Ans"],
    ["0", ".", "=", "+", ""],
]


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.configure(bg="#1e1e2e")
        self.resizable(False, False)
        self.degrees = True
        self.last_answer = "0"
        self.expr = tk.StringVar()
        self.result = tk.StringVar(value="0")
        self._build()
        self.bind("<Return>", lambda _e: self.calculate())
        self.bind("<BackSpace>", lambda _e: self.backspace())
        self.bind("<Escape>", lambda _e: self.clear())
        self.bind("<Key>", self._on_key)

    def _build(self):
        tk.Label(self, textvariable=self.expr, anchor="e", bg="#1e1e2e",
                 fg="#a6adc8", font=("Consolas", 14), width=28).grid(row=0, column=0, columnspan=5, padx=8, pady=(10, 0))
        tk.Label(self, textvariable=self.result, anchor="e", bg="#1e1e2e",
                 fg="#cdd6f4", font=("Consolas", 28, "bold"), width=14).grid(row=1, column=0, columnspan=5, padx=8, pady=(0, 8))
        self.buttons = {}
        for r, row in enumerate(BUTTONS, start=2):
            for c, label in enumerate(row):
                if not label:
                    continue
                color = "#89b4fa" if label == "=" else "#f38ba8" if label in ("C", "⌫") else \
                        "#45475a" if label.isdigit() or label == "." else "#313244"
                fg = "#1e1e2e" if label == "=" else "#cdd6f4"
                b = tk.Button(self, text=label, width=6, height=2, bg=color, fg=fg,
                              relief="flat", font=("Segoe UI", 11),
                              command=lambda t=label: self.press(t))
                b.grid(row=r, column=c, padx=3, pady=3)
                self.buttons[label] = b
        self.buttons["="].grid_configure(columnspan=1)

    def press(self, label):
        if label == "C":
            self.clear()
        elif label == "⌫":
            self.backspace()
        elif label == "=":
            self.calculate()
        elif label == "DEG":
            self.degrees = not self.degrees
            self.buttons["DEG"].config(text="DEG" if self.degrees else "RAD")
        elif label == "Ans":
            self.expr.set(self.expr.get() + self.last_answer)
        else:
            self.expr.set(self.expr.get() + label)

    def _on_key(self, event):
        if event.char and event.char in "0123456789.+-*/^()%":
            self.expr.set(self.expr.get() + {"*": "×", "/": "÷"}.get(event.char, event.char))

    def clear(self):
        self.expr.set("")
        self.result.set("0")

    def backspace(self):
        self.expr.set(self.expr.get()[:-1])

    def calculate(self):
        try:
            value = format_result(evaluate(self.expr.get(), degrees=self.degrees))
            self.result.set(value)
            self.last_answer = value
        except CalculatorError as err:
            self.result.set("Error")
            self.expr.set(f"{self.expr.get()}   ({err})")


if __name__ == "__main__":
    CalculatorApp().mainloop()
