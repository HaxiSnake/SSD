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
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # 创建视频输出对象
    output_name = name.split(".")[0] + "_%02d"%(1) + ".avi" # eg: example_01.avi
    writer = cv2.VideoWriter(output_path+output_name, fourcc, _fps, shape)

    SPLIT_FRAMES = 7500 # 分段视频的帧数 5*60*25
    count = 1 
    print("saving %s ..."%(output_name))
    while True:
        ret,frame = cap.read()
        if(ret is False):
            break
        # key=cv2.waitKey(1)
        writer.write(frame)
        # 
        if (count%SPLIT_FRAMES==0):
            writer.release()
            print("save %s done!"%(output_name))
            output_name = name.split(".")[0] + "_%02d"%(count//SPLIT_FRAMES+1) + ".avi" # eg: example_01.avi
            writer = cv2.VideoWriter(output_path+output_name, fourcc, _fps, shape)
            print("saving %s ..."%(output_name))
        count+=1
    writer.release()
    print("save %s done!"%(output_name))
    cap.release()  

if __name__ == "__main__":
    source_path=r"L:\Download\Data\teaching\\"
    output_path=r"L:\Download\Data\teaching\tmp\\"
    name = "01.mp4"
    main(source_path,name,output_path)