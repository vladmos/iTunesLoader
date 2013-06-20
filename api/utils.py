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
        if key in self:
            return self[key]
        if not self:
            return
        key = simplify(key)
        substring_length, closest_key = max((len(longest_common_substring(key, k)), k) for k in self.iterkeys())
        if substring_length > min(len(closest_key), len(key)) / 2:
            return self[closest_key]


def longest_common_substring(s1, s2):
    """
    Longest common substring (not to be confused with subsequence).
    Used as an euristics in comparing track names from the file tags to ones from the online database.
    Track names might be slightly different, for example, missing alternative name or an apostrophe.
    """
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest:x_longest]
