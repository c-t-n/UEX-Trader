from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QStyleFactory
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from config_tab import ConfigTab
from trade_tab import TradeTab
from trade_route_tab import TradeRouteTab
from best_trade_route import BestTradeRouteTab
from config_manager import ConfigManager
from translation_manager import TranslationManager


class UexcorpTrader(QWidget):
    def __init__(self, app, loop):
        super().__init__()
        self.app = app
        self.loop = loop
        self.config_manager = ConfigManager()
        self.translation_manager = TranslationManager()
        self.initUI(self.config_manager.get_lang())
        self.apply_appearance_mode()
        self.apply_lang(self.config_manager.get_lang())

    def initUI(self, lang="en"):
        self.setWindowTitle(self.translation_manager.get_translation("window_title", lang))
        self.setWindowIcon(QIcon("resources/UEXTrader_icon_resized.png"))

        tabs = QTabWidget()
        self.configTab = ConfigTab(self)
        self.tradeTab = TradeTab(self)
        self.tradeRouteTab = TradeRouteTab(self)
        self.bestTradeRouteTab = BestTradeRouteTab(self)
        tabs.addTab(self.configTab, self.translation_manager.get_translation("config_tab", lang))
        tabs.addTab(self.tradeTab, self.translation_manager.get_translation("trade_tab", lang))
        tabs.addTab(self.tradeRouteTab, self.translation_manager.get_translation("trade_route_tab", lang))
        tabs.addTab(self.bestTradeRouteTab, self.translation_manager.get_translation("best_trade_route_tab", lang))

        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

        # Restore window size
        width, height = self.config_manager.get_window_size()
        self.resize(width, height)

    def apply_lang(self, lang="en"):
        self.initUI(lang)

    def apply_appearance_mode(self, appearance_mode=None):
        if not appearance_mode:
            appearance_mode = self.config_manager.get_appearance_mode()
        if appearance_mode == self.translation_manager.get_translation("appearance_dark", self.config_manager.get_lang()):
            self.app.setStyle(QStyleFactory.create("Fusion"))
            dark_palette = self.create_dark_palette()
            self.app.setPalette(dark_palette)
        else:
            self.app.setStyle(QStyleFactory.create("Fusion"))
            self.app.setPalette(QApplication.style().standardPalette())

    def create_dark_palette(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        return dark_palette

    def closeEvent(self, event):
        # Save window size
        self.config_manager.set_window_size(self.width(), self.height())
        super().closeEvent(event)
        self.loop.stop()
        self.loop.close()

    def set_gui_enabled(self, enabled):
        self.configTab.set_gui_enabled(enabled)
        self.tradeTab.set_gui_enabled(enabled)
        self.tradeRouteTab.set_gui_enabled(enabled)
        self.bestTradeRouteTab.set_gui_enabled(enabled)
