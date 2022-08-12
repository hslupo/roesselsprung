from time import perf_counter as pfc
import pynogram as pn
import json

get_bin = lambda x, n: format(x, 'b').zfill(n)
def bitbloecke(bits = 10) :

    di = {}
    di['0'] = [0]
    for i in range(2**bits):
        s = get_bin(i, bits)
        v = [x for x in s.split('0') if x != '']
        w = ""
        for x in v:      # BitBlöcke erstellen
            w += str(len(x)) + ' '
        w = w.strip()
        if w in di:
            di[w].append(i)
        else:
            di[w] = [i]

        # print(i, s, v, w)
    return di


def bitbloecke1(bits = 10) :
    # deutlich langsamer
    di = {}
    di['0'] = [0]
    for i in range(2**bits):
        s = ''
        h = 0
        bit = 1
        for j in range(bits):
            if i & bit:
                h += 1
            elif h:
                s += str(h) + ' '
                h = 0
            bit *= 2
        if h:
            s += str(h) + ' '
        s = ' '.join(s.strip().split()[::-1])
        if s in di:
            di[s].append(i)
        else:
            di[s] = [i]
        # print(i, j, i & 2**j, get_bin(i, bits), get_bin(i & (2 ** j), bits), s)
    return di


if __name__ == '__main__':
    start = pfc()
    bits = 21
    d = bitbloecke(bits)
    print(pfc() - start)
    print(d.__len__())
    tf = open(f"myBitBloecke{bits}.json", "w")
    json.dump(d, tf)
    tf.close()
    start = pfc()
    tf = open(f"myBitBloecke{bits}.json", "r")
    new_dict = json.load(tf)
    print('Laden der Datei: ', pfc() - start)
    # print(new_dict)