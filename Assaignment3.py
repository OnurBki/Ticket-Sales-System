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
alphabet_index = {k: v for (k, v) in zip(letters, range(26))}   # assigns number to each letter starting from zero


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


def sell_ticket(arg):

    def sold_ticket_organizer(total, st):
        if payment == 'full':
            categories_seats[category][row_number][column] = 'F'
            total += 20
        elif payment == 'student':
            categories_seats[category][row_number][column] = 'S'
            total += 10
        elif payment == 'season':
            categories_seats[category][row_number][column] = 'T'
            total += 250

        # I will utilize from this expression while showing category table and cancelling tickets

        sold_ticket_category[name] = (category, st, payment)

    def interval_tickets(total):
        for seat_col in range(bottom, top + 1):
            if categories_seats[category][row_number1][seat_col] != 'X':
                results.append(f"Error: The seats {seat} cannot be sold to {name} due some of them have already been sold!")
                return None
        for seat_col in range(bottom, top + 1):
            if payment == 'full':
                categories_seats[category][row_number1][seat_col] = 'F'
                total += 20
            elif payment == 'student':
                categories_seats[category][row_number1][seat_col] = 'S'
                total += 10
            elif payment == 'season':
                categories_seats[category][row_number1][seat_col] = 'T'
                total += 250

            ticket_seats.append(row1 + str(seat_col))

        sold_ticket_category[name] = (category, ticket_seats, payment)
        results.append(f"Success: {name} has bought {seat} at {category}")
        # I used the same loops since first one checks if any of given seat are sold
        # and the second one sells the seats if the first loop are passed successfully

    arguments = arg.split()
    name, payment, category = arguments[0], arguments[1], arguments[2]
    wanted_seats = arguments[3:]
    total_cost = 0

    if name not in customer_list:
        if category in categories_seats:
            for seat in wanted_seats:
                max_row, max_column = int(categories_r_c[category][0]) - 1, int(categories_r_c[category][1]) - 1
                # I subtracted 1 because category of rows' index stars from 0
                # but elements' index of categories_r_c starts from 1

                if '-' not in seat:
                    row, column = seat[0], int(seat[1:])
                    row_number = alphabet_index[row]

                    ticket_seats = []
                    if row_number <= max_row and column <= max_column:
                        if categories_seats[category][row_number][column] == 'X':
                            ticket_seats.append(seat)
                            sold_ticket_organizer(total_cost, ticket_seats)

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
                    row1, column_interval = seat[0], seat[1:].split('-')
                    row_number1 = alphabet_index[row1]
                    bottom, top = int(column_interval[0]), int(column_interval[1])

                    if row_number1 <= max_row and top <= max_column:
                        ticket_seats = []
                        interval_tickets(total_cost)
                    elif row_number1 <= max_row and top > max_column:
                        results.append(f"Error: The category '{category}' has less column than the specified index {seat}!")
                    elif row_number1 > max_row and top <= max_column:
                        results.append(f"Error: The category '{category}' has less row than the specified index {seat}!")
                    elif row_number1 > max_row and top > max_column:
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
                for ticket in sold_ticket_category:
                    if sold_ticket_category[ticket][0] == category and seat in sold_ticket_category[ticket][1]:
                        target = categories_seats[category][row_number][column]
                        if target == 'S':
                            sold_ticket_category[ticket][2] -= 10
                            sold_ticket_category[ticket][1].remove(seat)
                        elif target == 'F':
                            sold_ticket_category[ticket][2] -= 20
                            sold_ticket_category[ticket][1].remove(seat)
                        elif target == 'T':
                            sold_ticket_category[ticket][2] -= 250
                            sold_ticket_category[ticket][1].remove(seat)

                        categories_seats[category][row_number][column] = 'X'

                        results.append(f"Success: The seat {seat} at '{category}' has been canceled and now ready to sell again")
                    elif sold_ticket_category[ticket][0] == category and seat not in sold_ticket_category[ticket][1]:
                        results.append(f"Error: The seat {seat} at '{category}' has already been free! Nothing to cancel")
                        # burayı fonksiyona çevir

            elif row_number > max_row and column <= max_column:
                return f"Error: The category '{category}' has less row than the specified index {seat}!"
            elif row_number <= max_row and column > max_column:
                return f"Error: The category '{category}' has less column than the specified index {seat}!"
            elif row_number > max_row and column > max_column:
                return f"Error: The category '{category}' has less row and column than the specified index {seat}!"


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


write_results()
