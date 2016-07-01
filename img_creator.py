'''
1、获取运行参数，验证运行参数的合法性
2、读取图片目录中的所有图片，*.png、*.jpg、*.jpeg、*.bmp
3、筛选成对的图片，记录下图片原始名称（pic_name_NormalSuffix、pic_name_HighlightSuffix），pic_name为原始名称
4、读取模板文件
5、为每一对图片写入数据
'''


import os
import sys
import shutil

PARAM_NORMAL_SUFFIX = "-ns"
PARAM_HIGHLIGHT_SUFFIX = "-hs"
PARAM_PIC_LOCATION = "-l"
PARAM_PICS_DIR = "-pd"

PIC_PNG = "PNG"
PIC_JPG = "JPG"
PIC_JPEG = "JPEG"
PIC_BMP = "BMP"



normal_suffix = ""     #普通后缀
highlight_suffix = ""  #高亮后缀
pic_location = ""      #图片位置
pics_dir = ""          #图片目录
all_pics = []          #所有图片
pics_normal = []       #正常图片
pics_highlight = []    #高亮图片
pair_pics = []         #成对的图片




#读取参数
for i in range(1, len(sys.argv)-1):
    if PARAM_NORMAL_SUFFIX == sys.argv[i]:
        normal_suffix = sys.argv[i+1]
    elif PARAM_HIGHLIGHT_SUFFIX == sys.argv[i]:
        highlight_suffix = sys.argv[i+1]
    elif PARAM_PIC_LOCATION == sys.argv[i]:
        pic_location = sys.argv[i+1]
    elif PARAM_PICS_DIR == sys.argv[i]:
        pics_dir = sys.argv[i+1]



 
 
#验证运行参数
if (normal_suffix == "" and highlight_suffix == "") or pic_location == "" or pics_dir == "":
    print("参数不合法(-ns:普通后缀、-hs:高亮后缀、-l:图片位置、-pd:图片目录)")
    os._exit(0)

 
 
#读取录下面所有图片
files = os.listdir(pics_dir)
for file in files :
    suffix_upper = file[file.rfind(".")+1 :].upper()
    if suffix_upper == PIC_PNG or suffix_upper == PIC_JPG or suffix_upper == PIC_JPEG or suffix_upper == PIC_BMP:
        all_pics.append(file)
  
 

 
 
 
#筛选成对的图片
for pic in all_pics :
    if normal_suffix == "" :
        if pic.find(highlight_suffix) == -1 :
            pics_normal.append(pic[0 : pic.rfind(".")])
        else :
            pics_highlight.append(pic[0 : pic.rfind(highlight_suffix)-1])
   
    elif highlight_suffix == "" :
        if pic_find(normal_suffix) == -1 :
            pics_highlight.append(pic[0 : pic.rfind(".")])
        else :
            pics_normal.append(pic[0 : pic.rfind(normal_suffix)-1])
  
    else :
        if pic.find(normal_suffix) != -1 and pic.find(highlight_suffix) == -1 :
            pics_normal.append(pic[0 : pic.rfind(normal_suffix)-1])
        if pic.find(normal_suffix) == -1 and pic.find(highlight_suffix) != -1 :
             pics_highlight.append(pic[0 : pic.rfind(highlight_suffix)-1])
 
pair_pics = list(set(pics_normal).intersection(set(pics_highlight)))



 
 
 
#读取模板文件
file_template = open("template.xml", "r")
content_template = file_template.read()
file_template.close()


def get_content(pic_name):
    if highlight_suffix == "" :
        content = content_template.replace("<pic_name_hightlight>", pic_name)
    else :
        content = content_template.replace("<pic_name_hightlight>", pic_name + "_" + highlight_suffix)
  
    if normal_suffix == "" :
        content = content.replace("<pic_name_normal>", pic_name)
    else :
        content = content.replace("<pic_name_normal>", pic_name + "_" + normal_suffix)
  
    content = content.replace("<location>", pic_location)
    return content



#写入每一对图片数据
if os.path.exists("output"):
    shutil.rmtree("output")
os.mkdir("output")

for pic in pair_pics :
    pic_file = open("output\\" + pic + ".xml", "w")
    pic_file.write(get_content(pic))
    pic_file.close()






