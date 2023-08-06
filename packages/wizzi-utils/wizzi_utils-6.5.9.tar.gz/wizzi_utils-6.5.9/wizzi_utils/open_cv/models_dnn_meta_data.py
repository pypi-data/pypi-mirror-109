from enum import Enum
from wizzi_utils.open_cv.labels_bank import PASCAL_VOC_2012_21_LABELS
from wizzi_utils.open_cv.labels_bank import PASCAL_VOC_2012_20_LABELS
from wizzi_utils.open_cv.labels_bank import COCO_YOLO_80_LABELS
from wizzi_utils.open_cv.labels_bank import ILSVRC2016_201_LABELS
from wizzi_utils.open_cv.labels_bank import COCO_183_LABELS
from wizzi_utils.open_cv.labels_bank import COCO_182_LABELS


# from wizzi_utils_test.downloaded_models.labels_bank import IMAGENET


class Jobs(Enum):
    OBJECT_DETECTION = 'object_detection'
    SEGMENTATION = 'segmentation'
    OPEN_POSE = 'openpose'


class DnnFamily(Enum):
    Caffe = 'Caffe'
    Darknet = 'Darknet'
    TF = 'TensorFlow'


class DownloadStyle(Enum):
    Direct = 'Direct'
    Tar = 'tar'
    Zip = 'zip'


# models from: https://github.com/opencv/opencv_extra/tree/master/testdata/dnn
#  self.model.setInputParams(size=(416, 416), scale=1 / 255, swapRB=True)
MODELS_DNN_META_DATA = {
    'MobileNetSSD_deploy': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': (300, 300),  # TODO try both = (800,600)
        'scalefactor': 1 / 127.5,
        'mean': (127.5, 127.5, 127.5),
        'swapRB': False,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': PASCAL_VOC_2012_21_LABELS,
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/' +
                        'daef68a6c2f5fbb8c88404266aa28180646d17e0/MobileNetSSD_deploy.prototxt',
            'caffemodel': 'https://drive.google.com/uc?export=download&id=0B3gersZ2cHIxRm5PMWRoTkdHdHc',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'yolov4': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Darknet.value,
        'in_dims': (416, 416),
        'scalefactor': 1 / 255,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_YOLO_80_LABELS,
        'URL': {
            'cfg': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/yolov4.cfg',
            'weights': 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights',
            'cfg_download_style': DownloadStyle.Direct.value,
            'weights_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'yolov4-tiny': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Darknet.value,
        'in_dims': (416, 416),
        'scalefactor': 1 / 255,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_YOLO_80_LABELS,
        'URL': {
            'cfg': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/yolov4-tiny.cfg',
            'weights': 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights',
            'cfg_download_style': DownloadStyle.Direct.value,
            'weights_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'yolov3': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Darknet.value,
        'in_dims': (416, 416),
        'scalefactor': 1 / 255,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_YOLO_80_LABELS,
        'URL': {
            'cfg': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/yolov3.cfg',
            'weights': 'https://pjreddie.com/media/files/yolov3.weights',
            'cfg_download_style': DownloadStyle.Direct.value,
            'weights_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'yolov3_tiny': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Darknet.value,
        'in_dims': (416, 416),
        'scalefactor': 1 / 255,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_YOLO_80_LABELS,
        'URL': {
            'cfg': 'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg',
            'weights': 'https://github.com/ultralytics/yolov3/releases/download/v8/yolov3-tiny.weights',
            'cfg_download_style': DownloadStyle.Direct.value,
            'weights_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'yolov3-ssp': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Darknet.value,
        'in_dims': (416, 416),
        'scalefactor': 1 / 255,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_YOLO_80_LABELS,
        'URL': {
            'cfg': 'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-spp.cfg',
            'weights': 'https://github.com/ultralytics/yolov3/releases/download/v8/yolov3-spp.weights',
            'cfg_download_style': DownloadStyle.Direct.value,
            'weights_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'yolo-voc': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Darknet.value,
        'in_dims': (416, 416),
        'scalefactor': 1 / 255,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': PASCAL_VOC_2012_20_LABELS,
        'URL': {
            'cfg': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/yolo-voc.cfg',
            'weights': 'https://pjreddie.com/media/files/yolo-voc.weights',
            'cfg_download_style': DownloadStyle.Direct.value,
            'weights_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'yolov2-tiny-voc': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Darknet.value,
        'in_dims': (416, 416),
        'scalefactor': 1 / 255,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': PASCAL_VOC_2012_20_LABELS,
        'URL': {
            'cfg': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/tiny-yolo-voc.cfg',
            'weights': 'https://pjreddie.com/media/files/yolov2-tiny-voc.weights',
            'cfg_download_style': DownloadStyle.Direct.value,
            'weights_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'VGG_ILSVRC2016_SSD_300x300_deploy': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': (300, 300),
        'scalefactor': 1,
        'mean': (104, 117, 123),
        'swapRB': False,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': ILSVRC2016_201_LABELS,
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/ssd_vgg16.prototxt',
            'caffemodel': 'https://www.dropbox.com/s/8apyk3uzk2vl522/' +
                          'VGG_ILSVRC2016_SSD_300x300_iter_440000.caffemodel?dl=1',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'VGG_ILSVRC_16_layers': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': (800, 600),
        'scalefactor': 1,
        'mean': (102.9801, 115.9465, 122.7717),
        'swapRB': False,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': PASCAL_VOC_2012_21_LABELS,
        'need_normalize': 'normalize output needed',
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                        'faster_rcnn_vgg16.prototxt',
            'caffemodel': 'https://dl.dropboxusercontent.com/s/o6ii098bu51d139/faster_rcnn_models.tgz?dl=0',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Tar.value,
            'caffemodel_name': 'VGG16_faster_rcnn_final.caffemodel',
            'info1': 'TODO',
        }
    },
    'rfcn_pascal_voc_resnet50': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': (800, 600),
        'scalefactor': 1,
        'mean': (102.9801, 115.9465, 122.7717),
        'swapRB': False,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': PASCAL_VOC_2012_21_LABELS,
        'need_normalize': 'normalize output needed',
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                        'rfcn_pascal_voc_resnet50.prototxt',
            'caffemodel': 'https://onedrive.live.com/download?' +
                          'cid=10B28C0E28BF7B83&resid=10B28C0E28BF7B83%215317&authkey=%21AIeljruhoLuail8',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Tar.value,
            'caffemodel_name': 'resnet50_rfcn_final.caffemodel',
            'info1': 'TODO',
        }
    },
    'faster_rcnn_zf': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': (800, 600),
        'scalefactor': 1,
        'mean': (102.9801, 115.9465, 122.7717),
        'swapRB': False,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': PASCAL_VOC_2012_21_LABELS,
        'need_normalize': 'normalize output needed',
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                        'faster_rcnn_zf.prototxt',
            'caffemodel': 'https://dl.dropboxusercontent.com/s/o6ii098bu51d139/' +
                          'faster_rcnn_models.tgz?dl=0',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Tar.value,
            'caffemodel_name': 'ZF_faster_rcnn_final.caffemodel',
            'info1': 'TODO',
        }
    },
    'fcn8s-heavy-pascal': {
        'job': Jobs.OPEN_POSE.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': 'x',
        'scalefactor': 'x',
        'mean': 'x',
        'swapRB': False,
        'crop': False,
        'default_threshold': 0,
        'default_nms_threshold': 0,
        'labels_dict': 'x',
        'need_normalize': '??? normalize output needed',
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                        'fcn8s-heavy-pascal.prototxt',
            'caffemodel': 'http://dl.caffe.berkeleyvision.org/fcn8s-heavy-pascal.caffemodel',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Direct.value,
            'info1': 'TODO',
        }
    },
    'openpose_pose_mpi': {
        'job': Jobs.OPEN_POSE.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': 'x',
        'scalefactor': 'x',
        'mean': 'x',
        'swapRB': False,
        'crop': False,
        'default_threshold': 0,
        'default_nms_threshold': 0,
        'labels_dict': 'x',
        'need_normalize': '??? normalize output needed',
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                        'openpose_pose_mpi.prototxt',
            'caffemodel': 'http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/mpi/pose_iter_160000.caffemodel',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Direct.value,
            'info1': 'https://www.programmersought.com/article/3282857837/',
        }
    },
    'openpose_pose_coco': {
        'job': Jobs.OPEN_POSE.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': 'x',
        'scalefactor': 'x',
        'mean': 'x',
        'swapRB': False,
        'crop': False,
        'default_threshold': 0,
        'default_nms_threshold': 0,
        'labels_dict': 'x',
        'need_normalize': '??? normalize output needed',
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                        'openpose_pose_coco.prototxt',
            'caffemodel': 'http://posefs1.perception.cs.cmu.edu/OpenPose/models/pose/coco/pose_iter_440000.caffemodel',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Direct.value,
            'info1': 'https://github.com/CMU-Perceptual-Computing-Lab/openpose',
        }
    },
    'opencv_face_detector': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.Caffe.value,
        'in_dims': 'x',
        'scalefactor': 'x',
        'mean': 'x',
        'swapRB': False,
        'crop': False,
        'default_threshold': 0,
        'default_nms_threshold': 0,
        'labels_dict': 'x',
        'need_normalize': '??? normalize output needed',
        'URL': {
            'prototxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                        'opencv_face_detector.prototxt',
            'caffemodel': 'https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/' +
                          'res10_300x300_ssd_iter_140000.caffemodel',
            'prototxt_download_style': DownloadStyle.Direct.value,
            'caffemodel_download_style': DownloadStyle.Direct.value,
            'info1': 'https://www.programmersought.com/article/16544476883/',
        }
    },
    'ssd_inception_v2_coco_2017_11_17': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.TF.value,
        'in_dims': (300, 300),
        'scalefactor': 1,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_183_LABELS,
        # 'need_normalize': '??? normalize output needed',
        'URL': {
            'pbtxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                     'ssd_inception_v2_coco_2017_11_17.pbtxt',
            'pb': 'http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2017_11_17.tar.gz',
            'pbtxt_download_style': DownloadStyle.Direct.value,
            'pb_download_style': DownloadStyle.Tar.value,
            'pb_name': 'frozen_inference_graph.pb',
            'info1': '',
        }
    },
    'ssd_mobilenet_v1_coco': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.TF.value,
        'in_dims': (300, 300),
        'scalefactor': 1 / 255,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_183_LABELS,
        # 'need_normalize': '??? normalize output needed',
        'URL': {
            'pbtxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                     'ssd_mobilenet_v1_coco.pbtxt',
            'pb': 'http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_11_06_2017.tar.gz',
            'pbtxt_download_style': DownloadStyle.Direct.value,
            'pb_download_style': DownloadStyle.Tar.value,
            'pb_name': 'frozen_inference_graph.pb',
            'info1': '',
        }
    },
    'faster_rcnn_inception_v2_coco_2018_01_28': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.TF.value,
        'in_dims': (300, 300),
        'scalefactor': 1,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_182_LABELS,  # TODO check labels are correct
        # 'need_normalize': '??? normalize output needed',
        'URL': {
            'pbtxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                     'faster_rcnn_inception_v2_coco_2018_01_28.pbtxt',
            'pb': 'http://download.tensorflow.org/models/object_detection/' +
                  'faster_rcnn_inception_v2_coco_2018_01_28.tar.gz',
            'pbtxt_download_style': DownloadStyle.Direct.value,
            'pb_download_style': DownloadStyle.Tar.value,
            'pb_name': 'frozen_inference_graph.pb',
            'info1': '',
        }
    },
    'faster_rcnn_resnet50_coco_2018_01_28': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.TF.value,
        'in_dims': (300, 300),
        'scalefactor': 1,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_183_LABELS,  # TODO check labels are correct
        # 'need_normalize': '??? normalize output needed',
        'URL': {
            'pbtxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                     'faster_rcnn_resnet50_coco_2018_01_28.pbtxt',
            'pb': 'http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet50_coco_2018_01_28.tar.gz',
            'pbtxt_download_style': DownloadStyle.Direct.value,
            'pb_download_style': DownloadStyle.Tar.value,
            'pb_name': 'frozen_inference_graph.pb',
            'info1': '',
        }
    },
    'ssd_mobilenet_v1_coco_2017_11_17': {
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.TF.value,
        'in_dims': (300, 300),
        'scalefactor': 1,
        'mean': (0, 0, 0),
        'swapRB': True,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_183_LABELS,  # TODO check labels are correct
        # 'need_normalize': '??? normalize output needed',
        'URL': {
            'pbtxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                     'ssd_mobilenet_v1_coco_2017_11_17.pbtxt',
            'pb': 'http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2017_11_17.tar.gz',
            'pbtxt_download_style': DownloadStyle.Direct.value,
            'pb_download_style': DownloadStyle.Tar.value,
            'pb_name': 'frozen_inference_graph.pb',
            'info1': '',
        }
    },
    'ssd_mobilenet_v1_ppn_coco': {  # TODO check params
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.TF.value,
        'in_dims': (300, 300),
        'scalefactor': 1,
        'mean': (127, 127, 127),
        'swapRB': False,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_183_LABELS,  # TODO check labels are correct
        # 'need_normalize': '??? normalize output needed',
        'URL': {
            'pbtxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                     'ssd_mobilenet_v1_ppn_coco.pbtxt',
            'pb': 'http://download.tensorflow.org/models/object_detection/' +
                  'ssd_mobilenet_v1_ppn_shared_box_predictor_300x300_coco14_sync_2018_07_03.tar.gz',
            'pbtxt_download_style': DownloadStyle.Direct.value,
            'pb_download_style': DownloadStyle.Tar.value,
            'pb_name': 'frozen_inference_graph.pb',
            'info1': '',
        }
    },
    'ssd_mobilenet_v2_coco_2018_03_29': {  # TODO check params
        'job': Jobs.OBJECT_DETECTION.value,
        'family': DnnFamily.TF.value,
        'in_dims': (300, 300),
        'scalefactor': 1,
        'mean': (0, 0, 0),
        'swapRB': False,
        'crop': False,
        'default_threshold': 0.2,
        'default_nms_threshold': 0.4,
        'labels_dict': COCO_183_LABELS,  # TODO check labels are correct
        # 'need_normalize': '??? normalize output needed',
        'URL': {
            'pbtxt': 'https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/dnn/' +
                     'ssd_mobilenet_v2_coco_2018_03_29.pbtxt',
            'pb': 'http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz',
            'pbtxt_download_style': DownloadStyle.Direct.value,
            'pb_download_style': DownloadStyle.Tar.value,
            'pb_name': 'frozen_inference_graph.pb',
            'info1': '',
        }
    },
}
