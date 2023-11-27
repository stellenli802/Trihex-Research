# -*- coding: utf-8 -*-
"""trihexAlternativeSignatures.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JxCcrxNM2RMu-LW7POuI6X0otkBWtIqi

Import libraries
"""

import csv
import matplotlib.pyplot as plt
import math

"""Solve equations mod n"""

def solveEquationModN(aa, rr, nn):
  # solve for the variable x in the equation a*x = r mod n, returning the smallest positive integer solutions, and return None if there is no solution
  for ii in range(1,nn+1):
    if (aa*ii % nn) == (rr % nn):
        return ii
  print("ERROR IN solveEquationModN")
  return None

def findOrder(aa, nn):
  # find the order of aa in Z_nn
  return solveEquationModN(aa, 0, nn)

def findAltSigs(n1, r1, k1):
  # given the signatture for a trihex (n1, r1, k1), find the two alteranative signatures
  j2 = findOrder(k1, n1 + 1)
  j3 = findOrder (k1 + r1 + 1, n1 + 1)
  n2 = j2*(r1 + 1) - 1
  n3 = j3*(r1 + 1) - 1
  h = 2*n1*r1 + 2*n1 + 2*r1
  r2 = int((h - 2*n2)/(2*n2 + 2))
  r3 = int((h - 2*n3)/(2*n3 + 2))
  #p_2, the smallest non-zero number such that p_2*k_1 = r_2 + 1 mod (n1 + 1)
  p2 = solveEquationModN(k1, r2 + 1, n1 +1)
  #print("p2: " + str(p2))
  k2 = (n2 - p2*(r1 + 1) - r2) % (n2 + 1)
  altSig2 = (n2, r2, k2)
  #p_3, the smallest non-zero number such that p_3*(k_1 + r_1 + 1) = r_3 + 1 mod (n_1 + 1)
  p3 = solveEquationModN(k1 + r1 + 1, r3 + 1, n1 + 1)
  #print("p3: " + str(p2))
  k3 = (n3 - p3*r1 - p3 + 1) % (n3 + 1)
  altSig3 = (n3, r3, k3)
  return altSig2, altSig3

def findMirrorSig(n1, r1, k1):
  # given the signature (n1, r1, k1) find one mirror image signature
  k2 = (n1 - r1 - k1) % (n1 + 1)
  return (n1, r1, k2)

def findAltSigsCollapseMirrors(n1, r1, k1):
  # find all alternate signatures including the signatures of mirror image trihexes
  (alt2, alt3) = findAltSigs(n1, r1, k1)
  alt4 = findMirrorSig(n1, r1, k1)
  (alt5, alt6) = findAltSigs(alt4[0], alt4[1], alt4[2])
  return (alt2, alt3, alt4, alt5, alt6)

def sortAltSigs(n1, r1, k1):
  # find the signature with the lowest value of r, the number of belts. If there is a tie, use the lowest value of k, the offset, also
  # however, it might make more sense to tie break using a value of k closest to either 0 or n, since
  # a value k = i is mirror symmetric to k = n - i, or to use a value of k farthest from either 0 or n
  (altSig2, altSig3) = findAltSigs(n1, r1, k1)
  allSigs = ((n1, r1, k1), altSig2, altSig3)
  sortedSigs = sorted(allSigs, key=lambda tup: (tup[1], tup[2]))
  return sortedSigs

def sortAltSigsCollapseMirrors(n1, r1, k1):
  # find the signature with the lowest value of r, including signatures of mirror images. If there is a tie, use the lowest value of k also
  # however, it might make more sense to tie break using a value of k closest to either 0 or n, since
  # a value k = i is mirror symmetric to k = n - i, or to use a value of k farthest from either 0 or n
  (altSig2, altSig3, altSig4, altSig5, altSig6) = findAltSigsCollapseMirrors(n1, r1, k1)
  allSigs = ((n1, r1, k1), altSig2, altSig3, altSig4, altSig5, altSig6)
  sortedSigs = sorted(allSigs, key=lambda tup: (tup[1], tup[2]))
  return sortedSigs

def numberOfHexagonsForSignature(nn, rr, kk):
  # return the number of hexagons in a trihex with nn spines, rr belts, and kk as its offset
  return 2*nn*rr + 2*nn + 2*rr

def numberOfVerticesForSignature(nn, rr, kk):
  # return the number of vertices in a trihex with spines of length nn, rr belts, and kk as its offset
  return 4*nn*rr + 4*nn + 4*rr + 4

def printListOfAlternateSignatures(maxN, maxR):
  # print out a list of alternative signatures for all trihexes with up to maxN hexagons in a spine and up to maxR belts
  for ii in range(0,maxN):
    for jj in range(0, maxR):
      for kk in range(0, ii + 1):
        altSig1 = (ii, jj, kk)
        (altSig2, altSig3) = findAltSigs(ii, jj, kk)
        print(altSig1, altSig2, altSig3)
        print()

def storeCsvFileOfAlternateSignatures(maxN, maxR):
  # store a list of trihex signatures in a csv file
  with open('triHexSigs.csv', mode='w') as sig_file:
    sig_writer = csv.writer(sig_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sig_writer.writerow(["s1", "b1", "f1", "s2", "b2", "f2", "s3", "b3", "f3", "hexagons", "vertices"])
    for ii in range(0,maxN):
      for jj in range(0, maxR):
        for kk in range(0, ii + 1):
          numHexes = numberOfHexagonsForSignature(ii, jj, kk)
          numVertices = numberOfVerticesForSignature(ii, jj, kk)
          altSig1 = (ii, jj, kk)
          (altSig2, altSig3) = findAltSigs(ii, jj, kk)
          sig_writer.writerow([ii, jj, kk, altSig2[0], altSig2[1], altSig2[2], altSig3[0], altSig3[1], altSig3[2], numHexes, numVertices])

def storeCsvFileOfSortedAlternateSignatures(maxN, maxR):
   # store a list of trihex signatures in a csv file. The trihexes are sorted in each row but the rows are not sorted in a logical way
  with open('triHexSigs.csv', mode='w') as sig_file:
    sig_writer = csv.writer(sig_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sig_writer.writerow(["s1", "b1", "f1", "s2", "b2", "f2", "s3", "b3", "f3", "hexagons", "vertices"])
    for ii in range(0,maxN):
      for jj in range(0, maxR):
        for kk in range(0, ii + 1):
          altSig1 = (ii, jj, kk)
          numHexes = numberOfHexagonsForSignature(ii, jj, kk)
          numVertices = numberOfVerticesForSignature(ii, jj, kk)
          ss = sortAltSigs(ii, jj, kk)
          if altSig1 == ss[1]:
            sig_writer.writerow([ss[0][0], ss[0][1], ss[0][2], ss[1][0], ss[1][1], ss[1][2], ss[2][0], ss[2][1], ss[2][2], numHexes, numVertices])

def storeCsvFileOfSortedAlternateSignatures2(maxN, maxR):
    # store a list of trihex signatures in a csv file. The trihexes are sorted in each row and the rows are sorted by number of hexagons
    # the resulting .csv file was used to create Table 1 in the manuscript
  rowSortedLongList = []
  for ii in range(0,maxN):
    for jj in range(0, maxR):
      for kk in range(0, ii + 1):
        altSig1 = (ii, jj, kk)
        numHexes = numberOfHexagonsForSignature(ii, jj, kk)
        numVertices = numberOfVerticesForSignature(ii, jj, kk)
        ss = sortAltSigs(ii, jj, kk)
        if altSig1 == ss[1]:
          rowSortedLongList.append((ss[0][0], ss[0][1], ss[0][2], ss[1][0], ss[1][1], ss[1][2], ss[2][0], ss[2][1], ss[2][2], numHexes, numVertices))
  longList = sorted(rowSortedLongList, key=lambda tup: (tup[10], -tup[0], tup[1], tup[2]))
  with open('triHexSigs.csv', mode='w') as sig_file:
    sig_writer = csv.writer(sig_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sig_writer.writerow(["s1", "b1", "f1", "s2", "b2", "f2", "s3", "b3", "f3", "hexagons", "vertices"])
    for mm in range(0, len(longList)):
      sig_writer.writerow([longList[mm][0], longList[mm][1], longList[mm][2], longList[mm][3], longList[mm][4], longList[mm][5], longList[mm][6], longList[mm][7], longList[mm][8], longList[mm][9], longList[mm][10]])

storeCsvFileOfAlternateSignatures(11, 11)
storeCsvFileOfSortedAlternateSignatures2(11, 11)

def getMinimalSig(n1, r1, k1):
  # return the alternate signature with the smallest number of belts. In case of a tie, the smallest offset is used
  ss = sortAltSigs(n1, r1, k1)
  return ss[0]

def getMinimalSigCollapseMirrors(n1, r1, k1):
    # return the alternate signature with the smallest number of belts. Include signatures of mirror images in the list.
    # In case of a tie, the smallest offset is used
  ss = sortAltSigsCollapseMirrors(n1, r1, k1)
  return ss[0]

"""Find how many trihexes with each number of hexagons"""

def getSumOfFactors(x):
  # return the sum of the factors of a number
  y = get_divisors(x)
  mySum = 0
  for num in y:
    mySum = mySum + num
  return mySum

def get_divisors(n):
  # return a list of the factors of a number
  listOfDivisors = []
  for i in range(1, int(n / 2) + 1):
    if n % i == 0:
      listOfDivisors.append(i)
  listOfDivisors.append(n)
  return listOfDivisors

def getSigsForGivenNumberOfHexes(hh):
  # return a list of signatures for a given number of hexagons
  if hh % 2 == 1:
    return None
  listOfSigs = []
  for jj in get_divisors(int(hh/2) + 1):
    n1 = jj - 1
    r1 = int((hh/2 + 1)/jj - 1)
    for kk in range(n1+1):
       listOfSigs.append( (n1, r1, kk) )
  return listOfSigs

def getUniqueSigsForGivenNumberOfHexes(hh):
  # get all signatures for a given number of hexagons, with no repeats
  if hh % 2 == 1:
    return []
  listOfSigs = []
  for jj in get_divisors(int(hh/2) + 1):
    n1 = jj - 1
    r1 = int((hh/2 + 1)/jj - 1)
    for kk in range(n1+1):
      if getMinimalSig(n1, r1, kk) == (n1, r1, kk):
        listOfSigs.append((n1, r1, kk))
  return listOfSigs

def getUniqueSigsCollapseMirrorsForGivenNumberOfHexes(hh):
  # signatures that are equivalent by mirror symmetry are considered the same
  if hh % 2 == 1:
    return []
  listOfSigs = []
  for jj in get_divisors(int(hh/2) + 1):
    n1 = jj - 1
    r1 = int((hh/2 + 1)/jj - 1)
    for kk in range(n1+1):
      if getMinimalSigCollapseMirrors(n1, r1, kk) == (n1, r1, kk):
        listOfSigs.append((n1, r1, kk))
  return listOfSigs

def listNumberOfTrihexesWithAtMostNumberOfHexes(hh):
  # get a count of the number of trihexes for spines of length at most hh. Consider mirror images of chiral trihexes as distinct.
  trihexCount = []
  for ii in range(hh+1):
    trihexCount.append(len(getUniqueSigsForGivenNumberOfHexes(ii)))
  return trihexCount

def listNumberOfTrihexesCollapseMirrorsWithAtMostNumberOfHexes(hh):
  # get a count of the number of trihexes for spines of length at most hh. Consider mirror images the same.
  trihexCount = []
  for ii in range(hh+1):
    trihexCount.append(len(getUniqueSigsCollapseMirrorsForGivenNumberOfHexes(ii)))
  return trihexCount

def listNumberOfTrihexesCollapseMirrorsNoGodseyesWithAtMostNumberOfHexes(hh):
  # get a count of the number of trihexes for spines of length at most hh. Consider mirror images the same. Omit godseyes
  trihexCount = []
  for ii in range(hh+1):
      if (ii % 2 == 0):
        next = len(getUniqueSigsCollapseMirrorsForGivenNumberOfHexes(ii))-1
      else:
        next = 0
      trihexCount.append(next) # because exactly one is a godseye
  return trihexCount

hh = 8
print("number of signatures for ", hh, " hexagons", len(getSigsForGivenNumberOfHexes(8)))
print("number of unique signatures for ", hh, " hexagons", len(getUniqueSigsForGivenNumberOfHexes(8)))
print("number of unique signatures for ", hh, " hexagons, mirrors counted the same", len(getUniqueSigsCollapseMirrorsForGivenNumberOfHexes(8)))
print("number of unique signatures for all numbers of hexagons up through ", hh, " is ", listNumberOfTrihexesWithAtMostNumberOfHexes(hh))
print("number of unique signatures for all numbers of hexagons up through ", hh, " with mirror images counted as the same is ",listNumberOfTrihexesCollapseMirrorsWithAtMostNumberOfHexes(hh))
print("number of signatures for all numbers of hexagons up through ", hh, "with mirror images counted as the same and no godseyes is ", listNumberOfTrihexesCollapseMirrorsNoGodseyesWithAtMostNumberOfHexes(hh))

def getTrihexCounts(zz):
# get the number of trihexes for each number of hexagons, where mirror images are first considered different and then are considered the same
# compare to bounds obtained from the number of factors of the number of hexagons
# This is figure 18 in the manuscript

   xx = range(zz+1)
   aa = listNumberOfTrihexesWithAtMostNumberOfHexes(zz)
   bb = listNumberOfTrihexesCollapseMirrorsWithAtMostNumberOfHexes(zz)
   yy = [getSumOfFactors(hexes/2 + 1) for hexes in xx]

   return([aa, bb, yy])

def plotTrihexCounts(mirrorsDiff, mirrorsSame, sumOfFactors):
# plot the counts of trihexes with mirrors counted either the same or different
# compared to the lower bounds from the sumOfFactors
# plot only for the even numbers of hexagons, which is vertices number that are multiples of 4
# This is Figure 18 in the manuscript
   ww = [num/3 for num in sumOfFactors]
   zz = len(mirrorsDiff)
   xx = range(zz+1)
   vv = [0]*(zz+1)
   for ii in xx:
    vv[ii] = 2*ii + 4
   pp = [math.ceil(num/3) for num in sumOfFactors]
   ff = [num/6 for num in sumOfFactors]
   gg = [math.ceil(num/6) for num in sumOfFactors]

   plt.figure().set_figheight(6)
   plt.plot(vv[0::2], mirrorsDiff[0::2], label = r'$\alpha(v)$')
   plt.plot(vv[0::2], ww[0::2], label = r'$\sigma(v)/3$')
   plt.plot(vv[0::2], mirrorsSame[0::2], label = r'$\beta(v)$')
   plt.plot(vv[0::2], ff[0::2], label = r'$\sigma(v)/6$')
   plt.legend()
   plt.xlabel("Vertices")
   plt.ylabel("Counts")
   plt.show()

def storeCsvFileOfCounts(alpha, beta, omega):
  # store counts of trihexes for each number of hexagons with the lower bounds
  # this is Table 2 in the manuscript
  with open('triHexSigs.csv', mode='w') as sig_file:
    sig_writer = csv.writer(sig_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    sig_writer.writerow(["h", "v", "alpha", "omega/3", "beta", "omega/6"])
    for ii in range(0,len(alpha)):
      if (ii % 2  == 0):
        sig_writer.writerow([ii, 2*ii+4, alpha[ii], math.ceil(omega[ii]/3), beta[ii], math.ceil(omega[ii]/6)])

def getDevianceMirrorsDifferent(minNumHexes, maxNumHexes):
# get statistics on how far the actual numbers are from the lower bounds, when counting mirror images as distinct
# note that the number of vertices is twice the number of hexagons plus 4
# so to get number of vertices <= v, use numHexes = (v-4)/2 = v/2 - 2
   xx = range(maxNumHexes+1)
   yy = [getSumOfFactors(hexes/2 + 1) for hexes in xx]
   aa = listNumberOfTrihexesWithAtMostNumberOfHexes(maxNumHexes)
   deviant = 0
   percentDeviant = 0
   maxDeviant = 0
   maxPercentGap = 0
   foundItGap = 0
   foundItPercentGap = 0
   for ii in range(minNumHexes, maxNumHexes+1, 2):
     gap = aa[ii] - math.ceil(yy[ii]/3)
     percentGap = gap/math.ceil(yy[ii]/3)
     percentGap = gap/(yy[ii]/3)
     if (gap > 1):
       deviant  = deviant + 1
     if (percentGap > 0.1):
       percentDeviant  = percentDeviant + 1
     if (gap > maxDeviant):
       maxDeviant = gap
       foundItGap = ii
     if (percentGap > maxPercentGap):
       maxPercentGap = percentGap
       foundItPercentGap = ii
   print("maxDeviant = ", maxDeviant)
   print("number deviant", deviant)
   print("fractionDeviant =", deviant/((maxNumHexes - minNumHexes)/2 + 1))
   print("maxPercentGap =", maxPercentGap)
   print("number over percent deviant", percentDeviant)
   print("fractionPercentDeviant ", percentDeviant/((maxNumHexes - minNumHexes)/2 + 1))
   print("locationOfMaxPercentGap  ", foundItPercentGap)
   print("locationOfMaxGap  ", foundItGap)
   print("number of vertices from ", 2*minNumHexes + 4, " up through ", 2*maxNumHexes + 4)
   return([maxDeviant, maxPercentGap,foundItPercentGap, foundItGap])

getDevianceMirrorsDifferent(98, 198)

def getDevianceMirrorsSame(minNumHexes, maxNumHexes):
# get statistics on how far the actual numbers are from the lower bounds, when counting mirror images as the same
# note that the number of vertices is twice the number of hexagons plus 4
# so to get number of vertices <= v, use numHexes = (v-4)/2 = v/2 - 2
   xx = range(maxNumHexes+1)
   yy = [getSumOfFactors(hexes/2 + 1) for hexes in xx]
   bb = listNumberOfTrihexesCollapseMirrorsWithAtMostNumberOfHexes(maxNumHexes)
   deviant = 0
   percentDeviant = 0
   maxDeviant = 0
   maxPercentGap = 0
   foundItGap = 0
   foundItPercentGap = 0
   for ii in range(minNumHexes, maxNumHexes+1, 2):
     gap = bb[ii] - math.ceil(yy[ii]/6)
     percentGap = gap/math.ceil(yy[ii]/6)
     percentGap = gap/(yy[ii]/6)
     if (gap > 1):
       deviant  = deviant + 1
     if (percentGap > 0.1):
       percentDeviant  = percentDeviant + 1
     if (gap > maxDeviant):
       maxDeviant = gap
       foundItGap = ii
     if (percentGap > maxPercentGap):
       maxPercentGap = percentGap
       foundItPercentGap = ii
   print("maxDeviant = ", maxDeviant)
   print("number deviant", deviant)
   print("fractionDeviant =", deviant/((maxNumHexes - minNumHexes)/2 + 1))
   print("maxPercentGap =", maxPercentGap)
   print("number over percent deviant", percentDeviant)
   print("fractionPercentDeviant ", percentDeviant/((maxNumHexes - minNumHexes)/2 + 1))
   print("locationOfMaxPercentGap  ", foundItPercentGap)
   print("locationOfMaxGap  ", foundItGap)
   print("number of vertices from ", 2*minNumHexes + 4, " up through ", 2*maxNumHexes + 4)
   return([maxDeviant, deviant/len(bb), maxPercentGap, percentDeviant/len(bb), foundItPercentGap, foundItGap])

getDevianceMirrorsSame(98, 198)

[mirrorsDiff200, mirrorsSame200, sumOfFactors200] = getTrihexCounts(200)
storeCsvFileOfCounts(mirrorsDiff200, mirrorsSame200, sumOfFactors200)
plotTrihexCounts(mirrorsDiff200, mirrorsSame200, sumOfFactors200)