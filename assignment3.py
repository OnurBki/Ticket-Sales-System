import sys
import string

file = sys.argv[1]

with open(file, "r") as inputs:
    file_inputs = inputs.read().splitlines()
    inputs.close()


results = []


def write_results():
    output_file = open("output.txt", "w")
    for text in results:
        output_file.write(text + '\n')
        print(text)
    output_file.close()


letters = [x for x in string.ascii_uppercase]
alphabet_index = {k: v for (k, v) in zip(letters, range(26))}   # assigns a number to each letter starting from zero
index_alphabet = {k: v for (k, v) in zip(range(26), letters)}   # assigns a letter to each number starting from A


categories_seats = {}   # all seats with category names
categories_r_c = {}     # rows' and columns' numbers of each categories
sold_ticket_category = {}    # seat category [0], seat ([B17, C21]) [1], payment type [2] respect to name


# that function creates categories and puts them into categories_seats dict with every row and column

def create_category(arg):
    arguments = arg.split()
    category_name = arguments[0]

    if category_name not in categories_seats:
        rows_columns = arguments[1].split('x')
        row, column = int(rows_columns[0]), int(rows_columns[1])
        seat_number = row * column

        if row <= 26:
            categories_r_c[category_name] = (row, column)

            seat_matrix = [[]] * row
            for i in range(row):
                seat_matrix[i] = ['X'] * column
            categories_seats[category_name] = seat_matrix

            results.append(f"The category '{category_name}'  having {seat_number} seats has been created")
        else:
            results.append(f"Warning: Category {category_name} cannot create due number of rows must"
                           f"not be bigger than 26")   # limit is 26 because rows are made of English alphabet
    else:
        results.append(f"Warning: Cannot create the category for the second time."
                       f" The stadium has already {category_name}.")


customer_list = []
total_cost = 0


def sell_ticket(arg):

    def sold_ticket_organizer(column):
        if payment == 'full':
            categories_seats[category][row_number][column] = 'F'
        elif payment == 'student':
            categories_seats[category][row_number][column] = 'S'
        elif payment == 'season':
            categories_seats[category][row_number][column] = 'T'

    def interval_tickets():
        for seat_col in range(bottom, top + 1):
            if categories_seats[category][row_number][seat_col] != 'X':
                results.append(f"Error: The seats {seat} cannot be sold to {name} due some of them have already been sold!")
                return None
        for seat_col in range(bottom, top + 1):
            sold_ticket_organizer(seat_col)

        results.append(f"Success: {name} has bought {seat} at {category}")
        # I used the same loop twice since first one checks if any of given seat are sold
        # and the second one sells the seats if the first loop are passed successfully

    arguments = arg.split()
    name, payment, category = arguments[0], arguments[1], arguments[2]
    wanted_seats = arguments[3:]

    if name not in customer_list:
        if category in categories_seats:
            for seat in wanted_seats:
                max_row, max_column = int(categories_r_c[category][0]) - 1, int(categories_r_c[category][1]) - 1
                # I subtracted 1 because category of rows' index stars from 0
                # but elements' index of categories_r_c starts from 1

                if '-' not in seat:
                    row, column = seat[0], int(seat[1:])
                    row_number = alphabet_index[row]

                    if row_number <= max_row and column <= max_column:
                        if categories_seats[category][row_number][column] == 'X':
                            sold_ticket_organizer(column)

                            results.append(f"Success: {name} has bought {seat} at {category}")
                        else:
                            results.append(f"Warning: The seat {seat} cannot be sold to {name} since it was already sold!")
                    elif row_number <= max_row and column > max_column:
                        results.append(f"Warning: The category '{category}' has less column than the specified index {seat}!")
                    elif row_number > max_row and column <= max_column:
                        results.append(f"Warning: The category '{category}' has less row than the specified index {seat}!")
                    elif row_number > max_row and column > max_column:
                        results.append(f"Warning: The category '{category}' has less row and column than the specified index {seat}!")
                else:
                    row, column_interval = seat[0], seat[1:].split('-')
                    row_number = alphabet_index[row]
                    bottom, top = int(column_interval[0]), int(column_interval[1])

                    if row_number <= max_row and top <= max_column:
                        interval_tickets()
                    elif row_number <= max_row and top > max_column:
                        results.append(f"Error: The category '{category}' has less column than the specified index {seat}!")
                    elif row_number > max_row and top <= max_column:
                        results.append(f"Error: The category '{category}' has less row than the specified index {seat}!")
                    elif row_number > max_row and top > max_column:
                        results.append(f"Error: The category '{category}' has less row and column than the specified index {seat}!")
        else:
            results.append(f"Warning: Category {category} is not available!")

        customer_list.append(name)
    else:
        results.append(f"Warning: {name} has already bought some ticket!")


def cancel_ticket(arg):

    arguments = arg.split()
    category = arguments[0]
    cancel_seats = arguments[1:]

    if category not in categories_seats:
        results.append(f"Warning: Category {category} is not available!")
    else:
        for seat in cancel_seats:
            max_row, max_column = int(categories_r_c[category][0]) - 1, int(categories_r_c[category][1]) - 1

            row, column = seat[0], int(seat[1:])
            row_number = alphabet_index[row]
            if row_number <= max_row and column <= max_column:
                if seat != 'X':
                    categories_seats[category][row_number][column] = 'X'
                    results.append(f"Success: The seat {seat} at '{category}' has been canceled and now ready to sell again")
                elif seat == 'X':
                    results.append(f"Error: The seat {seat} at '{category}' has already been free! Nothing to cancel")
            elif row_number > max_row and column <= max_column:
                results.append(f"Error: The category '{category}' has less row than the specified index {seat}!")
            elif row_number <= max_row and column > max_column:
                results.append(f"Error: The category '{category}' has less column than the specified index {seat}!")
            elif row_number > max_row and column > max_column:
                results.append(f"Error: The category '{category}' has less row and column than the specified index {seat}!")


def balance(arg):
    category = arg

    student = 0
    full = 0
    seasonal = 0

    if category in categories_seats:
        for row in categories_seats[category]:
            student += row.count('S')
            full += row.count('F')
            seasonal += row.count('T')

        revenue = (student * 10) + (full * 20) + (seasonal * 250)

        title = f"Category report of '{category}'"
        header = title + '\n' + ('-' * len(title))
        content = header + '\n' f"Sum of students = {student}, Sum of full pay = {full}," \
                          f" Sum of season ticket= {seasonal}, and Revenues = {revenue} Dollars"
        results.append(content)
    else:
        results.append(f"Warning: Category {category} is not available!")


def show_category(arg):
    category_name = arg
    category = categories_seats[category_name]

    if category_name in categories_seats:
        table = []
        column_line = ''

        column_range = list(range(categories_r_c[category_name][1]))
        for column in column_range:
            if column == column_range[0]:
                column_line += f" {column: ^3}"
            else:
                column_line += f"{column: ^3}"

        column_line.rstrip()
        table.append(column_line)

        line_letter = 0
        for row in category:
            table_line = f"{index_alphabet[line_letter]} "

            for column in row:
                table_line += f"{column: <3}"

            table.append(table_line.rstrip())
            line_letter += 1

        table.append(f"Printing category layout of {category_name}")
        table.reverse()
        for line in table:
            results.append(line)
    else:
        results.append(f"Warning: Category {category} is not available!")


def command_organizer():
    for command in file_inputs:
        if command.startswith('CREATECATEGORY'):
            argument = command.split(' ', 1)
            create_category(argument[1])
        elif command.startswith('SELLTICKET'):
            argument = command.split(' ', 1)
            sell_ticket(argument[1])
        elif command.startswith('CANCELTICKET'):
            argument = command.split(' ', 1)
            cancel_ticket(argument[1])
        elif command.startswith('BALANCE'):
            argument = command.split(' ', 1)
            balance(argument[1])
        elif command.startswith('SHOWCATEGORY'):
            argument = command.split(' ', 1)
            show_category(argument[1])


command_organizer()
write_results()
