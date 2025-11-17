<div align=center>
<img width=64 src="resources/huskarui_icon.svg">

# 「 PyHuskarUI 」 基于 Qml 的现代 UI

Qt Qml 的 Ant 设计组件库

</div>

<div align=center>

![win-badge] ![linux-badge] ![macos-badge] ![android-badge]

[![Issues][issues-open-image]][issues-open-url] [![Issues][issues-close-image]][issues-close-url] [![Release][release-image]][release-url]

[![QQGroup][qqgroup-image]][qqgroup-url]

[English](./README.md) | 中文

</div>

[win-badge]: https://img.shields.io/badge/Windows-passing-brightgreen?style=flat-square
[linux-badge]: https://img.shields.io/badge/Linux-passing-brightgreen?style=flat-square
[macos-badge]: https://img.shields.io/badge/MacOS-passing-brightgreen?style=flat-square
[android-badge]: https://img.shields.io/badge/Android-passing-brightgreen?style=flat-square

[issues-open-image]: https://img.shields.io/github/issues/mengps/PyHuskarUI?label=Issue&style=flat-square
[issues-open-url]: https://github.com/mengps/PyHuskarUI/issues
[issues-close-image]: https://img.shields.io/github/issues-closed/mengps/PyHuskarUI?color=brightgreen&label=Issue&style=flat-square
[issues-close-url]: https://github.com/mengps/PyHuskarUI/issues?q=is%3Aissue%20state%3Aclosed

[release-image]: https://img.shields.io/github/v/release/mengps/PyHuskarUI?label=Release&style=flat-square
[release-url]: https://github.com/mengps/PyHuskarUI/releases

[qqgroup-image]: https://img.shields.io/badge/QQGroup-490328047-f74658?style=flat-square
[qqgroup-url]: https://qm.qq.com/q/cMNHn2tWeY

<div align=center>

## 🌈 陈列室预览

<img width=800 height=500 src="https://github.com/mengps/HuskarUI/blob/master/preview/light.png">
<img width=800 height=500 src="https://github.com/mengps/HuskarUI/blob/master/preview/dark.png">
<img width=800 height=500 src="https://github.com/mengps/HuskarUI/blob/master/preview/doc.png">

</div>

## ✨ 特性

- 📦 一套开箱即用的优质 Qml 组件.
- 🎨 强大的主题定制系统.
- 💻 基于Qml，完全跨平台.
- 🔧 高度灵活的基于委托的组件定制.

## 🗺️ 路线图

开发计划可以在这里看到: [组件路线图](https://github.com/mengps/PyHuskarUI/discussions/5).

任何人都可以通过 issue/qq群/wx群 进行讨论, 最终有意义的组件/功能将添加到开发计划.

## 🌐 在线 wiki
- [PyHuskarUI 在线 wiki (AI)](https://deepwiki.com/mengps/PyHuskarUI)

## 📺 在线演示

  - [哔哩哔哩](https://www.bilibili.com/video/BV1jodhYhE8a/?spm_id_from=333.1387.homepage.video_card.click)

## 🗂️ 预编译包

预编译了两个平台的 `Windows / Linux` 程序包和二进制库包.

前往 [Release](https://github.com/mengps/PyHuskarUI/releases) 中下载.

## 🔨 如何构建

- 克隆
```auto
git clone --recursive https://github.com/mengps/PyHuskarUI.git
```
- 构建
```auto
uv sync
uv run update_qrc.py
uv run update_shader.py
uv build
```
- 安装
  - use pypi package
  ```auto
  uv pip install pyhuskarui
  ```
  - use source code
  ```auto
  uv pip install .
  ```
- 运行 Gallery
```auto
uv run ./gallery/main.py
```

## 📦 上手

 - 创建 QtQuick 应用 `QtVersion >= 6.7`
 - 添加下面的代码到您的 `main.py` 中
 ```python
 from huskarui.husapp import HusApp

 if __name__ == "__main__":
     ...
     app = QGuiApplication(sys.argv);
     engine = QQmlApplicationEngine();
     HusApp.initialize(&engine);
     ...
 ```
 - 添加下面的代码到您的 `.qml` 中
 ```qml
  import HuskarUI.Basic
  HusWindow { 
    ...
  }
 ```
好了，你现在可以愉快的开始使用 PyHuskarUI 了。

## 🚩 参考

- Ant-d 组件: https://ant-design.antgroup.com/components/overview-cn
- Ant 设计: https://ant-design.antgroup.com/docs/spec/introduce-cn

## 💓 许可证

使用 `MIT LICENSE`

## 🌇 环境

Windows 11 / Ubuntu 24.04.2, Qt Version >= 6.7

## 🎉 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=mengps/PyHuskarUI&type=Date)](https://star-history.com/#mengps/PyHuskarUI&Date)