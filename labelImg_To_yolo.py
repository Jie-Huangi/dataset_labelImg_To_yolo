import argparse
import glob
from pathlib import Path
import random
import shutil
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

NUM_THREADS = min(8, max(1, os.cpu_count() - 1))

def run(func, this_iter, desc="Processing"):
    with ThreadPoolExecutor(max_workers=NUM_THREADS, thread_name_prefix='MyThread') as executor:
        results = list(
            tqdm(executor.map(func, this_iter), total=len(this_iter), desc=desc)
        )
    return results

def split_dataset_into_train_val_test(
    dataset_dir,
    save_dir,
    train_ratio=0.7,
    val_ratio=0.2,
    test_ratio=0.1,
    im_suffix='jpg'
):
    if isinstance(dataset_dir, str):
        dataset_dir = Path(dataset_dir)
    image_files = []
    for suffix in im_suffix:
        image_files += glob.glob(str(dataset_dir / 'images' / f"*.{suffix}"))
    total_images = len(image_files)
    random.shuffle(image_files)
    train_split = int(total_images * train_ratio)
    val_split = int(total_images * val_ratio)
    # test_split = int(total_images * test_ratio)

    if train_ratio + val_ratio == 1:
        train_images = image_files[:train_split]
        val_images = image_files[train_split:]
        test_images = []
    else:
        train_images = image_files[:train_split]
        val_images = image_files[train_split : train_split + val_split]
        test_images = image_files[train_split + val_split :]

    print('*'*25)
    print(
        "",
        f"Total images: {total_images}\n",
        f"Train images: {len(train_images)}\n",
        f"Val images: {len(val_images)}\n",
        f"Test images: {len(test_images)}"
    )
    print('*'*25)

    split_paths = [("train", train_images), ("val", val_images), ("test", test_images)]

    for split_name, images in split_paths:
        split_dir = Path(save_dir) / split_name
        for dir_name in ['images', 'labels']:
            if not (split_dir / dir_name).exists():
                (split_dir / dir_name).mkdir(exist_ok=True, parents=True)

        args_list = [(image, dataset_dir, split_dir) for image in images]

        run(process_image, args_list, desc=f"Creating {split_name} dataset")

        print(f"Created {split_name} dataset with {len(images)} images.")

def process_image(args):
    image_file, dataset_dir, split_dir = args
    annotation_file = dataset_dir / 'labels' / f"{Path(image_file).stem}.txt"
    assert annotation_file.exists(), f'{annotation_file} 不存在!'
    if not has_objects(annotation_file):
        return
    shutil.copy(image_file, split_dir / "images" / Path(image_file).name)
    shutil.copy(annotation_file, split_dir / "labels" / annotation_file.name)

def has_objects(annotation_path):
    with open(annotation_path, "r") as f:
        lines = f.readlines()
    return len(lines) > 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--data', default='./nailong_data')  # 数据集Images路径
    parser.add_argument('--save', default='./mydata')  # 保存路径
    parser.add_argument('--images_suffix', default=['jpg', 'png', 'jpeg'], help='images suffix')  # 图片后缀名

    opt = parser.parse_args()

    split_dataset_into_train_val_test(
        dataset_dir=opt.data,
        save_dir=opt.save,
        train_ratio=0.8,
        val_ratio=0.2,
        im_suffix=opt.images_suffix
    )
