[← 返回主目录](../index.md)

[← 返回本类别目录](./index.md)

# HusPage 页面


一个容器控件，可以方便地向页面添加页眉和页脚项。

* **模块 { HuskarUI.Basic }**

* **继承自 { Page }**


<br/>

### 支持的代理：

- 无


<br/>

### 支持的属性：

属性名 | 类型 | 默认值 | 描述
------ | --- | :---: | ---
colorBg | color | - | 背景颜色

<br/>

## 代码演示

### 示例 1

使用方法等同于 `Page`。

```qml
import QtQuick
import HuskarUI.Basic

Column {
    spacing: 15

    HusTabView {
        width: parent.width
        height: 200
        contentDelegate: HusPage {
            header: HusText {
                width: parent.width
                padding: 5
                font.pixelSize: HusTheme.Primary.fontPrimarySizeHeading4
                horizontalAlignment: Text.AlignHCenter
                text: 'Title - Page ' + (index + 1)
            }
            contentItem: Item {
                width: parent.width

                HusDivider {
                    anchors.top: parent.top
                    width: parent.width
                }

                HusText {
                    anchors.centerIn: parent
                    text: model.content + (index + 1)
                }

                HusDivider {
                    anchors.bottom: parent.bottom
                    width: parent.width
                }
            }
            footer: HusText {
                width: parent.width
                padding: 5
                horizontalAlignment: Text.AlignHCenter
                text: '(' + (index + 1) + ')'
            }
        }
        initModel: [
            {
                iconSource: HusIcon.CreditCardOutlined,
                title: 'Tab 1',
                content: 'Content of page ',
            },
            {
                iconSource: HusIcon.CreditCardOutlined,
                title: 'Tab 2',
                content: 'Content of page ',
            },
            {
                iconSource: HusIcon.CreditCardOutlined,
                title: 'Tab 3',
                content: 'Content of page ',
            }
        ]
    }
}
```

