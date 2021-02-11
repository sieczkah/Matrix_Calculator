# Returns minor matrix from given m-matrix and its dimensions column x row
def minor_matrix(m, c, r):
    return [row[:c] + row[c + 1:] for row in (m[:r] + m[r + 1:])]

# Multiplies Col x Rows sized matrix by constant
def multiply(matrix, constant, col, rows):
    return [[float(matrix[r][c]) * constant for c in range(col)] for r in range(rows)]

# Rounds all matrix numbers to 3 decimal points
# can be skipped but matrix can get messy
def round_matirx(matrix):
    return [[round(i, 3) for i in s] for s in matrix]


class Matrices:
    """Do various opererations on matrices"""

    def __init__(self):
        self.rows1 = None
        self.col1 = None
        self.rows2 = None
        self.col2 = None
        self.matrix_1 = None
        self.matrix_2 = None
        self.ui()

# Shows menu and calls methods
    def ui(self):
        print("""1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""")
        action = input('Your choice: ')
        if action == '1':
            self.add()
        elif action == '2':
            self.multiply_constant()
        elif action == '3':
            self.multiply_matrices()
        elif action == '4':
            self.transponse()
        elif action == '5':
            self.determinant()
        elif action == '6':
            self.matrix_inverse()
        else:
            pass

# Enter single Matrix needs to match entered size
    def enter_single(self):
        self.rows1, self.col1 = map(int, input('Enter matrix size:').split())
        print('Enter matrix:')
        self.matrix_1 = [input().split() for _ in range(self.rows1)]

# Enter two matrices - need to match entered sizes
    def enter_two(self):
        self.rows1, self.col1 = map(int, input('Enter size of first matrix:').split())
        print('Enter first matrix:')
        self.matrix_1 = [input().split() for _ in range(self.rows1)]
        self.rows2, self.col2 = map(int, input('Enter size of second matrix:').split())
        print('Enter second matrix:')
        self.matrix_2 = [input().split() for _ in range(self.rows2)]

    @staticmethod
    def print_result(result):
        for s in result:
            print(*s)

# Adds Matrices, matrices need to be same size
    def add(self):
        self.enter_two()
        if self.rows1 != self.rows2 and self.col1 != self.col2:
            print('The operation cannot be performed.')
            self.ui()
        else:
            print('The result is:')
            result = [[float(self.matrix_1[r][c]) + float(self.matrix_2[r][c]) for c in range(self.col2)] for r in
                      range(self.rows2)]
            self.print_result(result)
            self.ui()

# Multiply matrix by number
    def multiply_constant(self):
        self.enter_single()
        constant = float(input('Enter constant: '))
        print('The result is:')
        result = multiply(self.matrix_1, constant, self.col1, self.rows1)
        self.print_result(result)
        self.ui()

# Multiply matrices - rule to do it is Number of Columns of Matrix1 is equal
# to number of Rows of Matrix 2.
# The Result have number of columns same as matrix1 and number of rows same sa matrix2
    def multiply_matrices(self):
        self.enter_two()
        if self.col1 != self.rows2:
            print('The operation cannot be performed.')
            self.ui()
        else:
            print('The result is:')
            # First element of first row in new matrix is First_row_of_Matrix1 multiplied by First_column_of_Matrix2
            # Second element of first row is First row of M1 multiplied by Second column of M2
            result = [[sum(float(self.matrix_1[r][c]) * float(self.matrix_2[c][x]) for c in range(self.col1)) for x in
                       range(self.col2)] for r in range(self.rows1)]
            self.print_result(result)
            self.ui()

    # Transponse of matrix
    def trans_main(self, matrix):
        return [[matrix[r][c] for r in range(self.rows1)] for c in range(self.col1)]

    def transponse(self):
        print('\n1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line')
        t_action = input('Your choice: ')
        # MAIN DIAGONAL TRANSPONSE
        if t_action == '1':
            self.enter_single()
            print('The result is:')
            self.print_result(self.trans_main(self.matrix_1))
        # SIDE DIAGONAL TRANSPONSE
        elif t_action == '2':
            self.enter_single()
            trans_sdiag = [[self.matrix_1[-(r + 1)][-(c + 1)] for r in range(self.rows1)] for c in range(self.col1)]
            print('The result is:')
            self.print_result(trans_sdiag)
        # VERTICAL LINE TRANSPONSE
        elif t_action == '3':
            self.enter_single()
            trans_vertical = [[self.matrix_1[r][-(c + 1)] for c in range(self.col1)] for r in range(self.rows1)]
            print('The result is:')
            self.print_result(trans_vertical)
        # HORIZONTAL LINE TRANSPONSE
        elif t_action == '4':
            self.enter_single()
            trans_horizontal = self.matrix_1[::-1]
            print('The result is:')
            self.print_result(trans_horizontal)

    # Interface to call count_deter
    def determinant(self):
        self.enter_single()
        if self.col1 != self.rows1:
            print('The operation cannot be performed.')
            self.ui()
        else:
            print('The result is:')
            print(self.count_deter(self.matrix_1))

    # m - matrix, c - column, r - row
    # Counting determinant using Laplace expansion its recursive and uses minor_matrix function
    def count_deter(self, matrix):
        col, row = len(matrix[0]), len(matrix)
        det = 0
        sign = 1
        if col == 1:
            det += float(matrix[0][0])
            return det
        else:
            for i in range(col):
                det += float(matrix[0][i]) * sign * self.count_deter(minor_matrix(matrix, i, 0))
                sign *= -1
            return det

    # returns matrix of cofactor
    def cofactor(self):
        cofactors_matrix = []
        for r in range(self.rows1):
            row = []
            for c in range(self.col1):
                row.append(self.count_deter(minor_matrix(self.matrix_1, c, r)) * ((-1) ** (c + r)))
            cofactors_matrix.append(row)
        return cofactors_matrix

    # counts inveresed matrix which is transposed matrix multiplied by 1/determinant
    def matrix_inverse(self):
        self.enter_single()
        if self.col1 != self.rows1:
            print('The operation cannot be performed.')
            self.ui()
        else:
            determinant = self.count_deter(self.matrix_1)
            if determinant:
                transposed = self.trans_main(self.cofactor())
                constant = 1 / determinant
                inversed_matrix = multiply(transposed, constant, self.col1, self.rows1)
                self.print_result(round_matirx(inversed_matrix))
            else:
                print("This matrix doesn't have an inverse.")


Matrices()
