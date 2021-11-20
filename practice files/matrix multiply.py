def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

x, y = -600.0, 100.0

m1 = [[-1, -1],
      [ 1,  3]]
m2 = [[x], [y]]

#get the sizes of both lists
m1Rows, m1Cols = len(m1), len(m1[0])
m2Rows, m2Cols = len(m2), len(m2[0])
#if the dimensions don't match for matrix multiplication, return None
if m1Cols != m2Rows:
    print(None)
else:
#make a new list, loop through the rows of m1 and cols of m2
    newMatrix = make2dList(m1Rows, m2Cols)
    for i in range(m1Rows):
        for j in range(m2Cols):
            dotProduct = 0
            #loop through each index in the row/column and add to dot product
            for k in range(m1Cols):
                dotProduct += m1[i][k] * m2[k][j]
            #add the dotproduct to the ij'th position of the new matrix
            newMatrix[i][j] = dotProduct

print(newMatrix)