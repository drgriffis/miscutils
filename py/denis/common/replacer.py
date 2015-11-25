import re

class replacer:
    """
    Thanks to: http://stackoverflow.com/questions/6116978/python-replace-multiple-strings
    """
    @staticmethod
    def prepare(repls, onlyAtEnds=False):
        '''Compiles and returns a regex matching the input list of strings to replace
        Note: returns two values wrapped as one; can feed tuple directly into apply
        '''
        rep = {key: '' for key in repls}
        rep = dict((re.escape(k), v) for k, v in rep.iteritems())
        if onlyAtEnds:
            expr = str.format("{0}|{1}",
                "|".join(['^%s' % key for key in rep.keys()]),
                "|".join(['%s$' % key for key in rep.keys()])
            )
        else:
            expr = "|".join(rep.keys())
        pattern = re.compile(expr)
        return (pattern, rep)

    @staticmethod
    def apply((pattern, rep), text):
        '''Uses a compiled pattern from .prepare() to replace all instances of desired strings in text
        '''
        return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
