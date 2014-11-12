#coding:utf-8
import time

def loadDataSet():
	dataSet = []
	f = open('chess.dat', 'r')
	i = 0
	for line in f.readlines():
		i += 1
		dataSet.append(line.split(' ')[:6])
		if i == 10:
			break
	f.close()
	return dataSet

def createC1(dataSet):
	C1 = []
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	return map(frozenset, C1)	# frozenset type

def scanD(D, Ck, minSupport):
	ssCnt = {}
	for tid in D:
		for can in Ck:
			if can.issubset(tid):
				if not ssCnt.has_key(can):
					ssCnt[can] = 1
				else:
					ssCnt[can] += 1
	numItems = float(len(D))
	retList = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key] / numItems
		if support >= minSupport:
			retList.insert(0, key)
		supportData[key] = support
	return retList, supportData

# 创建候选项集 Ck
def aprioriGen(Lk, k):
	retList = []
	lenLk = len(Lk)
	for i in range(lenLk):
		for j in range(i+1, lenLk):
			L1 = list(Lk[i])[:k-2]
			L2 = list(Lk[j])[:k-2]
			L1.sort()
			L2.sort()
			if L1 == L2:
				retList.append(Lk[i] | Lk[j])
	return retList

# apriori 主函数
def apriori(dataset, minSupport = 0.5):
	C1 = createC1(dataSet)
	D = map(set, dataset)
	L1, supportData = scanD(D, C1, minSupport)
	L = [L1]
	k = 2
	while (len(L[k-2]) > 0):
		Ck = aprioriGen(L[k-2], k)
		Lk, supK = scanD(D, Ck, minSupport)
		supportData.update(supK)
		L.append(Lk)
		k += 1
	return L, supportData

def generateRules(L, supportData, minConf = 0.7):
	bigRuleList = []
	for i in range(1, len(L)):		# 只获取有两个或更多元素的集合
		for freqSet in L[i]:
			H1 = [frozenset([item]) for item in freqSet]
			if (i>1):
				rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
			else:
				calcConf(freqSet, H1, supportData, bigRuleList, minConf)
	return bigRuleList

def calcConf(freqSet, H, supportData, brl, minConf = 0.7):
	prunedH = []
	for conseq in H:
		conf = supportData[freqSet] / supportData[freqSet - conseq]
		if conf >= minConf:
			print freqSet - conseq,'-->', conseq, 'conf', conf
			brl.append((freqSet-conseq, conseq, conf))
			prunedH.append(conseq)
	return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf = 0.7):
	m = len(H[0])
	if(len(freqSet) > (m + 1)):
		Hmp1 = aprioriGen(H, m+1)
		Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
		if( len(Hmp1) > 1):
			rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

def write_result_supp(L, supp):
	f = open('result_fre.txt', 'w')
	for line in L:
		for item in line:
			f.write(' '.join(set(item)) + '\n')
	f.close()
	
	f = open('result_supp.txt', 'w')
	for key, value in supp.iteritems():
		f.write('_'.join(set(key)) + ':' + str(value) + '\n')
	f.close()

if __name__ == '__main__':
	start_time = time.time()
	dataSet = loadDataSet()
	print 'data length', len(dataSet)
	print 'first data', dataSet[0]
	print 'Finding frequent itemset...'
	L, supportData = apriori(dataSet, 0.9)
	print 'Time elapse: ', time.time() - start_time
	# print supportData
	# for key, value in supportData.iteritems():
	# 	print set(key), value
	write_result_supp(L, supportData)
	# print len(L)
	# print L[0]
	# print supportData[0]


	# print L
	# rules = generateRules(L, supportData, minConf = 0.7)
	# print rules

	# print supportData
	# L2 = aprioriGen(L[0], 2)
	# print L2

	# for key, value in supportData:
	# 	print key, value
	# C1 = createC1(dataSet)
	# D = map(set, dataSet)
	# L1, suppData0 = scanD(D, C1, 0.5)
	# print L1
	# print suppData0
	# print "hehe"
	# l = [1, 2, 3]
	# for i in range(len(l)):
	# 	print i
