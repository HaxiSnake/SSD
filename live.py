import glob
import os

import torch
from PIL import Image
from tqdm import tqdm
from ssd.config import cfg
from ssd.data.datasets import COCODataset, VOCDataset, CLADataset
from ssd.modeling.predictor import Predictor
from ssd.modeling.vgg_ssd import build_ssd_model
import argparse
import numpy as np
import cv2

from ssd.utils.viz import draw_bounding_boxes


def run_demo(cfg, weights_file, iou_threshold, score_threshold, video_dir, output_dir, dataset_type):
    if dataset_type == "voc":
        class_names = VOCDataset.class_names
    elif dataset_type == 'coco':
        class_names = COCODataset.class_names
    elif dataset_type == 'cla':
        class_names = CLADataset.class_names
    else:
        raise NotImplementedError('Not implemented now.')

    device = torch.device(cfg.MODEL.DEVICE)
    model = build_ssd_model(cfg)
    model.load(weights_file)
    print('Loaded weights from {}.'.format(weights_file))
    model = model.to(device)
    predictor = Predictor(cfg=cfg,
                          model=model,
                          iou_threshold=iou_threshold,
                          score_threshold=score_threshold,
                          device=device)
    cpu_device = torch.device("cpu")
    stream = cv2.VideoCapture(video_dir)
#     image_paths = glob.glob(os.path.join(video_dir, '*.jpg'))
    # 获得输出视频大小，与原视频大小相同
    shape=(int(stream.get(cv2.CAP_PROP_FRAME_WIDTH)),int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # 获取输出视频的帧率
    _fps = stream.get(cv2.CAP_PROP_FPS)
    # 指定视频编码
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # 如果输出目录不存在 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 创建视频输出对象
    output_name = os.path.basename(video_dir)
    output_name = output_name.split('.')[0] + ".avi"
    writer = cv2.VideoWriter(os.path.join(output_dir, output_name), fourcc, _fps, shape)
    
    while True:
        ret, image = stream.read()
        if ret is False :
            break
        output = predictor.predict(image)
        boxes, labels, scores = [o.to(cpu_device).numpy() for o in output]
        drawn_image = draw_bounding_boxes(image, boxes, labels, scores, class_names).astype(np.uint8)
        writer.write(drawn_image)
    writer.release()
    stream.release()
#     for image_path in tqdm(image_paths):
#         image = Image.open(image_path).convert("RGB")
#         image = np.array(image)
#         output = predictor.predict(image)
#         boxes, labels, scores = [o.to(cpu_device).numpy() for o in output]
#         drawn_image = draw_bounding_boxes(image, boxes, labels, scores, class_names).astype(np.uint8)
#         image_name = os.path.basename(image_path)
#         Image.fromarray(drawn_image).save(os.path.join(output_dir, image_name))


def main():
    parser = argparse.ArgumentParser(description="SSD Demo.")
    parser.add_argument(
        "--config-file",
        default="",
        metavar="FILE",
        help="path to config file",
        type=str,
    )
    parser.add_argument("--weights", type=str, help="Trained weights.")
    parser.add_argument("--iou_threshold", type=float, default=0.5)
    parser.add_argument("--score_threshold", type=float, default=0.5)
    parser.add_argument("--video_dir", default='demo', type=str, help='Specify a video dir to do prediction.')
    parser.add_argument("--output_dir", default='demo/result', type=str, help='Specify a image dir to save predicted images.')
    parser.add_argument("--dataset_type", default="voc", type=str, help='Specify dataset type. Currently support voc and coco.')

    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )
    args = parser.parse_args()
    print(args)

    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()

    print("Loaded configuration file {}".format(args.config_file))
    with open(args.config_file, "r") as cf:
        config_str = "\n" + cf.read()
        print(config_str)
    print("Running with config:\n{}".format(cfg))

    run_demo(cfg=cfg,
             weights_file=args.weights,
             iou_threshold=args.iou_threshold,
             score_threshold=args.score_threshold,
             video_dir=args.video_dir,
             output_dir=args.output_dir,
             dataset_type=args.dataset_type)


if __name__ == '__main__':
    main()
