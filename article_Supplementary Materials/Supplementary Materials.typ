#import "@preview/tablex:0.0.8": tablex, rowspanx, colspanx
#import "@preview/tabut:1.0.2": tabut

#let songti = ("Times New Roman", "Songti SC", "Songti TC", "SimSun")
#let indent() = {
  box(width: 2em)
}

#show figure.where(
  kind: "表S"
): set figure.caption(position: top)
// #show figure.where(
//   kind: "表"
// ): set figure.caption(position: top)
#show figure.where(
  kind: "图S"
): set figure.caption(position: bottom)
#set table.hline(stroke: .6pt)
#set text(font: songti)
#set figure.caption(separator: [])
#set heading(numbering: "1.")


#align(center)[
  #text(size: 16pt)[《〈原神〉与〈崩坏：星穹铁道〉的文本风格考据》的补充材料]
]

#for _ in range(1, 10) { linebreak() }
本文件包含：
- 研究语料、研究方法
- 实验设计
- 图 S1 至 S
- 表 S1 至 S

#pagebreak()

// This omits numbering fisrt page, i.e. cover page.
#set page(
  numbering: "1",
)
#counter(page).update(1)

= 研究语料、研究方法
== 研究语料
#indent()由于《原神》和《崩坏：星穹铁道》官方并未公开游戏内使用的主线剧情文本#footnote([主线剧情指《原神》的“魔神任务”、《崩坏：星穹铁道》的“开拓任务”])，因此我只能从网上收集#footnote([《原神》主线剧情文本的访问日期均为：2024年4月4日；《崩坏：星穹铁道》主线剧情文本的访问分多次完成，具体时间见@tbls1。])由网友抄录的文本@wiki_ys@wiki_sr。bilibili wiki（bwiki）使用了自定义的标记语言，需要通过解析网页源代码才可以获得干净的生语料，通过Python和正则表达式可以方便地达成这一目的。由于原文本的收集方式为：按照bwiki上的分组方式，将源代码分别存储在一个文件中。此外，在研究中，对于那些没有名字的对话，均视为由两个游戏主角所说。

#linebreak()
== 研究方法
=== 语料处理
#indent()在bwiki中，《原神》的主线剧情文本是按照章节分组的，而《崩坏：星穹铁道》则是按照每章的小节来分组的。这样的分组模式不利于描写两个游戏每一章的统计文体学特征，因此，在获得生语料之后，还需要切分生语料。具体规则为：计算每个文件除标点外的字符数，按每1000字为单位，对每个文件实施切分，并分别存储。之后利用自然语言处理（natural language processing, NLP）技术对生语料分词（tokenization）、标注词性（part-of-speech tagging），并做依存句法分析（dependency parsing）以便量化文本的统计学特征，在本研究中，我使用了HanLP@he-choi-2021-stem。

=== 量化
#indent()经过NLP，需要对文本的各项特征进行量化以便开展后续实验。在量化之前，由于切分好的生语料文件可能存在长度不足的情况，我依照生语料长度，剔除了这一部分文件。我结合了不同特征以尽可能实现全面的描写。通过自行编写的Python分析脚本和借助外部工具，总共获得了60个不同的参数，具体可以分为三部分，分别由基于文章@WYDH202304004 自行编写的Python分析脚本，来自模仿原版QUITA@kubat_quita_2014 编写的用于分析中文文本的QUITA Python脚本（除特别标注外，下文中的QUITA均指该脚本），外部工具AlphaReadabilityChinese@WYWJ202401008 生成。需要注意，文章@WYDH202304004 中的“成语使用数”、“成语种类数/成语使用数”、“四字词语使用数”，由于前两个参数较难实现，我选择舍弃这两个参数，并加入对明喻修辞的计数。同时，由于文章@WYDH202304004 没有描述“词汇活动度”的具体算法，故该参数由QUITA计算。参考文章@CSTY202301004 加入了“句子节奏度”，参考所述“平均小句长”的算法。参考文章@CJXS200803021，加入了平均依存距离（Mean Dependency Distance, MDD），在实际应用过程中，由于每个文件都是由若干个句子组成，MDD是对每个单独的句子作计算，因而为了表示整个文件，我对每个文件中计算得到的MDD再次求平均，并求出相应的标准差，两个参数均记录在生成的参数文件中。此外，原版QUITA中提供了类符/形符比（Type-Token Ratio, TTR），但由于TTR易受文本长度影响@cvrvcek2015simplification，所以在这个研究中，我使用了标准化类符/形符比（Standardized Type-Token Ratio, STTR），该参数按照将200词（我使用的是按照词为切分单位，而不是字）归入一组，分别计算TTR（如果最后一组词数量不足200，但不少于200词的90%（180词），则视为200词，并参与计算），经过计算，获得到一组TTR，最后求该组TTR值的平均值，即为STTR。

#indent()量化完成之后还需要标注样本，即说明样本属于哪个游戏，来自哪个游戏的哪个章节。标注规则如下：（1）对于文本来自哪个游戏的标注主要采用二分法，即对于来自《崩坏：星穹铁道》的文本都标注为0，来自《原神》的文本均标注为1。（2）对于章节的标注则采用游戏内的章节号，需要注意的是，序章均标注为0，《原神》的间章则从90开始编号。

=== 特征识别
#indent()为了更好地发现文本的计量特征，这个研究中我使用了机器学习来学习特征、识别特征。这里有一个非常重要的假设——如果模型由良好的表现，那么可以认为不同文本之间的特征是明显的。本研究中使用了9种不同模型，分别是最近邻模型、线性支持向量机（Support Vector Machine, SVM）、径向基SVM、决策树、随机森林、神经网络、AdaBoost、朴素贝叶斯分类器、极端梯度提升（eXtreme Gredient Boost，XGB），在其他实验中还使用了线性判别分析、层次聚类。在实验时，我发现不同游戏、不同章节间，文本的数量存在很大差异，这就造成了数据集的不平衡。不平衡数据集会影响模型表现，导致模型可能会错误分类样本较少的数据@chawla2002smote。鉴于此问题在这个研究中也出现了，我使用了SMOTE算法@chawla2002smote 来平衡不同样本间的数据，以提升模型的表现。

=== 性能度量
#indent()我采用多种指标（@tbl1），全面衡量模型表现。在训练和测试模型时，对于每个模型，我都是从平衡过的数据中随机抽取70%的样本作为训练集，余下30%做测试集，如此重复100次，得到每个模型的各项指标（@tbl1）。

#align(center)[
  #figure(
    caption: [|本研究中用于衡量模型学习效果的指标、算法。算法中文名、具体算法均来自《机器学习》@zhou2016#super("29-35")。AUC和Acc公式中每一项符号的具体含义见下文所述。],
    kind: "表S",
    supplement: "表S",
  )[
    #table(
      stroke: none,
      columns: (auto, auto, auto),
      inset: 10pt,
      align: horizon,
      table.hline(),
      table.header(
        [名称], [缩写], [算法],
      ),
      table.hline(),
      [曲线下面积（Area Under Curve）], [AUC], [$ 1/2 sum_(i=1)^(n-1)(x_(i+1) - x_(i)) times (y_(i) + y_(i+1)) $],
      [准确度（Accuracy）], [Acc], [$ 1/m sum_(i=1)^m II(f(bold(x_i)) != y_i) $],
      [查准率（Precision）], [Pre], [$ "真正例数"/("真正例数" + "假正例数") $],
      [查全率（Recall）], [Rec], [$ "真正例数"/("真正例数" + "假反例数") $],
      [F1-度量（F1-Score）], [F1S], [$ (2 times "查准率" times "查全率")/("查准率" + "查全率") $],
      table.hline()
    )
  ]<tbl1>
]

#indent()接下来我会逐个介绍每一个指标的具体含义，但是考虑到连贯性，我将打乱表格的顺序。首先会介绍混淆矩阵，然后分别是查准率、查全率，接着是AUC的基础ROC（Received Operating Characteristic，受试者工作特征）曲线，之后会介绍AUC的含义，其后是介绍F1-度量，最后介绍准确度（因为准确度用了不同的算法，所以与上边几项无关，因而放在最开始和最后讲都可以）。本研究所用性能度量（@tbl1）的介绍，除特殊标注外，均来自《机器学习》@zhou2016#super("29-35")。

==== 混淆矩阵
#indent()混淆矩阵（Confusion Matrix，@tbl2）是理解@tbl1 中除准确度之外其它各项指标的基础，在此做简要介绍。机器分类结果可以分为四类，分别是真正例、假正例、假反例、真反例。举例说明以上四种情形，这里采用文章@nahm2022 中的例子来说明。假设现在需要机器学会根据肿瘤标志（Tumor Marker，TM）的数值分辨那些肿瘤是恶性的，那些是良性的。那么，真正例就是指根据TM机器正确地将恶性肿瘤的样本正确分类到了恶性肿瘤这个集合中；真反例是指机器将良性肿瘤的样本正确分类到了良性肿瘤这个集合中。假正例是指，机器将良性肿瘤误判为恶性肿瘤；假反例是指机器将恶性肿瘤分类为了良性肿瘤。显然，只有主对角线（从左上到右下）上的预测结果（真正例、真反例）是正确的预测结果。副对角线上的假反例和假正例都属于误判。

#align(center)[
  #figure(
    caption: [|分类结果混淆矩阵],
    kind: "表S",
    supplement: "表S"
  )[
    #tablex(
      columns: 3,
      align: center + horizon,
      auto-vlines: false,
      header-rows: 2,
      
      /* --- header --- */
      rowspanx(2)[实际情况], colspanx(2)[预测结果],    (),
      (),                      [正例], [反例],        (),
      /* -------------- */
      
      [正例], [真正例], [假反例],
      [反例], [假正例], [真反例],
    )
  ]<tbl2>
]

==== 查准率、查全率
#indent()根据查准率公式（@tbl1），它代表了在分类为正例的样本中，真正是正例的样本占所有机器分类为正例的结果的比例。这个数值越高，代表着机器的正确分类能力越好。查全率代表了在所有正例样本中，有多少样本被机器正确分类为正例。

#indent()查全率与查准率是一对相互对立的度量。原因在于，不同的任务对查准率和查全率的要求不同，如果我们更多要求机器能准确分类，那么要求机器只挑选那些最有把握的样本作为正例，但是可能也会有很多样本没能正确分类，这就导致了查全率的下降。相反，如果我们需要尽可能多的筛选出来正例，那么一些反例就有可能被误选进来，这样就使查准率下降了。在一些简单任务中，二者都有可能会很高。

#indent()对于本研究来说，查准率代表了机器从不同文本中识别出某一类文本（比如某一章节或某一游戏的文本）的能力，查全率则表示对同一类型的文本，机器能从中分辨出多少文本是来自这一类型。

==== 曲线下面积
#indent()在计算AUC之前，需要先获得ROC（Received Operating Characteristic，受试者工作特征）曲线，AUC中的“面积”就是指ROC曲线下面积。机器在分类正例和反例的时候是依据某个截断点（cut point），如果输出值大于截断点则判为正例，否则为反例。那么，如果让截断点的值从小到大变化，在每次变化中都会产生一个混淆矩阵，根据此表，结合以下两个公式：
$ "真正例率" &= "真正例数" / ("真正例数" + "假正例数") \ &= "查准率"， $
$ "假正例率" = "假正例数" / ("假正例数" + "真反例数")， $
便可绘制出一条ROC曲线@nahm2022。注意，“假正例率”沿用了《机器学习》@zhou2016#super([34])的说法。在文献@nahm2022 中，“真正例率”一般称为Sensitivity（敏感度），“假正例率”则是用1减去Specificity（特异度）的差值。

#indent()在实际情况中，ROC曲线的绘制都是由有限个样本完成的，因而曲线不是连续的。假设某ROC曲线由一系列坐标分别为${(x_1, y_1), (x_2, y_2), ..., (x_n, y_n)}$的点构成，那么利用积分知识便可得到@tbl1 中的AUC。

==== F1-度量
#indent()F1-度量是查准率和查全率的调和平均，即$ 1/"F1" = 1/2 times (1/"查准率" + 1/"查全率")， $它基本的形式为：$ F = ((beta^2 + 1.0) times "查准率" times "查全率") / (beta ^ 2 times "查准率" + "查全率")。 $ 如果$beta=1$（F1-度量）则说明查准率和查全率同等重要@Chinchor1992。

==== 准确率
#indent()机器在判别一个样本是正例还是反例的时候，存在误判的可能性，也就是说，把原本的正例误判成反例，或者反过来。准确率就是衡量在所有样本中，有多少样本被正确分类了。@tbl1 中的指示函数$#sym.II (#sym.circle.filled.tiny)$是指，对于给定样本$bold(x_1)$，机器学习算法$f(#sym.circle.filled.tiny)$的输出值如果与样本原本标签$y_1$一致，即$f(bold(x_1)) = y_1$，则指示函数输出值为1，否则为0。遍历所有样本（假设有$m$个样本），对指示函数求和，再除以样本数，便是准确率。准确率度量一个算法正确分类的能力。查准率和查全率与准确率的侧重有所不同，前两个更加强调机器识别正例的能力，而后者（准确率）则全面考虑了机器识别正确正例和反例的能力@powers2020。

=== 模型输出解释
#indent()机器学习已经在自然科学领域得到了广泛应用，但是由于其结构往往非常复杂，也正是由于这种复杂性让机器的学习能力不断提升、准确率不断上升@goodfellow2016#super([21])。同时，理解机器得出某个结果（prediction）是使机器学习能用于研究领域的前提@roscher2020。因此，为了能解释机器的结论，我用到了夏普利加性解释（#underline([SH])apley #underline([A])dditive ex#underline([P])lanations，SHAP）@lundberg2017。

#indent()SHAP的主要思想就是将机器学习模型视为一个“黑盒”（black box），观察特征对模型输出值的影响，具体公式如下：
$ phi.alt_i(f, x) = sum_(R in Re) 1/M! [f_(x)(P_i^R union i) - f_(x)(P_i^R) ]， $
其中，$Re$是样本全部特征的集合，$P_i^R$在特征$i$之前的所有特征，$M$是样本特征数量@lundberg2020，$f_x$则是模型。其中的$phi.alt_i$就是一个SHAP值@lundberg2017。从这个公式中可以看出，为了计算SHAP值需要两个模型，第一个模型的输入是特征$i$以及之前的所有特征，第二个模型的输入只有特征$i$之前的所有特征，这样就可以计算出特征$i$对模型输出的贡献。

#indent()根据模型筛选的结果，由于XGB表现出众，我主要是使用了属于SHAP之一的TreeSHAP@lundberg2020。同时，相较其他算法，SHAP的优势@lundberg2020 有：（1）独立于树深度的变化，公正地给样本的每个特征（feature）分配重要性；（2）结果不会发生改变；（3）SHAP的结果更加符合人类直觉。

// #linebreak()
// == 分布相似度
// #indent()如前文所述，我用了60个参数尽可能全面的描写文本特征（研究方法，量化），这就导致了一个问题——传统的分布相似度算法【即，柯尔莫哥洛夫-斯米尔诺夫检验（Kolmogorov-Smirnov test, KS检验）】不再适用，因为它是为了一维数据（只有一个变量的数据）而设计的。如果逐个检验每个变脸，可能会忽略样本间的一些信息@oja2004，因此需要找到一个适合高维数据的KS检验，这里我采用了$d$维柯尔莫哥洛夫-斯米尔诺夫检验【$d$-dimensional extension of the Kolmogorov-Smirnov test (ddKS检验)#footnote([ddKS代码见：https://github.com/pnnl/DDKS])】@hagen2021。需要注意的是，如果规定两个分布完全相同为1，完全不同为0，那么在得到ddKS检验统计量后需要用1减去该值，即$1-"ddKS"$。ddKS检验算法对样本维数（变量数量）极其敏感（@figs1），因此为了保证计算效率，我用了主成分分析（Principal Components Analogy，PCA）来给数据降维，经过PCA样本从60维降到了10维，这样不但能尽可能降低计算消耗的时间，同时还能确保原始数据分布得到了良好保存（@figs2）。

// #pagebreak()
// #align(center)[
//   #figure(
//     image("..\article_Supplementary Materials\figs\ddks_computational_complexity.png", width: 70%),
//     caption: [|不同样本维度下ddKS算法计算所消耗的时间。蓝色实线为算法运行所消耗的平均时间（单位：秒），蓝色阴影是95%置信区间。在测试ddKS计算时间消耗的实验中，样本数量保持固定（$N$=5），随着样本维数（每一个样本包含的变量数量）逐渐增大，算法运行消耗的时间呈指数型增长。通过实验可以发现，ddKS算法在9个变量及以下时，计算所消耗的平均时间没有明显区别，当样本维度超过9维之后，每次计算的时间快速上升。],
//     kind: "图S",
//     supplement: "图S"
//   )<figs1>
// ]

#pagebreak()
#align(center)[
  #figure(
    image("..\article_Supplementary Materials\figs\exp1\eval_res.png"),
    caption: [|实验一中用到的机器学习模型及其表现。方框的上部为上四分位（75%），下部为下四分位（25%）；方框中间的橙色实线是中位数，圆圈为异常值。],
    kind: "图S",
    supplement: "图S"
  )
]

#pagebreak()
#align(center)[
  #figure(
    image("..\article_Supplementary Materials\figs\exp3\GI_filtered.svg"),
    caption: [|《原神》中不同角色的对话文本的特征聚类。其中去除了对话文本数量较多的旅行者、派蒙。],
    kind: "图S",
    supplement: "图S"
  )
]

#pagebreak()
#align(center)[
  #figure(
    image("..\article_Supplementary Materials\figs\exp3\SR_filtered.svg"),
    caption: [|《原神》中不同角色的对话文本的特征聚类。其中去除了对话文本数量较多的三月七、开拓者。],
    kind: "图S",
    supplement: "图S"
  )
]

// #pagebreak()
// #align(center)[
//   #figure(
//     image("..\article_Supplementary Materials\figs\PCA_exp_var_ratio.png", width: 80%),
//     caption: [|前10个主成分的累计方差解释率。绿色三角代表均值，橙色横线为中位数，方框上边缘为上四分位（75%），下边缘为下四分位（25%）。方差解释率是指每个主成分所占的方差在总方差中的比例。方差解释率越高，信息保留得越多。*A*在分析两个游戏间文本计量特征分布相似度时，前10个主成分的累计方差解释率。*B*、*C*在分别计算两个游戏内不同章节之间文本计量特征分布相似度时，前10个主成分的累计方差解释率。],
//     kind: "图S",
//     supplement: "图S"
//   )<figs2>
// ]

// #pagebreak()
// #align(center)[
//   #figure(z
//     image("..\article_Supplementary Materials\figs\exp1\ddKS_inter.png"),
//     caption: [|游戏间不同章节文本文体ddKS检验结果。],
//     kind: "图S",
//     supplement: "图S"
//   )
// ]

// #pagebreak()
// #align(center)[
//   #figure(
//     image("..\article_Supplementary Materials\figs\exp2\ddKS_sim_intra.png"),
//     caption: [|两个游戏内不同章节文本文体ddKS检验结果。*A* 《原神》的章节间ddKS检验相似度热图。*B* 《崩坏：星穹铁道》的章节间ddKS检验相似度热图],
//     kind: "图S",
//     supplement: "图S"
//   )
// ]

#pagebreak()
#align(center)[
  #figure(
    caption: [|《崩坏：星穹铁道》主线剧情各个小节访问时间。在文本收集过程中，由于我是直接复制网页的源代码，
    所以文件的创建时间可以认为是网页访问时间。],
    kind: "表S",
    supplement: "表S",
  )[
    #table(
      stroke: none,
      columns: (auto, auto),
      inset: 10pt,
      align: horizon,
      table.hline(),
      table.header(
          [文件名], [创建时间],
      ),
        [2024-04-04], [1.2.10\_时不我待，我的朋友、
          1.2.11\_静静的星河、
          1.2.1\_在屋外的黑暗中洗涤、
          1.2.2\_不可制造偶像、
          1.2.3\_青年近卫军、
          1.2.4\_兵士们默默无言、
          1.2.5\_星星是冰冷的玩具、
          1.2.7\_这里的黎明……、
          1.2.8\_回归、
          1.2.9\_从凶险和泥泞的沼泽中、
          2.1.10\_诸天无安，迷途难返、
          2.1.11\_茸客鸣呦，玉角盘虬、
          2.1.1\_旅进青霄，不速之邀、
          2.1.2\_行遏流云，身入魔阴、
          2.1.3\_紫府通谒，将军定策、
          2.1.4\_旧影婆娑，追思错落、
          2.1.5\_犬迹追从，谛听狐踪、
          2.1.6\_迴星周旋，未卜知先、
          2.1.7\_长乐新朋，青鸟候风、
          2.1.8\_极数问玄，历事穷观、
          2.1.9\_神木重萌，掣转天衡、
          2.2.1\_金鼎灵树，穷途梼杌、
          2.2.2\_螣蛇无穴，旧梦亡阙、
          2.2.3\_得其雨露，安其壤土、
          2.2.4\_有龙矫矫，其渊渺渺、
          2.2.5\_仙骸成空，大劫有终、
          2.3.1\_安灵布奠，天清路远、
          3.1.10\_倘若在午夜醒来、
          3.1.11\_是谁杀死了…、
          3.1.1\_长日入夜行、
          3.1.2\_丑时三刻的敲门声、
          3.1.3\_那些逐梦的年轻人、
          3.1.4\_无眠之夜、
          3.1.5\_黄金年代的故事、
          3.1.6\_好兆头，我的朋友、
          3.1.7\_北风的安眠曲、
          3.1.8\_夜色名为温柔、
          3.1.9\_犹在镜中],
        [2024-04-05], [0.1.1\_混乱行至深处、
          0.1.2\_漩涡止于中心、
          0.1.3\_宇宙安宁片刻、
          0.1.4\_模拟宇宙-始发测试、
          0.1.4\_阴影从未离去、
          0.1.5\_旅途正在继续、
          0.1.6\_星间流浪、
          1.1.10\_已故去的必如雪崩再来、
          1.1.11\_躺在铁锈中、
          1.1.12\_腐烂或燃烧、
          1.1.13\_我们不擅长告别、
          1.1.1\_激「冻」人心的大冒险、
          1.1.2\_如果在冬夜，一群旅人、
          1.1.3\_永冬城之夜、
          1.1.4\_躲得过初一，躲不过十五、
          1.1.5\_捉迷藏、
          1.1.6\_第八条、也是最后一条规则、
          1.1.7\_她等待刀尖已经太久、
          1.1.8\_他们有多少人已掉进深渊、
          1.1.9\_相会在日落时分、
          3.2.1\_天鹅绒里的恶魔、
          3.2.2\_迷惘的一代人、
          3.2.3\_双重赔偿、
          3.2.4\_酒店关门之后、
          3.2.5\_外邦为何争闹？、
          3.2.6\_人间天堂、
          3.2.7\_泄密的心],
        [2024-04-06], [3.2.8\_所有悲伤的故事、
          3.2.9\_行过死荫之地],
        table.hline(),
    )
  ]<tbls1>
]

#pagebreak()
#align(center)[
  #figure(
    image("../article_Supplementary Materials\figs\exp2\GI_other_models_and_LDA_eval.png"),
    caption: [|各模型依据文本计量特征识别《原神》不同章节的性能度量。],
    kind: "表S",
    supplement: "表S",
  )
]

#pagebreak()
#align(center)[
  #figure(
    image("../article_Supplementary Materials\figs\exp2\SR_other_models_and_LDA_eval.png"),
    caption: [|各模型依据文本计量特征识别《崩坏：星穹铁道》不同章节的性能度量。],
    kind: "表S",
    supplement: "表S",
  )
]

#pagebreak()
#for _ in range(1, 4) { linebreak() }
#bibliography("ref.bib", style: "gb-7714-2015-numeric", title: "参考文献")