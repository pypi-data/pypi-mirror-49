from .abstract_module import AbstractModule
import subprocess
import os
import logging
import platform

class Setup(AbstractModule):
    def __init__(self, subparser):
        super(Setup, self).__init__(subparser)
        self.lgsp = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def add_module_to_parser(self, subparser):
        super().add_module_to_parser(subparser)
        self.module_parser.add_argument('--keyboard', type=str, dest='keyboard',
                                        help='keyboard options (internal / external)')

    def run(self, args):
        if (args.keyboard == 'internal'):
            self.set_keyboard_internal()
        elif (args.keyboard == 'external'):
            self.set_keyboard_external()

    def get_name(self):
        return "setup"

    def set_keyboard_internal(self):
        logging.info("- setting keyboard internal")
        assert platform.system() == 'Linux', 'Error: wrong OS, expected <Linux>'
        self.remap_keypad_comma_to_period()
        self.swap_ctrl_and_cmd_key()
        self.clear_xkb()
        os.system('setxkbmap -layout macintosh_vndr/ch')

    def set_keyboard_external(self):
        logging.info("- setting keyboard external")
        assert platform.system() == 'Linux', 'Error: wrong OS, expected <Linux>'
        self.remap_keypad_comma_to_period()
        self.unswap_ctrl_and_cmd_key()
        self.clear_xkb()
        os.system('setxkbmap -layout macintosh_vndr/ch')

    def remap_keypad_comma_to_period(self):
        self.sudo_cp(self.lgsp + '/resources/ch', '/usr/share/X11/xkb/symbols/macintosh_vndr/ch')

    def swap_ctrl_and_cmd_key(self):
        self.sudo_cp(self.lgsp + '/resources/pc_cmd_ctrl_swapped', '/usr/share/X11/xkb/symbols/pc')

    def unswap_ctrl_and_cmd_key(self):
        self.sudo_cp(self.lgsp + '/resources/pc_default', '/usr/share/X11/xkb/symbols/pc')

    def clear_xkb(self):
        self.sudo_rm_rf('/var/lib/xkb/')

    def sudo_cp(self, src, dest):
        cmd = f'sudo cp {src} {dest}'
        os.system(cmd)

    def sudo_rm_rf(self, dir):
        os.system(f'sudo rm -rf {dir}')

    def sudo_rm(self, file):
        os.system(f'sudo rm {file}')
