# PyHuskarUI
#
# Copyright (C) 2025 mengps (MenPenS)
# https://github.com/mengps/PyHuskarUI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List
from PySide6.QtCore import QObject, Property, Signal, Slot, QUrl, QUrlQuery
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "HuskarUI.Basic"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class HusRouterHistory(QObject):
    """路由器历史记录项"""

    locationChanged = Signal()

    def __init__(self, location: QUrl, parent: QObject = None):
        super().__init__(parent=parent)
        self._location = location

    @Property(QUrl, notify=locationChanged)
    def location(self) -> QUrl:
        return self._location

    @location.setter
    def location(self, location: QUrl):
        if self._location != location:
            self._location = location
            self.locationChanged.emit()


@QmlElement
class HusRouter(QObject):
    """路由"""

    currentUrlChanged = Signal()
    currentPathChanged = Signal()
    currentIndexChanged = Signal()
    historyChanged = Signal()
    historyMaxCountChanged = Signal()
    canGoBackChanged = Signal()
    canGoForwardChanged = Signal()

    def __init__(self, parent: QObject = None):
        super().__init__(parent=parent)
        self._currentUrl = QUrl()
        self._currentIndex = -1
        self._history: List[HusRouterHistory] = []
        self._historyMaxCount = 100

    @Property(QUrl, notify=currentUrlChanged)
    def currentUrl(self) -> QUrl:
        return self._currentUrl

    @Property(str, notify=currentPathChanged)
    def currentPath(self) -> str:
        return self._currentUrl.path()

    @Property(int, notify=currentIndexChanged)
    def currentIndex(self) -> int:
        return self._currentIndex

    @Property(list, notify=historyChanged)
    def history(self) -> List[HusRouterHistory]:
        return self._history

    @Property(int, notify=historyMaxCountChanged)
    def historyMaxCount(self) -> int:
        return self._historyMaxCount

    @historyMaxCount.setter
    def historyMaxCount(self, maxCount: int):
        if maxCount < 0 or self._historyMaxCount == maxCount:
            return

        self._historyMaxCount = maxCount

        while len(self._history) > self._historyMaxCount:
            history_item = self._history.pop(0)
            history_item.deleteLater()
            self._currentIndex -= 1

        if self._currentIndex < 0:
            self._currentUrl = QUrl()
            self._currentIndex = -1
        elif self._currentIndex >= len(self._history):
            self._currentIndex = len(self._history) - 1
            self._currentUrl = self._history[self._currentIndex].location

        if not self._history or self._currentIndex < 0:
            self._currentUrl = QUrl()
            self._currentIndex = -1
            self.currentUrlChanged.emit()
            self.currentPathChanged.emit()
            self.currentIndexChanged.emit()

        self.historyMaxCountChanged.emit()
        self.historyChanged.emit()

    @Property(bool, notify=canGoBackChanged)
    def canGoBack(self) -> bool:
        return self._currentIndex > 0 and len(self._history) > 0

    @Property(bool, notify=canGoForwardChanged)
    def canGoForward(self) -> bool:
        return self._currentIndex < len(self._history) - 1

    @Slot(QUrl)
    def push(self, url: QUrl):
        """导航到指定URL并将新URL添加到历史记录的顶部"""
        if url.isEmpty() or url == self._currentUrl:
            return

        self._currentUrl = url

        # 如果当前不在历史记录的末尾，需要删除后续的记录
        if self._currentIndex + 1 < len(self._history):
            for i in range(self._currentIndex + 1, len(self._history)):
                self._history[i].deleteLater()
            self._history = self._history[: self._currentIndex + 1]

        # 添加新记录
        self._currentIndex += 1
        self._history.append(HusRouterHistory(url, self))

        # 检查并处理历史记录大小限制
        while len(self._history) > self._historyMaxCount:
            history_item = self._history.pop(0)
            history_item.deleteLater()
            self._currentIndex -= 1

        self.currentUrlChanged.emit()
        self.currentPathChanged.emit()
        self.currentIndexChanged.emit()
        self.historyChanged.emit()
        self.canGoBackChanged.emit()
        self.canGoForwardChanged.emit()

    @Slot(QUrl)
    def replace(self, url: QUrl):
        """替换当前URL并将老的URL从历史记录中移除, 然后将新URL添加到历史记录顶部"""
        if url.isEmpty():
            return

        if url == self._currentUrl or self._currentIndex < 0 or self._currentIndex >= len(self._history):
            return

        self._history[self._currentIndex].setLocation(url)
        self._currentUrl = url

        self.currentUrlChanged.emit()
        self.currentPathChanged.emit()

    @Slot()
    def clear(self):
        """清空所有导航历史"""
        for history_item in self._history:
            history_item.deleteLater()

        self._history.clear()
        self._currentUrl = QUrl()
        self._currentIndex = -1

        self.currentUrlChanged.emit()
        self.currentPathChanged.emit()
        self.currentIndexChanged.emit()
        self.historyChanged.emit()
        self.canGoBackChanged.emit()
        self.canGoForwardChanged.emit()

    @Slot()
    def goBack(self):
        """后退到历史记录中的上一个URL"""
        if self.canGoBack:
            self._currentIndex -= 1
            self._currentUrl = self._history[self._currentIndex].location

            self.currentUrlChanged.emit()
            self.currentPathChanged.emit()
            self.currentIndexChanged.emit()
            self.canGoBackChanged.emit()
            self.canGoForwardChanged.emit()

    @Slot()
    def goForward(self):
        """前进到历史记录中的下一个URL"""
        if self.canGoForward:
            self._currentIndex += 1
            self._currentUrl = self._history[self._currentIndex].location

            self.currentUrlChanged.emit()
            self.currentPathChanged.emit()
            self.currentIndexChanged.emit()
            self.canGoBackChanged.emit()
            self.canGoForwardChanged.emit()

    @Slot(QUrl, result=dict)
    def getQueryParams(self, url: QUrl) -> dict:
        """以键值对的形式返回URL中的查询字符串"""
        result = {}
        query = QUrlQuery(url)

        for key, value in query.queryItems():
            result[key] = value

        return result
