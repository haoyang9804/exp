import matplotlib.pyplot as plt
node_num_list = [[], [], [],]
node_num_str = '''51	4	1
59	6	4
97	8	5
148	11	7
199	14	19
225	15	24
276	20	26
327	22	29
378	24	30
421	26	31
472	27	35
523	29	36
574	30	37
625	33	38
659	34	43
710	36	44
749	37	46
800	38	47
851	41	50
861	43	51
912	44	52
962	50	53
1011	54	54
1062	60	56
1113	61	57
1151	63	64
1183	64	65
1203	65	67
1254	67	68
1305	73	69
1356	74	76
1366	80	77
1417	81	79
1468	88	80
1519	89	81
1550	90	82
1580	94	83
1605	97	86
1649	100	87
1700	101	88
1741	113	91
1792	114	92
1834	123	93
1885	125	94
1936	129	95
1957	132	96
1982	137	97
2033	138	98
2058	141	99
2109	146	101'''

for line in node_num_str.split('\n'):
    temp = line.split('\t')
    print(len(temp))
    node_num_list[0].append(int(temp[0]))
    node_num_list[1].append(int(temp[1]))
    node_num_list[2].append(int(temp[2]))
print(len(node_num_list[1]))

x = range(0, 50)
y0 = node_num_list[0]
y1 = node_num_list[1]
y2 = node_num_list[2]

plt.plot(x, y0, label="constraint level 0",)

plt.plot(x, y1, label="constraint level 1",)

plt.plot(x, y2, label="constraint level 2",)

plt.xlabel('Graph Number', fontweight="bold", fontsize=14)
plt.ylabel('Node number', fontweight="bold", fontsize=14)
plt.legend()
plt.show()
