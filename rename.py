import os
import re
def rough_rename(src_path):
    s_names = os.listdir(src_path)
    for i, s_name in enumerate(s_names):
        s_path = src_path+'/'+s_name
        s_path_ = s_path.replace(' ', '\ ')
        if s_name == '.DS_Store':
            os.remove(s_path)
        else:
            s_eps_names = os.listdir(s_path)
            for j, s_eps_name in enumerate(s_eps_names):
                # print(s_eps_name)
                s_eps_path = s_path+'/'+s_eps_name
                if s_eps_name == '.DS_Store':
                    os.remove(s_eps_path)
                else:
                    s_eps_path = s_eps_path.replace(' ', '\ ')
                    pattern = re.compile(r'S..E..')
                    s_eps_name_new = re.search(pattern, s_eps_name)
                    if s_eps_name_new:
                        s_eps_name_new = s_eps_name_new.group()+'.mkv'
                        s_eps_path_new = s_path_+'/'+s_eps_name_new
                        # os.system('mv '+s_eps_path+' '+s_eps_path_new)

def mv_file(src_path, des_path):
    for i in range(10):
        s_path = '/Volumes/Macintosh HD/Downloads/Friends_mp4/S'+str(i+1)
        if not os.path.exists(s_path):
            os.mkdir(s_path)
        for j in range(25):
            src_file = src_path+str(i+1)+'/n'+str(i+1)+'-'+str(j+1)+'.mp4'
            des_file = des_path+str(i+1)+'/S'+str(i+1)+'-'+str(j+1)+'.mp4'
            os.system('mv '+src_file+' '+des_file)


def strict_rename(src_path):
    for i in range(10): # the number of season
        for j in range(25): # the number of episode
            if i < 9:
                if j>=9:
                    source_file_path = src_path+'/S'+str(i+1)+'/S0'+str(i+1)+'E'+str(j+1)+'.mkv'
                else:
                    source_file_path = src_path+'/S'+str(i+1)+'/S0'+str(i+1)+'E0'+str(j+1)+'.mkv'
            else:
                if j>=9:
                    source_file_path = src_path+'/S'+str(i+1)+'/S'+str(i+1)+'E'+str(j+1)+'.mkv'
                else:
                    source_file_path = src_path+'/S'+str(i+1)+'/S'+str(i+1)+'E0'+str(j+1)+'.mkv'
            target_file_path = src_path+'/S'+str(i+1)+'/S'+str(i+1)+'-'+str(j+1)+'.mkv'
            # print(source_file_path, target_file_path)
            os.system('mv '+source_file_path+' '+target_file_path)

def rough_extract_subtitle_and_mp4(src_path):
    for i in range(2): # the number of season
        for j in range(10): # the number of episode
            source_file_path = 'src/S' + str(i + 1) + '/S' + str(i + 1) + '-' + str(j + 1) + '.mkv'
            # target_subtitle_path = 'src/S'+ str(i + 1) +'/S'+str(i + 1) + '-' + str(j + 1) + '.ass'
            target_mp4_path = 'src/S'+ str(i + 1) +'/S'+str(i + 1) + '-' + str(j + 1) + '.mp4'
            # os.system('cd '+src_path+' && ffmpeg -i '+source_file_path+' -map 0:2 '+target_subtitle_path)
            os.system('cd '+src_path+' && ffmpeg -i '+source_file_path+' -c copy '+target_mp4_path)

def strict_classify_subtitle_and_mp4(src_path):
    for i in range(2): # the number of season
        for j in range(10): # the number of episode
            source_mp4_path = src_path+'/src/S'+ str(i + 1) +'/S'+str(i + 1) + '-' + str(j + 1) + '.mp4'
            source_subtitle_path = src_path+'/src/S'+ str(i + 1) +'/S'+str(i + 1) + '-' + str(j + 1) + '.ass'
            target_mp4_path = src_path+'/mp4/src/S'+str(i + 1) +'/S'+str(i + 1) + '-' + str(j + 1) + '.mp4'
            target_subtitle_path = src_path+'/assfile/S'+ str(i + 1) +'/S'+str(i + 1) + '-' + str(j + 1) + '.ass'
            os.system('mv -i '+source_mp4_path+' '+target_mp4_path)
            os.system('mv -i '+source_subtitle_path+' '+target_subtitle_path)

def file_moving(src_path):
    for i in range(10): # the number of season
        for j in range(30): # the number of episode
            # delete_path = src_path + '/txtfile/S' + str(i + 1) +'/S'+str(i+1)+ '-'+str(j+1)+'.txt/'
            # os.rmdir(delete_path)
            source_path = src_path+'/txtfile/S'+str(i+1)+'/'+str(i+1)+'-'+str(j+1)+'.txt'
            target_path = src_path+'/txtfile/S'+str(i + 1)+'/S'+str(i+1)+'-'+str(j+1)+'.txt'
            isExist = os.path.exists(target_path)
            if not isExist:
                os.makedirs(target_path)
            os.system('mv -i '+source_path+' '+target_path)

def delete_file(file_path):
    for i in range(10):
        for j in range(25):
            eps_path = file_path+str(i+1)+'/S'+str(i+1)+'-'+str(j+1)+'.mp4'
            os.remove(eps_path)



if __name__ == "__main__":
    # src_path = '/Volumes/Macintosh\ HD/Downloads/Friends_mkv/S' ## 美剧名字
    # des_path = '/Volumes/Macintosh\ HD/Downloads/Friends_mp4/S'
    # mv_file(des_path, des_path)
    # file_path = '/Volumes/Macintosh HD/Downloads/Friends_mp4/S'
    # delete_file(file_path)
    # rough_rename(src_path)
    # strict_rename(src_path)
    # rough_extract_subtitle_and_mp4(src_path)
    # strict_classify_subtitle_and_mp4(src_path)

    # src_path = 'Friends'
    # file_moving(src_path)