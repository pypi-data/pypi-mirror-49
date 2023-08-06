<h1 align="center">stage sep(aration) x</h1>
<p align="center">
    <em>detect stages in video automatically</em>
</p>

---
[![PyPI version](https://badge.fury.io/py/stagesepx.svg)](https://badge.fury.io/py/stagesepx)
[![Build Status](https://travis-ci.org/williamfzc/stagesepx.svg?branch=master)](https://travis-ci.org/williamfzc/stagesepx)
[![Maintainability](https://api.codeclimate.com/v1/badges/ef27756ce9a4f7f4ba94/maintainability)](https://codeclimate.com/github/williamfzc/stagesepx/maintainability)

---

## 关于 stagesepx

### 视频 与 软件工程

在软件工程领域，视频是一种较为通用的UI（现象）描述方法。它能够记录下用户到底做了哪些操作，以及界面发生了什么事情。例如，下面的例子描述了从桌面打开chrome进入amazon主页的过程：

[![openAmazonFromChrome.gif](https://i.loli.net/2019/07/17/5d2e8ed1e9d0b49825.gif)](https://i.loli.net/2019/07/17/5d2e8ed1e9d0b49825.gif)

### 让机器 "认知" 视频

人可以很轻易地理解界面上发生了什么现象、一共分为几个阶段，但是机器不行。人本身对于事件上下文的处理能力是非常强的，而对于机器而言，这无非是一组多维数据。stagesepx的第一个目标正是为了解决这个问题，让机器能够自动区分视频的阶段。目前它已经支持**自动侦测**并提取视频中的稳定或不稳定的阶段（例子中，stagesepx认为视频中包含三个稳定的阶段，分别是点击前、点击时与页面加载完成后）：

[![stage-min.png](https://i.loli.net/2019/07/17/5d2e97c5e3a0e96365.png)](https://i.loli.net/2019/07/17/5d2e97c5e3a0e96365.png)

---

在切割之后，你可以很轻松地对阶段进行图片采样（例子中为每个阶段采集3张图片，一共有3个稳定阶段，分别名为0、1、2）后保存起来，以备他用（例如AI训练、功能检测等等）：

[![sample_after_cut.png](https://i.loli.net/2019/07/17/5d2ea54271fe256939.png)](https://i.loli.net/2019/07/17/5d2ea54271fe256939.png)

### 切割器 与 分类器

可以看到，通过stagesepx我们能够用很简单且高效的方式自动地划分视频中稳定与不稳定的部分。得益于此，我们可以在该项技术上做一些进阶操作，例如，计算每个阶段对应的耗时。stagesepx自带的分类器能够直接利用切割器得到的结果，对整个视频进行逐帧分析，并计算出更加详细的结果！

[![stage_trend.png](https://i.loli.net/2019/07/17/5d2ea6720c58d44996.png)](https://i.loli.net/2019/07/17/5d2ea6720c58d44996.png)

在切割器部分，我们将视频分为0、1、2三个阶段。在分类器计算之后，我们可以很直观地得到每个阶段的耗时。例如，从图中可以看出，视频开始直到 0.76s 时维持在阶段0，在 0.76s 时从阶段0切换到阶段1，以此类推，我们能够对视频的每个阶段进行非常细致的评估。通过观察视频也可以发现，识别效果与实际完全一致。

> 当stagesepx无法将帧分为某特定类别、或帧不在待分析范围（可配置）内时，会被标记为 -1，一般会在页面发生变化的过程中出现

### 不同形态的分类器

stagesepx提供了两种不同类型的分类器，用于处理切割后的结果：

- 传统的 SSIM 分类器无需训练且较为轻量化，多用于阶段较少、较为简单的视频；
- SVM + HoG分类器在阶段复杂的视频上表现较好，你可以用不同的视频对它进行训练逐步提高它的识别效果，使其足够被用于生产环境；

目前基于CNN的分类器已经初步完成，在稳定后会加入 ：）但目前来看，前两个分类器在较短视频上的应用已经足够了（可能需要调优，但原理上是够用的）。

事实上，stagesepx在设计上更加鼓励开发者**根据自己的实际需要**设计并使用自己的分类器，以达到最好的效果。

### 需要更多数据？

想得到耗时？stagesepx已经帮你计算好了：

[![stage_time_cost.png](https://i.loli.net/2019/07/17/5d2ea67201ac283867.png)](https://i.loli.net/2019/07/17/5d2ea67201ac283867.png)

或者，每个阶段的占比？

[![pie.png](https://i.loli.net/2019/07/18/5d308bab8dd1b49028.png)](https://i.loli.net/2019/07/18/5d308bab8dd1b49028.png)

所有的一切，你只需要提供一个视频。

### 不可忽视的性能

在效率方面，吸取了 [stagesep2](https://github.com/williamfzc/stagesep2) 的教训（他真的很慢，而这一点让他很难被用于生产环境），在项目规划期我们就将性能的优先级提高。对于该视频而言，可以从日志中看到，它的耗时在惊人的300毫秒左右（windows7 i7-6700 3.4GHz 16G）：

```bash
2019-07-17 10:52:03.429 | INFO     | stagesepx.cutter:cut:200 - start cutting: test.mp4
...
2019-07-17 10:52:03.792 | INFO     | stagesepx.cutter:cut:203 - cut finished: test.mp4
```

### 定位

- 视频阶段划分与采样，作为数据采集者为其他工具（例如AI模型）提供自动化的数据支持。它应该提供友好的接口或其他形式为外部（包括分类器）提供支持。例如，`pick_and_save`方法完全是为了能够使数据直接被 [keras](https://github.com/keras-team/keras) 利用而设计的。
- 视频帧级别的分类，实现图片分类器，并能够利用采样结果。例如，你可以在前几次视频中用采样得到的数据训练你的AI模型，当它收敛之后在你未来的分析中你就可以直接利用训练好的模型进行分类，而不需要前置的采样过程了。

## 应用举例

所有stagesepx需要的只是一个视频，而且它本质上只跟视频有关联，并没有任何特定的使用场景！所以，你可以尽情发挥你的想象力，用它帮助你实现更多的功能。

### APP

- 前面提到的应用启动速度计算
- 那么同理，页面切换速度等方面都可以应用
- 除了性能，你可以使用切割器对视频切割后，用诸如[findit](https://github.com/williamfzc/findit)等图像识别方案对功能性进行校验
- 除了应用，游戏这种无法用传统测试方法的场景更是它的主场
- ...

### 除了APP？

- 除了移动端，当然PC、网页也可以同理计算出结果
- 甚至任何视频？

[![pen.gif](https://i.loli.net/2019/07/22/5d35a84e3e0df82450.gif)](https://i.loli.net/2019/07/22/5d35a84e3e0df82450.gif)

你可以直接得到出笔进入与移除的耗时！

[![pen_chart.png](https://i.loli.net/2019/07/22/5d35a8858640e67521.png)](https://i.loli.net/2019/07/22/5d35a8858640e67521.png)

Do whatever you want:)

## 使用

### 安装

Python >= 3.6

```python
pip install stagesepx 
```

### 例子

sample code中提供了详细的注释。

- 切割器
    - [常规分类器](./example/cut.py)
- 分类器
    - [常规分类器](./example/classify.py)
    - [SVM分类器](./example/classify_with_svm.py)
- 完整例子
    - [单视频](./example/cut_and_classify.py)
    - [多视频](./example/multi_video.py)

例子中使用的视频可以[点此](https://raw.githubusercontent.com/williamfzc/stagesep2-sample/master/videos/demo.mp4)下载。

## 实现原理

### 核心

核心算法围绕着 SSIM 展开。[SSIM介绍](https://zh.wikipedia.org/wiki/%E7%B5%90%E6%A7%8B%E7%9B%B8%E4%BC%BC%E6%80%A7)

应明确，两张图片的SSIM可以一定程度上描述他们的相似度（变化程度），即他们是否发生了变化。那么以此类推，如果在一段连续图片上应用该方法，我们即可衡量该阶段内的变化情况。

而，视频即是由连续图片组成的。如果计算一段视频相邻帧的SSIM变化趋势，我们可以发现一些规律：

![ssim_trend](docs/pics/ssim_trend.png)

可以看到，实际上每当图像发生变化时，ssim数值会有明显的下跌；而当画面趋于平稳，ssim会回到接近1的位置。那么我们可以得到结论：

- 波谷区间对应视频的变化区间
- 平缓区间对应视频的稳定区间
- 波谷深度对应变化的剧烈程度

### 架构与流程

为了满足不同的使用需求，stagesepx主要由两个概念组成：

- 切割器
- 分类器

#### 切割器

顾名思义，切割器的功能是将一个视频按照一定的规律切割成多个部分。

例如，根据上述的思想，我们能够切割并提取视频中的稳定区间。得到稳定区间之后，我们可以很轻易地知道视频中有几个稳定阶段、提取稳定阶段对应的帧等等。

切割器的定位是预处理，降低其他模块的运作成本及重复度。

#### 分类器

针对上面的例子，分类器应运而生。它主要是加载（在AI分类器上可能是学习）一些分类好的图片，并据此对帧（图片）进行分类。

例如，当加载上述例子中稳定阶段对应的帧后，分类器即可将视频进行帧级别的分类，得到每个阶段的准确耗时。

![stage](docs/pics/stage.png)

分类器的定位是高准确度的图片分类，它应该有不同的存在形态（例如机器学习模型）、以达到不同的分类效果。stagesep2本质上是一个分类器。

### 性能与效率

stagesep2 遇到的致命问题就是，它太慢了，即便效率对于该类项目来说并不是优先级很高。这导致了它在生产环境中必须在准确性与效率中做取舍。

除了常规的基于图像本身的优化手段，stagesepx主要利用采样机制进行性能优化，它指把时间域或空间域的连续量转化成离散量的过程。由于分类器的精确度要求较高，该机制更多被用于切割器部分，用于加速切割过程。它在计算量方面优化幅度是非常可观的，以5帧的步长为例，它相比优化前节省了80%的计算量。

当然，采样相比连续计算会存在一定的误差，如果你的视频变化较为激烈或者你希望有较高的准确度，你也可以关闭采样功能。

### 稳定性

stagesep2存在的另一个问题是，对视频本身的要求较高，抗干扰能力不强。这主要是它本身使用的模块（template matching、OCR等）导致的，旋转、分辨率、光照都会对识别效果造成影响；由于它强依赖预先准备好的模板图片，如果模板图片的录制环境与视频有所差异，很容易导致误判的发生。

而SSIM本身的抗干扰能力相对较强。如果使用默认的SSIM分类器，所有的数据（训练集与测试集）都来源于同一个视频，保证了环境的一致性，规避了不同环境（例如旋转、光照、分辨率等）带来的影响，大幅度降低了误判的发生。

## License

[MIT](LICENSE)
