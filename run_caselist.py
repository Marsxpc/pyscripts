

import sys,os

casefile = 'tclist.txt'

# 先产生参数文件
with open(casefile) as inf, open('args.txt','w') as outf:

    # 产生用例列表
    arglines = []
    icontent = inf.read().replace('\n','')
    cases = icontent.split('|')
    for case in cases:
        case = case.strip()
        if case:
            arglines.append('--test *' + case)

    # 去除重复部分,可以网上搜索关键字
    arglines = list(set(arglines))

    # 生成用例列表参数行
    argsStr = '\n'.join(arglines)

    # 加上其他参数
    argsStr += '\n--pythonpath .'
    argsStr += '\ntc'
    print (argsStr)

    outf.write(argsStr)

# 再执行自动化测试

os.system('robot --loglevel debug -A   args.txt ')

# 再打开运行结果

os.system('log.html ')