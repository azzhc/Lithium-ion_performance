# 文件说明
此部分为电池数据,文件命名为电池充电策略，每种策略下有两块电池，每块电池数据分为txt和xlsx格式，是一样的。
预测目标是使用v的数据分别预测IC和SOH的数据，数据是行与行对应的。
一般使用一块电池的数据训练模型，另一块电池的数据作为预测集评估模型。
## 充电策略介绍
以6C-60per_3C为例，电池以6C速率（额定容量1.1Ah,充电速率6.6A）充电至60%SOC；后转为3C速率充电至80%SOC;最终再使用1C的CCCV策略充满至100%SOC。
## 目录结构如下

<pre>
data
├───6C-60per_3C
│   ├───CH29
│   └───CH30
└───7C-40per_3C
    ├───CH37
    └───CH38
</pre>