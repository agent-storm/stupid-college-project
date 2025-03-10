import sys
import json
import random
import qrcode
import hashlib
import datetime

# from config import mycol

# VERIFICATION_URL = "http://localhost:8080/?id="
VERIFICATION_URL = "http://127.0.0.1:5000/verify/"

class Login:

	MANF = ""
	LOGGEDIN = False
	MANUFACTURERS = {
		"DRREDDY": "password123",
		"LUPIN": "hello123",
		"KOTLIN": "qwerty",
		"ADMIN": "qwerty"
	}

	def main(self):
		loginid = input("Enter your login id:\t")
		password = input("Enter your password:\t")

		if loginid in self.MANUFACTURERS.keys():
			if self.MANUFACTURERS[loginid] == password:
				self.LOGGEDIN = True
				self.MANF = loginid

	def isLoggedIn(self):
		if self.LOGGEDIN:
			print("\nWelcome to the blockchain world\n")
		else:
			sys.exit("Please login to experience the blockchain world")

	def getManf(self):
		return self.MANF


class BlockChain:

	def __init__(self):
		self.department = ""
		self.student_name = ""
		self.academic_year = ""
		self.regnum = ""
		self.joining_date = ""
		self.end_date = ""
		self.mark = ""
		self.certfile = ""
		self.personality = ""
		

	def actions(self):
		choice = input("Enter 1 to ADD item or 2 to Verify BlockChain\n")

		if choice == "1":
			self.department = input("Enter the department:\n")
			self.student_name = input("Enter student name:\n")
			self.academic_year = input("Enter academic year:\n")
			self.regnum = input("Enter reg number:\n")
			self.joining_date= input("Enter joining date:\n")
			self.end_date = input("Enter end date:\n")
			self.mark= input("Enter student mark:\n")
			self.certfile = input("uploed certificate file:\n")
			self.personality= input("Enter student infomation:\n")
			self.newCertificate()
		
		elif choice == "2":
			if self.isBlockchainValid():
				sys.exit("BlockChain is valid")
			else:
				sys.exit("BlockChain is invalid")

		else:
			sys.exit("Logged out successfully")

	
	def newCertificate(self):
		data = {
		"Department": self.department ,
		"Studentname": self.student_name ,
		"AcademicYear": self.academic_year,
		"RegNum": self.regnum,
		"JoiningDate": self.joining_date,
		"EndDate": self.end_date ,
		"Mark": self.mark,
		"CertificateFile": self.certfile ,
		"Personality": self.personality
		}

		proHash = hashlib.sha256(str(data).encode()).hexdigest()
		print(proHash)
		data["hash"] = proHash

		# x = mycol.insert_one(data)
		
		self.createBlock(data)

		imgName  = self.imgNameFormatting()
		self.createQR(proHash, imgName)

	def addCertificate(
		self,
		department, 
		student_name, 
		academic_year, 
		regnum, 
		joining_date, 
		end_date, 
		mark,
		certfile,
		personality 
	):
		self.student_name = student_name
		data = {
			"Department":department ,
			"Studentname":student_name ,
			"AcademicYear":academic_year,
			"RegNum":regnum,
			"JoiningDate":joining_date,
			"EndDate":end_date ,
			"Mark":mark,
			"CertificateFile":certfile ,
			"Personality":personality
		}

		proHash = hashlib.sha256(str(data).encode()).hexdigest()
		print(proHash)
		data["hash"] = proHash

		# x = mycol.insert_one(data)
		
		self.createBlock(data)

		imgName  = self.imgNameFormatting()
		self.createQR(proHash, imgName)


	def createBlock(self, data):

		if self.isBlockchainValid():
			blocks = []
			for block in open('./NODES/N1/blockchain.json', 'r'):
				blocks.append(block)
			print(blocks[-1], "jsdata===========")

			preBlock = json.loads(blocks[-1])

			index = preBlock["index"] + 1
			preHash = hashlib.sha256(str(preBlock).encode()).hexdigest()

		transaction = {
			'index': index,
			'proof': random.randint(1, 1000),
			'previous_hash': preHash,
			# 'hash': proHash,
			'timestamp': str(datetime.datetime.now()),
			'data': str(data),
		}

		with open("./NODES/N1/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N2/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N3/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))
		with open("./NODES/N4/blockchain.json", "a") as file:
			file.write("\n" + json.dumps(transaction))

		# currHash = hashlib.sha256(str(transaction).encode()).hexdigest()
		# imgName  = self.imgNameFormatting()

		# self.createQR(currHash, imgName)
		return


	def createQR(self, hashc, imgName):
		img = qrcode.make(VERIFICATION_URL + hashc)
		img.save("./static/QRcodes/" + imgName)

		
		return


	def imgNameFormatting(self):
		dt = str(datetime.datetime.now())
		dt = dt.replace(" ", "_").replace("-", "_").replace(":", "_")
		return self.student_name+".png"


	def isBlockchainValid(self):
		with open("./NODES/N1/blockchain.json", "r") as file:
			n1_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n1_hash)
		with open("./NODES/N2/blockchain.json", "r") as file:
			n2_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n2_hash)
		with open("./NODES/N3/blockchain.json", "r") as file:
			n3_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n3_hash)
		with open("./NODES/N4/blockchain.json", "r") as file:
			n4_hash = hashlib.sha256(str(file.read()).encode()).hexdigest()
			print(n4_hash)

		if n1_hash == n2_hash == n3_hash == n4_hash:
			return True
		else:
			return False


if __name__ == "__main__":
	lof = Login()
	lof.main()
	lof.isLoggedIn()

	LOGGEDINUSER = lof.getManf()

	bc = BlockChain()
	bc.actions()