def lcss_distance(X, Y):
    m = len(X)
    n = len(Y)

    # Create a DP table to store the lengths of LCS for prefixes of X and Y
    L = [[None]*(n+1) for i in range(m+1)]
    # Fill the first row and column of LCS with 0
    for i in range(m+1):
        L[i][0] = 0
    for j in range(n+1):
        L[0][j] = 0

    # Build the DP table
    for i in range(m + 1):
        for j in range(n + 1):
            # Compare X[i-1] and Y[j-1] 
            # Start from LCS[1][1]
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
                # Point an arrow to LCS[i][j]
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
                # Point an arrow to max(LCS[i-1][j], LCS[i],[j-1])

    # Backtrack to find the LCSS
    lcss = ""
    i = m
    j = n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcss = X[i - 1] + lcss
            i -= 1
            j -= 1
        else:
            if L[i - 1][j] > L[i][j - 1]:
                i -= 1
            else:
                j -= 1
    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n], lcss

if __name__ == "__main__" :

    print("Enter the X string:")
    X = input().strip()
    print("Enter the Y string: ")
    Y = input().strip()

    distances, LCSS= lcss_distance(X,Y)
    print("Distance : {}".format(distances))
    print("LCSS = {}".format(LCSS))
