import requests
import re
import json

URL = "http://59.144.74.15/scheme16/studentresult/details.asp"

CLASS_CAPACITY = 58
dele = []
dele1 = []

dele.append(r"<[^>]*>")
dele.append(r"\.auto-style\d")
dele.append("{")
dele.append("}")
dele.append("font-family:(.*);")
dele.append("color:(.*);")
dele.append("font-size:(.*);")
dele.append("Semester : ")
dele.append("Sr. No&nbsp;")
dele.append("Subject Code")
dele.append("Subject")
dele.append("Sub Point")
dele.append("Grade")
dele.append("Sub GP")
dele.append("NATIONAL INSTITUTE OF TECHNOLOGY HAMIRPUR, \[HP\]")
dele.append("text-align: center;")
dele.append("Result Details")

dele2=r"(\n)(\s)*(\n)*|\r|\t"

dele1.append(r"  ")

class_data = {}
ROLLNO = "16MI5%02d" 

for i in range(1,CLASS_CAPACITY+1):
	if i==17:
		continue
	rollno = ROLLNO%i
	r = requests.post(url=URL,data={'RollNumber':rollno})
	h = r.content.decode()

	for i in dele:
		h=re.sub(i,"",h)
	for i in dele1:
		for j in range(50):
			h=re.sub(i,"",h)
	for j in range(50):
		h=re.sub(dele2,"\n",h)

	h.partition("Name")[2]

	# print(h)
	student_data={}
	data_list = h.split("\n")
	student_data['Name'] = data_list[data_list.index("Name")+1]
	student_data['Roll No'] = data_list[data_list.index("Roll Number")+1]
	i=data_list.index("Roll Number")+1
	s = 0
	sem = {}
	while i<len(data_list):
		# print(data_list[i])
		if re.match(r"S\d\d", str(data_list[i])):
			if len(sem) != 0:
				student_data['Semester ' + str(s)] = sem
			s=(data_list[i][-2]*10) + data_list[i][-1]
			sem = {}
			i+=1
		elif s!=0:
			if re.match(r"Note(.)*", data_list[i]):
				student_data['Semester ' + str(s)] = sem
				break
			elif data_list[i]!='SGPI':
				sub = {}
				sub['Subject Name'] = data_list[i+1]
				sub['Subject Code'] = data_list[i+2]
				sub['Sub Point'] = int(data_list[i+3])
				sub['Pointer'] = int(data_list[i+5])/sub['Sub Point']
				sem[sub['Subject Code']] = sub
				i=i+6
			else:
				i+=8
		else:
			i+=1
	class_data[student_data['Roll No']]=student_data
class_data = json.dumps(class_data)
parsed = json.loads(class_data)
print(json.dumps(parsed, indent = 4, sort_keys = True))

