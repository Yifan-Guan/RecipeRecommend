### 前端运行

```powershell
cd vue-ui
npm install
npm run dev
```

### 后端运行

#### 依赖安装

运行前请安装依赖，建议使用conda虚拟环境

#### API配置

在langchain-server文件夹下新建.env文件，写入如下内容：

```shell
# langsmith配置，可选，用于跟踪langchain运行情况
LANGSMITH_TRACING = true
LANGSMITH_ENDPOINT = ""
LANGSMITH_API_KEY = ""
LANGSMITH_PROJECT = ""
# OpenAI API配置
OPENAI_API_KEY = ""
OPENAI_BASE_URL = ""
```



#### 数据库初始化

以root用户登录MySQL数据库，运行langserve/recipe-recommend-de-init.sql文件以初始化数据库

#### 启动服务

```powershell
cd langchain-server
poetry run langchain serve --port=8000
```

