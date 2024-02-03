import os
import argparse
import cv2
import glob
import imageio


def controller():
    pars = argparse.ArgumentParser(description='Resize images according to user input',
                                   allow_abbrev=False)
    pars.add_argument('-x',
                      '--resize_x',
                      metavar='int',
                      help='px value for image height resize (Required)',
                      action='store', type=int, required=True)
    pars.add_argument('-y',
                      '--resize_y',
                      metavar='int',
                      help='px value for image height resize (Required)',
                      action='store', type=int, required=True)
    pars.add_argument('-p',
                      '--prefix',
                      metavar='str',
                      help='rename images with custom prefix (Optional)',
                      action='store', type=str, default='resized')
    pars.add_argument('datapath',
                      help='the directory path containing the images to be resized',
                      action='store', type=str)
    pars.add_argument('output',
                      help='the output directory that will contain the resized images',
                      action='store', type=str)
    args = pars.parse_args()

    original_path = args.datapath
    img_name_list = glob.glob(os.path.join(args.datapath, '*'))
    resized_directory = args.output
    height = int(args.resize_x)
    width = int(args.resize_y)
    pref = str(args.prefix)

    count = 0
    removed = 0
    total = len(img_name_list)

    for img_path in img_name_list:
        try:
            img_cv2 = cv2.imread(os.path.join(original_path, img_path))
            channels = imageio.imread(os.path.join(original_path, img_path)).shape[2] \
                if imageio.imread(os.path.join(original_path, img_path)).ndim == 3 else 1
            if channels == 1:
                count = count + 1
                print(f'Image not included (Wrong ndim value) : [{count}/{total}]')
                removed = removed + 1
            else:
                cv2.imwrite(os.path.join(resized_directory, pref + str(count).zfill(6) + '.jpg'),
                            cv2.resize(img_cv2, (height, width)))
                count = count + 1
                print(f'Completed: [{count}/{total}]')
        except Exception as e:
            print(str(e))

    print(f'{removed} images not included in resizing because they do not match the set ndim value (3).')
    print('Done.')


if __name__ == '__main__':
    controller()
