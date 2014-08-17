from gi.repository import Wnck, GObject, GdkX11


class WnckState(object):
    def __init__(self, avoid):
        self.workspaces = {}
        self.active_window = None
        self.prior_window = None
        self.active_workspace = None
        self.prior_workspace = None
        self.windows = {}
        self._avoid = avoid
        self._avoid_xid = None

    def connect_signals(self):
        GObject.signal_connect_closure(
            self.screen, "active-window-changed",
            self._on_active_window_changed, True)
        GObject.signal_connect_closure(
            self.screen, "active-workspace-changed",
            self._on_active_workspace_changed, True)
        GObject.signal_connect_closure(
            self.screen, "window-closed", self._on_window_closed, True)
        GObject.signal_connect_closure(
            self.screen, "window-opened", self._on_window_opened, True)
        GObject.signal_connect_closure(
            self.screen, "workspace-created", self._on_workspace_created, True)
        GObject.signal_connect_closure(
            self.screen, "workspace-destroyed",
            self._on_workspace_destroyed, True)

    @property
    def screen(self):
        return Wnck.Screen.get_default()

    def _on_active_window_changed(self, screen, prior_window):
        if self._avoid_xid is None:
            self._avoid_xid = self._avoid.get_window().get_xid()

        active_window = Wnck.Screen.get_active_window(screen)
        if active_window:
            active_window_xid = Wnck.Window.get_xid(active_window)

        if self._avoid_xid == active_window_xid:
            if self.active_window is None:
                self.active_window = prior_window
        else:
            self.active_window = active_window

        if prior_window:
            prior_window_xid = Wnck.Window.get_xid(prior_window)
            if prior_window_xid != active_window_xid:
                self.prior_window = prior_window

    def _on_active_workspace_changed(self, screen, prior_workspace):
        self.prior_workspace = prior_workspace
        self.active_workspace = Wnck.Screen.get_active_workspace(screen)

    def _on_window_closed(self, screen, window):
        if window:
            workspace = Wnck.Window.get_workspace(window)
            if workspace:
                self.workspaces[workspace].remove(window)

        self.active_workspace = Wnck.Screen.get_active_workspace(screen)

    def _on_window_opened(self, screen, window):
        workspace = Wnck.Window.get_workspace(window)
        if workspace:
            self.workspaces[workspace].append(window)
        GObject.signal_connect_closure(
            window, "geometry-changed", self._geometry_changed, True)
        GObject.signal_connect_closure(
            window, "workspace-changed", self._update_workspace, True)

    def _on_workspace_created(self, screen, workspace):
        self.workspaces[workspace] = []

    def _on_workspace_destroyed(self, screen, workspace):
        del self.workspaces[workspace]

    def _update_workspace(self, window):
        if window:
            workspace = Wnck.Window.get_workspace(window)
            if workspace:
                # remove from workspaces
                for ws, windows in self.workspaces.iteritems():
                    if window in windows:
                        self.workspaces[ws].remove(window)
                        break
                # add to workspaces
                self.workspaces[workspace].append(window)

    def _geometry_changed(self, window):
        geometry = Wnck.Window.get_geometry(window)
        if window:
            if window not in self.windows:
                self.windows[window] = {}
            self.windows[window]['geometry'] = geometry
