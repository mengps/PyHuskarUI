import QtQuick
import QtQuick.Controls.Basic
import HuskarUI.Basic

import '../../Controls'

Flickable {
    contentHeight: column.height
    ScrollBar.vertical: HusScrollBar { }

    Column {
        id: column
        width: parent.width - 15
        spacing: 30

        DocDescription {
            desc: qsTr(`
# HusMultiCheckBox 多复选框选择器 \n
下拉多复选框选择器。\n
* **模块 { HuskarUI.Basic }**\n
* **继承自 { [HusSelect](internal://HusSelect) }**\n
\n<br/>
\n### 支持的代理：\n
- **prefixDelegate: Component** 前缀代理\n
- **suffixDelegate: Component** 后缀代理\n
- **tagDelegate: Component** 标签代理，代理可访问属性：\n
  - \`index: var\` 标签索引\n
  - \`tagData: var\` 标签数据\n
\n<br/>
\n### 支持的属性：\n
属性名 | 类型 | 默认值 | 描述
------ | --- | :---: | ---
animationEnabled | bool | HusTheme.animationEnabled | 是否开启动画
options | array | [] | 选项模型列表
filterOption | function | - | 输入项将使用该函数进行筛选
text | string | '' | 当前输入文本
prefix | string | '' | 前缀文本
suffix | string | '' | 后缀文本
genDefaultKey | bool | true | 是否生成默认键(如果没有给定key则为label)
defaultSelectedKeys | array | [] | 默认选中的键数组
selectedKeys | array | [] | 选中项的键
searchEnabled | bool | true | 是否启用搜索
tagCount | int(readonly) | 0 | 当前(选择)标签数量
maxTagCount | int | -1 | 最多显示多少个标签(-1无限制)
tagSpacing | int | 5 | 标签间隔
colorTagText | color | - | 标签文本颜色
colorTagBg | color | - | 标签背景颜色
radiusTagBg | [HusRadius](internal://HusRadius) | - | 标签圆角
\n<br/>
\n### 模型{options}支持的属性：\n
属性名 | 类型 | 可选/必选 | 描述
------ | --- | :---: | ---
label | string | 必选 | 本选择项的标签
value | var | 可选 | 本选择项的值
enabled | bool | 可选 | 本选择项是否启用
\n<br/>
\n### 支持的函数：\n
- \`findKey(key: string): var\` 查找 \`key\` 处的选项数据 \n
- \`filter()\` 过滤选项列表 \n
- \`insertTag(index: int, key: string)\` 插入键为 \`key\` 的标签到 \`index\` 处(必须是 \`options\` 中的数据) \n
- \`appendTag(key: string)\` 在末尾添加键为 \`key\` 的标签(必须是 \`options\` 中的数据) \n
- \`removeTagAtKey(key: string)\` 删除 \`key\` 处的标签 \n
- \`removeTagAtIndex(index: int)\` 删除 \`index\` 处的标签 \n
- \`clearTag()\` 清空标签 \n
- \`clearInput()\` 清空输入 \n
- \`openPopup()\` 打开弹出框 \n
- \`closePopup()\` 关闭弹出框 \n
\n<br/>
\n### 支持的信号：\n
- \`search(input: string)\` 搜索补全项的时发出\n
  - \`input\` 输入文本\n
- \`select(option: var)\` 选择标签项时发出\n
  - \`option\` 选择的选项\n
- \`deselect(option: var)\` 删除标签项时发出\n
  - \`option\` 删除的选项\n
\n<br/>
\n### 注意事项：\n
\`options\` 列表通常需要 \`key\` 属性，如果未给出将使用 \`label\` 作为 \`key\`
                       `)
        }

        Description {
            title: qsTr('何时使用')
            desc: qsTr(`
- 弹出一个多选下拉菜单给用户多选操作，用于扩展单项选择器([HusSelect](internal://HusSelect))，或者需要一个更优雅的多选器时。\n
                       `)
        }

        ThemeToken {
            source: 'HusMultiCheckBox'
            historySource: 'https://github.com/mengps/HuskarUI/blob/master/src/imports/HusMultiCheckBox.qml'
        }

        Description {
            title: qsTr('代码演示')
        }

        CodeBox {
            width: parent.width
            descTitle: qsTr(`基本使用`)
            desc: qsTr(`
通过 \`options\` 设置数据源。\n
通过 \`filterOption\` 设置过滤选项，它是形如：\`function(input: string, option: var): bool { }\` 的函数。\n
                       `)
            code: `
                import QtQuick
                import HuskarUI.Basic

                Column {
                    width: parent.width
                    spacing: 10

                    HusRadioBlock {
                        id: sizeHintRadio
                        initCheckedIndex: 1
                        model: [
                            { label: 'Small', value: 'small' },
                            { label: 'Normal', value: 'normal' },
                            { label: 'Large', value: 'large' },
                        ]
                    }

                    HusMultiCheckBox {
                        width: 200
                        sizeHint: sizeHintRadio.currentCheckedValue
                        filterOption: (input, option) => option.label.toUpperCase().indexOf(input.toUpperCase()) !== -1
                        Component.onCompleted: {
                            const list = [];
                            for (let i = 10; i < 36; i++) {
                                list.push({
                                              label: i.toString(36) + i,
                                              value: i.toString(36) + i,
                                          });
                            }
                            options = list;
                        }
                    }
                }
            `
            exampleDelegate: Column {
                spacing: 10

                HusRadioBlock {
                    id: sizeHintRadio
                    initCheckedIndex: 1
                    model: [
                        { label: 'Small', value: 'small' },
                        { label: 'Normal', value: 'normal' },
                        { label: 'Large', value: 'large' },
                    ]
                }

                HusMultiCheckBox {
                    width: 200
                    sizeHint: sizeHintRadio.currentCheckedValue
                    filterOption: (input, option) => option.label.toUpperCase().indexOf(input.toUpperCase()) !== -1
                    Component.onCompleted: {
                        const list = [];
                        for (let i = 10; i < 36; i++) {
                            list.push({
                                          label: i.toString(36) + i,
                                          value: i.toString(36) + i,
                                      });
                        }
                        options = list;
                    }
                }
            }
        }

        CodeBox {
            width: parent.width
            descTitle: qsTr(`自定义下拉文本`)
            desc: qsTr(`
通过 \`textRole\` 设置弹窗显示的文本角色。\n
通过 \`searchEnabled\` 设置是否启用搜索。\n
通过 \`placeholderText\` 设置占位符文本。\n
                       `)
            code: `
                import QtQuick
                import HuskarUI.Basic

                Row {
                    width: parent.width
                    spacing: 10

                    HusMultiCheckBox {
                        width: 200
                        itemWidth: width
                        textRole: 'desc'
                        searchEnabled: false
                        placeholderText: 'select one country'
                        options: [
                            {
                                label: 'China',
                                value: 'china',
                                desc: '🇨🇳 China (中国)',
                            },
                            {
                                label: 'USA',
                                value: 'usa',
                                desc: '🇺🇸 USA (美国)',
                            },
                            {
                                label: 'Japan',
                                value: 'japan',
                                desc: '🇯🇵 Japan (日本)',
                            },
                            {
                                label: 'Korea',
                                value: 'korea',
                                desc: '🇰🇷 Korea (韩国)',
                            },
                        ]
                    }
                }
            `
            exampleDelegate: Row {
                spacing: 10

                HusMultiCheckBox {
                    width: 200
                    itemWidth: width
                    textRole: 'desc'
                    searchEnabled: false
                    placeholderText: 'select one country'
                    options: [
                        {
                            label: 'China',
                            value: 'china',
                            desc: '🇨🇳 China (中国)',
                        },
                        {
                            label: 'USA',
                            value: 'usa',
                            desc: '🇺🇸 USA (美国)',
                        },
                        {
                            label: 'Japan',
                            value: 'japan',
                            desc: '🇯🇵 Japan (日本)',
                        },
                        {
                            label: 'Korea',
                            value: 'korea',
                            desc: '🇰🇷 Korea (韩国)',
                        },
                    ]
                }
            }
        }

        CodeBox {
            width: parent.width
            descTitle: qsTr(`前缀和后缀`)
            desc: qsTr(`
通过 \`prefix\` 设置前缀文本。\n
通过 \`suffix\` 设置后缀文本。\n
通过 \`prefixDelegate\` 设置前缀代理。\n
通过 \`suffixDelegate\` 设置后缀代理。\n
                       `)
            code: `
                import QtQuick
                import HuskarUI.Basic

                Row {
                    width: parent.width
                    spacing: 10

                    HusMultiCheckBox {
                        width: 200
                        prefix: 'User'
                        options: [
                            { value: 'jack', label: 'Jack' },
                            { value: 'lucy', label: 'Lucy' },
                            { value: 'Yiminghe', label: 'yiminghe' },
                            { value: 'disabled', label: 'Disabled', enabled: false },
                        ]
                    }

                    HusMultiCheckBox {
                        width: 200
                        prefixDelegate: HusIconText { iconSource: HusIcon.SmileOutlined }
                        options: [
                            { value: 'jack', label: 'Jack' },
                            { value: 'lucy', label: 'Lucy' },
                            { value: 'Yiminghe', label: 'yiminghe' },
                            { value: 'disabled', label: 'Disabled', enabled: false },
                        ]
                    }

                    HusMultiCheckBox {
                        width: 200
                        suffix: 'User'
                        options: [
                            { value: 'jack', label: 'Jack' },
                            { value: 'lucy', label: 'Lucy' },
                            { value: 'Yiminghe', label: 'yiminghe' },
                            { value: 'disabled', label: 'Disabled', enabled: false },
                        ]
                    }

                    HusMultiCheckBox {
                        width: 200
                        suffixDelegate: HusIconText { iconSource: HusIcon.SmileOutlined }
                        options: [
                            { value: 'jack', label: 'Jack' },
                            { value: 'lucy', label: 'Lucy' },
                            { value: 'Yiminghe', label: 'yiminghe' },
                            { value: 'disabled', label: 'Disabled', enabled: false },
                        ]
                    }
                }
            `
            exampleDelegate: Column {
                spacing: 10

                Row {
                    spacing: 10

                    HusMultiCheckBox {
                        width: 200
                        prefix: 'User'
                        options: [
                            { value: 'jack', label: 'Jack' },
                            { value: 'lucy', label: 'Lucy' },
                            { value: 'Yiminghe', label: 'yiminghe' },
                            { value: 'disabled', label: 'Disabled', enabled: false },
                        ]
                    }

                    HusMultiCheckBox {
                        width: 200
                        suffix: 'User'
                        options: [
                            { value: 'jack', label: 'Jack' },
                            { value: 'lucy', label: 'Lucy' },
                            { value: 'Yiminghe', label: 'yiminghe' },
                            { value: 'disabled', label: 'Disabled', enabled: false },
                        ]
                    }
                }

                Row {
                    spacing: 10

                    HusMultiCheckBox {
                        width: 200
                        prefixDelegate: HusIconText { iconSource: HusIcon.SmileOutlined }
                        options: [
                            { value: 'jack', label: 'Jack' },
                            { value: 'lucy', label: 'Lucy' },
                            { value: 'Yiminghe', label: 'yiminghe' },
                            { value: 'disabled', label: 'Disabled', enabled: false },
                        ]
                    }

                    HusMultiCheckBox {
                        width: 200
                        suffixDelegate: HusIconText { iconSource: HusIcon.SmileOutlined }
                        options: [
                            { value: 'jack', label: 'Jack' },
                            { value: 'lucy', label: 'Lucy' },
                            { value: 'Yiminghe', label: 'yiminghe' },
                            { value: 'disabled', label: 'Disabled', enabled: false },
                        ]
                    }
                }
            }
        }

        CodeBox {
            width: parent.width
            descTitle: qsTr(`隐藏已选择选项`)
            desc: qsTr(`
隐藏下拉列表中已选择的选项。\n
                       `)
            code: `
                import QtQuick
                import HuskarUI.Basic

                HusMultiCheckBox {
                    width: 500
                    filterOption:
                        (input, option) => {
                            filteredOptions = theOptions.filter((o) => !selectedKeys.includes(o));
                            return filteredOptions.indexOf(option.label) != -1;
                        }
                    onSelect: {
                        filteredOptions = theOptions.filter((o) => !selectedKeys.includes(o));
                        options = filteredOptions.map((item) => ({ label: item }));
                    }
                    onDeselect: {
                        filteredOptions = theOptions.filter((o) => !selectedKeys.includes(o));
                        options = filteredOptions.map((item) => ({ label: item }));
                    }
                    Component.onCompleted: options = theOptions.map((item) => ({ label: item }));
                    property var theOptions: ['Apples', 'Nails', 'Bananas', 'Helicopters']
                    property var filteredOptions: []
                }
            `
            exampleDelegate: Row {
                spacing: 10

                HusMultiCheckBox {
                    width: 500
                    filterOption:
                        (input, option) => {
                            filteredOptions = theOptions.filter((o) => !selectedKeys.includes(o));
                            return filteredOptions.indexOf(option.label) != -1;
                        }
                    onSelect: {
                        filteredOptions = theOptions.filter((o) => !selectedKeys.includes(o));
                        options = filteredOptions.map((item) => ({ label: item }));
                    }
                    onDeselect: {
                        filteredOptions = theOptions.filter((o) => !selectedKeys.includes(o));
                        options = filteredOptions.map((item) => ({ label: item }));
                    }
                    Component.onCompleted: options = theOptions.map((item) => ({ label: item }));
                    property var theOptions: ['Apples', 'Nails', 'Bananas', 'Helicopters']
                    property var filteredOptions: []
                }
            }
        }

        CodeBox {
            width: parent.width
            descTitle: qsTr(`自定义选择标签`)
            desc: qsTr(`
允许自定义选择标签的样式。\n
通过 \`tagDelegate\` 设置标签代理。\n
                       `)
            code: `
                import QtQuick
                import HuskarUI.Basic

                HusMultiCheckBox {
                    id: customTag
                    width: 500
                    tagDelegate: HusTag {
                        text: tagData.label
                        presetColor: tagData.value
                        closeIconSource: HusIcon.CloseOutlined
                        closeIconSize: 12
                        onClose: customTag.removeTagAtIndex(index);
                    }
                    options: [
                        { label: 'gold', value: 'gold' },
                        { label: 'lime', value: 'lime' },
                        { label: 'green', value: 'green' },
                        { label: 'cyan', value: 'cyan' },
                    ]
                }
            `
            exampleDelegate: Row {
                spacing: 10

                HusMultiCheckBox {
                    id: customTag
                    width: 500
                    tagDelegate: HusTag {
                        text: tagData.label
                        presetColor: tagData.value
                        closeIconSource: HusIcon.CloseOutlined
                        closeIconSize: 12
                        onClose: customTag.removeTagAtIndex(index);
                    }
                    options: [
                        { label: 'gold', value: 'gold' },
                        { label: 'lime', value: 'lime' },
                        { label: 'green', value: 'green' },
                        { label: 'cyan', value: 'cyan' },
                    ]
                }
            }
        }

        CodeBox {
            width: parent.width
            descTitle: qsTr(`最大选中数量`)
            desc: qsTr(`
通过设置 \`maxTagCount\` 约束最多可选中的数量，当超出限制时会变成禁止选中状态。\n
                       `)
            code: `
                import QtQuick
                import HuskarUI.Basic

                HusMultiCheckBox {
                    width: 500
                    maxTagCount: 3
                    suffix: \`\${tagCount}/\${maxTagCount}\`
                    options: [
                        { value: 'Ava Swift', label: 'Ava Swift' },
                        { value: 'Cole Reed', label: 'Cole Reed' },
                        { value: 'Mia Blake', label: 'Mia Blake' },
                        { value: 'Jake Stone', label: 'Jake Stone' },
                        { value: 'Lily Lane', label: 'Lily Lane' },
                        { value: 'Ryan Chase', label: 'Ryan Chase' },
                        { value: 'Zoe Fox', label: 'Zoe Fox' },
                        { value: 'Alex Grey', label: 'Alex Grey' },
                        { value: 'Elle Blair', label: 'Elle Blair' },
                    ]
                }
            `
            exampleDelegate: Row {
                spacing: 10

                HusMultiCheckBox {
                    width: 500
                    maxTagCount: 3
                    suffix: `${tagCount}/${maxTagCount}`
                    options: [
                        { value: 'Ava Swift', label: 'Ava Swift' },
                        { value: 'Cole Reed', label: 'Cole Reed' },
                        { value: 'Mia Blake', label: 'Mia Blake' },
                        { value: 'Jake Stone', label: 'Jake Stone' },
                        { value: 'Lily Lane', label: 'Lily Lane' },
                        { value: 'Ryan Chase', label: 'Ryan Chase' },
                        { value: 'Zoe Fox', label: 'Zoe Fox' },
                        { value: 'Alex Grey', label: 'Alex Grey' },
                        { value: 'Elle Blair', label: 'Elle Blair' },
                    ]
                }
            }
        }

        CodeBox {
            width: parent.width
            descTitle: qsTr(`大数据`)
            desc: qsTr(`
100000 选择项。\n
                       `)
            code: `
                import QtQuick
                import HuskarUI.Basic

                Loader {
                    asynchronous: true
                    sourceComponent: HusMultiCheckBox {
                        width: 500
                        genDefaultKey: false
                        filterOption: (input, option) => option.label.toUpperCase().indexOf(input.toUpperCase()) !== -1
                        Component.onCompleted: {
                            const list = [];
                            for (let i = 0; i < 100000; i++) {
                                const label = \`\${i.toString(36)}\${i}\`;
                                list.push({ key: label, label: label, enabled: i % 10 !== 0 });
                            }
                            options = list;
                        }
                    }
                }
            `
            exampleDelegate: Row {
                spacing: 10

                Loader {
                    asynchronous: true
                    sourceComponent: HusMultiCheckBox {
                        width: 500
                        genDefaultKey: false
                        filterOption: (input, option) => option.label.toUpperCase().indexOf(input.toUpperCase()) !== -1
                        Component.onCompleted: {
                            const list = [];
                            for (let i = 0; i < 100000; i++) {
                                const label = `${i.toString(36)}${i}`;
                                list.push({ key: label, label: label, enabled: i % 10 !== 0 });
                            }
                            options = list;
                        }
                    }
                }
            }
        }
    }
}
