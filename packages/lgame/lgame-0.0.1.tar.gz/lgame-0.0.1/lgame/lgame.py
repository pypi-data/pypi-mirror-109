mport pygame, codecs
def text_print(text, font=None, size=50, color=(0,0,0), xy=(0,0), TF=True):
    """size=字体大小, font=字体名称, xy=位置"""
    a = pygame.font.SysFont(font, size)
    text_font = a.render(text, TF, color)
    screen = pygame.display.get_surface()
    screen.blit(text_font, xy)
def font_print(screen,text, font=None, size=50, color=(0,0,0), xy=(0,0), TF=True):
    """size=字体大小, font=字体名称, xy=位置"""
    a = pygame.font.SysFont(font, size)
    text_font = a.render(text, TF, color)
    screen.blit(text_font, xy)
# 对文件的操作
# 写入文本:
# 传入参数为content，strim，path；content为需要写入的内容，数据类型为字符串。
# path为写入的位置，数据类型为字符串。strim写入方式
# 传入的path需如下定义：path= r’ D:\text.txt’
# f = codecs.open(path, strim, 'utf8')中，codecs为包，需要用impor引入。
# strim=’a’表示追加写入txt，可以换成’w’，表示覆盖写入。
# 'utf8'表述写入的编码，可以换成'utf16'等。

def write_txt(content, strim, path):
    f = codecs.open(path, strim, encoding='utf8')
    f.write(str(content))
    f.close()
# 读取txt：
# 表示按行读取txt文件,utf8表示读取编码为utf8的文件，可以根据需求改成utf16，或者GBK等。
# 返回的为数组，每一个数组的元素代表一行，
# 若想返回字符串格式，可以将改写成return ‘\n’.join(lines)
def read_txt(path):
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return lines
print("hello!")