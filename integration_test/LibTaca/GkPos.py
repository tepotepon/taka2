import cv2

class GkPos:
	def __init__(self, N):
		self.NPOS = N;
		self.data = []
		for i in range(0,self.NPOS):
			self.data.append((0,0))
		self.s_x = 0
		self.s_x2 = 0
		self.oldest = 0 #index of the oldest element of data.
		self.newest = self.NPOS-1 #index of the newest element of data.
		self.diff_x	= self.data[self.newest][0]-self.data[self.oldest][0];

		self.y_i = 0 # y coordinate of the lower horizontal wall of the table.
		self.y_s = 480 # y coordinate of the upper horizontal wall of the table.
		self.x_gk = 460 # x coordinate of the goalkeeper vertical line trayectory.
		self.y_gk_i = 180 # y coordinate of the upper bound for the puppet reference.
		self.y_gk_s = 290 # y coordinate of the upper bound for the puppet reference.
		self.DMW = 10 # Don't Move Window: Minimum value of diff_x for which to consider ball movement.

	def push(self, p):
		# remove the oldest point from the sum terms
		self.s_x -=	self.data[self.oldest][0]
		self.s_x2 -= self.data[self.oldest][0]**2

		# replace the oldest point by the new one.
		self.data[self.oldest] = p

		# add the new point to the sum terms
		self.s_x += p[0]
		self.s_x2 += p[0]**2

		# Update the x-direction difference
		self.diff_x = p[0]-self.data[self.newest][0]

		# Update the index of the newest and oldest point
		self.newest = self.oldest
		self.oldest += 1
		if self.oldest >= self.NPOS:
			self.oldest = 0

	def get_estimate(self):

		# Check if the ball is moving on the right direction.
		if self.diff_x > self.DMW:

			# Compute the regression line parameters.

			m = 0.0
			b = 0.0
			for i in range(self.NPOS):
				m += 1.0*(self.NPOS*self.data[i][0]-self.s_x)*self.data[i][1]
				b += 1.0*(self.s_x2-self.s_x*self.data[i][0])*self.data[i][1]
			D = 1.0*(self.NPOS*self.s_x2-self.s_x**2)
			m = m/D
			b = b/D

			# Compute the interception point between the regression line and the goalkeeper line.
			y_raw = self.x_gk*m+b

			# Make sure the interception point is bounded to the goalkeeper range.
			if y_raw < self.y_gk_i and y_raw > self.y_gk_i - 50:
				y = self.y_gk_i
			elif y_raw > self.y_gk_s and y_raw < self.y_gk_s + 50:
				y = self.y_gk_s
			else:
				y = round(y_raw)
			return (self.x_gk,y)
		else:
			return (self.x_gk, round((self.y_gk_s+self.y_gk_i)/2.0))
	def get_const(self):
		return self.y_gk_s