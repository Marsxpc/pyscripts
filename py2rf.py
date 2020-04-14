#!/usr/bin/env python
# -*- coding:utf-8 -*-
# *************************************
# @Time    : 2020/4/6 22:15
# @Author  :
# @Desc    :这是python测试类写法转rf文件的脚本，主要转换两种文件。
# 第一种是__st__.py文件，它是测试套件的初始化，对应__init__.robot，当__st__.py文件存在时，必须定义suite_setup和
# suite_teardown方法，当指定force_tags时表示所在的目录下的用例都具有该标签。另一种是普通py文件，其中可以定义多个测试
# 类，一个类就对应一个用例，在类的上面可以定义suite_setup和suite_teardown方法，表明用例执行进入和退出该文件时会分别执
# 行这个初始化和清除，可以打force_tags标签，表示该文件所有用例都具有该标签，测试类里面也可以打tag标签，指定这条用例具有
# 该标签，使用tag和force_tags都必须传入列表的类型数据。类中必须赋值name指定用例名，用例名可以有中文，但不建议里面有空
# 格，类中必须定义setup，teardown，teststeps方法。
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

    with open(fpath, 'r', encoding='utf8') as f:
        content = f.read()
        if not content:
            # 空文件不转换
            return
        else:
            tree = ast.parse(content)
            # from pprint import pprint
            # pprint(ast.dump(tree))
            for classNode in tree.body:
                if isinstance(classNode, ast.FunctionDef):
                    if 'suite_setup' == classNode.name:
                        settingBody += '\n\nSuite Setup    M.suite_setup'
                    elif 'suite_teardown' == classNode.name:
                        settingBody += '\n\nSuite Teardown    M.suite_teardown'
                elif isinstance(classNode, ast.Assign):
                    if isinstance(classNode.targets[0], ast.Name):
                        if 'force_tags' == classNode.targets[0].id:
                            forceTagStr = ''.join(([f'  {forceTagStrObj.s}' for
                                                    forceTagStrObj in classNode.value.elts]))
                            settingBody += f'\n\nForce Tags  {forceTagStr}'
                elif isinstance(classNode, ast.ClassDef):
                    # print('class: %s' % classNode.name)
                    caseName = ''
                    caseMain = f'\n  [Setup]     {classNode.name}.' \
                               f'setup\n  [Teardown]  {classNode.name}.' \
                               f'teardown\n\n  {classNode.name}.teststeps\n'
                    settingBody += f'\n\nLibrary  {os.path.split(fpath)[-1][:-3]}.' \
                                   f'{classNode.name}   WITH NAME  {classNode.name}'
                    for node in ast.walk(classNode):
                        if isinstance(node, ast.Assign):
                            if isinstance(node.targets[0], ast.Name):
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
    return settingHead + settingBody + caseHead + caseBody


def stpy2rf(fpath):
    settingHead = '*** Settings ***'
    settingBody = f'\n\nLibrary  {os.path.split(fpath)[-1]}   WITH NAME  M' \
                  f'\n\nSuite Setup    M.suite_setup' \
                  f'\n\nSuite Teardown    M.suite_teardown'
    with open(fpath, 'r', encoding='utf8') as f:
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


def py2rf(basepath):
    clear_robot_file(basepath)
    for pyFilePath in list_files(basepath, 'py'):
        if '__st__.py' == os.path.split(pyFilePath)[-1]:
            toBeWrite = stpy2rf(pyFilePath)
            if not toBeWrite:
                print(f'{pyFilePath}========>空文件')
            else:
                robotFilePath = os.path.join(os.path.dirname(pyFilePath), '__init__.robot')
                with open(robotFilePath, 'w', encoding='utf8') as f:
                    f.write(toBeWrite)
                print(f'{pyFilePath}========>success')
        else:
            toBeWrite = commpy2rf(pyFilePath)
            if not toBeWrite:
                print(f'{pyFilePath}========>空文件')
            else:
                robotFilePath = pyFilePath[:-2] + 'robot'
                with open(robotFilePath, 'w', encoding='utf8') as f:
                    f.write(toBeWrite)
                print(f'{pyFilePath}========>success')


if __name__ == '__main__':
    fpath = r'D:\视频\代码\autotest_hyrobot\cases\功能1 - 副本.py'
    fpath1 = r'C:\Users\rg_16\Downloads\Compressed\autotest_bysms_02\cases\__st__.py'
    basepath = r'D:\tmp\yj_auto\cases'
    # print(commpy2rf(fpath))
    # print(stpy2rf(fpath1))

    # clear_robot_file(basepath)

    py2rf(basepath)