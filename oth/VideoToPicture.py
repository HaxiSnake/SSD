import cv2 
def main(source_path,output_path,name):
    video_path=source_path+name+'.avi'
    picture_dir=output_path+'JPEGImages\\'
    prfix=name+'_'
    cap = cv2.VideoCapture(video_path)
    frm_cnt=0
    print("saving pictures...")
    while True:
        ret,frame = cap.read()
        if(ret is False):
            break
        imname=picture_dir+prfix+"%04d"%(frm_cnt)+".jpg"
        frame=cv2.resize(frame,None,fx=0.5,fy=0.5)
        cv2.imwrite(imname,frame,(cv2.IMWRITE_JPEG_QUALITY,100))
        frm_cnt+=1
    print("finished! %d xmls saved"%(frm_cnt))
    cap.release()  

if __name__ == "__main__":
    source_path=r"L:\Download\Data\teaching\record\\"
    output_path=r"L:\Download\Data\teaching\record\\"
    main(source_path,output_path,"0101")