import numpy as np

array_a = np.array([[1, 2],
                    [3, 4]])

array_b = np.array([[5, 6],
                    [7, 8]])

# a. Concatenate arrays along the rows (vertically)
concatenate_arry=np.concatenate([array_a,array_b])
print(concatenate_arry)

# b. Concatenate arrays along the columns (horizontally)
concatenate_arry1=np.concatenate([array_a,array_b],axis=1)
print(concatenate_arry1)
