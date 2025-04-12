# 平台界面模块设计

**目录结构如下**
<pre>
component
│
├───ic					# IC模块
│   │───__init__.py			
│   │───background.jpg      # 界面总体背景			
│   │───ic_getii.py			# 打印IC相关状态
│   │───ic_getin.py			# IC数据读取
│   │───ic_logic.py			# IC界面逻辑
│   │───ic_model.py		    # IC模型设置
│   └───licon_ic.py			# IC界面初始化
│                       
├───llm				    # AI助手模块
│   │───LLM.py		        # LLM数据获取
│   │───documents.txt	     # LLM语料库
│   │───llm_logic.py		 # LLM界面逻辑
│   └───llm_ui.py  	         # LLM界面初始化
│                       
├───old			        # 老化机制量化模块
│   │───oldana.py			 # 老化页面初始化
│   │───oldana_import.py	 # 老化数据分析
│   └───oldana_logic.py		 # 老化界面逻辑
│                               
└───soh				    # SOH模块
│   │───licon_soh.py		 # SOH界面初始化
│   │───soh_getin.py		 # SOH数据读取
│   │───soh_logic.py		 # SOH界面逻辑
│   └───soh_model.py  	     # SOH模型设置
│                            
└───readme.md		    # component介绍
<pre>
