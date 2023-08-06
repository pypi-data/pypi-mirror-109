class Math():
	def __init__ (self, num1, num2):
		self.num1 = num1
		self.num2 = num2


	def Add(self):
		sum = float(self.num1) + float(self.num2)
		return sum
		print(sum)


	def Subtract(self):
		sub = float(self.num1) - float(self.num2)
		return sub
		print(sub)



	def Multiply(self):
		mul = float(self.num1) * float(self.num2)
		return mul
		print(mul)


	def Divide(self):
		div = float(self.num1) / float(self.num2)
		return div
		print(div)


class Sc():
	def __init__ (self, num1):
		self.num1 = num1


	def Square(self):
		sq = int(self.num1) * int(self.num1)
		return sq
		print(sq)


	def Cube(self):
		cb = int(self.num1) * int(self.num1) * int(self.num1)
		return cb
		print(cb)


	def Float_square(self):
		sqr = float(self.num1) * float(self.num1)
		return sqr
		print(sqr)


	def Float_cube(self):
		cbr = float(self.num1) * float(self.num1) * float(self.num1)
		return cbr
		print(cbr)
    	
