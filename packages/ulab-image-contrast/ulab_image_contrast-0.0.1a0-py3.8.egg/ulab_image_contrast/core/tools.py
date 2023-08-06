import pathlib
from enum import Enum

import cv2
import numpy as np

import os

from ulab_image_contrast.core.ssim import ssim


def make_dir(path: str):
    if os.path.isdir(path) is False:
        os.makedirs(path)


def get_file_paths(original_path):
    _original_path = os.path.sep.join(pathlib.Path(original_path).parts)
    file_paths = list(pathlib.Path(_original_path).glob('**/*.jpg'))
    file_paths.extend(list(pathlib.Path(_original_path).glob('**/*.png')))
    paths = []
    for file_path in file_paths:
        paths.append(os.path.sep.join(file_path.parts).replace(_original_path + os.path.sep, ""))
    return (_original_path, paths)


class ContrastGrade(Enum):
    GRAYSCALE = 1,
    MULTICOLOR = 2


# def get_ssim_result(original_path, modified_path):
#    score, imageA, imageB = ssim(original_path, modified_path)
#    vis = np.concatenate((imageA, imageB), axis=0)
#    return (score,imageA, imageB,vis)
class ImageContrastResult:
    score: 0.0

    original_marked_image: None
    modified_marked_image: None

    def get_combine_marked(self):
        return np.concatenate((self.original_marked_image, self.modified_marked_image), axis=0)

    def __init__(self, original_marked_image, modified_marked_image, score):
        self.original_marked_image = original_marked_image
        self.modified_marked_image = modified_marked_image
        self.score = score


def contrast_file(original_path: str, modified_path: str, grade: ContrastGrade):
    score, imageA, imageB = ssim(original_path, modified_path)
    return ImageContrastResult(imageA, imageB, score)


def contrast_dir(original_path: str, modified_path: str, grade: ContrastGrade) -> dict:
    _original_path, original_file_paths = get_file_paths(original_path)
    _modified_path, modified_file_paths = get_file_paths(modified_path)
    print(original_file_paths)
    print(modified_file_paths)
    intersection = list(set(modified_file_paths) & set(original_file_paths))
    result = {}
    for imagepath in intersection:
        imageApath = os.path.join(_original_path, imagepath)
        imageBpath = os.path.join(_modified_path, imagepath)
        result[imagepath] = contrast_file(imageApath, imageBpath, grade)
    return result
    # modified_files = list(pathlib.Path(modified_path).glob('**/*.jpg'))
    # print(modified_files)


def cmd_contrast_any_with_report(original_path: str, modified_path: str, grade: ContrastGrade = ContrastGrade.GRAYSCALE,
                                 combine_marked_image: bool = False, report_dir: str = "contrast_report"):
    if os.path.isfile(original_path) and os.path.isfile(modified_path):
        contrast_file(original_path, modified_path, grade)
    if os.path.isdir(original_path) and os.path.isdir(modified_path):
        res = contrast_dir(original_path, modified_path, grade)
        result_original_path = os.path.join(report_dir, "original")
        result_modified_path = os.path.join(report_dir, "modified")
        result_combine_path = os.path.join(report_dir, "combined")
        make_dir(result_original_path)
        make_dir(result_modified_path)
        for key in res:
            (dirname, filename) = os.path.split(key)
            make_dir(os.path.join(result_original_path, dirname))
            cv2.imwrite(os.path.join(result_original_path, key), res[key].original_marked_image)
            make_dir(os.path.join(result_modified_path, dirname))
            cv2.imwrite(os.path.join(result_modified_path, key), res[key].modified_marked_image)
        if combine_marked_image is True:
            make_dir(result_combine_path)
            for key in res:
                (dirname, filename) = os.path.split(key)
                make_dir(os.path.join(result_combine_path, dirname))
                cv2.imwrite(os.path.join(result_combine_path, key), res[key].get_combine_marked())
