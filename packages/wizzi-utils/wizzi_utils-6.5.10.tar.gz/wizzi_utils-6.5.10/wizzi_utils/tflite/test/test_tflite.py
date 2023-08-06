from wizzi_utils.tflite import tflite_tools as tflt
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.open_cv.test import test_open_cv_tools as cvtt
import os
# noinspection PyPackageRequirements
import cv2

SAVE_SCOPE = 'TFL'
BEST_MODEL = 'ssd_mobilenet_v3_large_coco_2020_01_14'
BEST_MODEL_SAVE_DIR = '{}/{}/{}'.format(mtt.TFL_MODELS, tflt.MODELS_TFL_META_DATA[BEST_MODEL]['job'], BEST_MODEL)


def get_tflite_version_test():
    mt.get_function_name(ack=True, tabs=0)
    tflt.get_tflite_version(ack=True)
    return


def __get_best_model():
    model = tflt.TfltObjectDetectionModels(
        save_load_dir=BEST_MODEL_SAVE_DIR,
        model_name=BEST_MODEL,
        # threshold=0.2,  # take default
        allowed_class=None,
        tabs=1
    )
    print(model)
    grid = (1, 1)
    display_im_size = (640, 480)
    return [model], grid, display_im_size


def __get_best_models():
    # Prepare models to compare
    models_names = [
        'ssd_mobilenet_v3_small_coco_2020_01_14',
        # 'ssd_mobilenet_v2_mnasfpn',
        'ssd_mobilenet_v3_large_coco_2020_01_14',
        # 'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19',
        # 'ssd_mobilenet_v1_1_metadata_1',
        # 'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess',
        # 'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'
    ]

    models = []
    for m_name in models_names:
        save_dir = '{}/{}/{}'.format(mtt.TFL_MODELS, tflt.MODELS_TFL_META_DATA[BEST_MODEL]['job'], m_name)
        m = tflt.TfltObjectDetectionModels(
            save_load_dir=save_dir,
            model_name=m_name,
            # threshold=0.2,  # take default
            allowed_class=None,
            tabs=1
        )
        print(m)
        models.append(m)

    grid = (1, 2)
    display_im_size = (640, 480)
    return models, grid, display_im_size


def __get_all_models():
    # Prepare models to compare
    models_names = [
        'ssd_mobilenet_v3_small_coco_2020_01_14',
        'ssd_mobilenet_v2_mnasfpn',
        'ssd_mobilenet_v3_large_coco_2020_01_14',
        'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19',
        'ssd_mobilenet_v1_1_metadata_1',
        'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess',
        'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'
    ]

    models = []
    for m_name in models_names:
        save_dir = '{}/{}/{}'.format(mtt.TFL_MODELS, tflt.MODELS_TFL_META_DATA[BEST_MODEL]['job'], m_name)
        m = tflt.TfltObjectDetectionModels(
            save_load_dir=save_dir,
            model_name=m_name,
            # threshold=0.2,  # take default
            allowed_class=None,
            tabs=1
        )
        print(m)
        models.append(m)

    grid = (2, 4)
    display_im_size = (320, 240)
    return models, grid, display_im_size


def best_model_images_test():
    mt.get_function_name(ack=True, tabs=0)
    models_compare_images_test(models_selection='best')
    return


def models_compare_images_test(
        cv_imgs_orig: list = None,
        images_names: list = None,
        models_selection: str = 'best_models',
        ms: int = cvtt.BLOCK_MS_NORMAL
):
    mt.get_function_name(ack=True, tabs=0)
    if models_selection == 'best_models':
        models, grid, im_size = __get_best_models()
    elif models_selection == 'all':
        models, grid, im_size = __get_all_models()
    else:
        models, grid, im_size = __get_best_model()
    if cv_imgs_orig is None:
        images_names = [mtt.DOGS1, mtt.PERSON]
        cv_imgs_orig = [cvtt.load_img_from_web(image_name) for image_name in images_names]
    else:
        if images_names is None:
            images_names = []
            for i in range(len(cv_imgs_orig)):
                images_names.append('unknown{}'.format(i))
        if len(images_names) != len(cv_imgs_orig):
            mt.exception_error('lists length differ {}, {}'.format(len(images_names), len(cv_imgs_orig)))
            return

    save_dir = '{}/{}/{}/{}'.format(mtt.IMAGES_OUTPUTS, mt.get_function_name(), SAVE_SCOPE, models_selection)
    mt.create_dir(save_dir)
    cvtt.__models_images_test(
        models=models,
        images_names=images_names,
        cv_imgs_orig=cv_imgs_orig,
        grid=grid,
        delay_ms=ms,
        save_dir=save_dir,
        display_im_size=im_size
    )
    return


def best_model_video_test():
    mt.get_function_name(ack=True, tabs=0)
    models_compare_video_test(models_selection='best')
    return


def models_compare_video_test(
        video_path: str = None,
        vid_name: str = 'unknown',
        work: int = 80,
        models_selection: str = 'best_models'
):
    mt.get_function_name(ack=True, tabs=0)
    if models_selection == 'best_models':
        models, grid, im_size = __get_best_models()
    elif models_selection == 'all':
        models, grid, im_size = __get_all_models()
    else:
        models, grid, im_size = __get_best_model()
    if video_path is None:  # default video
        vid_name = mtt.DOG1
        video_path = cvtt.get_vid_from_web(name=vid_name)

    if not os.path.exists(video_path):
        mt.exception_error(mt.NOT_FOUND.format(video_path))
        return
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        video_total_frames = cvt.get_frames_from_cap(cap)
        print('\tvid {} has {} frames'.format(vid_name, video_total_frames))
        save_dir = '{}/{}/{}/{}'.format(mtt.VIDEOS_OUTPUTS, mt.get_function_name(), SAVE_SCOPE, models_selection)
        mt.create_dir(save_dir)
        cvtt.__models_cap_test(
            models=models,
            cap=cap,
            total_frames=video_total_frames,
            work_every_x_frames=work,
            grid=grid,
            delay_ms=1,
            save_dir=save_dir,
            display_im_size=im_size,
            cap_desc=vid_name
        )
    else:
        mt.exception_error('cap is closed.')
    return


def best_model_cam_test():
    mt.get_function_name(ack=True, tabs=0)
    models_compare_cam_test(models_selection='best')
    return


def models_compare_cam_test(
        models_selection: str = 'best_models',
        total_frames: int = cvtt.MODEL_FRAMES_CAM
):
    mt.get_function_name(ack=True, tabs=0)
    if models_selection == 'best_models':
        models, grid, im_size = __get_best_models()
    elif models_selection == 'all':
        models, grid, im_size = __get_all_models()
    else:
        models, grid, im_size = __get_best_model()
    cam = cvt.CameraWu.open_camera(port=0, type_cam='cv2')
    if cam is not None:
        save_dir = '{}/{}/{}/{}'.format(mtt.VIDEOS_OUTPUTS, mt.get_function_name(), SAVE_SCOPE, models_selection)
        mt.create_dir(save_dir)
        cvtt.__models_cap_test(
            models=models,
            cap=cam,
            total_frames=total_frames,
            work_every_x_frames=1,
            grid=grid,
            delay_ms=1,
            save_dir=save_dir,
            display_im_size=im_size,
            cap_desc='cam 0'
        )
    else:
        mt.exception_error('cap is closed.')
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    get_tflite_version_test()
    best_model_images_test()
    best_model_video_test()
    best_model_cam_test()
    models_compare_images_test()
    models_compare_video_test()
    models_compare_cam_test()
    print('{}'.format('-' * 20))
    return
