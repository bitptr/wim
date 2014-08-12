from gi.repository import GObject, Wnck
import itertools
import datetime
import calendar


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
        GObject.signal_connect_closure(
            self.screen, "window-closed", self._remove_window, True)
        GObject.signal_connect_closure(
            self.screen, "window-opened", self._add_window, True)
        GObject.signal_connect_closure(
            self.screen, "workspace-created", self._add_workspace, True)
        GObject.signal_connect_closure(
            self.screen, "workspace-destroyed", self._remove_workspace, True)

    @property
    def screen(self):
        return Wnck.Screen.get_default()

    def shutdown(self):
        print("shutdown")

    def active_workspace_windows(self):
        return self.workspaces[self.active_workspace]

    def geometry_for(self, window):
        if window in self.windows and 'geometry' in self.windows[window]:
            return self.windows[window]['geometry']
        else:
            return Wnck.Window.get_geometry(window)

    def move_window_to_coordinates(self, window, x, y, w, h):
        Wnck.Window.set_geometry(
            window,
            Wnck.WindowGravity.STATIC,
            Wnck.WindowMoveResizeMask.X | Wnck.WindowMoveResizeMask.Y,
            x, y, w, h)

    def move_window_to_workspace(self, window, workspace):
        Wnck.Window.move_to_workspace(window, workspace)

    def activate_window(self, window):
        Wnck.Window.activate(window, self._now())

    def activate_workspace(self, workspace):
        Wnck.Workspace.activate(workspace, self._now())

    def workspace_number(self, number):
        return Wnck.Screen.get_workspace(self.screen, number)

    def by_xid(self, xid):
        return Wnck.Window.get(xid)

    def windows_for_group(self, group):
        return (Wnck.ClassGroup.get_windows(group) or [])

    def by_group(self, group):
        return Wnck.ClassGroup.get(group)

    def all_windows(self):
        return list(itertools.chain(*self.workspaces.values()))

    def window_name(self, window):
        return Wnck.Window.get_name(window)

    def window_pid(self, window):
        return Wnck.Window.get_pid(window)

    # Callbacks

    def _add_window(self, screen, window):
        workspace = Wnck.Window.get_workspace(window)
        if workspace:
            self.workspaces[workspace].append(window)
        GObject.signal_connect_closure(
            window, "geometry-changed", self._geometry_changed, True)
        GObject.signal_connect_closure(
            window, "workspace-changed", self._update_workspace, True)

    def _remove_window(self, screen, window):
        if window:
            workspace = Wnck.Window.get_workspace(window)
            if workspace:
                self.workspaces[workspace].remove(window)

    def _now(self):
        return calendar.timegm(datetime.datetime.utcnow().timetuple())

    def _add_workspace(self, screen, workspace):
        self.workspaces[workspace] = []

    def _remove_workspace(self, screen, workspace):
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
