#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/4/6 22:15
# @Author  :
# @Desc    :__st__.py是测试套件的初始化，对应__init__.robot，当指定force_tags时表示所在的目录下的用例都具有该标签，当存在__st__.py文件时，必须定义suite_setup和suite_teardown方法，普通py文件中可以定义多个测试类，一个类就对应一个用例，在类的上面可以打force_tags标签，表示该文件所有用例都具有该标签，测试类里面也可以打tag标签，指定这条用例具有该标签，使用tag和force_tags都必须传入列表的类型数据。类中可通过赋值name指定用例名，用例名可以有中文，但不建议里面有空格，类中必须定义setup，teardown，teststeps方法
# @File    : py2rf.py
# *************************************
import os, ast


def list_files(dirName, suffix):
    """
    :param dirName:目录
    :param suffix:查找的文件后缀
    :return:返回一个列表
    """
    ret = []
    for root, dirs, files in os.walk(dirName, topdown=False):
        py_files = filter(lambda file: file.endswith(f'.{suffix}'), files)
        for file in py_files:
            ret.append(os.path.join(root, file))
    return ret


def clear_robot_file(dirName):
    """
    :param dirName: 目录
    :return:无
    """
    ret = list_files(dirName, 'robot')
    for fp in ret:
        os.remove(fp)


def commpy2rf(fpath):
    """
    :param fpath:转换的py文件路径
    :return:py2rf文件填写内容
    """
    settingHead = '*** Settings ***'
    settingBody = f'\n\nLibrary  {os.path.split(fpath)[-1]}   WITH NAME  M'
    caseHead = '\n\n\n\n*** Test Cases ***'
    caseBody = ''

    with open(fpath, 'r',encoding='utf8') as f:
        content = f.read()
        if not content:
            # 空文件不转换
            return
        else:
            tree = ast.parse(content)
            # from pprint import pprint
            # pprint(ast.dump(tree))
            for classNode in tree.body:
                if not isinstance(classNode, ast.ClassDef):
                    for node in ast.walk(classNode):
                        if isinstance(node,ast.Assign):
                            if isinstance(node.targets[0],ast.Name):
                                if 'force_tags' == node.targets[0].id:
                                    # forceTagStr = ','.join(([f'\'{forceTagStrObj.s}\'' for
                                    #                          forceTagStrObj in node.value.elts]))
                                    # print('force_tags = [%s]' % forceTagStr)
                                    forceTagStr = ''.join(([f'  {forceTagStrObj.s}' for
                                                           forceTagStrObj in node.value.elts]))
                                    settingBody +=f'\n\nForce Tags  {forceTagStr}'
                else:
                    # print('class: %s' % classNode.name)
                    caseName = ''
                    caseMain = f'\n  [Setup]     {classNode.name}.' \
                               f'setup\n  [Teardown]  {classNode.name}.' \
                               f'teardown\n\n  {classNode.name}.teststeps\n'
                    settingBody += f'\n\nLibrary  {os.path.split(fpath)[-1][:-3]}.' \
                                   f'{classNode.name}   WITH NAME  {classNode.name}'
                    for node in ast.walk(classNode):
                        if isinstance(node,ast.Assign):
                            if isinstance(node.targets[0],ast.Name):
                                if 'name' == node.targets[0].id:
                                    # print('name = %s' % node.value.s)
                                    caseName = node.value.s
                                if 'tags' == node.targets[0].id:
                                    tagStr = ''.join(([f'  {tagStrObj.s}' for
                                                       tagStrObj in node.value.elts]))
                                    # print('tags = [%s]' % tagStr)
                                    caseMain = f'\n  [Tags]  {tagStr}\n  [Setup]     {classNode.name}.' \
                                               f'setup\n  [Teardown]  {classNode.name}.' \
                                               f'teardown\n\n  {classNode.name}.teststeps\n'
                    caseBody += f'\n\n{caseName}{caseMain}'
    return settingHead+settingBody+caseHead+caseBody


def stpy2rf(fpath):
    settingHead = '*** Settings ***'
    settingBody = f'\n\nLibrary  {os.path.split(fpath)[-1]}   WITH NAME  M' \
                  f'\n\nSuite Setup    M.suite_setup' \
                  f'\n\nSuite Teardown    M.suite_teardown'
    with open(fpath, 'r',encoding='utf8') as f:
        content = f.read()
        if not content:
            # 空文件不转换
            return
        else:
            tree = ast.parse(content)
            # from pprint import pprint
            # pprint(ast.dump(tree))
            for classNode in tree.body:
                if isinstance(classNode, ast.Assign):
                    for node in ast.walk(classNode):
                        if isinstance(node, ast.Assign):
                            if isinstance(node.targets[0], ast.Name):
                                if 'force_tags' == node.targets[0].id:
                                    forceTagStr = ''.join(([f'  {forceTagStrObj.s}' for
                                                            forceTagStrObj in node.value.elts]))
                                    settingBody += f'\n\nForce Tags  {forceTagStr}'
    return settingHead + settingBody

fpath = r'C:\Users\rg_16\Downloads\Compressed\autotest_bysms_02\cases\客户API\添加客户.py'
fpath1 = r'C:\Users\rg_16\Downloads\Compressed\autotest_bysms_02\cases\__st__.py'
basepath = r'C:\Users\rg_16\Downloads\Compressed\autotest_bysms_lesson3\cases'
# print(commpy2rf(fpath))
# print(stpy2rf(fpath1))
clear_robot_file(basepath)
for pyFilePath in list_files(basepath, 'py'):
    if '__st__.py' == os.path.split(pyFilePath)[-1]:
        toBeWrite = stpy2rf(pyFilePath)
        if not toBeWrite:
            print(f'{pyFilePath}========>空文件')
        else:
            robotFilePath = os.path.join(os.path.dirname(pyFilePath),'__init__.robot')
            with open(robotFilePath,'w',encoding='utf8') as f:
                f.write(toBeWrite)
            print(f'{pyFilePath}========>success')
    else:
        toBeWrite = commpy2rf(pyFilePath)
        if not toBeWrite:
            print(f'{pyFilePath}========>空文件')
        else:
            robotFilePath = pyFilePath[:-2]+'robot'
            with open(robotFilePath, 'w', encoding='utf8') as f:
                f.write(toBeWrite)
            print(f'{pyFilePath}========>success')