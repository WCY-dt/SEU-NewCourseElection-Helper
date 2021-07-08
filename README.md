# SEU-NewCourseElection-Helper

![Stars](https://img.shields.io/github/stars/wcy-dt/SEU-NewCourseElection-Helper.svg)
![Forks](https://img.shields.io/github/forks/wcy-dt/SEU-NewCourseElection-Helper.svg)

脚本共有两个版本

- 在线版（利用GitHub workflow）
- ~~离线版（请点击右侧Releases下载）~~已停止开发

离线版由于系统兼容性问题，目前已停止使用与开发。

脚本仍在改进中，且只经过我自己的账号测试无误，可能会有亿点点bug。欢迎提交issues报告问题。

另外，能不能点个star呀（可怜🥺

## 注意！！！

- 由于网站限制以及防止请求过多导致ip被封，目前安全的刷课时间为2秒一次！不提供修改手段，但如果你精通python，也**请不要擅自修改**！
- 程序**不会存储任何个人信息**，不放心的尽管查源码！
- 本人对因为程序产生的任何问题**不负责任**！
- 本脚本只能用于捡漏，**请勿用于抢课**！！！
- 请务必**仔细阅读**以下使用方法！！！

## 在线版使用步骤

1. 点击右上角的 fork，把本仓库 fork 走。（如果在这之前能点一个star我会很感激~）
2. 如下图所示，依次点击 settings，secrets，new repository secret按钮

![image-20210708215628085](pic/image-20210708215628085.png)

3. 新建四个secret，它们分别是

   - NAME：你的账号

   - PASSWORD：你的密码

   - TURN：选课轮次（如要第三轮就输入`3`）

   - CLASS：要选的课程

     例如`B5710350 [05]`表示课程编号为B5710350，选择编号为05的老师。仅有一个老师的也要填。不要忘记了中间的空格！

   例如，下面是填写NAME字段的一个示例

![image-20210708215835775](pic/image-20210708215835775.png)

最终效果如下所示

![image-20210708220030760](pic/image-20210708220030760.png)

4. 点击右上角的 star，即可自动运行。

   根据GitHub的政策，一次性最多可以运行6小时！
   
   如果要再次运行，取消star，再点一下star就好了！
