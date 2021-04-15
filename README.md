# 汉语成语逻辑关系推断系统设计与实现

## 技术流程与路线

### 1. 爬虫

[爬虫网址：造句网](https://zaojv.com/wordcy.html)

爬取数据：爬取多个成语造句的例子，筛去单个成语造句的例子。

数据格式：成语1	成语2	...	成语n	造句 **用","分隔**

数据处理：将**多成语造句**的格式改为**双成语造句**的格式

​						成语1,成语2,...,成语n,造句 -> 成语1,成语2,造句

**注意：**

* 爬虫时注意`,`的处理

* 注意**去重**

* 保存为`.csv`格式的文件，将**暂存**放于`DataCrawler\MyData`中，将文件分开写入。

  爬取的数据`.csv`文件将**长期**存放于百度网盘。（由于大文件不适合上传到GitHub中）

  ```
  链接：https://pan.baidu.com/s/1DQqQ3Eu45H55tqDJwRYgqg
  提取码：8hs9
  ```

爬取数据包含多成语造句数据`120900`条，总用时`6226s`，约`1h45min`。



### 2. 人工打标签

* 暂做**并列关系**与**转折关系**的逻辑关系推断 (可能添加**因果关系**的逻辑关系推断)

  多分类：c1	c2	造句	0/1/2

  二分类：c1	c2	造句	0/1

  ```
  并列关系 1
  转折关系 2
  ```
  
* 数据以及文件处理：
  * 由于`.csv`文件无法修改，所以将在`DataProcess.ipynb`中运行脚本将`.csv`转为`.xlsx`，方便打标签，暂存于`DataCrawler\MyXlsx`。
  * **打完标签后**再运行`DataProcess.ipynb`中的脚本将`.xlsx`转为`.csv`文件，暂存于`DataCrawler\MyCsv`。
  * 数据中的`header`为`idiom1, idiom2, sentence, label`。（其中label为打标签时手动添加）

* 百度云存放数据：

  ```
  打标签前数据：
  链接：https://pan.baidu.com/s/10leATYc9jEECdVhLQIafwA 
  提取码：ajf9
  打标签后数据：
  *****************************************************
  ```

  

### 3. 添加成语的举例(example)与解释(explanation)

使用：[中华新华字典数据库](https://github.com/pwxcoo/chinese-xinhua)添加每个成语的举例与解释到数据中。

使数据格式从**c1,c2,造句,0/1** -> **c1,c2,造句,c1解释,c2解释,c1举例,c2举例,0/1**

（因为目前没有确定使用**多分类**还是**二分类**，使用**成语的解释**还是**成语的举例**来构建模型输入，所以暂将所有信息包含在处理后的数据中）



### 4. 构建模型

* 采用**BERT微调**，添加一至两个处理与输出层并训练。

* 输入方案：

  * [CLS]<成语1的解释>[SEP]<成语2的解释>[SEP]

  * [CLS]<成语1的举例>[SEP]<成语2的举例>[SEP]  

    (这种暂不可取 因为[中华新华字典数据库](https://github.com/pwxcoo/chinese-xinhua)中有的成语没有`example`)

    ![数据问题](./img/README-1.png)

  * [CLS]<成语1的解释+举例>[SEP]<成语2的解释+举例>[SEP]

