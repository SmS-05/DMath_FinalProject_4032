# Sudoku Solver with SAT Solver

این پروژه برای درس **ریاضیات گسسته** طراحی شده است و هدف آن **حل جدول سودوکو با استفاده از SAT Solver** است.

## قابلیت‌ها
- رابط گرافیکی ساده برای ورود جدول
- تبدیل خودکار سودوکو به فرمول CNF و ذخیره در `sudoku.cnf`
- حل با **Glucose3 SAT Solver** (کتابخانه PySAT)
- ذخیره تصویر جواب در `sudoku_solution.png`

## پیش‌نیازها
```bash
pip install python-sat matplotlib numpy
```

## نحوه اجرا
```bash
python sudoku_solver.py
```
1. جدول سودوکو را در پنجره وارد کنید (0 یعنی خانه خالی).
2. روی دکمه **Done** کلیک کنید.
3. برنامه به طور خودکار فایل CNF را ایجاد کرده و جواب را ذخیره می‌کند.

## خروجی‌ها
- `sudoku.cnf` → قیود سودوکو در قالب DIMACS CNF  
- `sudoku_solution.png` → تصویر جدول حل‌شده

---
