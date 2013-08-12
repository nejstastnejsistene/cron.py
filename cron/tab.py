FIELDS = MINUTE, HOUR, DOM, MONTH, DOW = range(5)

MONTH_NAMES = 'jan feb mar apr may jun jul aug sep oct nov dec'.split()
DOW_NAMES = 'sun mon tue wed thu fre sat sun'.split()

MINUTE_INFO = 0, 59, None
HOUR_INFO = 0, 23, None
DOM_INFO = 1, 31, None
MONTH_INFO = 1, 12, MONTH_NAMES
DOW_INFO = 0, 7, DOW_NAMES

FIELD_INFO = MINUTE_INFO, HOUR_INFO, DOM_INFO, MONTH_INFO, DOW_INFO

PREDEFINED = {
    '@yearly':  '0 0 0 0 *',
    '@monthly': '0 0 0 * *',
    '@weekly':  '0 0 * * 0',
    '@daily':   '0 0 * * *',
    '@hourly':  '0 * * * *',
    }

PREDEFINED['@annually'] = PREDEFINED['@yearly']
PREDEFINED['@midnight'] = PREDEFINED['@daily']


class CronTab(object):
    pass


class CronTabEntry(object):

    def __init__(self, entry):
        self.entry = entry
        self.fields = []
        self.dom_or_dow_star = False
        self.when_reboot = False
        self.parse(entry)

    def parse(self, entry):

        # Reboot is a special case.
        if entry.lower().startswith('@reboot'):
            self.command = self.entry[7:].lstrip()
            self.when_reboot = True
            return

        # Replace predefined time specifiers.
        if entry.startswith('@'):
            try:
                token = entry.split()[0]
                val = PREDEFINED[token.lower()]
                entry = entry.replace(token, PREDEFINED[token], 1)
            except KeyError:
                mesg = 'bad time specifier: {!r}'.format(val)
                raise CronTabError, mesg

        # Parse the fields.
        for expr, field in zip(entry.split(), FIELDS):
            entry = entry[len(expr):]
            try:
                bits = self.parse_field(expr.lower(), field)
                self.fields.append(bits)
            except ValueError:
                mesg = 'error parsing field: {!r}'.format(expr)
                raise CronTabError, mesg

    def parse_field(self, expr, field):
        lo, hi, names = FIELD_INFO[field]
        bits = [False for i in range(hi - lo + 1)]

        # Replace names.
        if names is not None:
            for i, name in enumerate(names, lo):
                if name in expr:
                    expr = expr.replace(name, str(i))

        # Iterate through comma separated values.
        for val in expr.split(','):
            step = 1
            if '/' in val:
                # Slash changes the step amount.
                val, step = val.split('/')
                step = int(step)

            if val == '*':
                # Set the DOM/DOW flag.
                if field in (DOM, DOW):
                    self.dom_or_dow_start = True
                # Asterisk means to include all values.
                start, stop = lo, hi
            elif '-' in val:
                # Dash indicates a range of values.
                start, stop = map(int, v.split('-'))
            else:
                # Only a single number, not a range.
                bits[int(val) - lo] = True
                continue

            # Set all values in the range.
            for i in range(start, stop + 1, step):
                bits[i - lo] = True

        # Both 0 and 7 are Sunday.
        if field == DOW and (bits[0] or bits[7]):
            bits[0] = bits[7] = True
         
        return bits
