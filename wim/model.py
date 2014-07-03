from gi.repository import GObject, Wnck


class Model(object):
    def __init__(self):
        self.workspaces = {}
        self.active_window = None
        self.prior_window = None
        self.active_workspace = None
        self.prior_workspace = None
        self.windows = {}

    def startup(self):
        GObject.signal_connect_closure(
            self.screen, "active-window-changed",
            self._set_active_window, True)
        GObject.signal_connect_closure(
            self.screen, "active-workspace-changed",
            self._set_active_workspace, True)
        #GObject.signal_connect_closure(
        #    self.screen, "application-closed", ..., True)
        #GObject.signal_connect_closure(
        #    self.screen, "application-opened", ..., True)
        #GObject.signal_connect_closure(
        #    self.screen, "background-changed", ..., True)
        #GObject.signal_connect_closure(
        #    self.screen, "class-group-closed", ..., True)
        #GObject.signal_connect_closure(
        #    self.screen, "class-group-opened", ..., True)
        #GObject.signal_connect_closure(
        #    self.screen, "showing-desktop-changed", ..., True)
        #GObject.signal_connect_closure(
        #    self.screen, "viewports-changed", ..., True)
        GObject.signal_connect_closure(
            self.screen, "window-closed", self._remove_window, True)
        #GObject.signal_connect_closure(
        #    self.screen, "window-manager-changed", ..., True)
        GObject.signal_connect_closure(
            self.screen, "window-opened", self._add_window, True)
        #GObject.signal_connect_closure(
        #    self.screen, "window-stacking-changed", ..., True)
        GObject.signal_connect_closure(
            self.screen, "workspace-created", self._add_workspace, True)
        GObject.signal_connect_closure(
            self.screen, "workspace-destroyed", self._remove_workspace, True)

    def shutdown(self):
        print("shutdown")

    def active_workspace_windows(self):
        return self.workspaces[self.active_workspace]

    @property
    def screen(self):
        return Wnck.Screen.get_default()

    def geometry_for(self, window):
        if window in self.windows and 'geometry' in self.windows[window]:
            return self.windows[window]['geometry']
        else:
            return Wnck.Window.get_geometry(window)

    def move_window(self, window, x, y, w, h):
        Wnck.Window.set_geometry(
            window,
            Wnck.WindowGravity.STATIC,
            Wnck.WindowMoveResizeMask.X | Wnck.WindowMoveResizeMask.Y,
            x, y, w, h)

    def _add_window(self, screen, window):
        workspace = Wnck.Window.get_workspace(window)
        if workspace:
            self.workspaces[workspace].append(window)
        GObject.signal_connect_closure(
            window, "geometry-changed", self._geometry_changed, True)

    def _remove_window(self, screen, window):
        if window:
            workspace = Wnck.Window.get_workspace(window)
            if workspace:
                self.workspaces[workspace].remove(window)

    def _add_workspace(self, screen, workspace):
        self.workspaces[workspace] = []

    def _remove_workspace(self, screen, workspace):
        del self.workspaces[workspace]

    def _set_active_window(self, screen, prior_window):
        self.prior_window = prior_window
        self.active_window = Wnck.Screen.get_active_window(screen)

    def _set_active_workspace(self, screen, prior_workspace):
        self.prior_workspace = prior_workspace
        self.active_workspace = Wnck.Screen.get_active_workspace(screen)

    def _geometry_changed(self, window):
        geometry = Wnck.Window.get_geometry(window)
        if window:
            if window not in self.windows:
                self.windows[window] = {}
            self.windows[window]['geometry'] = geometry
