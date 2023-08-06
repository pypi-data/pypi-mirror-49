import os
import re
from functools import partial
from time import sleep

import nanome
from nanome.util import Logs
import utils

from contracts.Web3Helper import Web3Helper
from MatryxCortex import MatryxCortex
from menus.SettingsMenu import SettingsMenu
from menus.AccountsMenu import AccountsMenu
from menus.FilesMenu import FilesMenu
from menus.TournamentMenu import TournamentMenu
from menus.CreationsMenu import CreationsMenu
from menus.CreationMenu import CreationMenu
from menus.FirstToHashMenu import FirstToHashMenu
from menus.CreateTournamentMenu import CreateTournamentMenu
from menus.select_winners.SelectWinnersMenu import SelectWinnersMenu
from menus.Modal import Modal
from menus.Confirm import Confirm

import web3
import blockies

class Matryx(nanome.PluginInstance):
    def start(self):
        self._deferred = []
        self._menu_history = []
        self._refresh_flag = False
        self._account = None

        self._menu_matryx = nanome.ui.Menu.io.from_json('menus/json/matryx.json')
        menu = self._menu_matryx

        self._prefab_crumb = nanome.ui.LayoutNode.io.from_json('components/json/crumb.json')
        self.create_crumbs(menu)

        self._menu_settings = SettingsMenu(self, self.previous_menu)
        self._cortex = MatryxCortex()
        self._web3 = Web3Helper(self)
        self._web3.set_network('mainnet')

        self._menu_files = FilesMenu(self, self.previous_menu)
        self._menu_accounts = AccountsMenu(self, self.previous_menu)
        self._menu_creations = CreationsMenu(self, FirstToHashMenu(self, self.previous_menu), self.previous_menu)
        self._menu_creation = CreationMenu(self, self.previous_menu)
        self._menu_tournament = TournamentMenu(self, self.previous_menu)
        self._menu_first_to_hash = FirstToHashMenu(self, self.previous_menu)
        self._menu_create_tournament = CreateTournamentMenu(self, self.previous_menu)
        self._menu_select_winners = SelectWinnersMenu(self, self.previous_menu)
        self._menu_confirm = Confirm(self, self.previous_menu)
        self._modal = Modal(self, self.previous_menu)

        self._list_node = menu.root.find_node('List', True)
        self._list = self._list_node.get_content()
        self._error_message = menu.root.find_node('Error Message', True)

        self._button_account = menu.root.find_node('Account Button', True).get_content()
        self._button_account.register_pressed_callback(self._menu_accounts.show_menu)

        self._account_blockie = menu.root.find_node('Blockie')
        default_icon = os.path.join(os.path.dirname(__file__), 'images', 'addAccount.png')
        self._account_blockie.add_new_image(default_icon)
        self._account_eth = menu.root.find_node('ETH Balance').get_content()
        self._account_mtx = menu.root.find_node('MTX Balance').get_content()

        self._ln_settings = menu.root.find_node('Settings')
        self._button_settings = self._ln_settings.get_content()
        self._button_settings.register_pressed_callback(self._menu_settings.show_menu)
        menu.root.find_node('Settings Icon').add_new_image(os.path.join(os.path.dirname(__file__), 'images', 'settings.png'))

        self._button_all_tournaments = menu.root.find_node('All Tournaments').get_content()
        self._button_all_tournaments.register_pressed_callback(self.populate_all_tournaments)

        self._button_my_tournaments = menu.root.find_node('My Tournaments').get_content()
        self._button_my_tournaments.register_pressed_callback(self.populate_my_tournaments)

        self._button_my_creations = menu.root.find_node('My Creations').get_content()
        self._button_my_creations.register_pressed_callback(partial(self.populate_my_creations, 0))

        self._label_page = menu.root.find_node('Page Label').get_content()
        self._button_inc_page = menu.root.find_node('Inc Page').get_content()
        self._button_dec_page = menu.root.find_node('Dec Page').get_content()

        self._prefab_tournament_item = menu.root.find_node('Tournament Item Prefab')
        self._prefab_commit_item = menu.root.find_node('Commit Item Prefab')

        self.on_run()

    def on_run(self):
        self.set_to_refresh()
        self.open_matryx_menu()
        self.defer(self.populate_all_tournaments, 60)
        # self.print_node(self._menu_matryx.root)
        Logs.debug('requesting directory...')
        self.request_directory('/', self.on_directory_received)

    def update(self):
        if len(self._deferred):
            next_deferred = []
            for item in self._deferred:
                if item[0] == 0:
                    item[1]()
                else:
                    item[0] -= 1
                    next_deferred.append(item)

            self._deferred = next_deferred

    def defer(self, fn, frames):
        self._deferred.append([frames, fn])

    def on_directory_received(self, result):
        # If API couldn't access directory, display error
        if result.error_code != nanome.util.DirectoryErrorCode.no_error:
            Logs.error('Directory request error:', str(result.error_code))
            return

        # For each entry in directory, display name and if directory
        for entry in result.entry_array:
            Logs.debug(entry.name, 'Is Directory?', entry.is_directory)
            if entry.name == 'temp':
                self.request_files(['/temp/matryx_wallet.json'], self.on_files_received) # Read matryx.txt

    def on_files_received(self, file_list):
        # For each file we read, display if error, and file content
        for file in file_list:
            Logs.debug('Error?', str(nanome.util.FileErrorCode(file.error_code)), 'Content:', file.data.decode('utf-8'))

        if nanome.util.FileErrorCode(file.error_code) != nanome.util.FileErrorCode.file_unreachable:
            self._menu_accounts._wallet_json = file.data.decode('utf-8')

        # Prepare to write file 'api_test.txt', with content 'AAAA'
        # file = nanome.util.FileSaveData()
        # file.path = '/temp/matryx.txt'
        # file.write_text('0x123')
        # self.save_files([file], self.on_save_files_result) # Write file

    # def on_save_files_result(self, result_list):
    #     # Check for writing errors
    #     for result in result_list:
    #         nanome.util.Logs.debug('Saving', result.path, 'Error?', str(nanome.util.FileErrorCode(result.error_code)))

    def open_menu(self, menu=None, history=True):
        if history and menu is not self._menu_matryx:
            prev_menu = None
            if len(self._menu_history) > 0:
                prev_menu = self._menu_history[-1]
            if menu is not prev_menu:
                self._menu_history.append(menu)
                self.create_crumbs(menu)

        self.menu = menu
        menu.enabled = True
        self.update_menu(self.menu)

    def print_node(self, layout_node, depth=0):
        prefix = '|   ' * (depth - 1) + ('|-- ' if depth > 0 else '')
        Logs.debug(prefix + layout_node.name)

        children = layout_node.get_children()
        if len(children) > 0:
            for child in children:
                self.print_node(child, depth + 1)

        if depth == 0:
            Logs.debug('---------------------------------')

    def create_crumbs(self, menu):
        crumbs = menu.root.find_node('Breadcrumbs')
        crumbs.clear_children()

        for i, item in enumerate([self._menu_matryx] + self._menu_history):
            crumb = self._prefab_crumb.clone()
            crumb.set_size_fixed(0.1)
            crumb.find_node('Text').get_content().text_value = item.title

            button = crumb.find_node('Button').get_content()
            button.unusable = i == len(self._menu_history)
            button.register_pressed_callback(partial(self.pop_to_menu, item.title))

            arrow_path = os.path.join(os.path.dirname(__file__), 'images', 'arrow.png')
            crumb.find_node('Arrow').add_new_image(arrow_path)

            crumbs.add_child(crumb)

    def previous_menu(self, menu=None):
        self._menu_history.pop()
        if len(self._menu_history) == 0:
            Logs.debug('calling update on main menu...')
            self.refresh()
            self.open_matryx_menu()
        else:
            refresh = getattr(self._menu_history[-1], 'refresh', None)
            if callable(refresh):
                Logs.debug('calling update on menu' + str(self._menu_history[-1]))
                refresh()
            self.open_menu(self._menu_history[-1], False)

    def pop_menu_history(self, n=1):
        for i in range(n):
            self._menu_history.pop()

    def pop_to_menu(self, menu_title, button):
        while len(self._menu_history) > 0:
            if self._menu_history[-1].title == menu_title:
                break
            self._menu_history.pop()

        if len(self._menu_history) == 0:
            self.open_matryx_menu()
        else:
            self.open_menu(self._menu_history[-1], False)

    def set_to_refresh(self):
        self._refresh_flag = True

    def refresh(self):
        if self._refresh_flag:
            if self._account != None:
                self.update_account()
            if self._button_all_tournaments.selected:
                Logs.debug('all tournaments')
                self.populate_all_tournaments()
            elif self._button_my_tournaments.selected:
                Logs.debug('my tournaments')
                self.populate_my_tournaments()
            elif self._button_my_creations.selected:
                Logs.debug('my creations')
                self.populate_my_creations()

        self._refresh_flag = False

    def refresh_menu(self):
        self.update_menu(self.menu)

    def open_matryx_menu(self, button=None):
        self.refresh()
        self.open_menu(self._menu_matryx)

    def show_error(self, error):
        self._list_node.enabled = False
        self._error_message.enabled = True
        self._error_message.get_content().text_value = error

    def clear_error(self):
        self._list_node.enabled = True
        self._error_message.enabled = False

    def select_account(self, account, button=None):
        self._account = account
        self._button_account.text.value_idle = account.short_address
        self._account_blockie.add_new_image(account.blockie)
        self.update_account()
        self._menu_history.pop()
        self.set_to_refresh()
        self.open_matryx_menu()

    def update_account(self):
        account = self._account
        self._account_eth.text_value = utils.truncate(self._web3.get_eth(account.address)) + ' ETH'
        self._account_mtx.text_value = utils.truncate(self._web3.get_mtx(account.address)) + ' MTX'

    def check_account(self):
        if self._account:
            self.clear_error()
            return True

        self.show_error('please select an account')
        self.refresh_menu()

    def toggle_tab(self, active_tab):
        tabs = [
            self._button_all_tournaments,
            self._button_my_tournaments,
            self._button_my_creations
        ]

        for tab in tabs:
            tab.selected = False

        active_tab.selected = True

    def add_button_to_list(self, texts, callback):
        clone = self._prefab_commit_item.clone()
        btn = clone.get_content()
        btn.bolded = True
        btn.set_all_text(texts[next(iter(texts))])
        for key in texts:
            setattr(btn.text, key, texts[key])

        btn.register_pressed_callback(callback)
        self._list.items.append(clone)

    def populate_tournaments(self, offset=0, status='open', mine=False, button=None):
        params = {
            'offset': offset,
            'sortBy': 'round_end',
            'status': status
        }

        button_texts = {
            'value_idle' : '+',
            'value_selected' : 'create tournament',
            'value_highlighted' : 'create tournament'
        }

        self._list.items = []
        if mine:
            del params['status']
            params['owner'] = self._account.address
            self.add_button_to_list(button_texts, self._menu_create_tournament.clear_and_open)

        tournaments = self._cortex.get_tournaments(params)

        for tournament in tournaments:
            clone = self._prefab_tournament_item.clone()
            clone.enabled = True

            btn = clone.get_content()
            callback = partial(self._menu_tournament.load_tournament, tournament['address'])
            btn.register_pressed_callback(callback)

            title = clone.find_node('Title').get_content()
            text = tournament['title']
            text = text[0:55] + ('...' if len(text) > 55 else '')
            title.text_value = text

            bounty = clone.find_node('Bounty').get_content()
            bounty.text_value = str(tournament['bounty']) + ' MTX'
            self._list.items.append(clone)

        count = len(tournaments)
        self._label_page.text_value = 'Page %d' % int(offset / 12 + 1)

        self._button_dec_page.unusable = offset == 0
        cb = lambda x: self.populate_tournaments(offset - 12, status, mine, button)
        self._button_dec_page.register_pressed_callback(cb)

        self._button_inc_page.unusable = count < 12
        cb = lambda x: self.populate_tournaments(offset + 12, status, mine, button)
        self._button_inc_page.register_pressed_callback(cb)

        self.toggle_tab(button)
        self.refresh_menu()

    def populate_all_tournaments(self, button=None):
        if button == None:
            button = self._button_all_tournaments

        self.clear_error()
        self.populate_tournaments(button=button)

    def populate_my_tournaments(self, button=None):
        if button == None:
            button = self._button_my_tournaments

        if not self.check_account():
            self.toggle_tab(button)
            return

        self.populate_tournaments(mine=True, button=button)

    def populate_my_creations(self, offset=0, button=None):
        if button == None:
            button = self._button_my_creations

        self.toggle_tab(button)

        if not self.check_account():
            return

        self._list.items = []
        button_texts = {
            'value_idle' : '+',
            'value_selected' : 'new creation',
            'value_highlighted' : 'new creation'
        }
        self.add_button_to_list(button_texts, self._menu_first_to_hash.display_selected)

        params = { 'offset': offset }
        commits = self._cortex.get_commits(self._account.address, params)

        for commit in commits:
            clone = self._prefab_commit_item.clone()
            btn = clone.get_content()
            btn.set_all_text('Commit ' + commit['hash'][2:10])

            callback = partial(self._menu_creation.load_commit, commit['hash'])
            btn.register_pressed_callback(callback)

            self._list.items.append(clone)

        count = len(commits)
        self._label_page.text_value = 'Page %d' % int(count / 24 + 1)

        self._button_dec_page.unusable = offset == 0
        cb = partial(self.populate_my_creations, offset - 24)
        self._button_dec_page.register_pressed_callback(cb)

        self._button_inc_page.unusable = count < 24
        cb = partial(self.populate_my_creations, offset + 24)
        self._button_inc_page.register_pressed_callback(cb)

        self.refresh_menu()

def main():
    plugin = nanome.Plugin('Matryx', 'Interact with the Matryx platform', 'Utilities', False)
    plugin.set_plugin_class(Matryx)
    plugin.run('127.0.0.1', 8888)

if __name__ == '__main__':
    main()