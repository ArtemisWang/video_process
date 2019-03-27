import data_helper
import Friends_srt_helpers as fs
import codecs
import os
def senid2videoid(id_list, sen_list, senid_list):
    indexs = []
    sen_lists = []
    for i in senid_list:
        indexs.append(id_list[int(i)].replace('\'', '').strip(':[]').split(',')[0])
        sen_lists.append(sen_list[int(i)])
    return indexs, sen_lists

def indexs2video_part(indexs, video_path, part_path, list_i):
    srt = fs.srtParsing()
    concat_list = []
    eps_record = []
    time_records = []
    duration_list = []
    text_list = []
    for i, index in enumerate(indexs):
        [s, e, p] = index.split('-')
        p = int(p)
        f = codecs.open('Friends/srtfile/S' + s + '/S' + s + '-' + e + '.srt', 'r', 'utf-8')
        start, duration, text = srt.srtProcess(f)
        duration_list.append(duration[p])
        text_list.append(text[p])
        # if eps_record != [] and [s, e, p-1] == eps_record[-1]:
        if eps_record != [] and [s, e] == eps_record[-1][:2] and p - eps_record[-1][2] == 1:
            time_records[-1][1] = start[p]+duration[p]+1-time_records[-1][0]
            duration_list[-2] = start[p] - time_records[-1][0]
            duration_list[-1] = duration_list[-1] + 1
        else:
            time_records.append([start[p], duration[p]+1, s, e])
        eps_record.append([s, e, p])
        # print(text[int(p)])
    for j, record in enumerate(time_records):
        [start, duration, s, e] = record
        video_eps_path = video_path + s + '/S' + s + '-' + e + '.mkv'
        # video_eps_path = 'test.mp4'
        destination_path = part_path + str(list_i)+'-'+str(j) + '.mkv'
        concat_list.append(str(list_i)+'-'+str(j) + '.mkv')
        # print('ffmpeg -i '+video_eps_path+' -ss '+str(start)+' -t '+str(duration)+' -acodec copy '+destination_path)
        os.system(
            'ffmpeg -i ' + video_eps_path + ' -ss ' + str(start) + ' -t ' + str(duration) + ' -acodec copy ' + destination_path)
    temp_path = part_path + str(list_i) + 'temp.txt'
    output_path = part_path + 'result_'+str(list_i)+'.mkv'
    write_srt(part_path+'result_'+str(list_i)+'.srt', duration_list, text_list)
    with open(temp_path, 'w') as par:
        for k in concat_list:
            par.write('file \''+k+'\'\n')
    os.system('ffmpeg -f concat -i ' + temp_path + ' -c copy ' + output_path)
    os.remove(temp_path)
    for m in range(len(time_records)):
        os.remove(part_path + str(list_i)+'-'+str(m) + '.mkv')



# def concat_video(output_path, temp_path):
#     os.system('ffmpeg -f concat -i '+temp_path+' -c copy '+output_path)


def read_eps_list(filename):
    eps_list = []
    with open(filename, 'r') as f:
        for line in f:
            a = line.strip('[]\n').split(', ')
            if len(a) == 15 and a[-1] != '-1':
                eps_list.append(a)
    return eps_list

def auto_cut(eps_list_txt, sen2id_txt, video_path, part_path):
    eps_list = read_eps_list(eps_list_txt)
    sen_list, id_list = data_helper.build_p_input(sen2id_txt)
    # print(eps_list)
    for i, a in enumerate(eps_list):
        indexs, sen_lists = senid2videoid(id_list, sen_list, a)
        # print(indexs)
        if i>143:
            indexs2video_part(indexs, video_path, part_path, i)
    print('Edit finished.')

def write_srt(filename, duration_list, text_list):
    start_time = 0
    with open(filename, 'w') as f:
        for i, duration in enumerate(duration_list):
            end_time = start_time+duration
            m_s, s_s = divmod(start_time, 60)
            h_s, m_s = divmod(m_s, 60)
            m_e, s_e = divmod(end_time, 60)
            h_e, m_e = divmod(m_e, 60)
            f.write(str(i+1)+'\n')
            f.write('%02d:%02d:%02d,200 --> %02d:%02d:%02d,000\n'%(h_s, m_s, s_s, h_e, m_e, s_e))
            f.write(text_list[i]+'\n')
            f.write('\n')
            start_time = end_time


if __name__ == '__main__':
    # auto_cut('eps_list.txt', 'sen2id.txt', '/Volumes/Macintosh\ HD/Downloads/Friends_mp4/S', 'temp/')
    # word2id, id2word, predictSamples = data_helper.loadDataset_predict('data/predict_data.pkl')
    # eps_list = read_eps_list('eps_list.txt')
    sen_list, id_list = data_helper.build_p_input('sen2id.txt')
    # a = sorted([7856, 8700, 36588, 8146, 27101, 16537, 7698, 52051, 17873, 45575, 7695, 19122, 26166])
    # a = [7695, 7696, 7698, 7699, 7700, 7856, 7857, 7858, 8146, 8147, 8148, 8700, 8701, 8702, 16537, 16538, 16539, 17873,
    #  17874, 42057, 42058, 42059, 19122, 19123, 19124, 27101, 27102, 27103, 36588, 36589, 36590,
    #  45575, 45576, 45577, 52051, 52052, 52053]
    # a = [55377, 55378, 55379, 55380, 55381, 11513, 11514, 11515, 11516, 11517, 17605, 17606, 17607, 17608, 17609, 19257, 19258, 19259, 19260, 19261, 20029, 20030, 20031, 20032, 20033, 20060, 20061, 20062, 20063, 20064, 20584, 20585, 20586, 20587, 918, 919, 920, 66261, 45832, 45833, 45834, 57538, 57539, 57540, 57541, 57542, 23643, 23644, 23645, 23646]
    # a = [54191, 54192, 54193, 7856, 7857, 44515, 66135, 11786, 41099, 27138, 57326, 57327, 57328, 9001, 9002, 9003, 9004, 9181, 9182, 9183, 9185, 9186, 9187, 9188, 11806, 11807, 11808, 11809, 12920, 12921, 12922, 12923, 16537, 16538, 16539, 16540, 17024, 17025, 17026, 17027, 51794, 51795, 51797, 37832, 37833, 18607, 18608, 18609, 18611]
    a = [54191, 54192, 54193, 7856, 7857, 44515, 66135, 11786, 41099, 27138, 57326, 57327, 57328, 9001, 9002, 9003, 9004, 9181, 9182, 9183, 9185, 9186, 9187, 9188, 11806, 11807, 11808, 11809, 12920, 12921, 12922, 12923, 16537, 16538, 16539, 16540, 17024, 17025, 17026, 17027, 51794, 51795, 51797, 37832, 37833, 18607, 18608, 18609, 18611]
    b = [52051, 52052, 51794, 19122, 19123, 19124, 19125, 36588, 36589, 36590, 36591, 39192, 39193, 39194, 39195, 39399,
         39400, 39401, 39402, 47729, 47730, 47731, 47732, 56042, 56043, 56044, 56045, 69149, 69150, 69151, 31531, 68077,
         68078, 68079, 68080, 60206, 60207]
    # i love you 0.8
    d = [54191, 54192, 54193, 54194, 8696, 8697, 8698, 8699, 8700, 7856, 7857, 44515, 66135, 59455, 59456, 59457, 59458, 59459, 9001, 9002, 9003, 9004, 9005, 11806, 11807, 11808, 11809, 11810, 12920, 12921, 12922, 12923, 12924, 16537, 16538, 16539, 16540, 16541, 18607, 18608, 18609, 18611, 18612, 18613, 18614, 31531, 68077, 68078, 68079, 68080]
    # 0.6
    g = [54191, 54192, 54193, 7856, 7857, 44515, 66135, 11786, 41099, 27138, 57326, 57327, 57328, 9001, 9002, 9003,
         9004, 9181, 9182, 9183, 9185, 9186, 9187, 9188, 11806, 11807, 11808, 11809, 12920, 12921, 12922, 12923, 16537,
         16538, 16539, 16540, 17024, 17025, 17026, 17027, 51794, 51795, 51797, 37832, 37833, 18607, 18608, 18609, 18611]
    # 0.4
    h = [54191, 54192, 13637, 1562, 1563, 1564, 1565, 30011, 30012, 30013, 30014, 5037, 5038, 5039, 5041, 5042, 5043,
         5044, 57741, 37832, 37833, 5475, 5476, 5477, 46831, 6174, 6175, 6176, 6177, 51794, 51795, 51797, 6584, 6585,
         6586, 6587, 7695, 7696, 7697, 57582, 55173, 44554, 21992, 27138, 14187, 25712, 7701, 7702, 7703]
    # 0.2
    j = [54799, 54800, 6007, 32401, 18506, 26167, 26168, 26169, 26170, 26171, 71, 72, 73, 74, 75, 100, 101, 102, 103, 104,
     135, 136, 137, 138, 139, 196, 197, 198, 199, 200, 221, 222, 223, 224, 225, 234, 235, 236, 237, 238, 272, 273, 274,
     275, 276, 356, 357, 358, 359, 360]
    # basic 0.8
    k = [58769, 58770, 52832, 52833, 52834, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59, 71, 72, 73, 74, 75, 100, 101, 102, 103, 104, 135, 136, 137, 138, 139, 196, 197, 198, 199, 200, 217, 218, 219, 220, 61694, 61695, 61696, 26167, 26168, 26169, 26170, 26171, 221, 222, 223]
    # basic 0.6
    l = [58769, 58770, 52832, 52833, 52834, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59, 63, 64, 65, 66, 67, 71, 72, 73, 74, 75, 100, 101, 102, 103, 104, 135, 136, 137, 138, 139, 184, 185, 186, 187, 188, 196, 197, 198, 199, 200, 210, 211, 212, 213, 55278]
    # basic 0.4
    m = [58769, 58770, 61998, 40, 41, 47, 48, 49, 50, 51, 55, 56, 57, 58, 59, 63, 64, 65, 66, 67, 71, 72, 73, 74, 26167, 26168, 26169, 26170, 26171, 83, 84, 85, 86, 87, 100, 101, 102, 103, 104, 108, 109, 110, 111, 112, 135, 136, 137, 138, 139, 184, 185]
    # basic 0.2
    n = [38555, 38556, 38557, 38558, 38559, 56042, 56043, 56044, 56045, 56046]
    # basic(2) 0.8 效果很差
    o = [31150, 31151, 5778, 5779, 5780, 39399, 39400, 39401, 39402, 39403, 43103, 43104, 43105, 43106, 43107, 47729, 47730, 47731, 47732, 47733, 64605, 64606, 64607, 64608, 64609]
    # mrjacr(9) 0.8 效果很差
    # print(sen_list[:10], id_list[:10])
    indexs, sen_lists = senid2videoid(id_list, sen_list, m)
    with open('cand.txt', 'w') as f:
        for i in sen_lists:
            f.write(i)
            f.write('\n')
    print(sen_lists)
    # video_path = '/Volumes/Macintosh\ HD/Downloads/Friends_mkv_n/S'
    # part_path = 'temp/'
    # indexs2video_part(indexs, video_path, part_path, 1000)





