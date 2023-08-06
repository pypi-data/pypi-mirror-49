from prompt_toolkit import print_formatted_text, HTML
import re

def hl_matches(regexp, subject):
    m = re.search(regexp, subject)

    if m is None:
        print('No matches!')
        return

    n_matches = len(m.groups())
    overall_start, overall_end = m.span()

    spans = [m.span(n) for n in range(1, n_matches + 1)]
    starts = [span[0] for span in spans]
    ends = [span[1] for span in spans]

    output = ''

    for i, c in enumerate(subject):
        if i == overall_start:
            output += '<b>'

        if i in starts:
            output += '<firebrick>'

        if i in ends:
            output += '</firebrick>'

        if i == overall_end:
            output += '</b>'

        output += c

    if len(subject) in ends:
        output += '</firebrick>'
    if len(subject) == overall_end:
        output += '</b>'

    print_formatted_text(HTML(output))
