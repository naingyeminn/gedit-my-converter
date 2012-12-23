from gi.repository import GObject, Gtk, Gedit
import myanmar.converter as converter

UI_XML = """<ui>
<menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_3">
		<menuitem name="Zgy2Uni" action="Zgy2Uni"/>
        <menuitem name="Uni2Zgy" action="Uni2Zgy"/>
      </placeholder>
    </menu>
</menubar>
</ui>"""

class MyConvertPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "MyConvertPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def _add_ui(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup("MyConvertActions")
        self._actions.add_actions([
            ('Zgy2Uni', Gtk.STOCK_EDIT, "Zawgyi to _Unicode",
                None, "Convert Unicode to the current document.",
                self.on_zgy2uni_action_activate),
            ('Uni2Zgy', Gtk.STOCK_EDIT, "Unicode to _Zawgyi",
                None, "Convert Zawgyi to the current document.",
                self.on_uni2zgy_action_activate),
        ])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()

    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass

    def on_zgy2uni_action_activate(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            buff = view.get_buffer()
            strin = buff.get_property('text')
            strout = converter.convert(strin, "zawgyi", "unicode")
            buff.set_text(strout)

    def on_uni2zgy_action_activate(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            buff = view.get_buffer()
            strin = buff.get_property('text')
            strout = converter.convert(strin, "unicode", "zawgyi")
            buff.set_text(strout)

    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()
