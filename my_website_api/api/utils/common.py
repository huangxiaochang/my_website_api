# __*__ coding: utf-8 __*__

# 在指定的文件路径file_path下，写入文件file，该方法使用的是文件分块的写入法， 适合大文件， 当然小文件也可以用
def save_file(file, file_path):
    dest = open(file_path, 'wb+')
    for chunk in file.chunks():
        dest.write(chunk)
    dest.close()
