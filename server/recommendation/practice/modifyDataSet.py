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
	pinputFile = open('re_small_products.csv','r',encoding='"UTF-8"')
	iFile = csv.reader(pinputFile)
	outputFile = open('re_newstock.csv','w',encoding='"UTF-8"',newline='')
	oFile = csv.writer(outputFile)
	
	cos_dry_cre = []
	cos_dry_moi = []
	cos_dry_sun = []
	cos_oily_cre = []
	cos_oily_moi = []
	cos_oily_sun = []
	cos_sen_cre = []
	cos_sen_moi = []
	cos_sen_sun = []

	for i, line in enumerate(iFile):	
		if line[3] == "dry":
			if line[2] == "CREAM":
				cos_dry_cre.append(line)
			elif line[2] == "MOSITURIZER":
				cos_dry_moi.append(line)
			elif line[2] == "SUNSCREEN":
				cos_dry_sun.append(line)
		elif line[3] == "oily":
			if line[2] == "CREAM":
				cos_oily_cre.append(line)
			elif line[2] == "MOSITURIZER":
				cos_oily_moi.append(line)
			elif line[2] == "SUNSCREEN":
				cos_oily_sun.append(line)
		elif line[3] == "sensitive":
			if line[2] == "CREAM":
				cos_sen_cre.append(line)
			elif line[2] == "MOSITURIZER":
				cos_sen_moi.append(line)
			elif line[2] == "SUNSCREEN":
				cos_sen_sun.append(line)
		else:
			print("error")
	
	for i in range(11):
		if i == 0:
			outputFileList = ['vending_id','cosmetic_id','stock']
			oFile.writerow(outputFileList)
		else:
			if i == 1:
				write_file(cos_dry_cre, cos_dry_moi, cos_dry_sun, i, oFile, 1)
			elif i == 2:
				write_file(cos_dry_cre, cos_dry_moi, cos_dry_sun, i, oFile, 2)
			elif i == 3:
				write_file(cos_oily_cre, cos_oily_moi, cos_oily_sun, i, oFile, 1)
			elif i == 4:
				write_file(cos_oily_cre, cos_oily_moi, cos_oily_sun, i, oFile, 2)
			elif i == 5:
				write_file(cos_sen_cre, cos_sen_moi, cos_sen_sun, i, oFile, 1)
			elif i == 6	:
				write_file(cos_sen_cre, cos_sen_moi, cos_sen_sun, i, oFile, 2)
			elif i == 7 :
				write_file(cos_dry_cre, cos_dry_moi, cos_dry_sun, i, oFile, 1)
			elif i == 8:
				write_file(cos_dry_cre, cos_dry_moi, cos_dry_sun, i, oFile, 2)
			elif i == 9:
				write_file(cos_oily_cre, cos_oily_moi, cos_oily_sun, i, oFile, 1)
			elif i == 10:
				write_file(cos_oily_cre, cos_oily_moi, cos_oily_sun, i, oFile, 2)
	pinputFile.close()
	outputFile.close()

def write_file(cos_cre, cos_moi, cos_sun, i, file, pos):
	length = find_highest(len(cos_cre), len(cos_moi), len(cos_sun))
	print("len : ", len(cos_cre),len(cos_moi),len(cos_cre))
	print(length)
	for j in range(int(round(length/2,0))):
		num = j 
		if pos == 2:
			num = num + int(round(length/2,0))

		if(num < len(cos_cre)):
			file.writerow([i,cos_cre[num][0],round(uniform(3,15),0)])
		else:
			num = num-len(cos_cre)
			if(num-len(cos_cre) > len(cos_cre)):
				num = num - len(cos_cre)
			if(num < 0):
				num = j
			file.writerow([i,cos_cre[num][0],round(uniform(3,15),0)])

		if(num < len(cos_moi)):
			file.writerow([i,cos_moi[num][0],round(uniform(3,15),0)])
		else:
			num = num-len(cos_moi)
			if(num-len(cos_moi) > len(cos_moi)):
				num = num - len(cos_moi)
			if(num < 0):
				num = j	
			file.writerow([i,cos_moi[num][0],round(uniform(3,15),0)])
		
		if(num < len(cos_sun)):
			file.writerow([i,cos_sun[num][0],round(uniform(3,15),0)])
		else:
			num = num-len(cos_sun)
			if(num-len(cos_sun) > len(cos_sun)):
				num = num - len(cos_sun)
			if(num < 0):
				num = j	
			file.writerow([i,cos_sun[num][0],round(uniform(3,15),0)])

def find_highest(one, two, three):
	answer = one
	if two > answer:
		answer = two
	if three > answer:
		answer = three
	return answer

def modifyProductFile():
	pinputFile = open('newvendings.csv','r',encoding='"UTF-8"', errors='ignore')
	pFile = csv.reader(pinputFile)
	outputFile = open('newvending_s.csv','w',encoding='"UTF-8"',newline='')
	oFile = csv.writer(outputFile)

	for i, line in enumerate(pFile):
		print(line)
		oFile.writerow(line)
	
	pinputFile.close()
	outputFile.close()

def setRenameProductFile():
	inputFile = open('small_products.csv','r',encoding='"UTF-8"')
	iFile = csv.reader(inputFile)
	outputFile = open('re_small_products.csv','w',encoding='"UTF-8"',newline='')
	oFile = csv.writer(outputFile)

	save_line = []
	count = 0
	for i, line in enumerate(iFile):	
		if(i<=45):
			if(i is not 0):
				save_line.append(line)
				count = count+1
		elif(i<=90):
			line = [line[0],save_line[i-46][1].replace("cream","moisturize"),line[2],line[3],line[4],line[5]]
		else:
			line = [line[0],save_line[i-91][1].replace("cream","sunblock"),line[2],line[3],line[4],line[5]]
		oFile.writerow(line)
	print(count)
	inputFile.close()
	outputFile.close()				


setNewStockFile()