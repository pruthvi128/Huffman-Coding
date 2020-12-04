from heapq import heappush, heappop, heapify


def encode(freq):

    heap = [[wt, [sym, ""]] for sym, wt in freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


string = "Sample Text encoded"

frequency_dict = {}
for c in string.replace(" ", ""):
    if c in frequency_dict:
        frequency_dict[c] += 1
    else:
        frequency_dict[c] = 1

print(frequency_dict)
huff = encode(frequency_dict)

print("Symbol\tWeight\tHuffman Code")
for p in huff:
    print("%s\t%s\t%s" % (p[0], frequency_dict[p[0]], p[1]))
