filenames = ['finalfinal.ttl', 'final.ttl']
with open('result.ttl', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
