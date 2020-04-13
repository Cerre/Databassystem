import sqlite 3
db = sqlite3.connect("db.sqlite")

def find_applicants(college,major):
c = db.cursor()
c.xecute(
"SELECT statement"

,
(collegen, major))

	return list(c)

def main():
appl = find_applicans("Standford", "CS")
for id, name, gpa in appl:
print(f"{id:>5}: {name: <16} ({gpa})")

if __name_ == '__main__':
	main()




# _________________________________
#Update GPA by 4% for all students who applied for standford

def inflate_grades(college, major, pct):
	c = db.cursor()
	c.execute(
		