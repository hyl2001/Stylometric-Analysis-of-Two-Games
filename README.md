仓库里保存了所有我在写《〈原神〉与〈崩坏：星穹铁道〉的文本风格考据》专栏里用到的
- 数据、
- 代码、
- 补充材料（见`.\article_Supplementary Materials`文件夹中的`Supplimentary Materials.pdf`文件），
- 以及一些用于撰写专栏所需的文件。

# 一些重要文件的介绍
由于写专栏的代码、数据比较多，管理起来比较复杂，为了防止找不到需要的代码（或数据），亦或是不知道某个脚本（`.py`）的用处，下边对本仓库所存储文件、文件夹做简单介绍。如还有不清楚的地方，请提issue。介绍按实验顺序展开。

`.xlsx`或者`.csv`文件均保存了量化结果。

## 根目录

`.\config.py`其中存储了一些在清洗、量化、自然语言处理（NLP）等环节需要用到的配置，详见该文件。


`.\bwiki_parser.py`是用于处理从bilibili wiki上获取到的剧情文本的源代码，可以将源代码转成文本文件（`.txt`），并且去除其中的一些富文本代码。

`.\nlp.py`在经过清洗的文本文件上运行NLP的代码。

`.\get_params.py`用于量化文体风格（算法参考[[1]](#1)，其中一些算法也参考了[[2]](#2)，详见补充材料，实验方法，量化一节）。

`.\get_quita_indicators.py`是中文版QUITA的源代码，可是量化文体风格代码的一部分。

`.\main.py` 和 `.\main_exp4.py`这两个代码是运行以上脚本的“主脚本”，第一个是运行实验1、实验2、实验3（已废弃）的代码，第二个是运行的代码。

## `.\data`和`.\data_for_exp4`

`.\data`用于存储用于实验1、实验2、实验3（已废弃）的数据。`.\data_for_exp4`用于存储用于实验4的数据。

## `.\data_for_readability_calc`
其中存储了用于计算文本可读性的数据，与`.\data_for_exp4`下的同名文件夹一样。由于`AlphaReadabilityChinese`[[3]](#3)只能处理`.txt`格式的文件，并且是独立这个仓库中所存储代码的程序，因而只能单独建立一个文件夹用于存放所需文件。

`AlphaReadabilityChinese`仓库位于[这里](https://github.com/leileibama/AlphaReadabilityChinese)。

## `.\expirements`
里边包含实验1、实验2、实验3（已废弃）、实验4的代码（分别存放于独立文件夹中），其中`.\expirements\eval_models.py`是用于筛选实验1和实验2所需机器学习模型的代码，而`.\expirements\run_eval.py`则用于运行该脚本代码。每个独立文件夹下（除实验1之外）的`main.py`均是用于运行文件夹所代表之实验的代码，或生成所需图表。实验1的实验代码在Jupyter Notebook中运行。

## `.\article_figs`

该文件夹用于存储制作专栏中需要用到的图片的Power Point文件，以及一些生成的图片。

## `.\article_Supplementary Materials`

其中包含用于撰写补充材料的`typst`代码、图片，以及生成的补充材料的pdf。




# 参考文献

<a id="1">[1]</a>
仲文明,姚梦妮.基于降维分类模型的译者风格研究——以Silent Spring五译本为案例[J].外语电化教学,2023,(04):24-31+116. 

<a id="2">[2]</a>
仲文明,王靖涵.少年儿童翻译文学的译本风格计量研究——以Silent Spring三译本为例[J].外语与翻译,2023,30(01):20-27+98.DOI:10.19502/j.cnki.2095-9648.2023.01.010. 

<a id="3">[3]</a>
雷蕾, 韦瑶瑜, 刘康龙. 2024. AlphaReadabilityChinese：汉语文本可读性工具开发与应用. 外语与外语教学. 46(1):83-93.