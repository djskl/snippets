#encoding: gbk

with open(u"./全国重要生态功能区/土壤保持重要区/三峡库区土壤保持重要区.txt") as reader:
    cnt = reader.read()
    cnt = cnt.decode("gbk").encode("utf-8")

with open(u"./全国重要生态功能区/土壤保持重要区/三峡库区土壤保持重要区.txt", "w") as writer:
    writer.write(cnt)
