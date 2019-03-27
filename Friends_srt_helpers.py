import re
import codecs
class srtParsing():
    index = 0
    # hour minute sec = 0
    duration = 0
    # print(time.time())

    def srtGetIndex(self, line):
        reg = re.compile('\d')  ## 将正则表达式的字符串形式编译为Pattern实例，然后使用Pattern实例处理文本并获得匹配结果
        if (reg.search(line)):
            print(line)

    def srtGetTimeStamp(self, line):
        reg = re.compile('\-\-\>')
        if (reg.search(line)):
            # print(line)
            time = line.split('-->')

            # START TIME:
            hour_end = time[1].split(':')
            minute_end = int(hour_end[1])
            sec_end = hour_end[2].split(',')
            hour_end = int(hour_end[0])
            mis_end = int(sec_end[1])
            sec_end = int(sec_end[0])
            # print("end-->h:%d m:%d s:%d,mis:%d" % (hour_end, minute_end, sec_end, mis_end))

            # END TIME:
            hour_start = time[0].split(':')
            minute_start = int(hour_start[1])
            sec_start = hour_start[2].split(',')
            hour_start = int(hour_start[0])
            mis_start = sec_start[1]
            sec_start = int(sec_start[0])

            if mis_end > 100:
                sec_end += 1

            time_start = hour_start * 60 * 60 + minute_start * 60 + sec_start
            # print("start time:%d" % time_start)
            time_end = hour_end * 60 * 60 + minute_end * 60 + sec_end
            # print("end time:%d" % time_end)
            duration = time_end - time_start
            # print(duration)
            return time_start,duration,time_end
        else:
            return False, False, False

    def srtGetSubInfo(self, line):
        reg = re.compile(r'[a-zA-Z]')
        reg_s = re.compile('\[')
        reg_z = re.compile('[\u4e00-\u9fa5]')
        if (reg.search(line) and not reg_s.search(line) and not reg_z.search(line)):
            return line

    def srtProcess(self, file):
        time_start_dict = []
        duration_dict = []
        time_end_dict = []
        text_dict = []
        time_temp = []
        duration_temp = []
        time_end_temp = []
        for line in file:
            time_start, duration, time_end = self.srtGetTimeStamp(line)
            if duration > 0 and time_start > 0:
                time_temp.append(time_start)
                duration_temp.append(duration)
                time_end_temp.append(time_end)
            line_true = self.srtGetSubInfo(line)
            reg_ds = re.compile('^(\.\.\.)')
            reg_de = re.compile('(\.\.\.)$')
            reg_p = re.compile('\,$')
            if line_true and len(time_temp) > 0:
                if len(time_start_dict)>0 and time_start_dict[-1]==time_temp[-1] and duration_dict[-1]==duration_temp[-1]:
                    text_dict[-1] = text_dict[-1]+' '+line_true.strip('-').strip()
                elif (len(text_dict)>0 and reg_de.search(text_dict[-1]) and reg_ds.search(line_true))or(len(text_dict)>0 and reg_p.search(text_dict[-1])):
                    text_dict[-1] = text_dict[-1]+line_true.strip('-').strip()
                    duration_dict[-1] = time_end_dict[-1] - time_start_dict[-1]
                else:
                    time_end_dict.append(time_end_temp[-1])
                    time_start_dict.append(time_temp[-1])
                    duration_dict.append(duration_temp[-1])
                    text_dict.append(line_true.strip('-').strip())
        return time_start_dict, duration_dict, text_dict

if __name__ == "__main__":  ## __name__ 是当前模块名，当模块被直接运行时模块名为 __main__ 。这句话的意思就是，当模块被直接运行时，以下代码块将被运行，当模块是被导入时，代码块不被运行。
    srt = srtParsing()
    f = codecs.open("Friends/srtfile/S7/S7-6.srt",'r','utf-8')
    aa,bb,cc = srt.srtProcess(f)
    print(aa[175],bb[175],cc[175])
    print(len(aa), len(bb), len(cc))
