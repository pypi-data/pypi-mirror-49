## 快速开始

该类库将会把模型执行过程中的 `parameters` 和 `metrics` 提交到 `openbayes-server` 方便记录每次模型的结果。

```python
from openbayestool import log_param, log_metric

# 记录参数 `learning_rate=0.01`
log_param('learning_rate', 0.01)

# 同一参数将会记录最后一个请求的结果 `foo=3`
log_param('foo', 1)
log_param('foo', 2)
log_param('foo', 3)

# 记录模型的运行结果 `precision=0.77`
log_metric('precision', 0.77)

# 同一个结果 precision 多次记录会追加结果，即结果为 [0.79, 0.82, 0.86]
log_metric('precision', 0.79)
log_metric('precision', 0.82)
log_metric('precision', 0.86)
```

## 安装

```shell
pip install -U openbayestool
```

## 使用

**注意** 在 openbayes 所提交的任务会自动设置 **服务器以及相应的账号密码** 和 **要记录的容器的 url** 无需用户知晓。

### 设置服务器以及相应的账号密码

通过环境变量设置如下变量：

```
UAA_TOKEN_URL=http://<server-url>/users/login
UAA_USERNAME=<username>
UAA_PASSWORD=<password>
```

### 设置要记录的容器的 url

可以通过环境变量配置：`JOB_UPDATE_URL=<job-url>`，也可以在程序中采用 `api` 配置：

```python
from openbayestool import set_callback_url, get_callback_url

set_callback_url('<job-url>') # set the job-url
get_callback_url() # return the job-url
```

### 设置访问 API 的 token

可以通过环境变量 `JOB_ACCESS_TOKEN=<job-token>` 配置，也可以在程序中采用 `api` 配置：

```python
from openbayestool import set_access_token, get_access_token

set_access_token('<job-token>') # set the job-token
get_access_token() # return the job-token
```

### 通过 api 记录 `parameters` 和 `metrics`

```python
from openbayestool import log_param, log_metric

# 记录参数 `learning_rate=0.01`
log_param('learning_rate', 0.01)

# 同一参数将会记录最后一个请求的结果 `foo=3`
log_param('foo', 1)
log_param('foo', 2)
log_param('foo', 3)

# 记录模型的运行结果 `precision=0.77`
log_metric('precision', 0.77)

# 同一个结果 precision 多次记录会追加结果，即结果为 [0.79, 0.82, 0.86]
log_metric('precision', 0.79)
log_metric('precision', 0.82)
log_metric('precision', 0.86)
```

## 查看记录结果

在 openbayes 的 models 会展现以上的记录结果并作为自动建模确认下一步参数的依据。