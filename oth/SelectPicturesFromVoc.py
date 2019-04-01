# -*- coding: UTF-8 -*-
import xml.etree.ElementTree as ET 
import logging
import cv2
import os
import os.path as osp
import GetMainTxt

logging.basicConfig(level = logging.INFO,format = '%(asctime)s-%(funcName)s-%(lineno)d-%(levelname)s:: %(message)s')
logger = logging.getLogger(__name__)
def select_object(source,output,classname="person"):
    """
        从VOC格式的xml文件中筛选出特定的类并保存
        @source: 原VOC xml 文件
        @output: 新VOC xml 文件
        @classname: 选择的类
    """
    try:
        tree=ET.parse(source)
    except Exception as e:
        logging.error(e)
        return
    root=tree.getroot()
    for item in root.findall('object'):
        name=item.find('name').text
        if(name != classname):
            root.remove(item)
    tree.write(output)


def extract_voc(rootpath,classname,output_rootpath,prefix='unknownvoc'):
    """
        用于将VOC数据集中特定类的图片提取出来并存入新的VOC格式的数据集当中
        @rootpath: 原VOC数据集根目录 eg: /share/VOCdevkit/VOC2007/
        @classname: 指定特定的类 eg:person 这时会查找person_trainval.txt 和 person_test.txt
        @output_rootpath: 新的VOC格式数据集目录 eg:/share/DONG/CLASSROOM/
        @prefix: 用作新文件的前缀
    """
    logging.info("start extract %s from %s to %s, prefix is %s"%(classname,rootpath,output_rootpath,prefix))
    picture_path=osp.join(rootpath,"JPEGImages")
    xml_path = osp.join(rootpath,"Annotations")
    o_picture_path=osp.join(output_rootpath,"JPEGImages")
    o_xml_path=osp.join(output_rootpath,"Annotations")
    sets=["trainval","test"]
    fnames=[]
    for item in sets:
        filename = classname + "_" + item + ".txt"
        fname=osp.join(rootpath,"ImageSets","Main",filename)
        if(osp.exists(fname)):
            fnames.append(fname)
        else:
            logging.info("Can not find %s, go on ..."%(fname))
    for fname in fnames:
        for line in open(fname):
            line=line.strip()
            strlist = line.split(' ')
            name, ret = strlist[0],line[1]
            pic_name=name+".jpg"
            xml_name=name+".xml"
            ret=int(ret)
            if(ret==1):
                print(pic_name)
                new_picname=prefix + pic_name
                order = "cp %s %s"%( osp.join(picture_path , pic_name), osp.join(o_picture_path,new_picname))
                os.system(order)
                new_xmlname=prefix + xml_name
                select_object(osp.join(xml_path , xml_name),osp.join(o_xml_path,new_xmlname),classname=classname)

if __name__ == "__main__":
    outputpath = "/share/DONG/CLASSROOM"
    args_list=[
        {
            "rootpath":"/share/DONG/VOCdevkit/VOC2007/",
            "classname":"person",
            "output_rootpath":outputpath,
            "prefix":"voc07"
        },
        {
            "rootpath":"/share/DONG/VOCdevkit/VOC2012/",
            "classname":"person",
            "output_rootpath":outputpath,
            "prefix":"voc12"
        }
    ]
    for args in args_list:
        extract_voc(**args)  