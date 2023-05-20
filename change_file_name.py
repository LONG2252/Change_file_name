import os
from datetime import datetime


file_count=0
def scan_file(path,file_list=[]):#用以遍历文件夹
    if(os.path.exists(path)):
        files=os.listdir(path)
        for row in files:
            if(row[1:5]=='RECY' or row[1:5]=='yste'):
                files.remove(row)
        for file in files:
            if(os.path.isdir(os.path.join(path,file))):
                scan_file(os.path.join(path,file),file_list)
            else:
                file=os.path.join(path,file)
                change_name(file)

def change_name(file):#更新
    global file_count
    file_path = os.path.dirname(file)
    file_name = os.path.basename(file)
    scar_leng = len(the_scar)
    old_scar_len=len(old_scar)
    s=0
    if(scar_leng>0 and old_scar_len == 0): #删除字符长度大于0，增加字符的长度等于0 ，则说明需要增加字符串

        if (the_scar != file_name[:scar_leng]):
            new_file = file_path + '/' + the_scar + file_name
            s=1
        else:
            print('文件： ' + file + '已经有了同样的前缀！   ' + file_name[:scar_leng])
    elif(scar_leng > 0 and old_scar_len > 0): #增加字符的长度大于0，删除字符的长度也大于0，说明需要替换字符串
        if (old_scar == file_name[:old_scar_len]):#匹配旧字符串
            new_file = file_path + '/' + the_scar + file_name[old_scar_len:]
            s = 1
        else:
            print('文件名：'+file_name+'未匹配到旧字符串： ' + old_scar)
    elif(scar_leng == 0 and old_scar_len > 0): #增加字符的长度等于0，删除字符的长度也大于0，说明需要删除字符串
        if (old_scar == file_name[:old_scar_len]):
            new_file = file_path + '/' + file_name[old_scar_len:]
            s = 1
        else:
            print('文件名：'+file_name+'未匹配到旧字符串： ' + old_scar)
            #print(file_name[:scar_leng])
    if(s==1):
        try:
            print(new_file)
            os.rename(file, new_file)
            file_count=file_count+1
        except Exception as e:
            print('修改文件名时报错： '+str(e))
    else:
        print('请输入正确的字符！')


if __name__=="__main__":
    """
    如果只增加前缀，那就把 the_scar 的参数设置为想要增加的字符，把old_scar的参数设置为空值''
    如果只删除前缀，那就把 the_scar 的参数设置为空值''，把old_scar的参数设置为你要删除的前缀
    如果需要替换前缀，那就把 the_scar 的参数设置为想要增加的字符，把old_scar的参数设置为你要删除的前缀
    注：所有参数都需要用英文单引号圈起来！
    """

    the_scar = 'add_'      #需要加入的字符
    old_scar=''      #需要替换或删除的字符
    path='/data/workspace/test/'
    start_time=datetime.now()
    scan_file(path)
    end_time=datetime.now()
    message='\n\n\n程序执行完成，开始于：' + str(start_time) + ', 结束于：'+ str(end_time) +',总共修改成功文件数：' + str(file_count)  + '\n\n\n'
    print(message)
