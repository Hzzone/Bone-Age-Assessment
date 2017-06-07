#### fine tuning AlexNet with lmdb file
舍弃了13,27岁的几个样本
AlexNet dropout_ratio = 0.05
###### lmdb training set 1022, validation set 179


* base_lr = 0.001, batch_size = 100, policy = stepdown, 未修改dropout_ratio, 迭代1000代，在两百多代时停止。出现过拟合。

  ![](http://omoitwcai.bkt.clouddn.com/2017-06-07-150944.jpg)

  ​

  ​

* 与1相等，修改fc7和fc6层的dropout_ration为0.7，同样出现过拟合

![](http://omoitwcai.bkt.clouddn.com/2017-06-07-%E5%B1%8F%E5%B9%95%E5%BF%AB%E7%85%A7%202017-06-07%20%E4%B8%8B%E5%8D%8811.29.27.png)





* 与1相等，修改fc7和fc6层的dropout_ration为0.8，同样出现过拟合

![](http://omoitwcai.bkt.clouddn.com/2017-06-07-155444.jpg)