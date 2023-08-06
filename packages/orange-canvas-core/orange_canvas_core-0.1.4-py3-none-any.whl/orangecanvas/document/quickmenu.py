"""
==========
Quick Menu
==========

A :class:`QuickMenu` widget provides lists of actions organized in tabs
with a quick search functionality.

"""
import typing
import statistics
import sys
import logging

from collections import namedtuple

from typing import Optional, Any, List, Callable

from AnyQt.QtWidgets import (
    QWidget, QFrame, QToolButton, QAbstractButton, QAction, QTreeView,
    QButtonGroup, QStackedWidget, QHBoxLayout, QVBoxLayout, QSizePolicy,
    QStyleOptionToolButton, QStylePainter, QStyle, QApplication,
    QStyledItemDelegate, QStyleOptionViewItem, QSizeGrip,
    QAbstractItemView
)
from AnyQt.QtGui import (
    QIcon, QStandardItemModel, QPolygon, QRegion, QBrush, QPalette,
    QPaintEvent
)
from AnyQt.QtCore import (
    Qt, QObject, QPoint, QSize, QRect, QEventLoop, QEvent, QModelIndex,
    QTimer, QRegExp, QSortFilterProxyModel, QItemSelectionModel,
    QAbstractItemModel
)
from AnyQt.QtCore import pyqtSignal as Signal, pyqtProperty as Property

from .usagestatistics import UsageStatistics
from ..gui.framelesswindow import FramelessWindow
from ..gui.lineedit import LineEdit
from ..gui.tooltree import ToolTree, FlattenedTreeItemModel
from ..gui.utils import StyledWidget_paintEvent, create_css_gradient
from ..registry.qt import QtWidgetRegistry

from ..resources import icon_loader

log = logging.getLogger(__name__)


class _MenuItemDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        # type: (QStyleOptionViewItem, QModelIndex) -> QSize
        option = QStyleOptionViewItem(option)
        self.initStyleOption(option, index)
        size = super().sizeHint(option, index)

        # TODO: get the default QMenu item height from the current style.
        size.setHeight(max(size.height(), 25))
        return size


class MenuPage(ToolTree):
    """
    A menu page in a :class:`QuickMenu` widget, showing a list of actions.
    Shown actions can be disabled by setting a filtering function using the
    :func:`setFilterFunc`.

    """
    def __init__(self, parent=None, title="", icon=QIcon(), **kwargs):
        # type: (Optional[QWidget], str, QIcon, Any) -> None
        super().__init__(parent, **kwargs)

        self.__title = title
        self.__icon = QIcon(icon)
        self.__sizeHint = None  # type: Optional[QSize]

        self.view().setItemDelegate(_MenuItemDelegate(self.view()))
        self.view().entered.connect(self.__onEntered)
        self.view().viewport().setMouseTracking(True)

        # Make sure the initial model is wrapped in a ItemDisableFilter.
        self.setModel(self.model())

    def setTitle(self, title):
        # type: (str) -> None
        """
        Set the title of the page.
        """
        if self.__title != title:
            self.__title = title
            self.update()

    def title(self):
        # type: () -> str
        """
        Return the title of this page.
        """
        return self.__title

    title_ = Property(str, fget=title, fset=setTitle, doc="Title of the page.")

    def setIcon(self, icon):  # type: (QIcon) -> None
        """
        Set icon for this menu page.
        """
        if self.__icon != icon:
            self.__icon = icon
            self.update()

    def icon(self):  # type: () -> QIcon
        """
        Return the icon of this menu page.
        """
        return QIcon(self.__icon)

    icon_ = Property(QIcon, fget=icon, fset=setIcon,
                     doc="Page icon")

    def setFilterFunc(self, func):
        # type: (Optional[Callable[[QModelIndex], bool]]) -> None
        """
        Set the filtering function. `func` should a function taking a single
        :class:`QModelIndex` argument and returning True if the item at index
        should be disabled and False otherwise. To disable filtering `func` can
        be set to ``None``.

        """
        proxyModel = self.view().model()
        proxyModel.setFilterFunc(func)

    def setModel(self, model):
        # type: (QAbstractItemModel) -> None
        """
        Reimplemented from :func:`ToolTree.setModel`.
        """
        proxyModel = ItemDisableFilter(self)
        proxyModel.setSourceModel(model)
        super().setModel(proxyModel)

        self.__invalidateSizeHint()

    def setRootIndex(self, index):
        # type: (QModelIndex) -> None
        """
        Reimplemented from :func:`ToolTree.setRootIndex`
        """
        proxyModel = self.view().model()
        mappedIndex = proxyModel.mapFromSource(index)
        super().setRootIndex(mappedIndex)

        self.__invalidateSizeHint()

    def rootIndex(self):
        # type: () -> QModelIndex
        """
        Reimplemented from :func:`ToolTree.rootIndex`
        """
        proxyModel = self.view().model()
        return proxyModel.mapToSource(super().rootIndex())

    def sizeHint(self):
        # type: () -> QSize
        """
        Reimplemented from :func:`QWidget.sizeHint`.
        """
        if self.__sizeHint is None:
            view = self.view()
            model = view.model()

            # This will not work for nested items (tree).
            count = model.rowCount(view.rootIndex())

            # 'sizeHintForColumn' is the reason for size hint caching
            # since it must traverse all items in the column.
            width = view.sizeHintForColumn(0)

            if count:
                height = view.sizeHintForRow(0)
                height = height * count
            else:
                height = 0
            self.__sizeHint = QSize(width, height)

        return self.__sizeHint

    def __invalidateSizeHint(self):  # type: () -> None
        self.__sizeHint = None
        self.updateGeometry()

    def __onEntered(self, index):  # type: (QModelIndex) -> None
        if not index.isValid():
            return

        if self.view().state() != QTreeView.NoState:
            # The item view can emit an 'entered' signal while the model/view
            # is being changed (rows removed). When this happens, setting the
            # current item can segfault (in QTreeView::scrollTo).
            return

        if index.flags() & Qt.ItemIsEnabled:
            self.view().selectionModel().setCurrentIndex(
                index,
                QItemSelectionModel.ClearAndSelect
            )


if typing.TYPE_CHECKING:
    FilterFunc = Callable[[QModelIndex], bool]


class ItemDisableFilter(QSortFilterProxyModel):
    """
    An filter proxy model used to disable selected items based on
    a filtering function.

    """
    def __init__(self, parent=None, **kwargs):
        # type: (Optional[QObject], Any) -> None
        super().__init__(parent, **kwargs)
        self.__filterFunc = None  # type: Optional[FilterFunc]

    def setFilterFunc(self, func):
        # type: (Optional[FilterFunc]) -> None
        """
        Set the filtering function.
        """
        if not (callable(func) or func is None):
            raise TypeError("A callable object or None expected.")

        if self.__filterFunc != func:
            self.__filterFunc = func
            # Mark the whole model as changed.
            self.dataChanged.emit(self.index(0, 0),
                                  self.index(self.rowCount(), 0))

    def flags(self, index):
        # type: (QModelIndex) -> Qt.ItemFlags
        """
        Reimplemented from :class:`QSortFilterProxyModel.flags`
        """
        source = self.mapToSource(index)
        flags = source.flags()

        if self.__filterFunc is not None:
            enabled = flags & Qt.ItemIsEnabled
            if enabled and not self.__filterFunc(source):
                flags = Qt.ItemFlags(flags ^ Qt.ItemIsEnabled)

        return flags


class SuggestMenuPage(MenuPage):
    """
    A MenuMage for the QuickMenu widget supporting item filtering
    (searching).

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setModel(self, model):
        # type: (QAbstractItemModel) -> None
        """
        Reimplemented from :ref:`MenuPage.setModel`.
        """
        flat = FlattenedTreeItemModel(self)
        flat.setSourceModel(model)
        flat.setFlatteningMode(flat.InternalNodesDisabled)
        flat.setFlatteningMode(flat.LeavesOnly)
        proxy = SortFilterProxyModel(self)
        proxy.setFilterCaseSensitivity(Qt.CaseSensitive)
        proxy.setSourceModel(flat)
        # bypass MenuPage.setModel and its own proxy
        # TODO: store my self.__proxy
        ToolTree.setModel(self, proxy)
        self.ensureCurrent()

    def __proxy(self):
        # type: () -> SortFilterProxyModel
        model = self.view().model()
        assert isinstance(model, SortFilterProxyModel)
        assert model.parent() is self
        return model

    def setFilterFixedString(self, pattern):
        # type: (str) -> None
        """
        Set the fixed string filtering pattern. Only items which contain the
        `pattern` string will be shown.
        """
        proxy = self.__proxy()
        proxy.setFilterFixedString(pattern)
        self.ensureCurrent()

    def setFilterRegExp(self, pattern):
        # type: (QRegExp) -> None
        """
        Set the regular expression filtering pattern. Only items matching
        the `pattern` expression will be shown.
        """
        filter_proxy = self.__proxy()
        filter_proxy.setFilterRegExp(pattern)

        # re-sorts to make sure items that match by title are on top
        filter_proxy.invalidate()
        filter_proxy.sort(0)

        self.ensureCurrent()

    def setFilterWildCard(self, pattern):
        # type: (str) -> None
        """
        Set a wildcard filtering pattern.
        """
        filter_proxy = self.__proxy()
        filter_proxy.setFilterWildCard(pattern)
        self.ensureCurrent()

    def setFilterFunc(self, func):
        # type: (Optional[FilterFunc]) -> None
        """
        Set a filtering function.
        """
        filter_proxy = self.__proxy()
        filter_proxy.setFilterFunc(func)

    def setSortingFunc(self, func):
        # type: (Callable[[Any, Any], bool]) -> None
        """
        Set a sorting function.
        """
        filter_proxy = self.__proxy()
        filter_proxy.setSortingFunc(func)


class SortFilterProxyModel(QSortFilterProxyModel):
    """
    An filter proxy model used to sort and filter items based on
    a sort and filtering function.

    """
    def __init__(self, parent=None):
        # type: (Optional[QObject]) -> None
        super().__init__(parent)

        self.__filterFunc = None  # type: Optional[FilterFunc]
        self.__sortingFunc = None

    def setFilterFunc(self, func):
        # type: (Optional[FilterFunc]) -> None
        """
        Set the filtering function.
        """
        if not (func is None or callable(func)):
            raise ValueError("A callable object or None expected.")

        if self.__filterFunc is not func:
            self.__filterFunc = func
            self.invalidateFilter()

    def filterFunc(self):
        # type: () -> Optional[FilterFunc]
        return self.__filterFunc

    def filterAcceptsRow(self, row, parent=QModelIndex()):
        # type: (int, QModelIndex) -> bool
        flat_model = self.sourceModel()
        index = flat_model.index(row, self.filterKeyColumn(), parent)
        description = flat_model.data(index, role=QtWidgetRegistry.WIDGET_DESC_ROLE)
        if description is None:
            return False

        name = description.name
        keywords = description.keywords or []

        # match name and keywords
        accepted = False
        for keyword in [name] + keywords:
            if self.filterRegExp().indexIn(keyword) > -1:
                accepted = True
                break

        # if matches query, apply filter function (compatibility with paired widget)
        if accepted and self.__filterFunc is not None:
            model = self.sourceModel()
            index = model.index(row, self.filterKeyColumn(), parent)
            return self.__filterFunc(index)
        else:
            return accepted

    def setSortingFunc(self, func):
        # type: (Callable[[Any, Any], bool]) -> None
        self.__sortingFunc = func
        self.invalidate()
        self.sort(0)

    def sortingFunc(self):
        return self.__sortingFunc

    def lessThan(self, left, right):
        # type: (QModelIndex, QModelIndex) -> bool
        if self.__sortingFunc is None:
            return super().lessThan(left, right)
        model = self.sourceModel()
        left_data = model.data(left)
        right_data = model.data(right)

        flat_model = self.sourceModel()
        left_description = flat_model.data(left, role=QtWidgetRegistry.WIDGET_DESC_ROLE)
        right_description = flat_model.data(right, role=QtWidgetRegistry.WIDGET_DESC_ROLE)

        left_matches_title = self.filterRegExp().indexIn(left_description.name) > -1
        right_matches_title = self.filterRegExp().indexIn(right_description.name) > -1

        if left_matches_title != right_matches_title:
            return left_matches_title
        return self.__sortingFunc(left_data, right_data)


class SearchWidget(LineEdit):
    def __init__(self, parent=None, **kwargs):
        # type: (Optional[QWidget], Any) -> None
        super().__init__(parent, **kwargs)
        self.__setupUi()

    def __setupUi(self):
        icon = icon_loader().get("icons/Search.svg")
        action = QAction(icon, "Search", self)
        self.setAction(action, LineEdit.LeftPosition)


class MenuStackWidget(QStackedWidget):
    """
    Stack widget for the menu pages.
    """

    def sizeHint(self):
        # type: () -> QSize
        """
        Size hint is the maximum width and median height of the widgets
        contained in the stack.
        """
        default_size = QSize(200, 400)
        widget_hints = [default_size]
        for i in range(self.count()):
            hint = self.widget(i).sizeHint()
            widget_hints.append(hint)

        width = max([s.width() for s in widget_hints])

        if widget_hints:
            # Take the median for the height
            height = statistics.median([s.height() for s in widget_hints])
        else:
            height = default_size.height()
        return QSize(width, int(height))

    def __sizeHintForTreeView(self, view):
        # type: (QTreeView) -> QSize
        hint = view.sizeHint()
        model = view.model()

        count = model.rowCount()
        width = view.sizeHintForColumn(0)

        if count:
            height = view.sizeHintForRow(0)
            height = height * count
        else:
            height = hint.height()

        return QSize(max(width, hint.width()), max(height, hint.height()))


class TabButton(QToolButton):
    def __init__(self, parent=None, **kwargs):
        # type: (Optional[QWidget], Any) -> None
        super().__init__(parent, **kwargs)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.setCheckable(True)

        self.__flat = True
        self.__showMenuIndicator = False

    def setFlat(self, flat):
        # type: (bool) -> None
        if self.__flat != flat:
            self.__flat = flat
            self.update()

    def flat(self):
        # type: () -> bool
        return self.__flat

    flat_ = Property(bool, fget=flat, fset=setFlat,
                     designable=True)

    def setShownMenuIndicator(self, show):
        # type: (bool) -> None
        if self.__showMenuIndicator != show:
            self.__showMenuIndicator = show
            self.update()

    def showMenuIndicator(self):
        # type: () -> bool
        return self.__showMenuIndicator

    showMenuIndicator_ = Property(bool, fget=showMenuIndicator,
                                  fset=setShownMenuIndicator,
                                  designable=True)

    def paintEvent(self, event):
        # type: (QPaintEvent) -> None
        opt = QStyleOptionToolButton()
        self.initStyleOption(opt)
        if self.__showMenuIndicator and self.isChecked():
            opt.features |= QStyleOptionToolButton.HasMenu
        if self.__flat:
            # Use default widget background/border styling.
            StyledWidget_paintEvent(self, event)

            p = QStylePainter(self)
            p.drawControl(QStyle.CE_ToolButtonLabel, opt)
        else:
            p = QStylePainter(self)
            p.drawComplexControl(QStyle.CC_ToolButton, opt)

    def sizeHint(self):
        # type: () -> QSize
        opt = QStyleOptionToolButton()
        self.initStyleOption(opt)
        if self.__showMenuIndicator and self.isChecked():
            opt.features |= QStyleOptionToolButton.HasMenu
        style = self.style()

        hint = style.sizeFromContents(QStyle.CT_ToolButton, opt,
                                      opt.iconSize, self)
        return hint


_Tab = namedtuple(
    "_Tab",
    ["text",
     "icon",
     "toolTip",
     "button",
     "data",
     "palette"]
)


class TabBarWidget(QWidget):
    """
    A vertical tab bar widget using tool buttons as for tabs.
    """

    currentChanged = Signal(int)

    def __init__(self, parent=None, **kwargs):
        # type: (Optional[QWidget], Any) -> None
        super().__init__(parent, **kwargs)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.setSizePolicy(QSizePolicy.Fixed,
                           QSizePolicy.Expanding)
        self.__tabs = []  # type: List[_Tab]

        self.__currentIndex = -1
        self.__changeOnHover = False

        self.__iconSize = QSize(26, 26)

        self.__group = QButtonGroup(self, exclusive=True)
        self.__group.buttonPressed[QAbstractButton].connect(
            self.__onButtonPressed
        )
        self.setMouseTracking(True)

        self.__sloppyButton = None  # type: Optional[QAbstractButton]
        self.__sloppyRegion = QRegion()
        self.__sloppyTimer = QTimer(self, singleShot=True)
        self.__sloppyTimer.timeout.connect(self.__onSloppyTimeout)

    def setChangeOnHover(self, changeOnHover):
        #  type: (bool) -> None
        """
        If set to ``True`` the tab widget will change the current index when
        the mouse hovers over a tab button.
        """
        if self.__changeOnHover != changeOnHover:
            self.__changeOnHover = changeOnHover

    def changeOnHover(self):
        # type: () -> bool
        """
        Does the current tab index follow the mouse cursor.
        """
        return self.__changeOnHover

    def count(self):
        # type: () -> int
        """
        Return the number of tabs in the widget.
        """
        return len(self.__tabs)

    def addTab(self, text, icon=QIcon(), toolTip=""):
        # type: (str, QIcon, str) -> int
        """
        Add a new tab and return it's index.
        """
        return self.insertTab(self.count(), text, icon, toolTip)

    def insertTab(self, index, text, icon=QIcon(), toolTip=""):
        # type: (int, str, QIcon, str) -> int
        """
        Insert a tab at `index`
        """
        button = TabButton(self, objectName="tab-button")
        button.setSizePolicy(QSizePolicy.Expanding,
                             QSizePolicy.Expanding)
        button.setIconSize(self.__iconSize)
        button.setMouseTracking(True)

        self.__group.addButton(button)

        button.installEventFilter(self)

        tab = _Tab(text, icon, toolTip, button, None, None)
        self.layout().insertWidget(index, button)

        self.__tabs.insert(index, tab)
        self.__updateTab(index)

        if self.currentIndex() == -1:
            self.setCurrentIndex(0)
        return index

    def removeTab(self, index):
        # type: (int) -> None
        """
        Remove a tab at `index`.
        """
        if 0 <= index < self.count():
            tab = self.__tabs.pop(index)
            layout_index = self.layout().indexOf(tab.button)
            if layout_index != -1:
                self.layout().takeAt(layout_index)

            self.__group.removeButton(tab.button)

            tab.button.removeEventFilter(self)

            if tab.button is self.__sloppyButton:
                self.__sloppyButton = None
                self.__sloppyRegion = QRegion()

            tab.button.deleteLater()
            tab.button.setParent(None)

            if self.currentIndex() == index:
                if self.count():
                    self.setCurrentIndex(max(index - 1, 0))
                else:
                    self.setCurrentIndex(-1)

    def setTabIcon(self, index, icon):
        # type: (int, QIcon) -> None
        """
        Set the `icon` for tab at `index`.
        """
        self.__tabs[index] = self.__tabs[index]._replace(icon=QIcon(icon))
        self.__updateTab(index)

    def setTabToolTip(self, index, toolTip):
        # type: (int, str) -> None
        """
        Set `toolTip` for tab at `index`.
        """
        self.__tabs[index] = self.__tabs[index]._replace(toolTip=toolTip)
        self.__updateTab(index)

    def setTabText(self, index, text):
        # type: (int, str) -> None
        """
        Set tab `text` for tab at `index`
        """
        self.__tabs[index] = self.__tabs[index]._replace(text=text)
        self.__updateTab(index)

    def setTabPalette(self, index, palette):
        # type: (int, QPalette) -> None
        """
        Set the tab button palette.
        """
        self.__tabs[index] = self.__tabs[index]._replace(palette=QPalette(palette))
        self.__updateTab(index)

    def setCurrentIndex(self, index):
        # type: (int) -> None
        """
        Set the current tab index.
        """
        if self.__currentIndex != index:
            self.__currentIndex = index

            self.__sloppyRegion = QRegion()
            self.__sloppyButton = None

            if index != -1:
                self.__tabs[index].button.setChecked(True)

            self.currentChanged.emit(index)

    def currentIndex(self):
        # type: () -> int
        """
        Return the current index.
        """
        return self.__currentIndex

    def button(self, index):
        # type: (int) -> QAbstractButton
        """
        Return the `TabButton` instance for index.
        """
        return self.__tabs[index].button

    def setIconSize(self, size):
        # type: (QSize) -> None
        if self.__iconSize != size:
            self.__iconSize = QSize(size)
            for tab in self.__tabs:
                tab.button.setIconSize(self.__iconSize)

    def __updateTab(self, index):
        # type: (int) -> None
        """
        Update the tab button.
        """
        tab = self.__tabs[index]
        b = tab.button

        if tab.text:
            b.setText(tab.text)

        if tab.icon is not None and not tab.icon.isNull():
            b.setIcon(tab.icon)

        if tab.palette:
            b.setPalette(tab.palette)

    def __onButtonPressed(self, button):
        # type: (QAbstractButton) -> None
        for i, tab in enumerate(self.__tabs):
            if tab.button is button:
                self.setCurrentIndex(i)
                break

    def __calcSloppyRegion(self, current):
        # type: (QPoint) -> QRegion
        """
        Given a current mouse cursor position return a region of the widget
        where hover/move events should change the current tab only on a
        timeout.
        """
        p1 = current + QPoint(0, 2)
        p2 = current + QPoint(0, -2)
        p3 = self.pos() + QPoint(self.width()+10, 0)
        p4 = self.pos() + QPoint(self.width()+10, self.height())
        return QRegion(QPolygon([p1, p2, p3, p4]))

    def __setSloppyButton(self, button):
        # type: (QAbstractButton) -> None
        """
        Set the current sloppy button (a tab button inside sloppy region)
        and reset the sloppy timeout.
        """
        if not button.isChecked():
            self.__sloppyButton = button
            delay = self.style().styleHint(QStyle.SH_Menu_SubMenuPopupDelay, None)
            # The delay timeout is the same as used by Qt in the QMenu.
            self.__sloppyTimer.start(delay)
        else:
            self.__sloppyTimer.stop()

    def __onSloppyTimeout(self):
        # type: () -> None
        if self.__sloppyButton is not None:
            button = self.__sloppyButton
            self.__sloppyButton = None
            if not button.isChecked():
                index = [tab.button for tab in self.__tabs].index(button)
                self.setCurrentIndex(index)

    def eventFilter(self, receiver, event):
        if event.type() == QEvent.MouseMove and \
                isinstance(receiver, TabButton):
            pos = receiver.mapTo(self, event.pos())
            if self.__sloppyRegion.contains(pos):
                self.__setSloppyButton(receiver)
            else:
                if not receiver.isChecked():
                    index = [tab.button for tab in self.__tabs].index(receiver)
                    self.setCurrentIndex(index)
                #also update sloppy region if mouse is moved on the same icon
                self.__sloppyRegion = self.__calcSloppyRegion(pos)

        return super().eventFilter(receiver, event)

    def leaveEvent(self, event):
        self.__sloppyButton = None
        self.__sloppyRegion = QRegion()

        return super().leaveEvent(event)


class PagedMenu(QWidget):
    """
    Tabbed container for :class:`MenuPage` instances.
    """
    triggered = Signal(QAction)
    hovered = Signal(QAction)

    currentChanged = Signal(int)

    def __init__(self, parent=None, **kwargs):
        # type: (Optional[QWidget], Any) -> None
        super().__init__(parent, **kwargs)

        self.__currentIndex = -1

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.__tab = TabBarWidget(self)
        self.__tab.currentChanged.connect(self.setCurrentIndex)
        self.__tab.setChangeOnHover(True)

        self.__stack = MenuStackWidget(self)

        layout.addWidget(self.__tab, alignment=Qt.AlignTop)
        layout.addWidget(self.__stack)

        self.setLayout(layout)

    def addPage(self, page, title, icon=QIcon(), toolTip=""):
        # type: (QWidget, str, QIcon, str) -> int
        """
        Add a `page` to the menu and return its index.
        """
        return self.insertPage(self.count(), page, title, icon, toolTip)

    def insertPage(self, index, page, title, icon=QIcon(), toolTip=""):
        # type: (int, QWidget, str, QIcon, str) -> int
        """
        Insert `page` at `index`.
        """
        page.triggered.connect(self.triggered)
        page.hovered.connect(self.hovered)

        self.__stack.insertWidget(index, page)
        self.__tab.insertTab(index, title, icon, toolTip)
        return index

    def page(self, index):
        # type: (int) -> QWidget
        """
        Return the page at index.
        """
        return self.__stack.widget(index)

    def removePage(self, index):
        # type: (int) -> None
        """
        Remove the page at `index`.
        """
        page = self.__stack.widget(index)
        page.triggered.disconnect(self.triggered)
        page.hovered.disconnect(self.hovered)

        self.__stack.removeWidget(page)
        self.__tab.removeTab(index)

    def count(self):
        # type: () -> int
        """
        Return the number of pages.
        """
        return self.__stack.count()

    def setCurrentIndex(self, index):
        # type: (int) -> None
        """
        Set the current page index.
        """
        if self.__currentIndex != index:
            self.__currentIndex = index
            self.__tab.setCurrentIndex(index)
            self.__stack.setCurrentIndex(index)
            self.currentChanged.emit(index)

    def currentIndex(self):
        # type: () -> int
        """
        Return the index of the current page.
        """
        return self.__currentIndex

    def setCurrentPage(self, page):
        # type: (QWidget) -> None
        """
        Set `page` to be the current shown page.
        """
        index = self.__stack.indexOf(page)
        self.setCurrentIndex(index)

    def currentPage(self):
        # type: () -> QWidget
        """
        Return the current page.
        """
        return self.__stack.currentWidget()

    def indexOf(self, page):
        # type: (QWidget) -> int
        """
        Return the index of `page`.
        """
        return self.__stack.indexOf(page)

    def tabButton(self, index):
        # type: (int) -> QAbstractButton
        """
        Return the tab button instance for index.
        """
        return self.__tab.button(index)


def as_qbrush(value):
    # type: (Any) -> Optional[QBrush]
    if isinstance(value, QBrush):
        return value
    else:
        return None


TAB_BUTTON_STYLE_TEMPLATE = """\
TabButton {
    qproperty-flat_: false;
    background: %s;
    border: none;
    border-bottom: 1px solid palette(mid);
    border-right: 1px solid palette(mid);
}

TabButton:checked {
    background: %s;
    border: none;
    border-top: 1px solid #609ED7;
    border-bottom: 1px solid #609ED7;
    border-right: 1px solid #609ED7;
}
"""

# TODO: Cleanup the QuickMenu interface. It should not have a 'dual' public
# interface (i.e. as an item model view (`setModel` method) and `addPage`,
# ...)


class QuickMenu(FramelessWindow):
    """
    A quick menu popup for the widgets.

    The widgets are set using :func:`QuickMenu.setModel` which must be a
    model as returned by :func:`QtWidgetRegistry.model`

    """

    #: An action has been triggered in the menu.
    triggered = Signal(QAction)

    #: An action has been hovered in the menu
    hovered = Signal(QAction)

    def __init__(self, parent=None, **kwargs):
        # type: (Optional[QWidget], Any) -> None
        super().__init__(parent, **kwargs)
        self.setWindowFlags(Qt.Popup)

        self.__filterFunc = None  # type: Optional[FilterFunc]
        self.__sortingFunc = None  # type: Optional[Callable[[Any, Any], bool]]

        self.setLayout(QVBoxLayout(self))
        self.layout().setContentsMargins(6, 6, 6, 6)

        self.__search = SearchWidget(self, objectName="search-line")

        self.__search.setPlaceholderText(
            self.tr("Search for widget or select from the list.")
        )

        self.layout().addWidget(self.__search)

        self.__frame = QFrame(self, objectName="menu-frame")
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.__frame.setLayout(layout)

        self.layout().addWidget(self.__frame)

        self.__pages = PagedMenu(self, objectName="paged-menu")
        self.__pages.currentChanged.connect(self.setCurrentIndex)
        self.__pages.triggered.connect(self.triggered)
        self.__pages.hovered.connect(self.hovered)

        self.__frame.layout().addWidget(self.__pages)

        self.setSizePolicy(QSizePolicy.Fixed,
                           QSizePolicy.Expanding)

        self.__suggestPage = SuggestMenuPage(self, objectName="suggest-page")
        self.__suggestPage.setActionRole(QtWidgetRegistry.WIDGET_ACTION_ROLE)
        self.__suggestPage.setIcon(icon_loader().get("icons/Search.svg"))

        if sys.platform == "darwin":
            view = self.__suggestPage.view()
            view.verticalScrollBar().setAttribute(Qt.WA_MacMiniSize, True)
            # Don't show the focus frame because it expands into the tab bar.
            view.setAttribute(Qt.WA_MacShowFocusRect, False)

        i = self.addPage(self.tr("Quick Search"), self.__suggestPage)
        button = self.__pages.tabButton(i)
        button.setObjectName("search-tab-button")
        button.setStyleSheet(
            "TabButton {\n"
            "    qproperty-flat_: false;\n"
            "    border: none;"
            "}\n")

        self.__search.textEdited.connect(self.__on_textEdited)

        self.__navigator = ItemViewKeyNavigator(self)
        self.__navigator.setView(self.__suggestPage.view())
        self.__search.installEventFilter(self.__navigator)

        self.__grip = WindowSizeGrip(self)  # type: Optional[WindowSizeGrip]
        self.__grip.raise_()

        self.__loop = None   # type: Optional[QEventLoop]
        self.__model = None  # type: Optional[QAbstractItemModel]
        self.setModel(QStandardItemModel())
        self.__triggeredAction = None  # type: Optional[QAction]

    def setSizeGripEnabled(self, enabled):
        # type: (bool) -> None
        """
        Enable the resizing of the menu with a size grip in a bottom
        right corner (enabled by default).
        """
        if bool(enabled) != bool(self.__grip):
            if self.__grip:
                self.__grip.deleteLater()
                self.__grip = None
            else:
                self.__grip = WindowSizeGrip(self)
                self.__grip.raise_()

    def sizeGripEnabled(self):
        # type: () -> bool
        """
        Is the size grip enabled.
        """
        return bool(self.__grip)

    def addPage(self, name, page):
        # type: (str, MenuPage) -> int
        """
        Add the `page` (:class:`MenuPage`) with `name` and return it's index.
        The `page.icon()` will be used as the icon in the tab bar.
        """
        return self.insertPage(self.__pages.count(), name, page)

    def insertPage(self, index, name, page):
        # type: (int, str, MenuPage) -> int
        icon = page.icon()

        tip = name
        if page.toolTip():
            tip = page.toolTip()

        index = self.__pages.insertPage(index, page, name, icon, tip)

        # Route the page's signals
        page.triggered.connect(self.__onTriggered)
        page.hovered.connect(self.hovered)

        # Install event filter to intercept key presses.
        page.view().installEventFilter(self)

        return index

    def createPage(self, index):
        # type: (QModelIndex) -> MenuPage
        """
        Create a new page based on the contents of an index
        (:class:`QModeIndex`) item.
        """
        page = MenuPage(self)

        page.setModel(index.model())
        page.setRootIndex(index)

        view = page.view()

        if sys.platform == "darwin":
            view.verticalScrollBar().setAttribute(Qt.WA_MacMiniSize, True)
            # Don't show the focus frame because it expands into the tab
            # bar at the top.
            view.setAttribute(Qt.WA_MacShowFocusRect, False)

        name = str(index.data(Qt.DisplayRole))
        page.setTitle(name)

        icon = index.data(Qt.DecorationRole)
        if isinstance(icon, QIcon):
            page.setIcon(icon)

        page.setToolTip(index.data(Qt.ToolTipRole))
        return page

    def __clear(self):
        # type: () -> None
        for i in range(self.__pages.count() - 1, 0, -1):
            self.__pages.removePage(i)

    def setModel(self, model):
        # type: (QAbstractItemModel) -> None
        """
        Set the model containing the actions.
        """
        if self.__model is not None:
            self.__model.dataChanged.disconnect(self.__on_dataChanged)
            self.__model.rowsInserted.disconnect(self.__on_rowsInserted)
            self.__model.rowsRemoved.disconnect(self.__on_rowsRemoved)
            self.__clear()

        for i in range(model.rowCount()):
            index = model.index(i, 0)
            self.__insertPage(i + 1, index)

        self.__model = model
        self.__suggestPage.setModel(model)
        if model is not None:
            model.dataChanged.connect(self.__on_dataChanged)
            model.rowsInserted.connect(self.__on_rowsInserted)
            model.rowsRemoved.connect(self.__on_rowsRemoved)

    def __on_dataChanged(self, topLeft, bottomRight):
        # type: (QModelIndex, QModelIndex) -> None
        parent = topLeft.parent()
        # Only handle top level item (categories).
        if not parent.isValid():
            for row in range(topLeft.row(), bottomRight.row() + 1):
                index = topLeft.sibling(row, 0)
                # Note: the tab buttons are offest by 1 (to accommodate
                # the Suggest Page).
                button = self.__pages.tabButton(row + 1)
                brush = as_qbrush(index.data(QtWidgetRegistry.BACKGROUND_ROLE))
                if brush is not None:
                    base_color = brush.color()
                    button.setStyleSheet(
                        TAB_BUTTON_STYLE_TEMPLATE %
                        (create_css_gradient(base_color),
                         create_css_gradient(base_color.darker(120)))
                    )

    def __on_rowsInserted(self, parent, start, end):
        # type: (QModelIndex, int, int) -> None
        # Only handle top level item (categories).
        assert self.__model is not None
        if not parent.isValid():
            for row in range(start, end + 1):
                index = self.__model.index(row, 0)
                self.__insertPage(row + 1, index)

    def __on_rowsRemoved(self, parent, start, end):
        # type: (QModelIndex, int, int) -> None
        # Only handle top level item (categories).
        if not parent.isValid():
            for row in range(end, start - 1, -1):
                self.__removePage(row + 1)

    def __insertPage(self, row, index):
        # type: (int, QModelIndex) -> None
        page = self.createPage(index)
        page.setActionRole(QtWidgetRegistry.WIDGET_ACTION_ROLE)

        i = self.insertPage(row, page.title(), page)

        brush = as_qbrush(index.data(QtWidgetRegistry.BACKGROUND_ROLE))
        if brush is not None:
            base_color = brush.color()
            button = self.__pages.tabButton(i)
            button.setStyleSheet(
                TAB_BUTTON_STYLE_TEMPLATE %
                (create_css_gradient(base_color),
                 create_css_gradient(base_color.darker(120)))
            )

    def __removePage(self, row):
        # type: (int) -> None
        page = self.__pages.page(row)
        page.triggered.disconnect(self.__onTriggered)
        page.hovered.disconnect(self.hovered)
        page.view().removeEventFilter(self)
        self.__pages.removePage(row)

    def setSortingFunc(self, func):
        # type: (Callable[[Any, Any], bool]) -> None
        """
        Set a sorting function in the suggest (search) menu.
        """
        if self.__sortingFunc != func:
            self.__sortingFunc = func
            for i in range(0, self.__pages.count()):
                page = self.__pages.page(i)
                if isinstance(page, SuggestMenuPage):
                    page.setSortingFunc(func)

    def setFilterFunc(self, func):
        # type: (Optional[FilterFunc]) -> None
        """
        Set a filter function.
        """
        if func != self.__filterFunc:
            self.__filterFunc = func
            for i in range(0, self.__pages.count()):
                self.__pages.page(i).setFilterFunc(func)

    def popup(self, pos=None, searchText=""):
        # type: (Optional[QPoint], str) -> None
        """
        Popup the menu at `pos` (in screen coordinates). 'Search' text field
        is initialized with `searchText` if provided.
        """
        if pos is None:
            pos = QPoint()

        self.__clearCurrentItems()

        self.__search.setText(searchText)
        patt = QRegExp(r"(^|\W)"+searchText)
        patt.setCaseSensitivity(Qt.CaseInsensitive)
        self.__suggestPage.setFilterRegExp(patt)

        UsageStatistics.set_last_search_query(searchText)

        self.ensurePolished()

        if self.testAttribute(Qt.WA_Resized) and self.sizeGripEnabled():
            size = self.size()
        else:
            size = self.sizeHint()

        desktop = QApplication.desktop()
        screen_geom = desktop.availableGeometry(pos)

        # Adjust the size to fit inside the screen.
        if size.height() > screen_geom.height():
            size.setHeight(screen_geom.height())
        if size.width() > screen_geom.width():
            size.setWidth(screen_geom.width())

        geom = QRect(pos, size)

        if geom.top() < screen_geom.top():
            geom.setTop(screen_geom.top())

        if geom.left() < screen_geom.left():
            geom.setLeft(screen_geom.left())

        bottom_margin = screen_geom.bottom() - geom.bottom()
        right_margin = screen_geom.right() - geom.right()
        if bottom_margin < 0:
            # Falls over the bottom of the screen, move it up.
            geom.translate(0, bottom_margin)

        # TODO: right to left locale
        if right_margin < 0:
            # Falls over the right screen edge, move the menu to the
            # other side of pos.
            geom.translate(-size.width(), 0)

        self.setGeometry(geom)

        self.show()

        self.setFocusProxy(self.__search)

    def exec_(self, pos=None, searchText=""):
        # type: (Optional[QPoint], str) -> Optional[QAction]
        """
        Execute the menu at position `pos` (in global screen coordinates).
        Return the triggered :class:`QAction` or `None` if no action was
        triggered. 'Search' text field is initialized with `searchText` if
        provided.
        """
        self.popup(pos, searchText)
        self.setFocus(Qt.PopupFocusReason)

        self.__triggeredAction = None
        self.__loop = QEventLoop()
        self.__loop.exec_()
        self.__loop.deleteLater()
        self.__loop = None

        action = self.__triggeredAction
        self.__triggeredAction = None
        return action

    def hideEvent(self, event):
        """
        Reimplemented from :class:`QWidget`
        """
        super().hideEvent(event)
        if self.__loop:
            self.__loop.exit()

    def setCurrentPage(self, page):
        # type: (MenuPage) -> None
        """
        Set the current shown page to `page`.
        """
        self.__pages.setCurrentPage(page)

    def setCurrentIndex(self, index):
        # type: (int) -> None
        """
        Set the current page index.
        """
        self.__pages.setCurrentIndex(index)

    def __clearCurrentItems(self):
        # type: () -> None
        """
        Clear any selected (or current) items in all the menus.
        """
        for i in range(self.__pages.count()):
            self.__pages.page(i).view().selectionModel().clear()

    def __onTriggered(self, action):
        # type: (QAction) -> None
        """
        Re-emit the action from the page.
        """
        self.__triggeredAction = action

        # Hide and exit the event loop if necessary.
        self.hide()
        self.triggered.emit(action)

    def __on_textEdited(self, text):
        # type: (str) -> None
        patt = QRegExp(r"(^|\W)" + text)
        patt.setCaseSensitivity(Qt.CaseInsensitive)
        self.__suggestPage.setFilterRegExp(patt)
        self.__pages.setCurrentPage(self.__suggestPage)
        self.__selectFirstIndex()
        UsageStatistics.set_last_search_query(text)

    def __selectFirstIndex(self):
        # type: () -> None
        view = self.__pages.currentPage().view()
        model = view.model()

        index = model.index(0, 0)
        view.setCurrentIndex(index)

    def triggerSearch(self):
        # type: () -> None
        """
        Trigger action search. This changes to current page to the
        'Suggest' page and sets the keyboard focus to the search line edit.
        """
        self.__pages.setCurrentPage(self.__suggestPage)
        self.__search.setFocus(Qt.ShortcutFocusReason)

        # Make sure that the first enabled item is set current.
        self.__suggestPage.ensureCurrent()

    def keyPressEvent(self, event):
        if event.text():
            # Ignore modifiers, ...
            self.__search.setFocus(Qt.ShortcutFocusReason)
            self.setCurrentIndex(0)
            self.__search.keyPressEvent(event)

        super().keyPressEvent(event)
        event.accept()

    def event(self, event):
        if event.type() == QEvent.ShortcutOverride:
            log.debug("Overriding shortcuts")
            event.accept()
            return True
        return super().event(event)

    def eventFilter(self, obj, event):
        if isinstance(obj, QTreeView):
            etype = event.type()
            if etype == QEvent.KeyPress:
                # ignore modifiers non printable characters, Enter, ...
                if event.text() and event.key() not in \
                        [Qt.Key_Enter, Qt.Key_Return]:
                    self.__search.setFocus(Qt.ShortcutFocusReason)
                    self.setCurrentIndex(0)
                    self.__search.keyPressEvent(event)
                    return True

        return super().eventFilter(obj, event)


class ItemViewKeyNavigator(QObject):
    """
    A event filter class listening to key press events and responding
    by moving 'currentItem` on a :class:`QListView`.
    """
    def __init__(self, parent=None, **kwargs):
        # type: (Optional[QObject], Any) -> None
        super().__init__(parent, **kwargs)
        self.__view = None  # type: Optional[QAbstractItemView]

    def setView(self, view):
        # type: (Optional[QAbstractItemView]) -> None
        """
        Set the QListView.
        """
        if self.__view != view:
            self.__view = view

    def view(self):
        # type: () -> Optional[QAbstractItemView]
        """
        Return the view
        """
        return self.__view

    def eventFilter(self, obj, event):
        etype = event.type()
        if etype == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Down:
                self.moveCurrent(1, 0)
                return True
            elif key == Qt.Key_Up:
                self.moveCurrent(-1, 0)
                return True
            elif key == Qt.Key_Tab:
                self.moveCurrent(0, 1)
                return  True
            elif key == Qt.Key_Enter or key == Qt.Key_Return:
                self.activateCurrent()
                return True

        return super().eventFilter(obj, event)

    def moveCurrent(self, rows, columns=0):
        # type: (int, int) -> None
        """
        Move the current index by rows, columns.
        """
        if self.__view is not None:
            view = self.__view
            model = view.model()

            curr = view.currentIndex()
            curr_row, curr_col = curr.row(), curr.column()

            sign = 1 if rows >= 0 else -1
            row = curr_row + rows

            row_count = model.rowCount()
            for i in range(row_count):
                index = model.index((row + sign * i) % row_count, 0)
                if index.flags() & Qt.ItemIsEnabled:
                    view.setCurrentIndex(index)
                    break
            # TODO: move by columns

    def activateCurrent(self):
        # type: () -> None
        """
        Activate the current index.
        """
        if self.__view is not None:
            curr = self.__view.currentIndex()
            if curr.isValid():
                self.__view.activated.emit(curr)

    def ensureCurrent(self):
        # type: () -> None
        """
        Ensure the view has a current item if one is available.
        """
        if self.__view is not None:
            model = self.__view.model()
            curr = self.__view.currentIndex()
            if not curr.isValid():
                for i in range(model.rowCount()):
                    index = model.index(i, 0)
                    if index.flags() & Qt.ItemIsEnabled:
                        self.__view.setCurrentIndex(index)
                        break


class WindowSizeGrip(QSizeGrip):
    """
    Automatically positioning :class:`QSizeGrip`.
    The widget automatically maintains its position in the window
    corner during resize events.

    """
    def __init__(self, parent):
        super().__init__(parent)
        self.__corner = Qt.BottomRightCorner

        self.resize(self.sizeHint())

        self.__updatePos()

    def setCorner(self, corner):
        """
        Set the corner (:class:`Qt.Corner`) where the size grip should
        position itself.

        """
        if corner not in [Qt.TopLeftCorner, Qt.TopRightCorner,
                          Qt.BottomLeftCorner, Qt.BottomRightCorner]:
            raise ValueError("Qt.Corner flag expected")

        if self.__corner != corner:
            self.__corner = corner
            self.__updatePos()

    def corner(self):
        """
        Return the corner where the size grip is positioned.
        """
        return self.__corner

    def eventFilter(self, obj, event):
        if obj is self.window():
            if event.type() == QEvent.Resize:
                self.__updatePos()
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        if self.window() != self.parent():
            log.error("%s: Can only show on a top level window.",
                      type(self).__name__)
        return super().showEvent(event)

    def __updatePos(self):
        window = self.window()

        if window is not self.parent():
            return

        corner = self.__corner
        size = self.sizeHint()

        window_geom = window.geometry()
        window_size = window_geom.size()

        if corner in [Qt.TopLeftCorner, Qt.BottomLeftCorner]:
            x = 0
        else:
            x = window_geom.width() - size.width()

        if corner in [Qt.TopLeftCorner, Qt.TopRightCorner]:
            y = 0
        else:
            y = window_size.height() - size.height()

        self.move(x, y)
