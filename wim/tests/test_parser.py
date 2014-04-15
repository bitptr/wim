from unittest import TestCase

from wim.language import parser


class TestParser(TestCase):
    def test_window_xid_shade(self):
        s = '<#25>s " shade window with XID 25, on current workspace'
        exp = ['<', '#', '25', '>', 's']
        self.assertParse(s, exp)

    def test_window_class_and_name_and_regexp_vertical_maximize(self):
        s = '<.term @/~/>vM " vertical maximize all'
        exp = ['<', '.', 'term', ' ', '@', '/', '~', '/', '>', 'vM']
        self.assertParse(s, exp)

    def test_global_window_class_move_workspace_name(self):
        s = 'g<.term>m[@Terminals] " move all'
        exp = ['g', '<', '.', 'term', '>', 'm', '[', '@', 'Terminals', ']']
        self.assertParse(s, exp)

    def test_current_window_toggle_shading(self):
        s = '%tS " toggle shading on the current window'
        exp = ['%', 'tS']
        self.assertParse(s, exp)

    def test_prior_window_activate(self):
        s = '# " activate the prior window'
        exp = ['#']
        self.assertParse(s, exp)

    def test_current_window_move_3rd_workspace(self):
        s = '%m[2] " move the current window to the 3rd workspace'
        exp = ['%', 'm', '[', '2', ']']
        self.assertParse(s, exp)

    def test_9th_workspace_jump(self):
        s = '[8]j " jump to the 9th workspace'
        exp = ['[', '8', ']', 'j']
        self.assertParse(s, exp)

    def test_windows(self):
        self.assertParse('windows', ['windows'])

    def test_desktop(self):
        self.assertParse('desktop', ['desktop'])

    def test_current_workspace(self):
        s = '[] " produce the current workspace'
        exp = ['[', ']']
        self.assertParse(s, exp)

    def test_current_window(self):
        s = '<> " produce the current window'
        exp = ['<', '>']
        self.assertParse(s, exp)

    def test_current_window_alias(self):
        s = '% " produce the current window'
        exp = ['%']
        self.assertParse(s, exp)

    def test_current_workspace_move_right(self):
        s = '[]mr " move to the workspace to the right'
        exp = ['[', ']', 'm', 'r']
        self.assertParse(s, exp)

    def test_2nd_workspace_move_right_3(self):
        s = '[1]m3r " move to the workspace 3 to the right'
        exp = ['[', '1', ']', 'm', '3', 'r']
        self.assertParse(s, exp)

    def test_application_pid_maximize(self):
        s = '{&1234}M'
        exp = ['{', '&', '1234', '}', 'M']
        self.assertParse(s, exp)

    def test_windows_any_type_close(self):
        s = '<?normal,?dialog,?toolbar,?utility>x'
        exp = ['<', '?', 'normal', ',', '?', 'dialog', ',', '?',
               'toolbar', ',', '?', 'utility', '>', 'x']
        self.assertParse(s, exp)

    def assertParse(self, string, expected):
        results = parser.parseString(string)
        self.assertEqual(results.asList(), expected)
