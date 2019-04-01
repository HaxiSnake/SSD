import cv2 
def main(source_path,name,output_path):
    video_path=source_path+name
    # 读取视频文件
    cap = cv2.VideoCapture(video_path)
    # 获得输出视频大小，与原视频大小相同
    shape=(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # 获取输出视频的帧率
    _fps = cap.get(cv2.CAP_PROP_FPS)
    # 指定视频编码
    fourcc = cv2.VideoWriter_fourcc(*'MPG4')
    # 创建视频输出对象
    output_name = name.split(".")[0] + ".mp4" # eg: example_01.avi
    writer = cv2.VideoWriter(output_path+output_name, fourcc, _fps, shape)

    count = 1 
    print("saving %s ..."%(output_name))
    while True:
        ret,frame = cap.read()
        if(ret is False):
            break
        img=cv2.flip(frame,0)
        # key=cv2.waitKey(1)
        writer.write(img)
        
        count+=1
    writer.release()
    print("save %s done!"%(output_name))    
    cap.release()  

if __name__ == "__main__":
    source_path=r"H:\output\chosen\\"
    output_path=r"H:\output\chosen\\"
    names=["%02d.avi"%(i) for i in range(1,2)]

    for name in names:
        print(name)
        main(source_path,name,output_path)