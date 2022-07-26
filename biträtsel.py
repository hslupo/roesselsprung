get_bin = lambda x, n: format(x, 'b').zfill(n)
print(get_bin(2 ** 11 - 1, 15))
di = {}
for i in range(2**10):
    s = get_bin(i, 10)
    v = [x for x in s.split('0') if x != '']
    w = ""
    for x in v:
        w += str(len(x)) + ' '
    w = w.strip()
    if w in di:
        di[w].append(i)
    else:
        di[w] = [i]

    print(i, s, v, w)
for k in di:
    w = 2**10 - 1
    for u in di[k]:

        w = w & u
    di[k].append(w)

print(di)
print(di.keys())
for x in di['3 4']:
    print(get_bin(x, 11))

