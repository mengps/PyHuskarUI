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

import ctypes
import sys
from ctypes import wintypes
from enum import IntEnum
from loguru import logger
from PySide6.QtCore import QAbstractNativeEventFilter, QOperatingSystemVersion, QVersionNumber
from PySide6.QtGui import QCursor, QWindow

# Constants
WM_NCCALCSIZE = 0x0083
WM_NCHITTEST = 0x0084
WM_SYSCOMMAND = 0x0112
WM_GETMINMAXINFO = 0x0024
WM_DESTROY = 0x0002

WS_CAPTION = 0x00C00000
WS_THICKFRAME = 0x00040000
WS_MAXIMIZEBOX = 0x00010000
WS_MINIMIZEBOX = 0x00020000
WS_SYSMENU = 0x00080000

GWL_STYLE = -16

SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_FRAMECHANGED = 0x0020
SWP_NOZORDER = 0x0004
SWP_NOOWNERZORDER = 0x0200

HTLEFT = 10
HTRIGHT = 11
HTTOP = 12
HTTOPLEFT = 13
HTTOPRIGHT = 14
HTBOTTOM = 15
HTBOTTOMLEFT = 16
HTBOTTOMRIGHT = 17
HTCAPTION = 2
HTCLIENT = 1

SC_MAXIMIZE = 0xF030
SC_RESTORE = 0xF120
SC_MOVE = 0xF010

ABM_GETSTATE = 0x00000004
ABM_GETTASKBARPOS = 0x00000005
ABS_AUTOHIDE = 0x00000001

MONITOR_DEFAULTTONEAREST = 0x00000002
MONITOR_DEFAULTTOPRIMARY = 0x00000001

SM_CXSIZEFRAME = 32
SM_CYSIZEFRAME = 33
SM_CXPADDEDBORDER = 92


# DWM Constants for Shadow
class DWMNCRENDERINGPOLICY(IntEnum):
    DWMNCRP_USEWINDOWSTYLE = 0
    DWMNCRP_DISABLED = 1
    DWMNCRP_ENABLED = 2
    DWMNCRP_LAST = 3


class DWM_WINDOW_CORNER_PREFERENCE(IntEnum):
    DWMWCP_DEFAULT = 0
    DWMWCP_DONOTROUND = 1
    DWMWCP_ROUND = 2
    DWMWCP_ROUNDSMALL = 3


# Windows 10+ DWM attributes
class DWMWINDOWATTRIBUTE(IntEnum):
    DWMWA_NCRENDERING_POLICY = 2
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_USE_HOSTBACKDROP_BRUSH = 17
    DWMWA_SYSTEMBACKDROP_TYPE = 38
    DWMWA_MICA_EFFECT = 1029  # Windows 11 22H2+ MICA效果
    DWMWA_WINDOW_CORNER_PREFERENCE = 33  # 窗口圆角


# Window Attributes
class WINDOWCOMPOSITIONATTRIB(IntEnum):
    WCA_UNDEFINED = 0
    WCA_NCRENDERING_ENABLED = 1
    WCA_NCRENDERING_POLICY = 2
    WCA_TRANSITIONS_FORCEDISABLED = 3
    WCA_ALLOW_NCPAINT = 4
    WCA_CAPTION_BUTTON_BOUNDS = 5
    WCA_NONCLIENT_RTL_LAYOUT = 6
    WCA_FORCE_ICONIC_REPRESENTATION = 7
    WCA_EXTENDED_FRAME_BOUNDS = 8
    WCA_HAS_ICONIC_BITMAP = 9
    WCA_THEME_ATTRIBUTES = 10
    WCA_NCRENDERING_EXILED = 11
    WCA_NCADORNMENTINFO = 12
    WCA_EXCLUDED_FROM_LIVEPREVIEW = 13
    WCA_VIDEO_OVERLAY_ACTIVE = 14
    WCA_FORCE_ACTIVEWINDOW_APPEARANCE = 15
    WCA_DISALLOW_PEEK = 16
    WCA_CLOAK = 17
    WCA_CLOAKED = 18
    WCA_ACCENT_POLICY = 19
    WCA_FREEZE_REPRESENTATION = (20,)
    WCA_EVER_UNCLOAKED = 21
    WCA_VISUAL_OWNER = 22
    WCA_HOLOGRAPHIC = 23
    WCA_EXCLUDED_FROM_DDA = 24
    WCA_PASSIVEUPDATEMODE = 25
    WCA_USEDARKMODECOLORS = 26
    WCA_CORNER_STYLE = 27
    WCA_PART_COLOR = 28
    WCA_DISABLE_MOVESIZE_FEEDBACK = 29
    WCA_LAST = 30


# Backdrop types for Windows 11
class DWM_SYSTEMBACKDROP_TYPE(IntEnum):
    DWMSBT_AUTO = 0
    DWMSBT_NONE = 1
    DWMSBT_MAINWINDOW = 2
    DWMSBT_TRANSIENTWINDOW = 3
    DWMSBT_TABBEDWINDOW = 4


# ACCENT_STATE
class ACCENT_STATE(IntEnum):
    ACCENT_DISABLED = 0
    ACCENT_ENABLE_GRADIENT = 1
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
    ACCENT_ENABLE_BLURBEHIND = 3
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
    ACCENT_ENABLE_HOST_BACKDROP = 5
    ACCENT_INVALID_STATE = 6


# ACCENT_FLAG
class ACCENT_FLAGS(IntEnum):
    ACCENT_NONE = 0
    ACCENT_ENABLE_ACRYLIC = 1
    ACCENT_ENABLE_ACRYLIC_WITH_LUMINOSITY = 482


# Types
class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG),
    ]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wintypes.HWND),
        ("message", wintypes.UINT),
        ("wParam", wintypes.WPARAM),
        ("lParam", wintypes.LPARAM),
        ("time", wintypes.DWORD),
        ("pt", POINT),
    ]


class MINMAXINFO(ctypes.Structure):
    _fields_ = [
        ("ptReserved", POINT),
        ("ptMaxSize", POINT),
        ("ptMaxPosition", POINT),
        ("ptMinTrackSize", POINT),
        ("ptMaxTrackSize", POINT),
    ]


class NCCALCSIZE_PARAMS(ctypes.Structure):
    _fields_ = [("rgrc", RECT * 3), ("lppos", wintypes.LPVOID)]


class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.ULONG),
        ("hWnd", wintypes.HWND),
        ("uCallbackMessage", wintypes.UINT),
        ("uEdge", wintypes.UINT),
        ("rc", RECT),
        ("lParam", wintypes.LPARAM),
    ]


class MONITORINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.ULONG), ("rcMonitor", RECT), ("rcWork", RECT), ("dwFlags", wintypes.DWORD)]


class MARGINS(ctypes.Structure):
    _fields_ = [
        ("cxLeftWidth", wintypes.INT),
        ("cxRightWidth", wintypes.INT),
        ("cyTopHeight", wintypes.INT),
        ("cyBottomHeight", wintypes.INT),
    ]


class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("dwAccentState", wintypes.DWORD),
        ("dwAccentFlags", wintypes.DWORD),
        ("dwGradientColor", wintypes.DWORD),
        ("dwAnimationId", wintypes.DWORD),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attrib", wintypes.DWORD),
        ("pvData", ctypes.POINTER(ACCENT_POLICY)),
        ("cbData", wintypes.UINT),
    ]


# DLLs
user32 = ctypes.windll.user32
shell32 = ctypes.windll.shell32
dwmapi = ctypes.windll.dwmapi


def is_greater_equal_win8_1():
    """determine if the windows version ≥ Win8.1"""
    cv = QOperatingSystemVersion.current()
    cv = QVersionNumber(cv.majorVersion(), cv.minorVersion(), cv.microVersion())
    return cv >= QVersionNumber(8, 1, 0)


def is_greater_equal_win10():
    """determine if the windows version ≥ Win10"""
    cv = QOperatingSystemVersion.current()
    return cv.majorVersion() >= 10


def is_greater_equal_win11():
    """determine if the windows version ≥ Win11"""
    return is_greater_equal_win10() and sys.getwindowsversion().build >= 22000


def is_maximized(hwnd):
    return user32.IsZoomed(hwnd)


def is_composition_enabled() -> bool:
    result = ctypes.c_int(0)
    dwmapi.DwmIsCompositionEnabled(ctypes.byref(result))
    return bool(result.value)


def get_monitor_info(hwnd):
    monitor = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
    info = MONITORINFO()
    info.cbSize = ctypes.sizeof(MONITORINFO)
    user32.GetMonitorInfoW(monitor, ctypes.byref(info))
    return info


def get_resize_border_thickness(hwnd, horizontal=True, window=None):
    frame = SM_CXSIZEFRAME if horizontal else SM_CYSIZEFRAME
    result = user32.GetSystemMetrics(frame) + user32.GetSystemMetrics(SM_CXPADDEDBORDER)
    if result > 0:
        return result

    thickness = 8 if is_composition_enabled() else 4
    if window:
        return round(thickness * window.devicePixelRatio())
    return thickness


def set_window_attribute(hwnd: int, attribute: str, value: bool) -> bool:
    def effect_bug_workaround(hwnd: int):
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        user32.MoveWindow(hwnd, rect.left, rect.top, 1, 1, False)
        user32.MoveWindow(hwnd, rect.right - 1, rect.bottom - 1, 1, 1, False)
        user32.MoveWindow(hwnd, rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top, False)

    def extend_margins(hwnd: int, value: bool):
        margins = MARGINS(65536, 0, 0, 0) if value else MARGINS(0, 0, 0, 0)
        dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))

    if hwnd == 0:
        return False
    try:
        if attribute == "dark-mode":
            dark_mode = wintypes.BOOL(1 if value else 0)
            size = ctypes.sizeof(wintypes.BOOL)
            result = dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWINDOWATTRIBUTE.DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(dark_mode), size
            )
            return result == 0

        elif attribute == "dwm-blur":
            if value:
                accent_policy = ACCENT_POLICY()
                accent_policy.dwAccentState = ACCENT_STATE.ACCENT_ENABLE_BLURBEHIND
                accent_policy.dwAccentFlags = ACCENT_FLAGS.ACCENT_NONE
                window_composition_attr_data = WINDOWCOMPOSITIONATTRIBDATA()
                window_composition_attr_data.Attrib = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY
                window_composition_attr_data.pvData = ctypes.pointer(accent_policy)
                window_composition_attr_data.cbData = ctypes.sizeof(accent_policy)
                result = user32.SetWindowCompositionAttribute(hwnd, ctypes.pointer(window_composition_attr_data))
                return bool(result)
            else:
                accent_policy = ACCENT_POLICY()
                accent_policy.dwAccentState = ACCENT_STATE.ACCENT_DISABLED
                accent_policy.dwAccentFlags = ACCENT_FLAGS.ACCENT_NONE
                window_composition_attr_data = WINDOWCOMPOSITIONATTRIBDATA()
                window_composition_attr_data.Attrib = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY
                window_composition_attr_data.pvData = ctypes.pointer(accent_policy)
                window_composition_attr_data.cbData = ctypes.sizeof(accent_policy)
                result = user32.SetWindowCompositionAttribute(hwnd, ctypes.pointer(window_composition_attr_data))
                return bool(result)

        elif attribute == "acrylic-material":
            if value:
                extend_margins(hwnd, True)
            backdrop_type = (
                wintypes.DWORD(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_TRANSIENTWINDOW)
                if value
                else wintypes.DWORD(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_AUTO)
            )
            size = ctypes.sizeof(wintypes.DWORD)
            result = dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWINDOWATTRIBUTE.DWMWA_SYSTEMBACKDROP_TYPE,
                ctypes.byref(backdrop_type),
                size,
            )
            if not value:
                extend_margins(hwnd, False)
            effect_bug_workaround(hwnd)
            return result == 0

        elif attribute == "mica":
            if value:
                extend_margins(hwnd, True)
            backdrop_type = (
                wintypes.DWORD(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_MAINWINDOW)
                if value
                else wintypes.DWORD(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_AUTO)
            )
            size = ctypes.sizeof(wintypes.DWORD)
            result = dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWINDOWATTRIBUTE.DWMWA_SYSTEMBACKDROP_TYPE,
                ctypes.byref(backdrop_type),
                size,
            )
            if not value:
                extend_margins(hwnd, False)
            """
            enabled = wintypes.BOOL(1 if value else 0)
            size = ctypes.sizeof(wintypes.BOOL)
            result = dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_MICA_EFFECT,
                ctypes.byref(enabled), 
                size
            )
            """
            effect_bug_workaround(hwnd)
            return result == 0

        elif attribute == "mica-alt":
            if value:
                extend_margins(hwnd, True)
            backdrop_type = (
                wintypes.DWORD(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_TABBEDWINDOW)
                if value
                else wintypes.DWORD(DWM_SYSTEMBACKDROP_TYPE.DWMSBT_AUTO)
            )
            size = ctypes.sizeof(wintypes.DWORD)
            result = dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWINDOWATTRIBUTE.DWMWA_SYSTEMBACKDROP_TYPE,
                ctypes.byref(backdrop_type),
                size,
            )
            if not value:
                extend_margins(hwnd, False)
            effect_bug_workaround(hwnd)
            return result == 0

        return False

    except Exception as e:
        logger.error(f"Error setting window attribute: {e}")
        return False


class HusWinEventFilter(QAbstractNativeEventFilter):
    def __init__(self):
        super().__init__()
        self.windows = {}  # hwnd -> QWindow
        self.contexts = {}  # hwnd -> {'title_bar': item, 'hit_test_items': set(items)}
        self.resize_border = 8

    def add_window(self, window: QWindow):
        window.visibleChanged.connect(lambda visible: self._on_visible_changed(window, visible))
        if window.isVisible():
            self._init_window(window)

    def _on_visible_changed(self, window, visible):
        if visible:
            hwnd = int(window.winId())
            if hwnd not in self.windows:
                self._init_window(window)
            else:
                self._setup_window(hwnd)

    def _init_window(self, window: QWindow):
        hwnd = int(window.winId())
        self.windows[hwnd] = window
        if hwnd not in self.contexts:
            self.contexts[hwnd] = {"title_bar": None, "hit_test_items": set()}
        self._setup_window(hwnd)

    def remove_window(self, window: QWindow):
        hwnd = int(window.winId())
        if hwnd in self.windows:
            del self.windows[hwnd]
        if hwnd in self.contexts:
            del self.contexts[hwnd]

    def update_context(self, window: QWindow, title_bar=None, hit_test_items=None):
        hwnd = int(window.winId())
        if hwnd not in self.contexts:
            self.contexts[hwnd] = {"title_bar": None, "hit_test_items": set()}

        if title_bar is not None:
            self.contexts[hwnd]["title_bar"] = title_bar
        if hit_test_items is not None:
            self.contexts[hwnd]["hit_test_items"] = hit_test_items

    def _setup_window(self, hwnd):
        style = user32.GetWindowLongPtrW(hwnd, GWL_STYLE)
        style |= WS_CAPTION | WS_THICKFRAME | WS_MAXIMIZEBOX | WS_MINIMIZEBOX | WS_SYSMENU
        user32.SetWindowLongPtrW(hwnd, GWL_STYLE, style)
        user32.SetWindowPos(
            hwnd, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_FRAMECHANGED | SWP_NOZORDER | SWP_NOOWNERZORDER
        )

        # Enable Shadow and Rounded Corners
        ncrp = ctypes.c_int(DWMNCRENDERINGPOLICY.DWMNCRP_ENABLED)
        dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY, ctypes.byref(ncrp), ctypes.sizeof(ncrp)
        )

        corner_preference = ctypes.c_int(DWM_WINDOW_CORNER_PREFERENCE.DWMWCP_ROUND)
        dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWINDOWATTRIBUTE.DWMWA_WINDOW_CORNER_PREFERENCE,
            ctypes.byref(corner_preference),
            ctypes.sizeof(corner_preference),
        )

        # Extend frame into client area to show shadow
        margins = MARGINS(0, 0, 1, 0)  # 1 pixel at top is enough to trigger shadow
        dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))

    def nativeEventFilter(self, eventType, message):
        if eventType != b"windows_generic_MSG":
            return False, 0

        msg_ptr = int(message)
        try:
            msg = MSG.from_address(msg_ptr)
        except Exception:
            return False, 0

        hwnd = msg.hwnd
        message_id = msg.message
        wParam = msg.wParam
        lParam = msg.lParam

        if hwnd not in self.windows:
            return False, 0

        window = self.windows[hwnd]

        if message_id == WM_NCCALCSIZE:
            if wParam:
                params = ctypes.cast(lParam, ctypes.POINTER(NCCALCSIZE_PARAMS)).contents
                if is_maximized(hwnd):
                    ty = get_resize_border_thickness(hwnd, False, window)
                    params.rgrc[0].top += ty
                    params.rgrc[0].bottom -= ty
                    tx = get_resize_border_thickness(hwnd, True, window)
                    params.rgrc[0].left += tx
                    params.rgrc[0].right -= tx

                    abd = APPBARDATA()
                    abd.cbSize = ctypes.sizeof(APPBARDATA)
                    state = shell32.SHAppBarMessage(ABM_GETSTATE, ctypes.byref(abd))
                    if state & ABS_AUTOHIDE:
                        edge = -1
                        abd2 = APPBARDATA()
                        abd2.cbSize = ctypes.sizeof(APPBARDATA)
                        abd2.hWnd = user32.FindWindowW("Shell_TrayWnd", None)
                        if abd2.hWnd:
                            window_monitor = user32.MonitorFromWindow(hwnd, MONITOR_DEFAULTTONEAREST)
                            taskbar_monitor = user32.MonitorFromWindow(abd2.hWnd, MONITOR_DEFAULTTOPRIMARY)
                            if window_monitor == taskbar_monitor:
                                shell32.SHAppBarMessage(ABM_GETTASKBARPOS, ctypes.byref(abd2))
                                edge = abd2.uEdge
                        if edge == 1:
                            params.rgrc[0].top += 1
                        elif edge == 3:
                            params.rgrc[0].bottom -= 1
                        elif edge == 0:
                            params.rgrc[0].left += 1
                        elif edge == 2:
                            params.rgrc[0].right -= 1
                        else:
                            params.rgrc[0].bottom -= 1
                else:
                    # For normal window, we need to adjust bottom by 1 pixel if we extended frame into client area
                    # But usually returning 0 is enough if we handle painting correctly.
                    # However, to ensure shadow is drawn, we might need to be careful.
                    # Actually, for standard frameless window with shadow,
                    # we just return 0 (handled by returning True, 0 below)
                    pass

                return True, 0

        if message_id == WM_NCHITTEST:
            x = ctypes.c_short(lParam & 0xFFFF).value
            y = ctypes.c_short((lParam >> 16) & 0xFFFF).value

            rect = RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))

            border = self.resize_border

            # Resize borders (Use physical coordinates)
            if x >= rect.left and x < rect.left + border:
                if y >= rect.top and y < rect.top + border:
                    return True, HTTOPLEFT
                if y >= rect.bottom - border and y < rect.bottom:
                    return True, HTBOTTOMLEFT
                return True, HTLEFT
            if x >= rect.right - border and x < rect.right:
                if y >= rect.top and y < rect.top + border:
                    return True, HTTOPRIGHT
                if y >= rect.bottom - border and y < rect.bottom:
                    return True, HTBOTTOMRIGHT
                return True, HTRIGHT
            if y >= rect.top and y < rect.top + border:
                return True, HTTOP
            if y >= rect.bottom - border and y < rect.bottom:
                return True, HTBOTTOM

            # Title Bar and Hit Test Items (Use logical coordinates for Qt items)
            context = self.contexts.get(hwnd)
            if context:
                # Use QCursor.pos() to get logical coordinates compatible with Qt's mapFromGlobal
                qt_cursor_pos = QCursor.pos()

                # Check excluded items first (buttons)
                for item in context["hit_test_items"]:
                    if item and item.isVisible():
                        local_pt = item.mapFromGlobal(qt_cursor_pos)
                        if item.contains(local_pt):
                            return False, 0  # HTCLIENT

                # Check Title Bar
                title_bar = context["title_bar"]
                if title_bar and title_bar.isVisible():
                    local_pt = title_bar.mapFromGlobal(qt_cursor_pos)
                    if title_bar.contains(local_pt):
                        return True, HTCAPTION

            return False, 0

        if message_id == WM_GETMINMAXINFO:
            mmi = ctypes.cast(lParam, ctypes.POINTER(MINMAXINFO)).contents
            monitor_info = get_monitor_info(hwnd)
            work_area = monitor_info.rcWork
            monitor_area = monitor_info.rcMonitor
            mmi.ptMaxPosition.x = work_area.left - monitor_area.left
            mmi.ptMaxPosition.y = work_area.top - monitor_area.top
            mmi.ptMaxSize.x = work_area.right - work_area.left
            mmi.ptMaxSize.y = work_area.bottom - work_area.top
            dp_ratio = window.devicePixelRatio()
            min_w = int(window.minimumWidth() * dp_ratio)
            min_h = int(window.minimumHeight() * dp_ratio)
            max_w = int(window.maximumWidth() * dp_ratio)
            max_h = int(window.maximumHeight() * dp_ratio)
            if max_w == 0:
                max_w = mmi.ptMaxSize.x
            if max_h == 0:
                max_h = mmi.ptMaxSize.y
            mmi.ptMinTrackSize.x = min_w
            mmi.ptMinTrackSize.y = min_h
            mmi.ptMaxTrackSize.x = max_w
            mmi.ptMaxTrackSize.y = max_h
            return True, 0

        return False, 0


_native_event_filter = None


def install_filter(app):
    global _native_event_filter
    if _native_event_filter is None:
        _native_event_filter = HusWinEventFilter()
        app.installNativeEventFilter(_native_event_filter)
    return _native_event_filter


def ReleaseCapture():
    return user32.ReleaseCapture()


def SendMessage(hwnd, msg, wparam, lparam):
    return user32.SendMessageW(hwnd, msg, wparam, lparam)
