"""
统计训练集和验证集的数据并生成相应.txt文件
"""
import os

train_annotation_dir = "./mydata/train/labels"
val_annotation_dir = "./mydata/val/labels"


assert os.path.exists(train_annotation_dir), "train_annotation_dir not exist!"
assert os.path.exists(val_annotation_dir), "val_annotation_dir not exist!"


def calculate_data_txt(txt_path, dataset_dir):
    # create my_data.txt file that record image list
    with open(txt_path, "w") as w:
        for file_name in os.listdir(dataset_dir):
            if file_name == "classes.txt":
                continue

            img_path = os.path.join(dataset_dir.replace("labels", "images"),
                                    file_name.split(".")[0]) + ".jpg"
            line = img_path + "\n"
            assert os.path.exists(img_path), "file:{} not exist!".format(img_path)
            w.write(line)


def create_data_data(create_data_path, label_path, train_path, val_path, classes_info):
    # create my_data.data file that record classes, train, valid and names info.
    # shutil.copyfile(label_path, "./data/my_data_label.names")
    with open(create_data_path, "w") as w:
        w.write("classes={}".format(len(classes_info)) + "\n")  # 记录类别个数
        w.write("train={}".format(train_path) + "\n")           # 记录训练集对应txt文件路径
        w.write("valid={}".format(val_path) + "\n")             # 记录验证集对应txt文件路径
        w.write("names=data/my_data_label.names" + "\n")        # 记录label.names文件路径


def main():
    # 统计训练集和验证集的数据并生成相应txt文件
    train_txt_path = "mydata/my_train_data.txt"
    val_txt_path = "mydata/my_val_data.txt"
    calculate_data_txt(train_txt_path, train_annotation_dir)
    calculate_data_txt(val_txt_path, val_annotation_dir)


if __name__ == '__main__':
    main()
