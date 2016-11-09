def app_type():
    try:
        with open('protocol_list.txt','r') as fp:
            lines = fp.readlines()
    except IOError:
        path = os.path.join(pwd, 'reportlog/nDPI_support_protocol_list.txt')
        with open(path,'r') as fp:
            lines = fp.readlines()

    num = lambda x:x.split(',')[0].strip('\n')
    name = lambda x:x.split(',')[1].strip('\n')

    name_type = { num(line):name(line) for line in lines }
    return name_type

print app_type()

