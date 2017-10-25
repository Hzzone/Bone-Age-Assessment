import os
import random
import shutil
if __name__ == "__main__":
    f = []
    for root, dirs, files in os.walk("/home/bw/DeepLearning/female_regression/train"):
        for file in files:
            f.append(os.path.join(root, file))
    random.shuffle(f)
    random.shuffle(f)
    for index, file in enumerate(f):
        if index % 10 == 0:
            shutil.move(file, "/home/bw/DeepLearning/female_regression/test")
            print(file)
