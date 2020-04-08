import os, time

#按照对比图顺序命名
def copyName():
    success = 0
    fail = 0
    name_list = []
    img_list = []
    base_path = './name'
    name_li = os.listdir(base_path)
    for one in name_li:
        
        if one.split('.')[-1] in 'jpg|png':
            if not one[:3].isdigit():
                print('提示：图片前三位不是数字,[5s]之后自动停止\关闭程序...')
                time.sleep(5)
                os._exit(0)
        else:
            continue
        name_list.append(one)

    img_path = './Screenshots'
    img_li = os.listdir(img_path)
    for one in img_li:
        
        if one.split('.')[-1] not in 'jpg|png':
            continue
        img_list.append(one)
    

    length = len(name_list)
    if length != len(img_list):
        print('提示：图片数量对不上,[5s]之后自动停止\关闭程序...')
        time.sleep(5)
        os._exit(0)
    for i in range(length):
        old_name = os.path.join(img_path, img_list[i])
        new_name = os.path.join(img_path, name_list[i])
        try:
            os.rename(old_name, new_name)
            print('成功:',new_name)
            success += 1
        except FileExistsError as reason:
            print(i)
            print('失败：该图片已存在',new_name)
            fail += 1
            pass
            
    print('重命名已完成：成功 %d 张， 失败 %d 张。' % (success,fail))
    time.sleep(300)

if __name__ == '__main__':
    try:
        copyName()
    except IndexError:
        print('pass')
        time.sleep(5)
