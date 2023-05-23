from random import shuffle
from tkinter import *   
import copy
import PIL
from PIL import Image
from PIL import Image as im
from numpy import asarray
import numpy as np
from PIL import Image as im
from PIL import ImageTk, Image  
from tkinter import filedialog 

import os

import sys
"""
SudokuGenerator
input: grid can be a 2-D matrix of a Sudoku puzzle to solve, or None to generate a new puzzle.
"""



array = np.zeros([720, 720, 3], dtype=np.uint8)#pentru imaginea stego







class SudokuGenerator:
	"""generates and solves Sudoku puzzles using a backtracking algorithm"""
	def __init__(self,grid=None):
		self.counter = 0
		#path is for the matplotlib animation
		self.path = []
		#if a grid/puzzle is passed in, make a copy and solve it
		if grid:
			if len(grid[0]) == 9 and len(grid) == 9:
				self.grid = grid
				self.original = copy.deepcopy(grid)
				self.solve_input_sudoku()
			else:
				print("input needs to be a 9x9 matrix")
		else:
			#if no puzzle is passed, generate one
			self.grid = [[0 for i in range(9)] for j in range(9)]
			self.generate_puzzle()
			self.original = copy.deepcopy(self.grid)
		
		
	def solve_input_sudoku(self):
		"""solves a puzzle"""
		self.generate_solution(self.grid)
		return

	def generate_puzzle(self):
		"""generates a new puzzle and solves it"""
		self.generate_solution(self.grid)
		#self.print_grid('full solution')
		self.remove_numbers_from_grid()
		#self.print_grid('with removed numbers')
		return

	def print_grid(self, grid_name=None):
		if grid_name:
			print(grid_name)
		for row in self.grid:
			print(row)
		return

	def test_sudoku(self,grid):
		"""tests each square to make sure it is a valid puzzle"""
		for row in range(9):
			for col in range(9):
				num = grid[row][col]
				#remove number from grid to test if it's valid
				grid[row][col] = 0
				if not self.valid_location(grid,row,col,num):
					return False
				else:
					#put number back in grid
					grid[row][col] = num
		return True

	def num_used_in_row(self,grid,row,number):
		"""returns True if the number has been used in that row"""
		if number in grid[row]:
			return True
		return False

	def num_used_in_column(self,grid,col,number):
		"""returns True if the number has been used in that column"""
		for i in range(9):
			if grid[i][col] == number:
				return True
		return False

	def num_used_in_subgrid(self,grid,row,col,number):
		"""returns True if the number has been used in that subgrid/box"""
		sub_row = (row // 3) * 3
		sub_col = (col // 3)  * 3
		for i in range(sub_row, (sub_row + 3)): 
			for j in range(sub_col, (sub_col + 3)): 
				if grid[i][j] == number: 
					return True
		return False

	def valid_location(self,grid,row,col,number):
		"""return False if the number has been used in the row, column or subgrid"""
		if self.num_used_in_row(grid, row,number):
			return False
		elif self.num_used_in_column(grid,col,number):
			return False
		elif self.num_used_in_subgrid(grid,row,col,number):
			return False
		return True

	def find_empty_square(self,grid):
		"""return the next empty square coordinates in the grid"""
		for i in range(9):
			for j in range(9):
				if grid[i][j] == 0:
					return (i,j)
		return

	def solve_puzzle(self, grid):
		"""solve the sudoku puzzle with backtracking"""
		for i in range(0,81):
			row=i//9
			col=i%9
			#find next empty cell
			if grid[row][col]==0:
				for number in range(1,10):
					#check that the number hasn't been used in the row/col/subgrid
					if self.valid_location(grid,row,col,number):
						grid[row][col]=number
						if not self.find_empty_square(grid):
							self.counter+=1
							break
						else:
							if self.solve_puzzle(grid):
								return True
				break
		grid[row][col]=0  
		return False

	def generate_solution(self, grid):
		"""generates a full solution with backtracking"""
		number_list = [1,2,3,4,5,6,7,8,9]
		for i in range(0,81):
			row=i//9
			col=i%9
			#find next empty cell
			if grid[row][col]==0:
				shuffle(number_list)      
				for number in number_list:
					if self.valid_location(grid,row,col,number):
						self.path.append((number,row,col))
						grid[row][col]=number
						if not self.find_empty_square(grid):
							return True
						else:
							if self.generate_solution(grid):
								#if the grid is full
								return True
				break
		grid[row][col]=0  
		return False

	def get_non_empty_squares(self,grid):
		"""returns a shuffled list of non-empty squares in the puzzle"""
		non_empty_squares = []
		for i in range(len(grid)):
			for j in range(len(grid)):
				if grid[i][j] != 0:
					non_empty_squares.append((i,j))
		shuffle(non_empty_squares)
		return non_empty_squares

	def remove_numbers_from_grid(self):
		"""remove numbers from the grid to create the puzzle"""
		#get all non-empty squares from the grid
		non_empty_squares = self.get_non_empty_squares(self.grid)
		non_empty_squares_count = len(non_empty_squares)
		rounds = 3
		while rounds > 0 and non_empty_squares_count >= 17:
			#there should be at least 17 clues
			row,col = non_empty_squares.pop()
			non_empty_squares_count -= 1
			#might need to put the square value back if there is more than one solution
			removed_square = self.grid[row][col]
			self.grid[row][col]=0
			#make a copy of the grid to solve
			grid_copy = copy.deepcopy(self.grid)
			#initialize solutions counter to zero
			self.counter=0      
			self.solve_puzzle(grid_copy)   
			#if there is more than one solution, put the last removed cell back into the grid
			if self.counter!=1:
				self.grid[row][col]=removed_square
				non_empty_squares_count += 1
				rounds -=1
		return



def convert_matrix_to_base_9():
	for i in range(0,9):
		for j in range(0,9):
			sudoku_matrix[i][j]=sudoku_matrix[i][j]-1


def convert_matrix_to_reference_matrix():
	for i in range (0,27):
		for j in range(0,27):
			if i>8 or j >8:
				M[i][j]=sudoku_matrix[i%9][j%9]
			if i<=8 and j<=8:
				M[i][j]=sudoku_matrix[i][j]

def convert_message_from_text_to_decimal():
	for i in range(0, len(content)):
		for j in range(0,len(content[i])):
			if(ord(content[i][j]) <= 127):
				secret_message_in_base_10.append(ord(content[i][j]))


def convert_message_from_decimal_to_base_9():
	#print(secret_message_in_base_10)
	for i in range(0,len(secret_message_in_base_10)):
		message=secret_message_in_base_10[i]
		lista_caracter=[]
		if secret_message_in_base_10[i]<=80:
			secret_message_in_base_9.append(0)	
			while message!=0:
				lista_caracter.append(message%9)
				message=int(message//9)
			lista_caracter.reverse()
			secret_message_in_base_9.append(lista_caracter[0])
			secret_message_in_base_9.append(lista_caracter[1])
		else:
			while message!=0:
				lista_caracter.append(message%9)
				message=int(message//9)
			lista_caracter.reverse()
			secret_message_in_base_9.append(lista_caracter[0])
			secret_message_in_base_9.append(lista_caracter[1])
			secret_message_in_base_9.append(lista_caracter[2])
	#print(secret_message_in_base_10)
	#print(secret_message_in_base_9)
	#print(x)
	for i in secret_message_in_base_10:
		if i < 9:
			print(1)
	#print("A",len(secret_message_in_base_10))
	#print("B",len(secret_message_in_base_9))
	


def convertire_lista_pixeli():
	for i in range(0,720):
		for j in range(0,720):
			lista_pixeli.append(image_array[i][j][0])
			lista_pixeli.append(image_array[i][j][1])
			lista_pixeli.append(image_array[i][j][2])


def creare_candidates():
	#print(len(lista_pixeli))
	lungime=(len(secret_message_in_base_9)*2)	#lungimea mesajul ori 2 pentru ca luam cate 2 perechi din lista de pixeli
	#print("C",lungime)
	contor_mesaj=0							#primul element din mesajul secret
	posx_ceb=0
	posy_ceb=0
	for p in range(0,lungime,2):			#aici vom modifica dimensiunea in functie de mesajul secret
		PIx=(lista_pixeli[p]%9)+9
		PIy=(lista_pixeli[p+1]%9)+9
		#print(p)
		#cream CEH 
		for i in range(0,9):
			pos=(i+4)%9
			CEH[pos]=M[PIx][PIy]
			PIy=(PIy+1)%9+9
		#cream CEV
		for j in range(0,9):
			pos=(j+4)%9
			CEV[pos]=M[PIx][PIy]
			PIx=(PIx+1)%9+9
		#cream CEB
		#Cazul 1 dreapta jos
		lista_cutie=[]
		flag=1 				#verficam daca sunt elemente unice
		ok=0 				#contor verificare casuta corecta
		for i in range(0,3):
			for j in range(0,3):
				lista_cutie.append(M[PIx+i][PIy+j])
		flag = len(set(lista_cutie)) == len(lista_cutie)
		if flag==1:
			k=0
			for i in range(0,3):
				for j in range(0,3):
					CEB[i][j]=lista_cutie[k]
					k=k+1
			ok=1
			posx_ceb=PIx
			posy_ceb=PIy
		#Cazul 2 dreapta sus
		if ok==0:
			PIx=PIx-2
			lista_cutie=[]
			flag=0
			for i in range(0,3):
				for j in range(0,3):
					lista_cutie.append(M[PIx+i][PIy+j])
			flag = len(set(lista_cutie)) == len(lista_cutie)
			if flag==1:
				k=0
				for i in range(0,3):
					for j in range(0,3):
						CEB[i][j]=lista_cutie[k]
						k=k+1
				ok=1
				posx_ceb=PIx
				posy_ceb=PIy
		#Cazul 3 stanga sus
		if ok==0:
			PIy=PIy-2
			lista_cutie=[]
			flag=0
			for i in range(0,3):
				for j in range(0,3):
					lista_cutie.append(M[PIx+i][PIy+j])
			flag = len(set(lista_cutie)) == len(lista_cutie)
			if flag==1:
				k=0
				for i in range(0,3):
					for j in range(0,3):
						CEB[i][j]=lista_cutie[k]
						k=k+1
				ok=1
				posx_ceb=PIx
				posy_ceb=PIy
		#Cazul 4 stanga jos
		if ok==0:
			PIx=PIx+2
			lista_cutie=[]
			flag=0
			for i in range(0,3):
				for j in range(0,3):
					lista_cutie.append(M[PIx+i][PIy+j])
			flag = len(set(lista_cutie)) == len(lista_cutie)
			if flag==1:
				k=0
				for i in range(0,3):
					for j in range(0,3):
						CEB[i][j]=lista_cutie[k]
						k=k+1
				ok=1
				posx_ceb=PIx
				posy_ceb=PIy
		PIx=(lista_pixeli[p]%9)+9
		PIy=(lista_pixeli[p+1]%9)+9
		#Cautam Si in CEH
		for i in range(0,9):
			if CEH[i]==secret_message_in_base_9[contor_mesaj]:
				DH=(i-4)
		#Cautam Si in CEV
		for i in range(0,9):
			if CEV[i]==secret_message_in_base_9[contor_mesaj]:
				DV=(i-4)
		#Cautam Si in CEB
		for i in range(0,3):
			for j in range(0,3):
				if M[i+posx_ceb][j+posy_ceb]==secret_message_in_base_9[contor_mesaj]:
					posx=(i+posx_ceb)
					posy=(j+posy_ceb)
		SQX=(posx-(PIx))
		SQY=(posy-(PIy))
		SQD=SQX+SQY
		lista_candidati=[]
		lista_candidati.append(abs(DV))
		lista_candidati.append(abs(DH))
		if(ok==1):
			lista_candidati.append(abs(SQD))
		else:
			SQD=100		#aici introducem o valoare mare pentru SQD pentru a nu fi cel mai mic candidat din lista, si pentru a modifica aiurea pixelii
		ok1=1
		if min(lista_candidati)==abs(DV) and ok1==1:
			lista_pixeli[p]=lista_pixeli[p]+DV
			ok1=0
		if min(lista_candidati)==abs(SQD) and ok1==1:
			lista_pixeli[p]=lista_pixeli[p]+SQX
			lista_pixeli[p+1]=lista_pixeli[p+1]+SQY
			ok1=0
		if min(lista_candidati)==abs(DH) and ok1==1:
			lista_pixeli[p+1]=lista_pixeli[p+1]+DH
			ok1=0
		##########
		if lista_pixeli[p]<0:
			lista_pixeli[p]=lista_pixeli[p]+9
		if lista_pixeli[p]>255:
			lista_pixeli[p]=lista_pixeli[p]-9
		if lista_pixeli[p+1]<0:
			lista_pixeli[p+1]=lista_pixeli[p+1]+9
		if lista_pixeli[p+1]>255:
			lista_pixeli[p+1]=lista_pixeli[p+1]-9
		contor_mesaj=contor_mesaj+1
	contor_terminare_ascundere_mesaj=1
	print("Mesaj ascuns cu succes",contor_terminare_ascundere_mesaj)
	return contor_terminare_ascundere_mesaj


def creare_pixeli_imagine():
	r=0
	for i in range(0,720):
		for j in range(0,720):
			array[i][j][0]=(lista_pixeli[r])
			r=r+1
			array[i][j][1]=(lista_pixeli[r])
			r=r+1
			array[i][j][2]=(lista_pixeli[r])
			r=r+1

def convertire_lista_pixeli_stego():
	for i in range(0,720):
		for j in range(0,720):
			lista_pixeli_stego.append(array[i][j][0])
			lista_pixeli_stego.append(array[i][j][1])
			lista_pixeli_stego.append(array[i][j][2])

def extractia_mesajului():
	lungime=len(secret_message_in_base_9)*2
	for p in range(0,lungime,2):
		extracted_message.append(M[lista_pixeli_stego[p]%9+9][lista_pixeli_stego[p+1]%9+9])
	#print("D",len(extracted_message))

def verificare_mesaj_extras(secret_message_in_base_9,extracted_message):
	ok=0
	for i in range(0,len(secret_message_in_base_9)):
		if(secret_message_in_base_9[i]!=extracted_message[i]):
			ok=ok+1
	if ok==0:
		print("OK")
	else:
		print("NOT OK",ok)

def export_extracted_message():
	with open("output.txt","a") as file:
		for i in range(0, len(extracted_message),3):
			base_9=0
			if(extracted_message[i]==0):
				base_9=extracted_message[i+1]*9+extracted_message[i+2]
			else:
				base_9=extracted_message[i]*81+extracted_message[i+1]*9+extracted_message[i+2]
			file.write(chr(base_9))

def hidding_message():
	creare_candidates()
	creare_pixeli_imagine()
	img = Image.fromarray(array)
	img.save('teste.png')

def extract_message():
	convertire_lista_pixeli_stego()
	extractia_mesajului()
	export_extracted_message()
	verificare_mesaj_extras(secret_message_in_base_9,extracted_message)





new_puzzle = SudokuGenerator()
solved = SudokuGenerator(grid=new_puzzle.grid)
#print(new_puzzle.grid)

y=0
sudoku_matrix = solved.grid.copy()
M = [ [ 0 for i in range(27) ] for j in range(27) ]        #sudoku_matrix_reference
secret_message_in_base_10 = []
secret_message_in_base_9 = []
secret_message_in_base_10 = []
secret_message_in_base_9 = []

extracted_message=[]
lista_pixeli=[]
lista_pixeli_stego=[]
CEH=[0,0,0,0,0,0,0,0,0]
CEV=[0,0,0,0,0,0,0,0,0]
CEB=[[0,0,0],
 	 [0,0,0],
	 [0,0,0]]

h = open('secret_message.txt', 'r')
 
# Reading from the file
content = h.readlines()

#print(content[0])

'''
sudoku_matrix=[ [4,7,8,3,1,5,6,2,0],
			    [5,2,0,4,6,8,7,3,1],
			    [1,3,6,7,2,0,8,5,4],
			    [8,0,7,2,5,1,4,6,3],
			    [2,6,1,8,3,4,5,0,7],
			    [3,5,4,0,7,6,2,1,8],
			    [0,4,2,6,8,3,1,7,5],
			    [6,8,5,1,0,7,3,4,2],
			    [7,1,3,5,4,2,0,8,6]]'''
#print(sudoku_matrix)


convert_matrix_to_base_9()
#for i in range(0,9):
#	print(sudoku_matrix[i])
convert_matrix_to_reference_matrix()
#for i in range(27):
#	print(sudoku_matrix_reference[i])
#print(secret_message)
#secret_message = convert_message_to_base_9(secret_message)
convert_message_from_text_to_decimal()
convert_message_from_decimal_to_base_9()

image = PIL.Image.open("cover.jpg")
image_array = np.array(image)
#print(image_array)
convertire_lista_pixeli()




 




# create a tkinter window



root = Tk()     


def destroy(btn):
    #btn.pack_forget()
    btn['state'] = 'disabled'

def UploadAction(event=None):
    btn = Button(root, text = 'Extract message !', bd = '10', command =  extract_message)
    btn.place(x=500, y=250)


# Open window having dimension 100x100
root.title("Welcome to Message hidding")
root.geometry('800x400')



root.configure(background='pink')

img =Image.open('xerion.png')
bg = ImageTk.PhotoImage(img)


# Add image
label = Label(root, image=bg)
label.place(x = 0,y = 0)


# Create a Button
btn = Button(root, text = 'Hide message !', bd = '10',command = hidding_message)
btn.place(x=100, y=150)

btn1 = Button(root, text = 'Extract message !', bd = '10',command= extract_message)
btn1.place(x=600, y=150)



'''
hidding_button = Button(root, text = 'Hide message !', bd = '10', command =  lambda:[UploadAction(), destroy(hidding_button)])
hidding_button.pack()

extract_button = Button(root, text = 'Extract message !', bd = '10', command =  lambda:[UploadAction(), destroy(extract_button)])
extract_button.pack()
'''






btn2 = Button(root, text = 'Exit !', bd = '5',command = root.destroy)
 
# Set the position of button on the top of window.
btn2.pack(side = 'bottom') 

#print(secret_message_in_base_9)
#print(extracted_message)

root.mainloop()
