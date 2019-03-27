import os
def mkv2mp4(mkv_path):
    for i in range(10):  ## the num of season
        # isExists = os.path.exists(mp4_path + str(i + 1)+'/S'+str(i+1)+'-1.mp4')
        # if not isExists:
        #     os.makedirs(mp4_path + str(i + 1)+'/S'+str(i+1)+'-1.mp4')
        for j in range(25):  ## the num of episode
            source_path = mkv_path+str(i+1)+'/S'+str(i+1)+'-'+str(j+1)+'.mkv'
            target_path = mkv_path+str(i+1)+'/S'+str(i+1)+'-'+str(j+1)+'.mp4'
            os.system('ffmpeg -i '+source_path+' -vcodec copy -acodec copy '+target_path)
            # print('ffmpeg -i '+source_path+' -c copy '+target_path)

def mp42mp4(mp4_path, des_path):
    for i in range(10):
        for j in range(25):
            source_path = mp4_path+str(i+1)+'/S'+str(i+1)+'-'+str(j+1)+'.mkv'
            target_path = des_path+str(i+1)+'/S'+str(i+1)+'-'+str(j+1)+'.mkv'
            os.system('ffmpeg -i '+source_path+' -vcodec copy -acodec libfdk_aac -profile:a aac_he -b:a 48k '+target_path)


if __name__ == '__main__':
    mkv_path = '/Volumes/Macintosh\ HD/Downloads/Friends_mkv/S'
    mp4_path = '/Volumes/Macintosh\ HD/Downloads/Friends_mp4/S'
    des_path = '/Volumes/Macintosh\ HD/Downloads/Friends_mkv_n/S'
    # mkv2mp4(mkv_path, mp4_path)
    mp42mp4(mkv_path, des_path)