from sys import stdout
from scipy import zeros, exp, pi, sqrt, arange, array, log
from matplotlib import pyplot as plt


def perror(string):
	stdout(string)
	exit(0)


def calSigma2(width):
	s = width / 2.0 / sqrt(2.0 * log(2.0))
	return s * s


def mixGaussian(centers, heights, rmin, rmax, interval, width):
	x = arange(rmin, rmax, interval)
	N = x.shape[0]
	y = zeros(shape=N)
	s2 = calSigma2(width)
	alpha = sqrt(0.5 / pi) * s2
	for i in range(N):
		y[i] = alpha * (heights * exp(-0.5 * (x[i] - centers)**2 / s2)).sum()
	return x, y


filepath = "./spectra.dat"
fp = open(filepath)

# Set the default half-width to 0.2 eV
width = 0.2

# Set the simulation interval
interval = 0.05

# Gaussian centers and gaussian relative heights
centers = []
heights = []

# Set the simulation range
pStart = 1.0
pEnd = 9.0

# X/Y description
Ydes = None
Xdes = None

# The interval on x axis
Xi = 0.5

# The title of the graph
title = None

for line in fp:
	line = line.strip()
	if line == "":
		continue
	elements = line.split()
	if elements[0] == "#":
		continue
	elif elements[0] == "w":
		# Get the width of the gassian
		if len(elements) != 2:
			perror("Wrong format for width!")
		pass
		width = float(elements[1])
	elif elements[0] == "i":
		# Get the interval
		if len(elements) != 2:
			perror("Wrong format for interval!")
		pass
		interval = float(elements[1])
	elif elements[0] == "e":
		# Get the data
		if len(elements) == 3:
			centers.append(float(elements[1]))
			heights.append(float(elements[2]))	
		elif len(elements) == 2:
			centers.append(float(elements[1]))
		else:
			perror("Wrong format for data!")
		pass
	elif elements[0] == "min":
		pStart = float(elements[1])
	elif elements[0] == "max":
		pEnd = float(elements[1])
	elif elements[0] == "Y":
		# Get the Y description
		Ydes = " ".join(elements[1:len(elements)])
	elif elements[0] == "X":
		# Get the X description
		Xdes = " ".join(elements[1:len(elements)])
	elif elements[0] == "Xi":
		# Get the X interval
		Xi = float(elements[1])
		if Xi < 0.1:
			Xi = 0.1
	elif elements[0] == "title":
		title = " ".join(elements[1:len(elements)])
	pass
pass

if len(centers) == 0:
	perror("No data points specified!")
pass

# Use default height for every centers
if len(heights) == 0:
	heights = [1.0] * len(centers)
pass

x, y = mixGaussian(array(centers), array(heights), pStart, pEnd, interval, width)

plt.plot(x, y)

outfile = open("simulation.txt", "w")
for i in range(x.shape[0]):
    outfile.write("{:f} {:f}\n".format(x[i], y[i]))
pass
outfile.close()

if Ydes is not None:
	plt.ylabel(Ydes, fontsize=16)

if Xdes is not None:
	plt.xlabel(Xdes, fontsize=16)

if title is not None:
	plt.title(title)

# Hide the y numbers
plt.gca().axes.get_yaxis().set_ticks([])

# Calculate x ticks
xt = list(arange(pStart, pEnd + Xi, Xi))
plt.gca().axes.get_xaxis().set_ticks(xt)
l = plt.gca().axes.get_xticklabels()
newTickLabel = []
for val in xt:
	delta = abs(val - float(int(val)))
	if delta > 0.01 and delta < 0.99:
		newTickLabel.append("")
	else:
		if delta > 0.99:
			newTickLabel.append("{:d}".format(int(val) + 1))
		else:
			newTickLabel.append("{:d}".format(int(val) + 0))
		pass
	pass
pass
plt.gca().axes.set_xticklabels(newTickLabel)
plt.show()


