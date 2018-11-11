import csv
from random import uniform

inputFile = open('products.csv','r',encoding='"UTF-8"')
iFile = csv.reader(inputFile)
outputFile1 = open('newproducts.csv','w',encoding='"UTF-8"',newline='')
oFile1 = csv.writer(outputFile1)
outputFile2 = open('newratings.csv','w',encoding='"UTF-8"',newline='')
oFile2 = csv.writer(outputFile2)

def setNewProductFile():
	for i, line in enumerate(iFile):
		if(i == 0):
			outputList = [line[0],line[2],line[3],"price","rating"]
			oFile2.writerow(outputList)
			print(outputList)
		else:
			ratingList = []
			for user in range(100):
				if(uniform(0,100)>80):
					ratingList.append(str(user)+":"+str(round(uniform(0,5),1))+',')
				else:
					ratingList.append(str(user)+":"+str(0)+',')
			ratingListStr = ''.join(str(e) for e in ratingList)
			outputList = [line[0],line[2],line[3][1:-1],round(uniform(10,150),1),'['+ratingListStr[:-1]+']']
			oFile1.writerow(outputList)

def setNewRatingFile():
	for i, line in enumerate(iFile):
		if(i == 0):
			outputStr = ["User_id","Cos_id","rating"]
			oFile2.writerow(outputStr)
			print(outputStr)
		else:
			for user in range(100):
				if(uniform(0,100)>80):
					outputStr = [str(user),line[0],str(round(uniform(0,5),1))]
					oFile2.writerow(outputStr)
				

setNewRatingFile()

inputFile.close()
outputFile1.close()
outputFile2.close()