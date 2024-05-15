## 代码作用
生成可训练的YOLO数据集，文件存放格式如下。

```
# ├── datasets
#     └── mydata
#         └── train
#             └── images
#             └── labels
#         └── val
#             └── images
#             └── labels
#         └── test
```


## 代码使用方法

使用labelImg软件，标注自制数据集，并且将 images文件 和 labels文件存放在 nailong_data 文件夹中。

代码中，data 路径选择 
```
parser.add_argument('--data', default='./nailong_data')  # 数据集Images路径
```
save 路径选择。这里的mydata会制动生成，无需另外创建。
```
parser.add_argument('--save', default='./mydata')  # 保存路径
```

函数 split_dataset_into_train_val_test 中的实参 train_ratio 和 val_ratio 可以调整，一般比例为 0.8 和 0.2 

```
split_dataset_into_train_val_test(
        dataset_dir=opt.data,
        save_dir=opt.save,
        train_ratio=0.8,
        val_ratio=0.2,
        im_suffix=opt.images_suffix
    )
```

