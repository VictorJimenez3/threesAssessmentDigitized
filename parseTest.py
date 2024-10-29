"""
Programmed by Victor Jimenez
"""

from pprint import pprint

numData = [
        ["8103", "83727895", "769158", "31678925", "3294059", "73914", "3512407", "8089170", "1992939", "2120"], 
        ["4567", "8092573", "45013", "29758", "530345", "618475", "12445683", "30127987", "366305", "297539"], 
        ["139723", "45298716", "3295870", "3980", "253970", "579340", "6138", "432063", "81924982", "6583"], 
        ["9813", "32145678", "84673", "139475", "58145469", "13820", "37428981", "63017980", "45607", "13925647"], 
        ["34602458", "3643", "83921", "4512693", "4698723", "836438", "5801", "89063", "23972165", "3263"], 
        ["42915", "5853", "72631", "34670654", "36135", "4626071", "83959", "4959398", "68130", "6301"], 
        ["987302", "9672", "4286158", "7807347", "675246", "946053", "2002193", "6004745", "35671", "1061"], 
        ["5732186", "45013", "84203", "56239", "671302", "3004", "38672168", "80873", "4108", "371903"], 
        ["6837", "183820", "43612063", "90542145", "784352", "3956", "23781", "198378", "187123", "6004216"], 
        ["3407", "1792635", "4067903", "98103", "5624", "780523", "56792604", "37801", "6356791", "93956467"], 
        ["431025", "4297589", "83961", "56465421", "6138940", "4295901", "6476023", "97654985", "13283", "21243"], 
        ["613947", "43169857", "4302", "3251673", "70765583", "760536", "37821245", "4623", "1308418", "9212494"], 
        ["8077", "3824510", "53906", "4389", "80610972", "3120", "760530", "3940", "8405737", "89203"], 
        ["579103", "970943", "42057", "87652143", "3048", "497538", "1230", "93745125", "19081257", "23456"]
    ]

# numData is treated as a global constant

def ol_count_crossed_threes(clickData): #FIN
    crossed_counts = {}
    
    # Iterate over each entry in clickData
    for entry in clickData:
        row, column, index, _ = entry
        
        # Ensure row is in the specified range (0-4) and within bounds of numData
        if 0 <= column <= 4 :
            # Check if the value at numData[row][column] is 3
            if numData[row][column][index] == "3":
                # Use the (row, column) as the key in crossed_counts dictionary
                if (row, column) not in crossed_counts:
                    crossed_counts[(row, column)] = 1  # First click
                else:
                    crossed_counts[(row, column)] += 1  # Toggle click
    # Count the entries that were clicked an odd number of times (crossed)
    pprint(crossed_counts)
    count = sum(1 for times in crossed_counts.values() if times % 2 == 1)
    
    return count

# numData is treated as a global constant

def or_count_crossed_threes(clickData): #FIN
    crossed_counts = {}
    
    # Iterate over each entry in clickData
    for entry in clickData:
        row, column, index, _ = entry
        
        # Ensure row is in the specified range (5-9) and within bounds of numData
        if 5 <= column <= 9:
            # Check if the value at numData[row][column] is 3
            if numData[row][column][index] == "3":
                # Use the (row, column) as the key in crossed_counts dictionary
                if (row, column) not in crossed_counts:
                    crossed_counts[(row, column)] = 1  # First click
                else:
                    crossed_counts[(row, column)] += 1  # Toggle click
            else:
                print(f"MISSED DATA @3comp: {row} {column} {index}, values: ")
        else:
            print(f"MISSED DATA @row col comp: {row} {column} {index}, values: {5 <= row <= 9} {0 <= column <= len(numData)}")
    # Count the entries that were clicked an odd number of times (crossed)
    count = sum(1 for times in crossed_counts.values() if times % 2 == 1)
    
    return count
# Assume count_crossed_threes is already defined

def ol_count_missed_threes(clickData): #FIN
    return 60 - ol_count_crossed_threes(clickData)

def or_count_missed_threes(clickData): #FIN
    return 60 - or_count_crossed_threes(clickData)

#for row in range(len(numData)):

def count_crossed_threes_left_half_all_rows(clickData):  #FIN by Victor
    crossed_counts = 0
    # Iterate through all rows and columns in numData
    for row in range(len(numData)):
        for column in range(len(numData[row])):
            number_str = numData[row][column]  # Get the number string
            length = len(number_str)

            # Get the left half of the string (ignore middle if odd length)
            left_half = number_str[:length // 2]

            # Check each "3" in the left half to see if it was clicked an odd number of times
            for index, char in enumerate(left_half):
                if char == '3':
                    # Check for clicks at the exact (row, column, index) position
                    clicks = sum(1 for e in clickData if e[0] == row and e[1] == column and e[2] == index)
                    
                    if clicks % 2 == 1:  # Crossed if clicked an odd number of times
                        crossed_counts += 1

    return crossed_counts

def count_crossed_threes_right_half_all_rows(clickData):  #FIN by Victor
    crossed_counts = 0

    # Iterate through all rows and columns in numData
    for row in range(len(numData)):
        for column in range(len(numData[row])):
            number_str = str(numData[row][column])
            length = len(number_str)

            # Get the right half of the string (ignore middle if odd length)
            right_half = number_str[(length + 1) // 2:]

            # Iterate over each character in the right half, adjusting index based on the full number's length
            for relative_index, char in enumerate(right_half):
                actual_index = (length + 1) // 2 + relative_index  # Adjust index to match `numData`

                if char == '3':
                    # Check if this '3' was clicked an odd number of times at this specific (row, column, actual_index)
                    clicks = sum(1 for e in clickData if e[0] == row and e[1] == column and e[2] == actual_index)
                    
                    if clicks % 2 == 1:  # Crossed if clicked an odd number of times
                        crossed_counts += 1

    return crossed_counts


def count_missed_threes_left_half_all_rows(clickedData): #FIN
    return 60 - count_crossed_threes_left_half_all_rows(clickedData)

def count_missed_threes_right_half_all_rows(clickedData): #FIN
    return 60 - count_crossed_threes_right_half_all_rows(clickedData)


#function for r

def number_of_crossed_3s_column_left_side(clickedData, column):#FIN
    
    crossed_counts = 0
    # Iterate through all rows and columns in numData
    for row in range(len(numData)):
        number_str = numData[row][column]  # Get the number string
        length = len(number_str)

        # Get the left half of the string (ignore middle if odd length)
        left_half = number_str[:length // 2]

        # Check each "3" in the left half to see if it was clicked an odd number of times
        for index, char in enumerate(left_half):
            if char == '3':
                # Check for clicks at the exact (row, column, index) position
                clicks = sum(1 for e in clickedData if e[0] == row and e[1] == column and e[2] == index)
                
                if clicks % 2 == 1:  # Crossed if clicked an odd number of times
                    crossed_counts += 1

    return crossed_counts

# question r
def number_of_crossed_3s_column_right_side(clickedData,column): #FIN
    crossed_counts = 0

    # Iterate through all rows and columns in numData
    for row in range(len(numData)):
        number_str = str(numData[row][column])
        length = len(number_str)

        # Get the right half of the string (ignore middle if odd length)
        right_half = number_str[(length + 1) // 2:]

        # Iterate over each character in the right half, adjusting index based on the full number's length
        for relative_index, char in enumerate(right_half):
            actual_index = (length + 1) // 2 + relative_index  # Adjust index to match `numData`

            if char == '3':
                # Check if this '3' was clicked an odd number of times at this specific (row, column, actual_index)
                clicks = sum(1 for e in clickedData if e[0] == row and e[1] == column and e[2] == actual_index)
                
                if clicks % 2 == 1:  # Crossed if clicked an odd number of times
                    crossed_counts += 1

    return crossed_counts



def number_of_crossed_3s_column_quads(clickedData, brow, row, bcolumn, column):  # FIN
    crossed_count = 0

    for i in range(brow, row):
        for j in range(bcolumn, column):
            number_str = numData[i][j]  # Get the number string at this position

            # Debug: Print current position and number string for verification
            #print(f"Checking quadrant for position ({i}, {j}): {number_str}")

            # Iterate over each character and index in the number string
            for index, char in enumerate(number_str):
                if char == '3':
                    # Check if this '3' was clicked an odd number of times at this specific (row, column, index)
                    clicks = sum(1 for e in clickedData if int(e[0]) == i and int(e[1]) == j and int(e[2]) == index)

                    # Debug: Print click count for each "3" found
                   # print(f"3 found at ({i}, {j}, {index}) with clicks: {clicks}")

                    if clicks % 2 == 1:  # Crossed if clicked an odd number of times
                        crossed_count += 1

    return crossed_count

    #print(f"quad 1:  {number_of_crossed_3s_column_quads(click_data, 0, 6, 0, 5)}") # quad 1 is 7x5 (6 to 4)
    #pprint(f"quad 2:  {number_of_crossed_3s_column_quads(click_data, 0, 6, 5, 10)}") #quad 2
    #pprint(f"quad 3:  {number_of_crossed_3s_column_quads(click_data, 6, 13, 0, 5)}") #quad 3
    #pprint(f"quad 4:  {number_of_crossed_3s_column_quads(click_data, 6, 13, 5, 10)}") #quad4 
    #Remeber the numbers so I can implement it into the back end later

def total_crossed_3s(clickedData): #FIN
    crossed_count = 0

    # Iterate through all rows and columns in the entire 14x10 table
    for row in range(len(numData)):
        for column in range(len(numData[row])):
            number_str = numData[row][column]  # Get the number string at this position

            # Iterate over each character and index in the number string
            for index, char in enumerate(number_str):
                if char == '3':
                    # Check if this '3' was clicked an odd number of times at this specific (row, column, index)
                    clicks = sum(1 for e in clickedData if e[0] == row and e[1] == column and e[2] == index)

                    if clicks % 2 == 1:  # Crossed if clicked an odd number of times
                        crossed_count += 1

    return crossed_count
def total_omissions(clickedData): #FIN
    return 120 - total_crossed_3s(clickedData)



def page_centered_omission(clickedData): #FIN
    return ol_count_missed_threes(clickedData) - or_count_missed_threes(clickedData)

def string_centered_omissions(clickedData): #FIN
    return count_missed_threes_left_half_all_rows(clickedData) - count_missed_threes_right_half_all_rows(clickedData)
