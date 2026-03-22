def max3(a, b, c):
    m = a
    if (b > m):
        m = b
    if (c > m):
        m = c
    return m

x = 3
y = 9
z = 5
r = 0
r = max3(x, y, z)
print("Maior:")
print(r)