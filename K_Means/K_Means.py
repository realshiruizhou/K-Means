from PIL import Image
import urllib.request
import io
import sys
import random
from collections import deque


# this method is for finding the means
def k_means():
    # distinct is a dict, key is the (r, g, b), and the int is the frequency
    means = random.sample(list(distinct), k)  # selects k random different rgb values
    print("Random means: ", means)
    done = False
    while not done:  # go until means found
        group = {}
        for a in means:
            group[a] = set()
        for colors in distinct:
            min_distance = float('inf')
            closest = ()
            for each in means:
                d = squared_distance(each, colors)
                if d < min_distance:
                    min_distance = d
                    closest = each
            group[closest].add(colors)
        new_means = []
        for c in group:
            r = 0
            g = 0
            b = 0
            total_pixels = 0
            for d in group[c]:
                r += d[0] * distinct[d]
                g += d[1] * distinct[d]
                b += d[2] * distinct[d]
                total_pixels += distinct[d]
            new_means.append((r/total_pixels, g/total_pixels, b/total_pixels))
        if means == new_means:
            done = True
        means = new_means
    return group


def squared_distance(a, b):
    total = 0
    for c in range(0, len(a)):
        total += (a[c] - b[c]) ** 2
    return total


def flood_fill_helper():
    global regions
    visited = set()
    for a in range(0, img.size[0]):
        for b in range(0, img.size[1]):
            if (a, b) not in visited:
                visited.add((a, b))
                flood_fill((a, b), pix[a, b], visited)
                regions[pix[a, b]] = regions[pix[a, b]] + 1


def flood_fill(location, color, visited):
    q = deque()
    q.append(location)
    while len(q) != 0:
        n = q.popleft()
        (x, y) = n
        if x + 1 < img.size[0]:
            if y + 1 < img.size[1] and (x + 1, y + 1) not in visited and pix[x + 1, y + 1] == color:
                q.append((x + 1, y + 1))
                visited.add((x + 1, y + 1))
            if (x + 1, y) not in visited and pix[x + 1, y] == color:
                q.append((x + 1, y))
                visited.add((x + 1, y))
            if y - 1 > 0 and (x + 1, y - 1) not in visited and pix[x + 1, y - 1] == color:
                q.append((x + 1, y - 1))
                visited.add((x + 1, y - 1))
        if x - 1 >= 0:
            if y + 1 < img.size[1] and (x - 1, y + 1) not in visited and pix[x - 1, y + 1] == color:
                q.append((x - 1, y + 1))
                visited.add((x - 1, y + 1))
            if (x - 1, y) not in visited and pix[x - 1, y] == color:
                q.append((x - 1, y))
                visited.add((x - 1, y))
            if y - 1 >= 0 and (x - 1, y - 1) not in visited and pix[x - 1, y - 1] == color:
                q.append((x - 1, y - 1))
                visited.add((x - 1, y - 1))
        if y + 1 < img.size[1]:
            if (x, y + 1) not in visited and pix[x, y + 1] == color:
                q.append((x, y + 1))
                visited.add((x, y + 1))
        if y - 1 >= 0:
            if (x, y - 1) not in visited and pix[x, y - 1] == color:
                q.append((x, y - 1))
                visited.add((x, y - 1))


k = int(sys.argv[1])
if 'https://' in sys.argv[2]:
    img = Image.open(io.BytesIO(urllib.request.urlopen(sys.argv[1]).read()))
else:
    img = Image.open(sys.argv[2])
pix = img.load()
print("Size: " + str(img.size[0]) + " x " + str(img.size[1]))
print("Pixels: " + str(img.size[0] * img.size[1]))
distinct = {}
for a in range(0, img.size[0]):
    for b in range(0, img.size[1]):
        if pix[a, b] in distinct:
            distinct[pix[a, b]] = distinct[pix[a, b]] + 1
        else:
            distinct[pix[a, b]] = 1
print("Distinct Pixel Count: " + str(len(distinct)))
common = ()
m = 0
for keys in distinct:
    if distinct[keys] > m:
        common = keys
        m = distinct[keys]
print("Most common pixel: ", common, " => " + str(m))
print("Finding k_means with k=" + str(k))
final = k_means()
count = 1
print()
print("Final Means:")
regions = {}
for k in final:
    groups = 0
    for a in final[k]:
        groups += distinct[a]
    print(str(count) + ": ", k, " => " + str(groups))
    regions[(round(k[0]), round(k[1]), round(k[2]))] = 0
    count += 1
for x in range(0, img.size[0]):
    for y in range(0, img.size[1]):
        for f in final:
            if pix[x, y] in final[f]:
                pix[x, y] = (round(f[0]), round(f[1]), round(f[2]))
                break
img.save("2020szhou.png", "PNG")
flood_fill_helper()
r_to_print = []
for r in regions:
    r_to_print.append(regions[r])
print("Number of Regions: " + str(sum(r_to_print)))
print("Region Counts: ", r_to_print)
# python K_Means.py 4 cute_dog.jpg
