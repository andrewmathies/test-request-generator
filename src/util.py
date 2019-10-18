import base64

# the Confluence API expects base64encode(email:API key) as authorization
def encode_key(email, key):
    string = email + ':' + key
    encoded_auth = base64.b64encode(string.encode('utf-8'))
    return 'Basic ' + encoded_auth.decode('utf-8')

# returns an html table where the column names are take fron col_headers, and then each row 
# is the ith element of each list in cols
def build_table(col_headers, *cols):
    if not len(cols):
        raise SystemExit('build_table was called with no columns')
    
    table = '<table><tr><th></th>'

    for header in col_headers:
        table += '<th>' + header + '</th>'
  
    table += '</tr>'

    height = len(cols[0])
    if height == 0:
        return ''

    for i in range(height):
        table += '<tr><td>' + str(i + 1) + '</td>'
        for col in cols:
            table += '<td>' + col[i] + '</td>'
        table += '</tr>'
    
    table += '</table>'
    return table

# returns a list of strings that is the power set of the words in the phrase minus any non-adjacent groupings
# for example, given 'test example string' this function returns ['test', 'example', 'string', 'test example', 'example string', 'test example string']
# this is the power set minus ['test string'], because 'test' and 'string' aren't adjacent 
def subsets(phrase):
    words = phrase.split()
    out = []

    for length in range(1, len(words) + 1):
        for i in range(len(words) - length + 1):
            val = words[i]
            for j in range(1, length):
                if i + j >= len(words):
                  continue
                val += ' ' + words[i + j]
            out.append(val)

    return out