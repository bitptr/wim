from unittest import TestCase

from wim.language import parser


class TestParser(TestCase):
    def test_window_xid_shade(self):
        s = '<#25>s " shade window with XID 25, on current workspace'
        exp = ['<', '#', '25', '>', 's',
               '" shade window with XID 25, on current workspace']
        self.assertParse(s, exp)

    def test_window_hex_xid_shade(self):
        s = ('<#0x160000d>s " shade window with XID 0x160000d,'
             ' on current workspace')
        exp = ['<', '#', '0x160000d', '>', 's',
               '" shade window with XID 0x160000d, on current workspace']
        self.assertParse(s, exp)

    def test_global_window_class_move_workspace_name(self):
        s = 'g<.term>m[@Terminals] " move all'
        exp = ['g', '<', '.', 'term', '>', 'm', '[', '@', 'Terminals', ']',
               '" move all']
        self.assertParse(s, exp)

    def test_current_window_toggle_shading(self):
        s = '%tS " toggle shading on the current window'
        exp = ['%', 'tS', '" toggle shading on the current window']
        self.assertParse(s, exp)

    def test_prior_window_activate(self):
        s = '# " activate the prior window'
        exp = ['#', '" activate the prior window']
        self.assertParse(s, exp)

    def test_current_window_move_3rd_workspace(self):
        s = '%m[2] " move the current window to the 3rd workspace'
        exp = ['%', 'm', '[', '2', ']',
               '" move the current window to the 3rd workspace']
        self.assertParse(s, exp)

    def test_9th_workspace_jump(self):
        s = '[8]j " jump to the 9th workspace'
        exp = ['[', '8', ']', 'j', '" jump to the 9th workspace']
        self.assertParse(s, exp)

    def test_windows(self):
        self.assertParse('windows', ['windows'])

    def test_desktop(self):
        self.assertParse('desktop', ['desktop'])

    def test_current_workspace(self):
        s = '[] " produce the current workspace'
        exp = ['[', ']', '" produce the current workspace']
        self.assertParse(s, exp)

    def test_current_window(self):
        s = '<> " produce all windows'
        exp = ['<', '>', '" produce all windows']
        self.assertParse(s, exp)

    def test_current_window_alias(self):
        s = '% " produce the current window'
        exp = ['%', '" produce the current window']
        self.assertParse(s, exp)

    def test_current_workspace_move_right(self):
        s = '[]mr " move to the workspace to the right'
        exp = ['[', ']', 'm', 'r', '" move to the workspace to the right']
        self.assertParse(s, exp)

    def test_2nd_workspace_move_right_3(self):
        s = '[1]m3r " move to the workspace 3 to the right'
        exp = ['[', '1', ']', 'm', '3', 'r',
               '" move to the workspace 3 to the right']
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

    def test_full_line_comment(self):
        s = '"This is a comment'
        exp = ['"This is a comment']
        self.assertParse(s, exp)

    def test_full_line_comment_with_leading_whitespace(self):
        s = ' "This is a comment'
        exp = ['"This is a comment']
        self.assertParse(s, exp)

    def test_activate_with_too_much_whitespace(self):
        s = '  #  "This is a comment'
        exp = ['#', '"This is a comment']
        self.assertParse(s, exp)

    def assertParse(self, string, expected):
        results = parser.parseString(string)
        self.assertEqual(results.asList(), expected)
