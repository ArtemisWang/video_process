from Friends_srt_helpers import srtParsing
import codecs
import os
import re
p1_path = 'Friends'
p3_path = 'Friends/srtfile/S'
def text_save(content,filename,mode='a'):
    # Try to save a list variable in txt file.
    file = open(filename,mode)
    for i in range(len(content)):
        file.write(str(content[i])+'\n')
    file.close()
for i in range(10):  ## 第i+1季
    p2_path = p1_path+'/S'+str(i+1)
    p4_path = p3_path+str(i+1)
    file_list = os.listdir(p4_path)
    c_s_path = p1_path + '/mp3file/C-S' + str(i + 1)
    c_s_path_ = c_s_path + '/'
    isExists = os.path.exists(c_s_path)
    if not isExists:
        os.makedirs(c_s_path)
        print('创建' + c_s_path + '目录成功')
    t_s_path = p1_path+'/txtfile/T-S'+str(i+1)
    isExists_t = os.path.exists(t_s_path)
    if not isExists_t:
        os.makedirs(t_s_path)
    j = 0
    for file_name in file_list: ## 第j+1集
        reg_srt = re.compile(r'srt$')
        file_name_path = p4_path + '/' + file_name
        if file_name == '.DS_Store':
            os.remove(file_name_path)
        elif reg_srt.search(file_name):
            [file_name_cut] = re.findall(r'S(.*).srt',file_name)
            file = codecs.open(file_name_path,'r','utf-8')
            # print(file)
            start,duration,text = srtParsing().srtProcess(file)
            text_path = p1_path+'/txtfile/T-S%d/'%(i+1)+file_name_cut+'.txt'
            # text_save(text,text_path,'w')
            part_path = c_s_path_+'S'+file_name_cut
            isExists_j = os.path.exists(part_path)
            if not isExists_j:
                os.makedirs(part_path)
                print('创建'+part_path+'目录成功')
            for k in range(len(start)):
                os.system('ffmpeg -i %s -ss %d -t %d -codec copy %s'%(p2_path+'/S'+file_name_cut+'.mp3',start[k],duration[k],part_path+'/S'+file_name_cut+'-%d.mp3'%(k)))
                # print('S'+file_name_cut+'-%d.mp3'%(k), len(text))
            j += 1

