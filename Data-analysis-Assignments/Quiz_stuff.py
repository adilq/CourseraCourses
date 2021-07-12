import re
import numpy as np

def result():
    s = 'ACAABAACAAABACDBADDDFSDDDFFSSSASDAFAAACBAAAFASD'

    result = []
    # compete the pattern below
    pattern = '[A-Z](?=AAA)'
    for item in re.finditer(pattern, s):
      # identify the group number below.
      result.append(item.group())
      
    return result

if __name__ == '__main__':

    # import pandas
    # df = pandas.DataFrame(data={'a': [5, 5, 71, 67], 'b': [6, 82, 31, 37], 'c': [20, 28, 92, 49]})
    # f = lambda x: x.max() + x.min()
    # df_new = df.apply(f)
    # print(df_new)

    r = [10, 20, np.nan]

    print(sum(r))



