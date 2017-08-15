#### How I do this 

##### middle layers output dimensions
```angular2html
conv1	(96, 3, 11, 11)		(96,)
conv2	(256, 48, 5, 5)		(256,)
conv3	(384, 256, 3, 3)	(384,)
conv4	(384, 192, 3, 3)	(384,)
conv5	(256, 192, 3, 3)	(256,)
fc6	    (4096, 9216)		(4096,)
fc7	    (4096, 4096)		(4096,)
my-fc8	(1, 4096)		    (1,)

```