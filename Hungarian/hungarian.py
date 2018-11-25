#!python3
'''
Code for 2018 Network Theory HW#3-3
'''

import csv
import math
from munkres import Munkres
import time 

## Read contents of CSV file
def read_csv_function(filename):

    ## Open file    
    file = open(filename)
    contents = csv.reader(file)

    ## Make matrix
    matrix = []

    ## Initialize matrix
    for row in contents:
        list = []
        for col in row:
            list.append(int(col))
        matrix.append(list)

    ## Close file
    file.close()

    ## Return matrix
    return matrix



## Find independent zero and solution
def dfs_function(cur_row, cost, path):
    ## If search is finished
    if cur_row == size_row:
        checker = 0
        for i in range(size_col):
            if bool_dfs_col_checker[i] == True:
                checker += 1
        if checker == size_col:
            return (cost, path)
        else:
            return (math.inf, [])

    solution = []
    result = []
    min_cost = math.inf

    ## Searching... for independent zeros
    for i in range(size_col):
        if matrix_modified[cur_row][i] > 0:
            continue
        if bool_dfs_col_checker[i] == True:
            continue
        
        bool_dfs_col_checker[i] = True
        new_path = path[:]
        new_path.append((cur_row,i))
        ## Next row
        result = dfs_function(cur_row + 1, cost + matrix_original[cur_row][i], new_path)
        if len(result) > 0:
            if result[0] < min_cost:
                min_cost = result[0]
                solution = result
        bool_dfs_col_checker[i] = False

    return solution

    

def solve(filename):
    ## Your lines of code
    ## that TA will
    ## use to check correctness

    ## Read contents from csv file
    global matrix_original
    matrix_original = read_csv_function(filename)
    
    ## Get size from matrix
    global size_row
    global size_col
    size_row = len(matrix_original)
    size_col = len(matrix_original[0])

    ## Copy matrix to use algorithm
    global matrix_modified
    matrix_modified = matrix_original[:]

    ## Zero variables
    count_zeros = 0
    group_lines_zero = {}
    group_zeros = {}

    ## Cover variables
    count_covers = 0
    group_rows_cover = set()
    group_cols_cover = set()


    '''
    Hungarian Agorithm
    '''

    ## Basic row operation
    for i in range(size_row):
        min = math.inf

        ## Find minimum value
        for j in range(size_col):
            if matrix_modified[i][j] < min:
                min = matrix_modified[i][j]

        ## Substraction operation
        for j in range(size_col):
            matrix_modified[i][j] -= min


    ## Basic column operation
    for i in range(size_col):
        min = math.inf

        ## Find minimum value
        for j in range(size_row):
            if matrix_modified[j][i] < min:
                min = matrix_modified[j][i]

        ## Substraction operation
        for j in range(size_row):
            matrix_modified[j][i] -= min

            ## If value is zero, save zero line information
            if matrix_modified[j][i] == 0:
                group_zeros[(j,i)] = False
                count_zeros += 1
                try:
                    group_lines_zero[('R',j)] += 1
                except:
                    group_lines_zero[('R',j)] = 1

                try:
                    group_lines_zero[('C',i)] += 1
                except:
                    group_lines_zero[('C',i)] = 1

    ## Repeat until "min cover == size of column"
    while True:

        ## Find zero lines
        count_covers = 0
        while count_zeros > 0:
            
            sorted_lines = sorted(group_lines_zero, key=lambda k : group_lines_zero[k], reverse=True)[0]
            
            ## Row line
            if sorted_lines[0] == 'R':
                row = sorted_lines[1]
                for i in range(size_col):
                    if matrix_modified[row][i] == 0 and group_zeros[(row,i)] == False:
                        group_zeros[(row,i)] = True
                        group_lines_zero[('R',row)] -= 1
                        group_lines_zero[('C',i)] -= 1
                        count_zeros -= 1
                        group_rows_cover.add(sorted_lines[1])

            ## Column line
            else:
                col = sorted_lines[1]
                for i in range(size_row):
                    if matrix_modified[i][col] == 0 and group_zeros[(i,col)] == False:
                        group_zeros[(i,col)] = True
                        group_lines_zero[('C',col)] -= 1
                        group_lines_zero[('R',i)] -= 1
                        count_zeros -= 1
                        group_cols_cover.add(sorted_lines[1])
            count_covers += 1

        ## Break while statement
        if count_covers == size_col:
            break

        ## Initialize duplicate variables
        bool_rows_zero = [False] * size_row
        bool_cols_zero = [False] * size_col
        group_duplicates = []

        ## Find duplicate
        for i in group_rows_cover:
            bool_rows_zero[i] = True
            for j in group_cols_cover:
                bool_cols_zero[j] = True
                group_duplicates.append((i,j))

        ## Find minimum value
        min = math.inf
        for i in range(0,size_row):
            for j in range(0,size_col):
                if bool_rows_zero[i] == True:
                    break
                if bool_cols_zero[j] == True:
                    continue
                if matrix_modified[i][j] < min:
                    min = matrix_modified[i][j]

        ## Add operation at duplicates
        for duplicate in group_duplicates:
            matrix_modified[duplicate[0]][duplicate[1]] += min      

        ## Substraction operation
        for i in range(size_row):
            for j in range(size_col):
                if bool_rows_zero[i] == True:
                    break
                if bool_cols_zero[j] == True:
                    continue
                matrix_modified[i][j] -= min

        ## Initialize zero variables
        count_zeros = 0
        group_lines_zero = {}
        group_zeros = {}

        ## Find zero lines
        for i in range(size_row):
            for j in range(size_col):
                if matrix_modified[i][j] == 0:
                    group_zeros[(i,j)] = False
                    count_zeros += 1
                    try:
                        group_lines_zero[('R',i)] += 1
                    except:
                        group_lines_zero[('R',i)] = 1

                    try:
                        group_lines_zero[('C',j)] += 1
                    except:
                        group_lines_zero[('C',j)] = 1
       

    ## Using DFS method(back tracking), find independent zeros
    global bool_dfs_col_checker
    bool_dfs_col_checker = []
    for i in range(size_col):
        bool_dfs_col_checker.append(False)

    min_cost = math.inf
    min_path = []
    for i in range(size_col):
        if matrix_modified[0][i] > 0:
            continue
        bool_dfs_col_checker[i] = True
        result = dfs_function(1, matrix_original[0][i], [(0,i)])
        if len(result) > 0:
            if result[0] < min_cost:
                min_cost = result[0]
                min_path = result[1]
        bool_dfs_col_checker[i] = False

    ## Return solution
    solution = min_path
    return solution


## Using library
def solve2(filename):
    ## Your lines of code
    ## that TA will
    ## use to check correctness

    ## Read contents from csv file
    matrix = read_csv_function(filename)
    
    ## Using library
    m = Munkres()
    indexes = m.compute(matrix)
    
    ## Save path
    solution = []
    for row, column in indexes:
        solution.append((row, column))

    return solution

def main():
    filename = "network_theory_hw3_assignment_costs.csv"
    ## by myself
    print('Implemented')
    start_time = time.time()
    print(solve(filename))
    print("%s seconds" %(time.time() - start_time))

    print()

    ## using Munkres library
    print('Munkres library')
    start_time = time.time()
    print(solve2(filename))
    print("%s seconds" %(time.time() - start_time))

if __name__ == '__main__':
    main()