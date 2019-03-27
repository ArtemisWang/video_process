import datetime

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
    duration_list = [3, 4, 2, 2, 4, 3, 4, 3, 4, 3, 2, 2, 3]
    text_list = ['I know I love you.', 'thing? I love you.', 'I love you.', 'Love you.', 'I love you the most.',
                 'I love you!', "That's right. I love you.", 'I love you. I know.', 'We had sex here, here, here...',
                 'You are so efficient. I love you.', 'Consider it forgotten. Thank you.', 'I love you goddesses.',
                 'You know, I love you.']
    write_srt('test.srt', duration_list, text_list)