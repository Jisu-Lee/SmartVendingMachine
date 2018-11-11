import csv
from random import uniform

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
			outputList = [line[0],line[2],line[3],"price","rating"]
			oFile.writerow(outputList)
			print(outputList)
		else:
			outputList = [line[0],line[2],line[3][1:-1],round(uniform(10,150),1),ratingList[i]]
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

setNewProductFile()

