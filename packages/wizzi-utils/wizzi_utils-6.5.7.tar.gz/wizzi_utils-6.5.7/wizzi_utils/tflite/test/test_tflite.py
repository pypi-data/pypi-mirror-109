from wizzi_utils.tflite import tflite_tools as tflt
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.open_cv.test import test_open_cv_tools as cvtt
import os
# noinspection PyPackageRequirements
import cv2


def get_tflite_version_test():
    mt.get_function_name(ack=True, tabs=0)
    tflt.get_tflite_version(ack=True)
    return


def best_model_images_test():
    """
    works much nicer if the images are frames from a movie.
        also independent images are ok
    :return:
    """
    mt.get_function_name(ack=True, tabs=0)
    best_model_name = 'ssd_mobilenet_v3_small_coco_2020_01_14'

    save_dir = '{}/{}'.format(mtt.TFL_MODELS, best_model_name)

    model = tflt.ssd_mobilenet_coco(
        save_load_dir=save_dir,
        model_name=best_model_name,
        threshold=0.5,
        # allowed_class=[  # if you care about specific classes
        #     'person',
        #     'dog'
        # ],
        tabs=1,
    )
    print(model)

    images_names = [mtt.DOGS1, mtt.PERSON]
    cv_imgs_orig = [cvtt.load_img_from_web(image_name) for image_name in images_names]
    cvtt.__models_images_test(
        models=[model],
        images_names=images_names,
        cv_imgs_orig=cv_imgs_orig,
        grid=(1, 1),
        delay_ms=cvtt.BLOCK_MS_NORMAL,
        save_dir=None,
        display_im_size=(640, 480)
    )
    return


def models_compare_images_test():
    mt.get_function_name(ack=True, tabs=0)

    # Prepare models to compare
    # models_names = tflt.ssd_mobilenet_coco.MODEL_CONF.keys()
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
        save_dir = '{}/{}'.format(mtt.TFL_MODELS, m_name)
        m = tflt.ssd_mobilenet_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            # allowed_class=[  # if you care about specific classes
            #     'person',
            #     'dog'
            # ],
            tabs=1,
        )
        print(m)
        models.append(m)

    # cvtt.__models_images_test(models, grid=(3, 3), delay_ms=cvtt.BLOCK_MS_NORMAL, scope='tflt',
    #                           display_im_size=(480, 320))
    images_names = [mtt.DOGS1, mtt.PERSON]
    cv_imgs_orig = [cvtt.load_img_from_web(image_name) for image_name in images_names]
    save_dir = '{}/{}/tflt'.format(mtt.IMAGES_OUTPUTS, mt.get_function_name())
    mt.create_dir(save_dir)
    cvtt.__models_images_test(
        models=models,
        images_names=images_names,
        cv_imgs_orig=cv_imgs_orig,
        grid=(3, 3),
        delay_ms=cvtt.BLOCK_MS_NORMAL,
        save_dir=save_dir,
        display_im_size=(320, 240)
    )
    return


def best_model_video_test():
    mt.get_function_name(ack=True, tabs=0)
    best_model_name = 'ssd_mobilenet_v3_small_coco_2020_01_14'

    save_dir = '{}/{}'.format(mtt.TFL_MODELS, best_model_name)

    model = tflt.ssd_mobilenet_coco(
        save_load_dir=save_dir,
        model_name=best_model_name,
        threshold=0.5,
        # allowed_class=[  # if you care about specific classes
        #     'person',
        #     'dog'
        # ],
        tabs=1,
    )
    print(model)

    vid_name = mtt.DOG1
    video_path = cvtt.get_vid_from_web(name=vid_name)

    if not os.path.exists(video_path):
        mt.exception_error(mt.NOT_FOUND.format(video_path))
        return
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        video_total_frames = cvt.get_frames_from_cap(cap)
        print('\tvid {} has {} frames'.format(vid_name, video_total_frames))
        cvtt.__models_cap_test(
            models=[model],
            cap=cap,
            total_frames=video_total_frames,
            work_every_x_frames=80,
            grid=(1, 1),
            delay_ms=1,
            save_dir=None,
            display_im_size=(640, 480),
            title=vid_name
        )
    else:
        mt.exception_error('cap is closed.')
    return


def models_compare_video_test():
    mt.get_function_name(ack=True, tabs=0)

    # Prepare models to compare
    # models_names = tflt.ssd_mobilenet_coco.MODEL_CONF.keys()
    models_names = [
        'ssd_mobilenet_v3_small_coco_2020_01_14',
        'ssd_mobilenet_v2_mnasfpn',
        'ssd_mobilenet_v3_large_coco_2020_01_14',
        'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19',
        'ssd_mobilenet_v1_1_metadata_1',
        'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess',
        'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'
    ]
    # models_names = ['ssd_mobilenet_v3_small_coco_2020_01_14']
    models = []
    for m_name in models_names:
        save_dir = '{}/{}'.format(mtt.TFL_MODELS, m_name)
        m = tflt.ssd_mobilenet_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            # allowed_class=[  # if you care about specific classes
            #     'person',
            #     'dog'
            # ],
            tabs=1,
        )
        print(m)
        models.append(m)

    # cvtt.__models_cap_test(models, grid=(3, 3), delay_ms=1, display_im_size=(480, 320))
    vid_name = mtt.DOG1
    video_path = cvtt.get_vid_from_web(name=vid_name)

    if not os.path.exists(video_path):
        mt.exception_error(mt.NOT_FOUND.format(video_path))
        return
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        video_total_frames = cvt.get_frames_from_cap(cap)
        print('\tvid {} has {} frames'.format(vid_name, video_total_frames))
        save_dir = '{}/{}/cv'.format(mtt.IMAGES_OUTPUTS, mt.get_function_name())
        mt.create_dir(save_dir)
        cvtt.__models_cap_test(
            models=models,
            cap=cap,
            total_frames=video_total_frames,
            work_every_x_frames=80,
            grid=(3, 3),
            delay_ms=1,
            save_dir=save_dir,
            display_im_size=(320, 240),
            title=vid_name
        )
    else:
        mt.exception_error('cap is closed.')
    return


def best_model_cam_test():
    mt.get_function_name(ack=True, tabs=0)
    mt.get_function_name(ack=True, tabs=0)
    best_model_name = 'ssd_mobilenet_v3_small_coco_2020_01_14'

    save_dir = '{}/{}'.format(mtt.TFL_MODELS, best_model_name)

    model = tflt.ssd_mobilenet_coco(
        save_load_dir=save_dir,
        model_name=best_model_name,
        threshold=0.5,
        # allowed_class=[  # if you care about specific classes
        #     'person',
        #     'dog'
        # ],
        tabs=1,
    )
    print(model)

    cam = cvt.CameraWu.open_camera(port=0, type_cam='cv2')
    if cam is not None:
        cvtt.__models_cap_test(
            models=[model],
            cap=cam,
            total_frames=cvtt.MODEL_FRAMES_CAM,
            work_every_x_frames=1,
            grid=(1, 1),
            delay_ms=1,
            save_dir=None,
            display_im_size=(640, 480),
            title='cam 0'
        )
    else:
        mt.exception_error('cap is closed.')
    return


def models_compare_cam_test():
    mt.get_function_name(ack=True, tabs=0)

    # Prepare models to compare
    # models_names = tflt.ssd_mobilenet_coco.MODEL_CONF.keys()
    models_names = [
        'ssd_mobilenet_v3_small_coco_2020_01_14',
        'ssd_mobilenet_v2_mnasfpn',
        'ssd_mobilenet_v3_large_coco_2020_01_14',
        'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19',
        'ssd_mobilenet_v1_1_metadata_1',
        'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess',
        'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'
    ]
    # models_names = ['ssd_mobilenet_v3_small_coco_2020_01_14']
    models = []
    for m_name in models_names:
        save_dir = '{}/{}'.format(mtt.TFL_MODELS, m_name)
        m = tflt.ssd_mobilenet_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            # allowed_class=[  # if you care about specific classes
            #     'person',
            #     'dog'
            # ],
            tabs=1,
        )
        print(m)
        models.append(m)

    cam = cvt.CameraWu.open_camera(port=0, type_cam='cv2')
    if cam is not None:
        save_dir = '{}/{}/cv'.format(mtt.IMAGES_OUTPUTS, mt.get_function_name())
        mt.create_dir(save_dir)
        cvtt.__models_cap_test(
            models=models,
            cap=cam,
            total_frames=cvtt.MODEL_FRAMES_CAM,
            work_every_x_frames=1,
            grid=(3, 3),
            delay_ms=1,
            save_dir=save_dir,
            display_im_size=(320, 240),
            title='cam 0'
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
