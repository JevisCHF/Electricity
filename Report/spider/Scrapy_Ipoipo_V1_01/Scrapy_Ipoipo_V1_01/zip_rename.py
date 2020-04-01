import os, time
import zipfile


def get_file_list(file_path):
    dir_list = os.listdir(file_path)
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=True)
        # print(dir_list)
        # print(dir_list[0])
        return dir_list[0]


# 解压    path:文件夹路径，new_path: 新文件夹路径，title：重命名，cate:目录分类
def un_zip(path, new_path, title, cate):
    """unzip zip file"""
    # 获取最新的文件名
    a = get_file_list(path)
    if ('zip' in a) and ('crdownload' not in a):
        # print(a)
        # 构建文件路径
        file_name = path + a
        # print(file_name)
        # print(file_name)
        # 解压
        zip_file = zipfile.ZipFile(file_name)

        if os.path.isdir(path):
            pass
        else:
            os.mkdir(path)

        for names in zip_file.namelist():
            zip_file.extract(names, path)
        zip_file.close()
        # 重新获取最新的文件名
        b = get_file_list(path)
        # 构建旧文件路径
        old_name = path + b
        # print(old_name)
        # 构建重命名
        item = {}
        for c, r in cate.items():
            if c in title:
                pa = new_path + f'\\{c}\\'
                if os.path.isdir(pa):
                    pass
                else:
                    os.mkdir(pa)
                new_name = pa + title
                try:
                    rename(old_name, new_name)
                    item['new_name'] = new_name
                    item['root_id'] = r
                    return item
                except:
                    return item

        power = new_path + '\\电力\\'
        if os.path.isdir(power):
            pass
        else:
            os.mkdir(power)
        new_name = power + title
        try:
            rename(old_name, new_name)
            item['new_name'] = new_name
            item['root_id'] = '4001001'
            return item
        except:
            return item


def rename(file_name, new):
    os.rename(file_name, new)


if __name__ == '__main__':

    path = 'D:\\report zip'
    title = '111.pdf'
    un_zip(path, title)
