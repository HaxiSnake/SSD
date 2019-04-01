import VideoToPicture
import XmlConvert
import GetMainTxt
# source_path=r"L:\Download\Data\teaching\record\\"
# source_name="0102"
# output_path=r"L:\Download\Data\teaching\record\CLASSROOM\\"
# VideoToPicture.main(source_path,output_path,source_name)
# XmlConvert.main(source_path,output_path,source_name)

names=["%02d"%(i) for i in range(1,6)]
source_path=r"K:\output\chosen\\"
output_path=r"K:\CLASSROOM\\"
for name in names:
    print(name)
    VideoToPicture.main(source_path,output_path,name)
    XmlConvert.main(source_path,output_path,name)
# GetMainTxt.main(output_path)
