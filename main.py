from   tabulate import tabulate
import pandas   as pd
import numpy    as np

# Input number of rows
while True:
    try:
        # If failed, make user retype again
        rows = int(input("#Enter of rows: "))
        
        # Check if input exceed the limit
        if rows > 100:
            # If exceeded, make user retype again
            print("Exceeded rows limit")
            continue
        break
    except ValueError:
        # If failed, make user retype again
        print("Not a valid number")

# Input number of columns
while True:
    try:
        # If failed, make user retype again
        cols = int(input("#Enter of cols: "))
        
        # Check if input exceed the limit
        if cols > 26:
            # If failed, make user retype again
            print("Exceeded columns limit")
            continue
        break
    except ValueError:
        # If exceeded, make user retype again
        print("Not a valid number")

# Create new dataframe with shape [rows, columns]
# Fill dataframe with zero
# Set column name to character using ASCII code
df = pd.DataFrame(np.zeros([rows, cols]), 
                  columns=[chr(x + 65) for x in range(cols)])

# Set index to start with 1 instead of 0
df.index = pd.RangeIndex(start=1, stop=len(df) + 1)

# Preview spreadsheet
print(tabulate(df, 
               headers="keys", 
               showindex=True, 
               tablefmt='fancy_grid'))

# Main Loop
while True:
    # Reset selected cell
    row, col = 0, 0
    
    while True:
        # Convert input to string and make it upper case
        cell = str(input("Choose cell: ")).upper()
        try:
            # Slice string into 2 part:
            #   First part, Column - String position 0
            #   Second part, Row - String postion 1 to end
            col  = ord(list(cell[0])[0]) - 65
            row  = int(cell[1:]) - 1
            
            # Check if cell position exceed table shape
            if (row > (rows - 1)) | (row < 0) | \
               (col > (cols - 1)) | (col < 0):
                # If exceed, make user retype cell position
                print("Exceeded rows/column limit")
                continue
            break
        except ValueError:
            # If failed to convert string to cell position
            # show error message and make user retype
            print("Please enter a valid cell")
    
    while True:
        # Receive input from user
        #   chr(col + 65) means that add column index by 65 which will
        #   convert int to ASCII code
        val = input("Enter value for cell " + chr(col + 65) + 
                    str(row + 1) + " [-1 to quit]: ")
        try:
            # Try to convert value to float
            
            # Check if value equals to -1
            if float(val) == -1:
                # Break Loop
                break
            
            # Replace cell value
            df.iloc[row, col] = float(val)
            # Preview spreadsheet
            print(tabulate(df, 
                           headers="keys", 
                           showindex=True, 
                           tablefmt='fancy_grid'))
            break
        except ValueError:
            # If failed to covert, check for formula
            
            # Check if string contains '=' in first position
            if val.startswith('='):
                # Remove all space and convert string to uppercase
                val = val.upper().replace(" ", "")
                
                # Loop through all cells
                for k in range(cols):
                    for l in range(rows):
                        # Check if cell is not current cell
                        if k == row and l == row:
                            continue
                        
                        # Replace variable with value of cell
                        val = val.replace(chr(k + 65) + str(l + 1), 
                                            str(df.iloc[l, k]))
                try:
                    # Try to evaluate formula
                    df.iloc[row, col] = eval(val[1:])
                    # Print equation
                    print(chr(col + 65), str(row + 1), " = ", val[1:], sep="")
                    # Preview spreadsheet
                    print(tabulate(df, 
                                   headers="keys", 
                                   showindex=True, 
                                   tablefmt='fancy_grid'))
                    break
                except:
                    # Show error messagee
                    print("ERROR : Please enter a valid formula.")
                    continue
            else:
                # Show error messagee
                print("ERROR : Incompatible value")
                continue