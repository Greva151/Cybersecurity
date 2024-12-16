# Magical Advisor

<b>Author</b>: lorenzobunaj<br>
<b>Category</b>: Reverse<br>
<b>Solves</b>: 12<br>

## How to run the server
To run the server you'll need [`docker`](https://docs.docker.com/get-docker/) and [`docker-compose`](https://docs.docker.com/compose/install/).<br>
Go into the `src` folder and from the command line run `docker-compose up --build -d`.<br>
Now you can connect to the server by running `nc localhost 1338` in your terminal.<br>
To stop the server, from the command line run `docker-compose down`.

## Solution
Decompiling the binary file, we can observe some key points in the C file:
- The hints that are shown when you get the sequence of numbers wrong are hard-coded, so they are useless.
- To find the required sequence of numbers, you need to find the unknown values ``` x[0], x[1], ..., x[7] ``` s.t. the 8 linear constrains are satisfied.

The following is the C code:

```c
bool r[8];
long int A[8][8] = {
    {1368, 1772, 1577, 1536, 1343, 1193, 1039, 1336},
    {1540, 1864, 1263, 1009, 1257, 1901, 1031, 1071},
    {1418, 1995, 1692, 1533, 1330, 1866, 1065, 1619},
    {1890, 1717, 1396, 1880, 1145, 1790, 1351, 1917},
    {1262, 1537, 1748, 1375, 1927, 1056, 1633, 1573},
    {1099, 1954, 1606, 1640, 1345, 1689, 1984, 1427},
    {1078, 1583, 1507, 1640, 1287, 1113, 1275, 1798},
    {1518, 1057, 1703, 1696, 1642, 1532, 1921, 1210}
};
long int b[8] = {38229434, 37289959, 42779314, 45094892, 41480368, 43384348, 38797458, 41751617};
long int rows[8], x[8];

printf("Give me 8 numbers: ");
scanf("%ld %ld %ld %ld %ld %ld %ld %ld", &x[0], &x[1], &x[2], &x[3], &x[4], &x[5], &x[6], &x[7]);

for (int i=0; i<8; i++) {
    rows[i] = 0;
    for (int j=0; j<8; j++) rows[i] += A[i][j] * x[j];

    r[i] = rows[i] == b[i];
}

if (r[0] && r[1] && r[2] && r[3] && r[4] && r[5] && r[6] && r[7]) {
    printf("Here's your flag: %s\n", secret);
}
```

So, to solve the challenge, we just need to solve a 8x8 linear system.
An easy way to do it is by using an SMT Solver, like Z3.

The setup implemented in Python3 looks like this:

```python
x = [Int(f'x[{i}]') for i in range(8)]

A = [
    [1368, 1772, 1577, 1536, 1343, 1193, 1039, 1336],
    [1540, 1864, 1263, 1009, 1257, 1901, 1031, 1071],
    [1418, 1995, 1692, 1533, 1330, 1866, 1065, 1619],
    [1890, 1717, 1396, 1880, 1145, 1790, 1351, 1917],
    [1262, 1537, 1748, 1375, 1927, 1056, 1633, 1573],
    [1099, 1954, 1606, 1640, 1345, 1689, 1984, 1427],
    [1078, 1583, 1507, 1640, 1287, 1113, 1275, 1798],
    [1518, 1057, 1703, 1696, 1642, 1532, 1921, 1210]
]

b = [38229434, 37289959, 42779314, 45094892, 41480368, 43384348, 38797458, 41751617]

solver = Solver()

for i in range(8):
    solver.add(Sum([A[i][j] * x[j] for j in range(8)]) == b[i])

if solver.check() == sat:
    model = solver.model()
    solution = [model[x[i]].as_long() for i in range(8)]

    return [solution[i] for i in range(8)]
else:
    return []

```

Once a candidate for x is found, the service will print the flag.