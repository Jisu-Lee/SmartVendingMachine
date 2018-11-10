import csv
from random import uniform

inputFile = open('products.csv','r',encoding='"ISO-8859-1"')
iFile = csv.reader(inputFile)
outputFile = open('newproducts.csv','w',encoding='"UTF-8"')
oFile = csv.writer(outputFile)

for i, line in enumerate(iFile):
	if(i == 0):
		outputList = [line[0],line[2],line[3],"price","rating_list"]
		oFile.writerow(outputList)
		print(outputList)
	else:
		ratingList = []
		for user in range(100):
			if(uniform(0,100)>30):
				ratingList.append(str(user)+":"+str(round(uniform(0,5),1))+',')
			else:
				ratingList.append(str(user)+":"+str(0)+',')
		ratingListStr = ''.join(str(e) for e in ratingList)
		outputList = [line[0],line[2],line[3][1:-1],round(uniform(10,150),1),'['+ratingListStr[:-1]+']']
		oFile.writerow(outputList)

inputFile.close()
outputFile.close()