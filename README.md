
## 应用简介

本应用将创建一个函数及对应资源，并配置打开"有状态异步调用"开关及异步调用目标 mns 队列。主函数体采用 sleep 方式模拟长时间执行的任务情形。
当函数开始异步执行后，可以通过控制台/SDK/API 查看/操作（停止）执行。
当函数执行失败（或手动停止后），异步执行结果消息将被推送到 mns 队列中来实现死信队列的功能，方便业务人员感知异步函数执行失败的消息并进行后续处理。

功能文档：https://help.aliyun.com/document_detail/181866.html
## 使用步骤

1. 在控制台创建一个 mns 队列，如名称为 stateful-invocation-dlq；
2. 更新 [fun](https://help.aliyun.com/document_detail/140283.html) 工具版本 > 3.6.18，并配置好 fun 工具；
3. git clone 本项目。更改 template.yml 第 99/100 行 mns 队列为实际资源 ARN（请将 {please_replace_me} 替换为您队列的名称），
并在项目目录中执行如下命令： `fun deploy --use-ros --stack-name xxxxx`
4. 您将看到创建了具有相应的异步配置的函数及 ram 资源。 

注意：操作 fun deploy 前请确认已经更新模板中的队列名称（第 3 步），避免因为消息队列不存在而造成发送目标失败。

## 实际测试
1. 异步配置仅在异步调用时才会生效。您可以使用 sdk/cli 工具发送异步调用请求。
    本示例我们使用 [fcli](https://help.aliyun.com/document_detail/52995.html) 发送异步触发请求，并观察 mns 队列：
    `invk main -t Async -s '{"failure":true}'`
    
2. 在控制台中查看、操作异步调用：
    (1) 查看异步配置情况：
    (2) 查看异步调用执行状态：
    (3) 停止进行中的异步调用：
    (4) 查看历史执行列表，以及某具体执行的结果：
    
3. 在函数执行完成后(以 cancel 操作为例)，我们可以从 mns 队列接收到如下消息：
    ```
    {"timestamp":xxxx,"requestContext":{"requestId":"xxxx","functionArn":"acs:fc:::services/Stateful-Invocation-demo.LATEST/functions/main","condition":"UnhandledInvocationError","approximateInvokeCount":1},"requestPayload":"{\"failure\":true}","responseContext":{"statusCode":200,"functionError":"UnhandledInvocationError"},"responsePayload":"{\"errorMessage\":\"Process exited unexpectedly before completing request (duration: 13689ms, maxMemoryUsage: 10.86MB)\"}"}
    ```
    即当异步调用失败（或手动中止）后，我们可以从 mns 接收到异步调用事件的详细错误信息。