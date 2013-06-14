def simplify(*args):
    """
    'Simplifies' strings: they become lowercase, stripped, all whitespaces are substituted with single space
    """
    if len(args) == 1 and type(args[0]) is tuple:
        args = args[0]
    simplified = tuple(' '.join(i.strip().lower().split()) for i in args)
    if len(args) == 1:
        simplified = simplified[0]
    return simplified


class CaseInsensitiveDict(dict):
    """
    The dict keys must be strings, but the lookups are case-insensitive.
    Keys are stored as simplified strings (see 'simplify' function above).
    """

    def __setitem__(self, key, value):
        return super(CaseInsensitiveDict, self).__setitem__(simplify(key), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(simplify(key))

    def __contains__(self, item):
        return super(CaseInsensitiveDict, self).__contains__(simplify(item))

    def get(self, k, d=None):
        return super(CaseInsensitiveDict, self).get(simplify(k), d)

    def get_closest(self, key):
        key = simplify(key)
        distance, closest_key = max((len(lcs(key, k)), k) for k in self.iterkeys())
        return self[closest_key]


def lcs(x, y):
    """
    Longest common subsequence.
    Used as an euristics in comparing track names from the file tags to ones from the online database.
    Track names might be slightly different, for example, missing alternative name or an apostrophe.
    """
    n = len(x)
    m = len(y)
    table = dict()  # a hashtable, but we'll use it as a 2D array here

    for i in range(n + 1):      # i = 0,1,...,n
        for j in range(m + 1):  # j = 0,1,...,m
            if i == 0 or j == 0:
                table[i, j] = 0
            elif x[i-1] == y[j-1]:
                table[i, j] = table[i-1, j-1] + 1
            else:
                table[i, j] = max(table[i-1, j], table[i, j-1])

    # Now, table[n, m] is the length of LCS of x and y.

    # Let's go one step further and reconstruct
    # the actual sequence from DP table:

    def recon(i, j):
        if i == 0 or j == 0:
            return []
        elif x[i-1] == y[j-1]:
            return recon(i-1, j-1) + [x[i-1]]
        elif table[i-1, j] > table[i, j-1]:
            return recon(i-1, j)
        else:
            return recon(i, j-1)

    return recon(n, m)
