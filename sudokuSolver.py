import tkinter 
from pysat.solvers import Glucose3
import matplotlib.pyplot as plt
import numpy 

## Making CNF ##
def varnum(i, j, v):
    return 81 * (v - 1) + 9 * i + j + 1

def exactly_one(literals):
    
    clauses = [literals[:]]
    
    for i in range(len(literals)):
        for j in range(i + 1, len(literals)):
            clauses.append([-literals[i],-literals[j]])
    return clauses

def sudoku_to_cnf(grid):
    clauses =[]

    # exactly one amount
    for i in range(9):
        for j in range(9):
            literals = [varnum(i, j, v) for v in range(1, 10)]
            clauses.extend(exactly_one(literals))

    # one time in each row
    for i in range(9):
        for v in range(1, 10):
            literals = [varnum(i, j, v) for j in range(9)]
            clauses.extend(exactly_one(literals))

    # one time in each collumn
    for j in range(9):
        for v in range(1, 10):
            literals = [varnum(i, j, v) for i in range(9)]
            clauses.extend(exactly_one(literals))

    # One time in each block
    for bi in range(3):
        for bj in range(3):
            for v in range(1, 10):
                literals = [varnum(bi * 3 + i, bj * 3 + j, v)
                            for i in range(3) for j in range(3)]
                clauses.extend(exactly_one(literals))

    # Adding entered sudoku
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                v = grid[i][j]
                clauses.append([varnum(i, j, v)])

    # Save CNF
    with open("sudoku.cnf", 'w') as f:
        f.write(f"p cnf 729 {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(str(x) for x in clause) + " 0\n")
    
    print(f"CNF saved as sudoku.cnf")

## Visualizing ##

def visualize_sudoku(grid):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Setup grid 
    ax.set_xticks(numpy.arange(10) - 0.5)
    ax.set_yticks(numpy.arange(10) - 0.5)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Draw thick lines 
    for i in range(0, 10, 3):
        ax.axhline(i - 0.5,color='#2c3e50',linewidth=3)
        ax.axvline(i - 0.5, color='#2c3e50',linewidth=3)
    # Draw thin lines
    for i in range(10):
        if i % 3 != 0:
            ax.axhline(i - 0.5,color='#7f8c8d',linewidth=1)
            ax.axvline(i - 0.5,color='#7f8c8d',linewidth=1)
    
    # Add numbers
    for i in range(9):
        for j in range(9):
                ax.text(j, i, str(grid[8-i][j]),va='center', ha='center', 
                       fontsize=16,color='#2c3e50',weight='bold')   
        
    # Save 
    plt.savefig("sudoku_solution.png",dpi=300, bbox_inches='tight')
    plt.close()
    print("sudoku solution saved as 'sudoku_solution.png'")

## Solving ##

def solve_sudoku(grid):
    clauses = []

    for i in range(9):
        for j in range(9):
            literals = [varnum(i, j, v) for v in range(1, 10)]
            clauses.extend(exactly_one(literals))

    for i in range(9):
        for v in range(1, 10):
            literals = [varnum(i, j, v) for j in range(9)]
            clauses.extend(exactly_one(literals))

    for j in range(9):
        for v in range(1, 10):
            literals = [varnum(i, j, v) for i in range(9)]
            clauses.extend(exactly_one(literals))

    for bi in range(3):
        for bj in range(3):
            for v in range(1, 10):
                literals = [varnum(bi * 3 + i, bj * 3 + j, v)
                            for i in range(3) for j in range(3)]
                clauses.extend(exactly_one(literals))

    # Adding entered sudoku
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                v = grid[i][j]
                clauses.append([varnum(i, j, v)])
    # Solve
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        result = [[0 for _ in range(9)] for _ in range(9)]

        for val in model:
            if val > 0:
                v = val - 1
                row = (v // 9) % 9
                col = v % 9
                num = v // 81 + 1
                result[row][col] = num

        visualize_sudoku(result)
    else:
        print("No solution found.")


## Getting input ##

root = tkinter.Tk()
root.title("Sudoku input")

grid = [[0 for _ in range(9)] for _ in range(9)]
buttons = [[None for _ in range(9)] for _ in range(9)]

def get_block_color(i, j):
    return "#f2f2f2" if ((i // 3 + j // 3) % 2 == 0) else "#d9d9d9"

def increment_cell(i, j):
    grid[i][j] = (grid[i][j] + 1) % 10
    buttons[i][j].config(text=str(grid[i][j]))

#create buttons
for i in range(9):
    for j in range(9):
        color = get_block_color(i, j)
        btn = tkinter.Button(root, text='0', width=4, height=2, font=("Carre", 20),
                        bg=color, command=lambda x=i, y=j: increment_cell(x, y))
        btn.grid(row=i, column=j)
        buttons[i][j] = btn
# Done
def finish_input():
    print("Entered Sudoku :")
    for row in grid:
        print(row)
    root.destroy()
    sudoku_to_cnf(grid)
    solve_sudoku(grid)
    
done_button = tkinter.Button(root, text="Done", width=10, height=2, font=("Arial", 12, "bold"),
                        bg="lightgreen", command=finish_input)
done_button.grid(row=9, column=0, columnspan=9, pady=10)

root.mainloop()





  

