import SplitVideo

source_path=r"L:\Download\Data\teaching\\"
output_path=r"H:\output\\"
names=["%02d.mp4"%(i) for i in range(1,15)]

for name in names:
    print(name)
    SplitVideo.main(source_path,name,output_path)
