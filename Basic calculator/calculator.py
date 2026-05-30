import tkinter as tk
from tkinter import ttk
import ast


def safe_eval(expr: str):
    """Safely evaluate a simple arithmetic expression.

    Supports +, -, *, / and unary +/- with parentheses and decimals.
    """
    node = ast.parse(expr, mode="eval")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        if isinstance(n, ast.BinOp):
            left = _eval(n.left)
            right = _eval(n.right)
            if isinstance(n.op, ast.Add):
                return left + right
            if isinstance(n.op, ast.Sub):
                return left - right
            if isinstance(n.op, ast.Mult):
                return left * right
            if isinstance(n.op, ast.Div):
                return left / right
            raise ValueError("Unsupported binary operator")
        if isinstance(n, ast.UnaryOp):
            val = _eval(n.operand)
            if isinstance(n.op, ast.UAdd):
                return +val
            if isinstance(n.op, ast.USub):
                return -val
            raise ValueError("Unsupported unary operator")
        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError("Only numbers allowed")
        if isinstance(n, ast.Num):
            return n.n
        raise ValueError("Unsupported expression")

    return _eval(node)


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Calculator")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.expression = tk.StringVar()

        self._build_ui()
        self.bind_events()

    def _build_ui(self):
        entry = ttk.Entry(self, textvariable=self.expression, font=(None, 20), justify="right")
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=8)
        entry.focus()

        btns = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for (text, r, c) in btns:
            cmd = (lambda t=text: self.on_button(t))
            b = ttk.Button(self, text=text, command=cmd)
            b.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

        clear = ttk.Button(self, text="C", command=self.clear)
        clear.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)
        back = ttk.Button(self, text="←", command=self.backspace)
        back.grid(row=5, column=2, sticky="nsew", padx=4, pady=4)
        neg = ttk.Button(self, text="±", command=self.negate)
        neg.grid(row=5, column=3, sticky="nsew", padx=4, pady=4)

        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)

    def bind_events(self):
        self.bind("<Return>", lambda e: self.evaluate())
        self.bind("=", lambda e: self.evaluate())
        self.bind("<BackSpace>", lambda e: self.backspace())
        self.bind("<Escape>", lambda e: self.clear())

    def on_button(self, char: str):
        if char == "=":
            self.evaluate()
            return
        cur = self.expression.get()
        self.expression.set(cur + char)

    def clear(self):
        self.expression.set("")

    def backspace(self):
        cur = self.expression.get()
        self.expression.set(cur[:-1])

    def negate(self):
        cur = self.expression.get()
        if not cur:
            return
        try:
            val = safe_eval(cur)
            self.expression.set(str(-val))
        except Exception:
            if cur.startswith("-"):
                self.expression.set(cur[1:])
            else:
                self.expression.set("-" + cur)

    def evaluate(self):
        expr = self.expression.get()
        try:
            result = safe_eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression.set(str(result))
        except ZeroDivisionError:
            self.expression.set("Error: division by zero")
        except Exception:
            self.expression.set("Error")


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
