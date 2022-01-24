from sys import exit
from time import sleep

try:
    import keyboard
except ModuleNotFoundError:
    print("Could not import \"keyboard\" library (pip install keyboard)")
    exit()

start_hotkey = "F7"
message_send_delay = 2
key_press_delay = 0.02

def send_message(string):
    # It's not about money, it's about sending a message
    keyboard.write(string, delay = key_press_delay)
    sleep(key_press_delay * 2)
    keyboard.send("enter")
    sleep(message_send_delay)

def calculate_earnings(employee_list):
    earnings = 0
    rarity_multiplier = {"L":2, "R":1.5, "U":1.25, "C":1}
    for emp in employee_list:
        earnings += int(emp[3]) * rarity_multiplier[emp[2]]
    return int(earnings)

# Read the employees text file
try:
    file = open("employees.txt", "r")
    text_lines = file.readlines()
    file.close()
except FileNotFoundError:
    print("Employees file does not exist")
    exit()
try:
    floors = int(text_lines[1].rstrip())
except IndexError:
    print("Employees file not set up correctly")
    exit()
except ValueError:
    print("Number of floors is not a number")
    exit()

# Extract a list of employees
employees = []
for i in range(len(text_lines) - 4):
    if text_lines[i + 4] != "":
        employee = text_lines[i + 4].rstrip().split(" ")
        if len(employee) < 4:
            print("Not all employees are set up correctly")
            print("Each employee needs a first name, last name, rarity, and assigned floor (0 for unassigned)")
            print("e.g. Guy Day U 4")
            exit()
        else:
            # Convert assigned floor to int
            try:
                employee[3] = int(employee[3])
            except ValueError:
                print("{} {}'s assigned floor is not a number".format(employee[0], employee[1]))
        employees.append(employee)
employees.sort()

# Sort employees by rarity, rarest first
sorted_employees = []
try:
    for letter in ["L", "R", "U", "C"]:
        for i in range(len(employees)):
            if employees[i][2] == letter:
                sorted_employees.append(employees[i])
except IndexError:
    print("Not all employees have first & last names and rarities")
    exit()

# If floors != employees
if floors > len(sorted_employees):
    print("More floors than employees, some floors will remain empty")
elif floors < len(sorted_employees):
    print("More employees than floors, some employees will remain unassigned")

# Determine which floor each employee will end up on
for i in range(len(sorted_employees)):
    sorted_employees[i].append(max(floors - i, 0))

# Calculate earnings pre-shuffle
earnings_before = calculate_earnings(sorted_employees)

# Wait until ready to begin typing
print("Ready to shuffle employees, place text cursor in Discord channel and press " + start_hotkey)
keyboard.wait(start_hotkey)

# Move employees
print("\nAssigning all employees to optimal floors")
for i in range(len(sorted_employees)):
    this_emp = sorted_employees[i]
    if this_emp[3] == this_emp[4]:
        print("{} {} already on the correct floor, skipping".format(this_emp[0], this_emp[1]))
    elif this_emp[4] == 0:
        print("Unassigning {} {}".format(this_emp[0], this_emp[1]))
        send_message(">tower employees unassign {} {} {}".format(this_emp[0], this_emp[1]))
        this_emp[3] = this_emp[4]
    else:
        swapped = False
        for j in range(len(sorted_employees)):
            if sorted_employees[j][3] == this_emp[4] and j != i:
                other_emp = sorted_employees[j]
                print("Swapping {} {} and {} {}".format(this_emp[0], this_emp[1], other_emp[0], other_emp[1]))
                send_message(">tower employees swap {} {} {} {}".format(this_emp[0], this_emp[1], other_emp[0], other_emp[1]))
                other_emp[3] = this_emp[3]
                this_emp[3] = this_emp[4]
        if not swapped:
            if this_emp[3] != this_emp[4]:
                print("Assigning {} {} to correct floor".format(this_emp[0], this_emp[1]))
                send_message(">tower employees assign {} {} {}".format(this_emp[0], this_emp[1], this_emp[4]))
                this_emp[3] = this_emp[4]

# Rewrite employees.txt to reflect changes
print("Updating employees.txt")
file = open("employees.txt", "w")
file.write("Number of floors to populate:\n")
file.write("{}\n\n".format(floors))
file.write("Employees - firstname lastname rarity(C/U/R/L) currentfloor:\n")
for emp in sorted_employees:
    emp.pop()
    emp[3] = str(emp[3])
    file.write(" ".join(emp) + "\n")
file.close()

# Calculate tower profit
earnings_after = calculate_earnings(sorted_employees)
print("\nHourly earnings before shuffling: {} ({} per 3 hours)".format(earnings_before, earnings_before * 3))
print("Hourly earnings after shuffling: {} ({} per 3 hours), {}% improvement".format(earnings_after, earnings_after * 3, int(100 - earnings_before/earnings_after * 100)))
input("\nPress enter to close")
