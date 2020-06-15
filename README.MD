# 问卷调查系统后端

开发语言：Python 3.7（>=3.5 应该可以）

数据库支持：MySQL（其他数据库未测试，由sqlalchemy支持）

支持平台：Windows/Linux（建议Linux，异步服务Windows下只支持select模式）

开发流程及文档：https://github.com/Wh1isper/QuestionnaireSystemDoc

前端：https://github.com/JellyBeanXiewh/QuestionnaireSystemFrontend



## 分支说明



目前拥有四个分支：

1. master分支：通过测试的代码将合入这里，始终保持windows/linux兼容
2. dev分支：windows/linux兼容的开发平台，用以主要功能的开发和测试
3. linuxdev分支：linux平台特供，针对linux平台进行优化，并添加redis缓存等功能（仍在规划中）
4. PerformanceTesting：专为性能测试开辟的分支，定期追赶主分支的进度



## 安装流程

### 1. 安装依赖包

pip install -r requirements.txt

### 2. 导入数据库表

见 /db/crebas.sql

### 3. 配置数据库

见 db_config.py

### 4. 运行app.py

### 5. 更改配置见config.py

# !!!不要恶意使用里面公开的邮件账号
# !!!你应该注册一个新的



## 维护说明

此项目在2020年7月份之后进入随缘维护模式……

