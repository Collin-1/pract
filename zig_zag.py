def func(s, num_row):
    #
    if num_row == 1 or num_row >= len(s):
        return s
    # create empty rows
    rows = [""] * num_row

    #keep track of rows
    current_row = 0
    going_down = False

    for char in s:
        rows[current_row]+= char

        #reverse directions at top or botton
        if current_row == 0 or current_row == num_row -1:
            going_down = not going_down
        print(going_down)

        current_row += 1 if going_down else -1

    return "".join(rows)
    

print(func("coderbyte", 3) == "creoebtdy")
print(func("kaamvjjfl", 4) == "kjajfavlm")