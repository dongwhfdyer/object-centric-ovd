import os
import argparse
import shutil

from tqdm import tqdm


def delete_folders(*folder_path):
    for folder in folder_path:
        if os.path.exists(folder):
            shutil.rmtree(folder)


def create_folders(*folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_path', default='/data/pcl/datasets/imagnet21k')
    parser.add_argument('--dst_path', default='datasets/imagenet/ImageNet-LVIS')
    parser.add_argument('--data_path', default='datasets/imagenet_lvis_wnid.txt')
    args = parser.parse_args()

    # #---------kkuhn-block------------------------------ # original seperating code: find the selected one and then unzip from tar files.
    # f = open(args.data_path)
    # for i, line in enumerate(f):
    #     cmd = 'mkdir {x} && tar -xf {src}/{l}.tar -C {x}'.format(
    #         src=args.src_path,
    #         l=line.strip(),
    #         x=args.dst_path + '/' + line.strip())
    #     print(i, cmd)
    #     os.system(cmd)
    # #---------kkuhn-block------------------------------

    # ---------kkuhn-block------------------------------ # updated one: fine the selected one and then sim-link these files from the original imagenet folder.
    f = open(args.data_path)
    delete_folders(args.dst_path)
    create_folders(args.dst_path)

    for i, line in tqdm(enumerate(f), desc="Creating symbolic links"):
        src_folder = os.path.join(args.src_path, line.strip())
        dst_folder = os.path.join(args.dst_path, line.strip())
        if not os.path.exists(dst_folder):
            os.symlink(src_folder, dst_folder)
            # ---------kkuhn-block------------------------------
