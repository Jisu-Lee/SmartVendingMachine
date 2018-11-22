import csv
from random import uniform
from random import randint
def setNewProductFile():
	pinputFile = open('products.csv','r',encoding='"UTF-8"')
	pFile = csv.reader(pinputFile)
	rinputFile = open('newratings.csv','r',encoding='"UTF-8')
	rFile = csv.reader(rinputFile)
	outputFile = open('newproducts.csv','w',encoding='"UTF-8"',newline='')
	oFile = csv.writer(outputFile)

	ratingList = [0 for i in range(11000)]
	ratingCountList = [0 for i in range(11000)]
	for i,line in enumerate(rFile):
		if(i is not 0):
			num = int(line[1])
			ratingList[num] = str(float(ratingList[num])+float(line[2]))
			ratingCountList[num] = str(int(ratingCountList[num])+1)
	
	for i in range(len(ratingList)):
		if ratingCountList[i] is 0:
			print(i)
		else:
			ratingList[i] = str(round((float(ratingList[i])/int(ratingCountList[i])),1))

	for i, line in enumerate(pFile):
		if(i == 0):
			outputList = [line[0],line[2],line[3],"skin_type","price","rating"]
			oFile.writerow(outputList)
		else:
			rnum = round(uniform(0.5,3.5),0)
			skin_type = ''
			if(rnum == 1): 
				skin_type = 'oily'
			elif(rnum == 2):
				skin_type = 'dry'
			else:
				skin_type = 'sensitive'
			outputList = [line[0],line[2],line[3][1:-1],skin_type,round(uniform(10,150),1),ratingList[i]]
			oFile.writerow(outputList)
	
	pinputFile.close()
	rinputFile.close()
	outputFile.close()

def setNewRatingFile():
	inputFile = open('products.csv','r',encoding='"UTF-8"')
	iFile = csv.reader(inputFile)
	outputFile = open('newratings.csv','w',encoding='"UTF-8"',newline='')
	oFile = csv.writer(outputFile)

	for i, line in enumerate(iFile):
		if(i == 0):
			outputStr = ["User_id","Cos_id","rating"]
			oFile.writerow(outputStr)
			print(outputStr)
		else:
			for user in range(100):
				if(uniform(0,100)>95):
					outputStr = [str(user),line[0],str(round(uniform(0,5),1))]
					oFile.writerow(outputStr)
	
	inputFile.close()
	outputFile.close()				

def setNewUserFile():
	rinputFile = open('newuser.csv','r',encoding='"UTF-8"')
	rFile = csv.reader(rinputFile)
	outputFile = open('newusers.csv','w',encoding='"UTF-8"',newline='')
	oFile = csv.writer(outputFile)

	for i, line in enumerate(rFile):
		if(i == 0):
			outputList = [line[0],line[1],line[2],"user_id","password","birthyear","gender"]
			oFile.writerow(outputList)
		else:
			birth_year = round(uniform(1990,1999),0)
			pw = round(uniform(1000,9999),0)
			gnum = round(uniform(0,1),0)
			gender = ''
			if gnum == 0:
				gender = 'male'
			else:
				gender = 'female'
			outputList = [line[0],line[1],line[2],line[1],pw,birth_year,gender]
			oFile.writerow(outputList)
	rinputFile.close()
	outputFile.close()

def setNewStockFile():
	outputFile = open('newstock.csv','w',encoding='"UTF-8"',newline='')
	oFile = csv.writer(outputFile)
	for i in range(11):
		if i == 0:
			outputFileList = ['vending_id','cosmetic_id','stock']
			oFile.writerow(outputFileList)
		else:
			stock = {}
			for j in range(30):
				rnum = randint(1,120)
				if rnum not in stock:
					snum = round(uniform(0,15),0)
					stock[rnum] = snum
					oFile.writerow([i,rnum,snum])
				else:
					j = j - 1
	outputFile.close()
					
def modifyProductFile():
	pinputFile = open('newproducts.csv','r',encoding='"UTF-8"', errors='ignore')
	pFile = csv.reader(pinputFile)
	outputFile = open('newproduct_s.csv','w',encoding='"UTF-8"',newline='')
	oFile = csv.writer(outputFile)

	for i, line in enumerate(pFile):
		oFile.writerow(line)
	
	pinputFile.close()
	outputFile.close()

modifyProductFile()