# 这是软件的界面实现部分

**目录结构如下**
<pre>
Component
│   readme.md
│
├───ic					# 这是ic功能的实现
│   │   ic_getii.py			
│   │   ic_getin.py			# 数据读取模块
│   │   ic_logic.py			# 页面逻辑
│   │   ic_model.py		     # ai训练模块
│   │   licon_ic.py			# 页面初始化模块
│   │   __init__.py
│
├───old			       		 # 这是老化分析功能的实现
│   │   oldana.py			 # 页面初始化模块
│   │   oldana_import.py	 # 数据分析模块
│   │   oldana_logic.py		 # 页面逻辑模块
│   │
│
└───soh				         # 这是soh功能的实现
│   │   soh_getin.py		 # 数据获取模块
│   │   soh_logic.py		 # 界面逻辑
│   │   soh_model.py  	     # ai训练
│   │   licon_soh.py		 # 界面初始化
└───llm				         # 这是llm功能的实现
    │   all-MiniLM-L6-v2		 # RAG模型
    │   LLM.py		         # 数据获取模块
    │   llm_logic.py		 # 界面逻辑
    │   llm_ui.py  	         # 界面初始化
    │   documents.txt	     # 语料库
<pre>