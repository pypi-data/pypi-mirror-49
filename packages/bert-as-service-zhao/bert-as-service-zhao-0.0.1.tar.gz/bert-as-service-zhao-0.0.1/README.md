
Design by zhaoguanzhi.
Email: zhaoguanzhi1992@163.com.

## 第一步 
###可以更改helper.py中的root_path的默认值，但不推荐
~~~
group1.add_argument('-root_path', 
                    type=str, 
                    default=r'C:\Users\RipperAaron\Desktop\seq2seq',
                    help='path of root path')
~~~
###推荐传入root_path的值
命令行terminal运行的方式
~~~
python3 step*.py -root_path C:\Users\RipperAaron\Desktop\seq2seq
~~~
或者加入到Paramaters
~~~
-root_path C:\Users\RipperAaron\Desktop\seq2seq
~~~

## 第二步
### 运行step10
~~~
python step10finalNerIrSeq2seq.py -root_path C:\Users\RipperAaron\Desktop\seq2seq
~~~