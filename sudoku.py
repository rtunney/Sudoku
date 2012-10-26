import random
import copy

#For the purposes of this code, the 9x9 sudoku matrix
#is described as having 9 'boxes' in each row and column.
#The nine 3x3 grids that make up the sudoku matrix 
#are each called a 'submatrix.'

#row and column indices range from 0-8

class sudoku_matrix(object):
	def __init__(self):
		self.matrix = [[[i for i in range(1, 10)] for j in range(9)] for k in range(9)]

	def __str__(self):
		s = ''
		for row in self.matrix:
			for box in row:
				s += '['
				for value in box:
					s += str(value)
				s += ']\t'
			s += '\n'
		return s

	def enter_values(self, entries):
		'''Takes a list of given values in the form [[row_index, column_index, value], ...]
		modifies the matrix to solve the specified boxes'''

		for row_index, column_index, value in entries:
			self.matrix[row_index][column_index] = [value]

	def transpose(self):
		self.matrix = [[row[i] for row in self.matrix] for i in range(9)]

	def submatrix_transpose(self):
		'''performs reversible "transpose" on matrix such that each 3x3
		submatrix becomes a row of the transposed matrix'''

		for i in range(9):
			if i%3 == 1:
				for j in range(3): 
					self.matrix[i][j], self.matrix[i-1][j+3] = self.matrix[i-1][j+3], self.matrix[i][j]
			if i%3 ==2:
				for j in range(3): 
					self.matrix[i][j], self.matrix[i-2][j+6] = self.matrix[i-2][j+6], self.matrix[i][j]
				for j in range(3, 6): 
					self.matrix[i][j], self.matrix[i-1][j+3] = self.matrix[i-1][j+3], self.matrix[i][j]

	def get_singletons(self):
		'''returns a list of boxes containing only one value in the 
		format [[row, column, value], ...]'''

		singletons = []
		for row_index, row in enumerate(self.matrix):
			for column_index, box in enumerate(row):
				if len(box) == 1:
					singletons.append([box[0], row_index, column_index])
		return singletons

	def clear_singletons(self):
		'''calls find_singletons and clears the value of solved boxes 
		from all other boxes in the same row'''

		for value, row_index, solved_box_index in self.get_singletons():
			for column_index in range(9):
				if column_index != solved_box_index:
					if value in self.matrix[row_index][column_index]:
						self.matrix[row_index][column_index].remove(value)

	def get_and_clear_uniques(self):
		'''finds values present in exactly one box in row and 
		removes all other values from that box'''

		for row in self.matrix:
			for value in range(1, 10):
				present_in = []
				for column_index, box in enumerate(row):
					if value in box: present_in.append(column_index)
				if len(present_in) == 1:
					row[present_in[0]] = [value]

	def get_matches(self):
		'''finds sets of n>=2 boxes in a row containing n identical values
		removes these values from all other boxes in row'''

		matches = []
		for row_index, row in enumerate(self.matrix):
			for column_index, box in enumerate(row):
				num_values = len(box)
				if num_values>1:
					match_indices = [column_index]
					for possible_match in range(column_index+1, 9):
						if box == row[possible_match]:
							match_indices.append(possible_match)
					if len(match_indices) == num_values:
						matches.append([box, row_index, match_indices])
		return matches

	def clear_matches(self):
		for match_values, row_index, match_indices in self.get_matches():
			for column_index in range(9):
				if column_index not in match_indices:
					for value in match_values:
						if value in self.matrix[row_index][column_index]:
							self.matrix[row_index][column_index].remove(value)

	def run_row_operations(self):
		self.clear_singletons()
		self.get_and_clear_uniques()
		self.clear_matches()

	def step(self):
		self.run_row_operations()
		self.transpose()
		self.run_row_operations()
		self.transpose()
		self.submatrix_transpose()
		self.run_row_operations()
		self.submatrix_transpose()

	def hundred_steps(self):
		for i in range(100):
			self.step()

	def is_singleton_matrix(self):
		'''returns True if each box in matrix has one value or less
		else returns False'''

		#Note: we allow for the possibility of boxes having 0 values because
		#in the solve() method, calling solve_random_unsolved_box() introduces
		#the possibility of picking the wrong value, which in subsequent 
		#calls of hundred_steps() can produce other boxes from which all 
		#values have been eliminated. 

		for row in self.matrix:
			for box in row:
				if len(box)>1:
					return False
		return True

	def has_valid_rows(self):
		'''returns True if each row contains at least one instance of each 1-9 value
		else returns False'''

		for row in self.matrix:
			row_values = []
			for box in row: 
				row_values.extend(box)
			for value in range(1, 10):
				if value not in row_values:
					return False
		return True

	def is_valid_solution(self):
		if not self.is_singleton_matrix(): return False
		if not self.has_valid_rows(): return False
		self.transpose()
		if not self.has_valid_rows(): return False
		self.transpose()
		self.submatrix_transpose()
		if not self.has_valid_rows(): return False
		self.submatrix_transpose()
		return True

	def get_unsolved_boxes(self):
		unsolved = []
		for row_index, row in enumerate(self.matrix):
			for column_index, box in enumerate(row):
				if len(box)>1:
					unsolved.append([row_index, column_index])
		return unsolved

	def solve_random_unsolved_box(self):
		'''picks a single random unsolved box
		arbitrarily solves the box by choosing one of its values'''
		unsolved = self.get_unsolved_boxes()
		row_index, column_index = random.choice(unsolved)
		self.matrix[row_index][column_index] = [random.choice(self.matrix[row_index][column_index])]

	def solve(self):
		self.hundred_steps()
		while True:
			copy_matrix = copy.deepcopy(self)

			while not copy_matrix.is_singleton_matrix():
				copy_matrix.solve_random_unsolved_box()
				copy_matrix.hundred_steps()

			if copy_matrix.is_valid_solution():
				return copy_matrix


def test()
	test = sudoku_matrix()
	entries = [[0, 2, 3], [0, 5, 8], [0, 6, 9], [1, 3, 9], [1, 6, 6], [2, 2, 8], [2, 3, 5],
	[2, 5, 4], [2, 7, 3], [3, 0, 8], [3, 2, 2], [4, 1, 1], [4, 3, 3], [4, 5, 7], [4, 7, 8],
	[5, 6, 4], [5, 8, 6], [6, 1, 6], [6, 3, 4], [6, 5, 5], [6, 6, 1], [7, 2, 4], [7, 5, 3], 
	[8, 2, 9], [8, 3, 1], [8, 6, 3]]
	test.enter_values(entries)
	print test
	test = test.solve()
	print test
	
if __name__ == '__main__':
	test()

		





