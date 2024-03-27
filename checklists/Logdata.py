def logdata(data):
    f = open('checklists\log.txt','+a')
    f.write(str(data)+"\n")
    f.close()
    return
