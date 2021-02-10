# jAccount 验证码识别器

叉自 https://github.com/PhotonQuantum/jaccount-captcha-solver
一个使用 ~~SVM 和~~ ResNet 的高准确率 SJTU jAccount 验证码识别器。

基于 Resnet 的识别器可达到 99% 的平均准确率。它将图片直接输入一个预训练的 ResNet-20 模型中进行推断。

预训练的模型来自 https://github.com/PhotonQuantum/jaccount-captcha-solver/releases/tag/v1.1 ，使用 `onnxruntime/tools/python/remove_initializer_from_input.py` 进行了重生成。

## 使用

使用 docker 部署，向 `http://localhost:8080` 以任意路径发起 `POST` 请求，请求中包含文件参数 `image` ，内容为验证码图片。
将返回 json 响应，响应范例如下，其中 `result` 的值是验证码识别结果。
```json
{
    "error": "succeed",
    "result": "gbmke"
}
```

## 许可证

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details

## 鸣谢

- [T.T. Tang](https://github.com/ElectronicElephant) for his idea and support on training a ResNet-20 model 
to do end-to-end multi-task learning on captcha images.

- [Yerlan Idelbayev](https://github.com/akamaster) for his ResNet implementation.
