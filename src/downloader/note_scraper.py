# -*- coding: utf-8 -*-

import numpy as np
import cv2
from itertools import chain

# original_image = cv2.imread('./pattern/1/お願い!シンデレラ_pro.png')
# original_image = cv2.imread('./pattern/15/あんずのうた_master.png')
# original_image = cv2.imread('./pattern/17/DOKIDOKIリズム_master.png')
# original_image = cv2.imread('./pattern/57/オルゴールの小箱_master.png')
# self.template_images = {
#     "tap": cv2.imread('./pattern/tap.png'),
#     "right": cv2.imread('./pattern/right.png'),
#     "left": cv2.imread('./pattern/left.png'),
#     "long": cv2.imread('./pattern/long.png')
# }


def convert_color_to_gray(src_img):
    gray_scale = cv2.cvtColor(src_img, cv2.COLOR_RGB2GRAY)
    return gray_scale


def convert_gray_to_binary(src_img):
    # return cv2.adaptiveThreshold(src_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 0)
    return cv2.adaptiveThreshold(src_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 0)
    # return cv2.threshold(src_img, 0, 255, cv2.THRESH_BINARY)
    # img = cv2.medianBlur(src_img, 5)
    # ret, filtered = cv2.threshold(src_img, 140, 255, cv2.THRESH_BINARY)
    # return filtered


def convert_color_to_binary(src_img):
    return convert_gray_to_binary(convert_color_to_gray(src_img))


class NoteScraper:
    def __init__(self, note_image_path, template_images_data):
        self.original_image = cv2.imread(note_image_path)
        self.template_images_data = template_images_data

    def _generate_pad_position_candidates(self, image_size):
        width, height = image_size
        # pad位置の候補を取得する
        # pad位置原点
        org_x = 60
        org_y = height - 30
        # pad間隔
        gap_x = 150
        dif_x = 22
        gap_y = 6

        pos_array = [[[(org_x + i * gap_x + dif_x * k, org_y - j * gap_y)
                       for k in range(5)]
                      for j in range(150)]
                     for i in range(100)]

        return pos_array

    def _get_matching_pattern_name(self, target_image, position, threshold):

        def get_matching_max_val(template, position):
            (x, y) = position
            w, h = 16, 16
            scoped_image = target_image[y-h/2:y+h/2, x-w/2:x+w/2]
            if scoped_image.shape != (w, h):
                return None
            res = cv2.matchTemplate(scoped_image, template, cv2.TM_CCOEFF_NORMED)
            (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(res)
            return max_val

        max_value = 0
        max_name = "none"
        for template_name, template in self.template_images_data.items():
            tmp_max = get_matching_max_val(template, position)
            # print 'tmp max: {0}'.format(tmp_max)
            if tmp_max > max_value:
                max_value = tmp_max
                max_name = template_name

        if max_value is 0:
            return "none"

        if max_value <= threshold:
            return "none"

        return max_name

    def _get_matching_pattern_name_of_one_line_if_exist(self, target_image, positions):
        threshold = 0.35
        names = [self._get_matching_pattern_name(target_image, pos, threshold) for pos in positions]
        for name in names:
            if name != 'none':
                return names

        return None

    def scrape(self):
        target_image = convert_color_to_binary(self.original_image)
        h, w = target_image.shape
        pad_position_candidates = self._generate_pad_position_candidates((w, h))
        notes = []
        for row, pad_positions_in_row in enumerate(pad_position_candidates):
            for column, pad_positions_in_one_line in enumerate(pad_positions_in_row):
                labels = self._get_matching_pattern_name_of_one_line_if_exist(target_image, pad_positions_in_one_line)
                if labels is not None:
                    notes.append({
                        'position': {
                            'row': row,
                            'column': column
                        },
                        'labels': labels
                    })

        return notes


def scrape():
    template_images_data_original = {
        'tap': cv2.imread('./templates/tap_all.png'),
        'right': cv2.imread('./templates/right_all.png'),
        'left': cv2.imread('./templates/left_all.png'),
        'long': cv2.imread('./templates/long_start_all.png'),
    }
    template_images_data = {}
    for key, data in template_images_data_original.items():
        template_images_data[key] = convert_color_to_binary(data)

    note_scraper = NoteScraper('./templates/co_pattern_6_4_master.png', template_images_data)
    notes = note_scraper.scrape()
    print(notes)


def main():
    names = ['tap', 'right', 'left', 'long_start', 'long_end']
    types = ['co', 'cu', 'pa', 'all']
    originals = [[cv2.imread('./templates/' + name + '_' + type + '.png') for name in names] for type in types]
    gray_scaled_imgs = [[convert_color_to_gray(img) for img in original] for original in originals]
    binary_imgs = [[convert_gray_to_binary(img) for img in grays] for grays in gray_scaled_imgs]

    def get_concat_img(src):
        output = None
        for v in src:
            tmp = cv2.vconcat(v)
            if output is None:
                output = tmp
            else:
                output = cv2.hconcat([output, tmp])
        return output

    # output_img = cv2.hconcat([get_concat_img(original), get_concat_img(filterd)])
    output_img = cv2.hconcat([get_concat_img(gray_scaled_imgs), get_concat_img(binary_imgs)])
    # output_img = get_concat_img(binary_imgs)
    # output_image = cv2.vconcat([convert_color_to_binary(image) for image in template_images_data.values()])

    # note_scraper = NoteScraper()
    cv2.imshow('capture', output_img)
    cv2.waitKey(0)

if __name__ == '__main__':
    # main()
    scrape()
