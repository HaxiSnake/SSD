import xml.etree.ElementTree as ET 

def read_xml(in_path):
  '''''读取并解析xml文件
    in_path: xml路径
    return: ElementTree'''
  return ET.parse(in_path)
def if_match(node, kv_map):
  '''''判断某个节点是否包含所有传入参数属性
    node: 节点
    kv_map: 属性及属性值组成的map'''
  for key in kv_map:
    if node.get(key) != kv_map.get(key):
      return False
  return True
#---------------search -----
def find_nodes(tree, path):
  '''''查找某个路径匹配的所有节点
    tree: xml树
    path: 节点路径'''
  return tree.findall(path)
def get_node_by_keyvalue(nodelist, kv_map):
  '''''根据属性及属性值定位符合的节点，返回节点
    nodelist: 节点列表
    kv_map: 匹配属性及属性值map'''
  result_nodes = []
  for node in nodelist:
    if if_match(node, kv_map):
      result_nodes.append(node)
  return result_nodes
#---------------write-----
def write_to_xml(nodes,output_path,attrs):
    annotation=ET.Element('annotation')
    filename = ET.SubElement(annotation,'filename')
    filename.text=attrs['filename']+'.jpg'
    folder = ET.SubElement(annotation,'folder')
    folder.text=attrs['folder']
    # 添加人物定位框
    for node in nodes:
        item=ET.SubElement(annotation,'object')
        name=ET.SubElement(item,'name')
        name.text=attrs['objectname']
        bndbox=ET.SubElement(item,'bndbox')
        keys=['xmin','ymin','xmax','ymax']
        attr=['xtl','ytl','xbr','ybr']
        for i in range(4):
            num=ET.SubElement(bndbox,keys[i])
            num.text=str(int(float(node.get(attr[i]))/2))
        attrdict={'difficult':'0','occluded':'0','pose':'Unsepcified','truncated':'1'}
        for key,value in attrdict.items():
            tmp=ET.SubElement(item,key)
            tmp.text=value
    # segmented 属性
    segmented = ET.SubElement(annotation,'segmented')
    segmented.text='0'
    # 添加图像大小
    size = ET.SubElement(annotation,'size')
    sizedict={}
    sizedict['depth']='3'
    sizedict['width']=attrs['width']
    sizedict['height']=attrs['height']
    for key,value in sizedict.items():
        tmp=ET.SubElement(size,key)
        tmp.text=value
    source=ET.SubElement(annotation,'source')
    names=['annotation','database','image']
    for key in names:
        tmp=ET.SubElement(source,key)
        tmp.text=attrs[key]
    # 增加换行符 
    def __indent(elem, level=0): 
        i = "\n" + level*"\t"
        if len(elem): 
            if not elem.text or not elem.text.strip(): 
                elem.text = i + "\t" 
            if not elem.tail or not elem.tail.strip(): 
                elem.tail = i 
            for elem in elem: 
                __indent(elem, level+1) 
            if not elem.tail or not elem.tail.strip(): 
                elem.tail = i 
        else: 
            if level and (not elem.tail or not elem.tail.strip()): 
                elem.tail = i
    __indent(annotation)
    tree = ET.ElementTree(annotation)
    tree.write(output_path+attrs['filename']+'.xml',encoding='utf-8',xml_declaration=True)
def write_by_frame(nodes,frame_id,output_path,prefix):
    attrs={
    'filename':'test',
    'folder':'CLASSROOM',
    'objectname':'person',
    'width':'640',
    'height':'360',
    'annotation':"CLASSROOM2019",
    'database':"CLASSROOM2019",
    'image':"video"
    }
    frame_nodes=get_node_by_keyvalue(nodes,{'frame':str(frame_id)})
    if(len(frame_nodes)>0):
        attrs['filename']=prefix+"%04d"%(frame_id)
        write_to_xml(frame_nodes,output_path,attrs)
        return True
    else:
        return False

def main(source_path,output_path,name):
    xml_filepath=source_path + name + ".xml"
    prefix = name+'_'
    output_path = output_path + "Annotations\\"
    #读取原始xml
    tree=read_xml(xml_filepath)
    #查找box节点
    path="track/box"
    nodes=find_nodes(tree,path)
    #按照帧数搜索object并保存至指定目录
    print("saving xmls...")
    i=0
    while(write_by_frame(nodes,i,output_path,prefix)):
        i=i+1
    print("finished! %d xmls saved"%(i))
    
if __name__ == "__main__":
    source_path=r"L:\Download\Data\teaching\record\\"
    output_path=r"L:\Download\Data\teaching\record\\"
    name="0101"
    main(source_path,output_path,name)


