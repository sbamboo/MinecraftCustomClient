# Description: To view/edit yaml files in TUI
# Requires config-tui.css in the same folder level
__author__ = 'PrudhviCh'
__version__ = '1.2.5'

import argparse
import json
import os
from ruamel.yaml import YAML

from rich.text import Text
from rich.highlighter import ReprHighlighter

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Footer, Input, Tree
from textual.widgets.tree import TreeNode

code_dir = os.path.dirname(os.path.abspath(__file__))
CSS_FILE = os.path.join(code_dir, 'config-tui.css')


class AlertScreen(ModalScreen[bool]):
    """Screen for a Dialog Box.

    Returns:
        boolean status of user's confirmation
    """

    CSS_PATH = CSS_FILE

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.message = kwargs['message']

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(f"{self.message}", id="dialog-msg"),
            Button("Yes", variant="success", id="yes"),
            Button("No", variant="primary", id="no"),
            id="dialog-box",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'yes':
            self.dismiss(True)
        else:
            self.dismiss(False)


class SaveScreen(ModalScreen):
    """Screen with a dialog to Save file as."""

    CSS_PATH = CSS_FILE

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.input_file = kwargs['input_file']
        self.config_type = kwargs['config_type']
        self.yml_obj = kwargs['yml_obj']
        self.new_json_data = kwargs['data']

    def compose(self) -> ComposeResult:
        self.out_file_name = Input(placeholder="Enter file name...", id="save-input", value=self.input_file)
        self.out_file_name.border_title = 'Save as'
        yield Grid(
            self.out_file_name,
            Button("Save", variant="success", id="yes"),
            Button("Cancel", variant="primary", id="no"),
            id="dialog-box",
        )

    def save_file(self) -> None:
        # save configuration & exit
        out_file = self.out_file_name.value
        with open(out_file, 'w') as out:
            if self.config_type == 'yaml':
                self.yml_obj.dump(self.new_json_data, out)
            elif self.config_type == 'json':
                json.dump(self.new_json_data, out, indent=2)

        self.app.exit(result=0, message=f'Configuration file exported successfully as [{out_file}]')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'no':
            self.app.pop_screen()
        else:
            self.save_file()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        event.stop()
        self.save_file()


class ConfigurationEditor(App):

    # TITLE = 'Configuration Editor'
    # SUB_TITLE = 'Edit your configuration files'

    BINDINGS = [
        ("o", "toggle_dark", "Toggle dark mode"),
        ("x", "toggle", "Expand/Collapse All"),
        ("i", "insert_node", "Insert Node"),
        ("d", "delete_node", "Delete Node"),
        ("e", "edit", "Edit Value"),
        ("r", "reload", "Reload"),
        ("s", "save", "Save"),
        ("q", "quit", "Quit"),
    ]

    CSS_PATH = CSS_FILE

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.config_file = kwargs['config_file']
        # delimiter to be dispayed in labels of tree
        self.delimiter = ': '
        # label highlighers in tree
        self.default_highlight = 'bold'
        self.edit_highlight = 'bold italic yellow'
        self.insert_highlight = 'bold italic green'
        self.delete_highlight = 'bold italic red'
        # placeholders for edit fields
        self.edit_node_help = "Select a node and press 'E' to edit..."
        self.add_node_help = "Provide input in json/dict format. [Ex: {'key1': 'val1', 'key2': [1, 2]}]"
        # define yaml loader
        self.yaml = YAML()              # by default, uses round-trip loader to load comments
        self.yaml.indent(mapping=2)     # default indentation is 2 spaces
        self.yaml.preserve_quotes = True
        # define type of configuration
        self.config_type = None

    def compose(self) -> ComposeResult:
        self.edit_box = Input(placeholder=self.edit_node_help, id="edit-node")
        self.edit_box.border_title = Text.from_markup('Enter your value [italic](press enter to save)[/]')
        self.json_tree = Tree('ROOT')
        yield Label("Configuration Editor", id='header')
        yield Footer()
        yield self.json_tree
        yield self.edit_box

    def on_mount(self) -> None:
        """Load the JSON when the app starts."""
        # load file
        self.load_file()
        # load into tree
        self.update_tree(self.config_type.upper(), self.json_tree.root, self.json_data, self.default_highlight)
        self.edit_box.disabled = True
        self.cur_node = self.json_tree.root.expand()

    def _text_highlighter_(self, highlighter, key=None, value=None) -> Text:
        """Helper function to highlight label text."""
        if key is not None and value is None:
            # paint label of nested data
            highlighted = Text.from_markup(f"[{highlighter}]{key}[/]")
        elif key is None and value is not None:
            # paint label with only value
            highlighted = Text.assemble(ReprHighlighter()(repr(value)))
        else:
            # paint label with both key and value
            highlighted = Text.assemble(
                Text.from_markup(f"[{highlighter}]{key}[/]{self.delimiter}"), ReprHighlighter()(repr(value))
            )

        return highlighted

    def _traverse_yaml_data_(self, keys: list) -> object:
        """Helper function to traverse the yaml data for a given list of keys

        Returns the corresponding object
        """
        current_dict = self.json_data
        for key in keys:
            current_dict = current_dict[key]

        return current_dict

    def _update_yaml_(self, new_value, action) -> bool:
        """Helper function to update the in-memory yaml

        Returns: True if update is successful, else False
        """
        # no need to update the in-memory yaml if config type is not yaml
        if self.config_type != 'yaml':
            return True

        current_dict = self._traverse_yaml_data_(self.cur_node.data['abs_key'][:-1])

        last_key = self.cur_node.data['abs_key'][-1]

        if action == 'edit':
            if self.cur_node.data['type'] == 'dict':        # handle nested key changes
                # Below steps are unneccessary overhead. When you pop and insert the item is inserted at the end.
                # For maintaining same position of keys, we need to re-insert all keys in the same-level :(
                keys = list(current_dict.keys())            # store keys separately or else you'll see Runtime OrderedDict mutation error
                for key in keys:
                    existing_value = current_dict.pop(key)
                    if key == last_key:
                        current_dict[new_value] = existing_value
                    else:
                        current_dict[key] = existing_value
            else:                                           # handle normal leaf-level key changes
                current_dict[last_key] = new_value
        elif action == 'insert':                            # handle addition of new elements
            if isinstance(current_dict[last_key], dict):
                current_dict[last_key].update(new_value)
            elif isinstance(current_dict[last_key], list):
                current_dict[last_key].append(new_value)
            else:
                current_dict[last_key] = new_value
        elif action == 'delete':                            # handle deletion of an existing element
            current_dict.pop(last_key)

        return True

    def _export_tree_to_json_(self, node):
        """
        Helper function to export a tree to JSON data.

        Args:
            node (TreeNode): Root node of the tree.

        Returns:
            JSON data representing the tree.
        """
        if not node.allow_expand:
            # Leaf node, return the data directly
            return node.data.get('value')
        else:
            # Non-leaf node, build a dictionary or list depending on the node type
            if node.data['type'] == 'dict':
                data = {}
            else:
                data = []

            for child in node.children:
                # Recursively export each child and add it to the dictionary or list
                child_data = self._export_tree_to_json_(child)
                if node.data['type'] == 'dict':
                    key = child.data['key']
                    data[key] = child_data
                else:
                    data.append(child_data)

            return data

    def _invalid_input_handler_(self, err_msg) -> None:
        """Handle error inputs in edit field."""
        self.edit_box.border_subtitle = f'{err_msg}'
        self.edit_box.styles.animate(attribute='background', value='red', duration=1.0, final_value=None)

    def update_tree(self, name: str, node: TreeNode, data: object, highlighter) -> None:
        """Adds a node to the tree.

        Args:
            name (str): Name of the node.
            node (TreeNode): Parent node.
            data (object): Data associated with the node.
        """

        def _get_type_(val) -> str:
            typ = str(type(val)).split("'")[1]
            # convert ruamel types to generic types
            typ = typ.replace('ruamel.yaml.comments.CommentedMap', 'dict').replace('ruamel.yaml.comments.CommentedSeq', 'list')
            return typ

        # add complete path of the key. populate it as a list of keys to preserve data type
        if node.is_root:
            abs_key = []
        else:
            abs_key = node.parent.data.get('abs_key').copy()
            abs_key.append(name)

        val_type = _get_type_(data)
        node.data = {
            'key': name,
            'value': name,
            'type': val_type,
            'abs_key': abs_key
        }
        if isinstance(data, dict):
            node.set_label(self._text_highlighter_(highlighter, f'{{}} {name}'))
            node.data.update({
                'editable': edit_dict_keys
            })
            for key, value in data.items():
                new_node = node.add("")
                self.update_tree(key, new_node, value, highlighter)
        elif isinstance(data, list):
            node.set_label(self._text_highlighter_(highlighter, f'[] {name}'))
            node.data.update({
                'editable': False
            })
            start_idx = len(node.children)  # start from an index depending on number of existing elements
            for index, value in enumerate(data):
                new_node = node.add("")
                # self.update_tree(None, new_node, value, highlighter)
                self.update_tree(index + start_idx, new_node, value, highlighter)
        else:
            node.allow_expand = False
            # add both key and value to label for displaying
            label = self._text_highlighter_(highlighter, name, data)
            node.set_label(label)
            # add data separately to node
            node.data.update({
                'value': data,
                'editable': True
            })

    def load_file(self) -> None:
        """Load the YAML file as JSON."""
        with open(self.config_file, 'r') as conf:
            # check if file is yaml
            try:
                self.json_data = self.yaml.load(conf)
                self.config_type = 'yaml'
            except:
                pass

            conf.seek(0)
            # check if file is json
            try:
                self.json_data = json.load(conf)
                self.config_type = 'json'
            except:
                pass

        if self.config_type is None:
            self.app.exit(result=1, message=f'Invalid configuration file. File must be a valid json/yaml file.')

    def edit_value(self) -> bool:
        """Update the value in a node.

        Returns:
            boolean status whether update is successful
        """

        old_value = self.cur_node.data.get('value')
        new_value = self.edit_box.value

        if allow_value_data_type_changes:
            # infer value type
            exprsn = f'{new_value}'
        elif self.cur_node.data.get('type') == 'str':
            # keep it in quotes to evalute as string
            exprsn = f'"{new_value}"'
        elif self.cur_node.data.get('type') in ['dict', 'list']:
            # cast value to it's originial type based on key's type
            typ = str(type(self.cur_node.data.get('key'))).split("'")[1]
            exprsn = f"{typ}({new_value})"
        else:
            # cast value to it's originial type
            exprsn = f"{self.cur_node.data.get('type')}({new_value})"

        try:
            new_value = eval(exprsn)
            if isinstance(new_value, (dict, list)):
                status = self.add_new_node()             # call add node function if new data type is nested
                return status
        except Exception as e:
            if allow_value_data_type_changes:
                pass
            else:
                self._invalid_input_handler_(f'INVALID VALUE. Error: {e}')
                return False    # do not make any changes if conversion failed

        # skip if there is no change
        if old_value == new_value:
            return True

        if self.cur_node.data.get('type') == 'dict':
            new_label = self._text_highlighter_(self.edit_highlight, f"{{}} {new_value}")
        elif self.cur_node.data.get('type') == 'list':
            new_label = self._text_highlighter_(self.edit_highlight, f"[] {new_value}")
        else:
            new_label = self._text_highlighter_(self.edit_highlight, self.cur_node.data['key'], new_value)
            # highligh parent node if edited value is in a list
            if self.cur_node.parent.data.get('type') == 'list':
                self.cur_node.parent.set_label(self._text_highlighter_(self.edit_highlight, f"{self.cur_node.parent.label}"))

        # update in-memory yaml object
        status = self._update_yaml_(new_value, action='edit')
        # update key for expandable/nested data
        if self.cur_node.data.get('type') in ['dict', 'list']:
            self.cur_node.data['key'] = new_value
            # update absolute key by replacing last occurrence with new value
            self.cur_node.data['abs_key'][-1] = new_value
        self.cur_node.data['value'] = new_value
        self.cur_node.set_label(new_label)

        return status

    def add_new_node(self) -> bool:
        """Add a new node to the tree.

        Returns:
            boolean status whether insertion is successful
        """
        data = self.edit_box.value
        try:
            data = eval(data)
            if self.cur_node.data['type'] == 'dict' and not isinstance(data, dict):
                raise Exception('Value must be a dictionary for a node of dict type')
        except Exception as e:
            self._invalid_input_handler_(f'INVALID FORMAT. Error: {e}')
            return False

        status = self._update_yaml_(data, action='insert')

        # convert leaf node to expandable
        self.cur_node.allow_expand = True
        if self.cur_node.data['type'] == 'list':
            data = [data]       # wrap data into list to render tree
        self.update_tree(self.cur_node.data['key'], self.cur_node, data, self.insert_highlight)
        if status: self.edit_box.value = ''        # reset edit field value

        return status

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_toggle(self) -> None:
        """An action to show/hide entire configuration."""
        if self.json_tree.root.is_expanded:
            self.json_tree.root.collapse_all()
        else:
            self.json_tree.root.expand_all()

    def action_reload(self, reload_from_disk=True) -> None:
        """Reload the configuration file."""
        # clear tree first
        tree = self.json_tree
        tree.clear()
        if reload_from_disk:
            # re-load file from disk
            self.load_file()
        # re-create tree
        self.update_tree('ROOT', tree.root, self.json_data, self.default_highlight)

    def action_edit(self) -> None:
        if not self.cur_node.data.get('editable') or self.cur_node.is_root:
            return      # do not allow edits if it is root or node is not editable

        if self.cur_node.parent.data['type'] == 'list' and self.cur_node.data['type'] == 'dict':
            return      # do not allow key edits if node is a dictionary in a list

        # set edit field properties for updates
        self.edit_box.placeholder = self.edit_node_help
        self.edit_box.tooltip = None
        if self.cur_node.data.get('editable'):
            self.edit_box.value = str(self.cur_node.data.get('value'))
            self.edit_box.disabled = False
        else:
            self.edit_box.value = ''
            self.edit_box.disabled = True

        # change focus to input box for editing
        self.edit_box.focus()

    @on(Tree.NodeHighlighted)
    def toggle_edit_field(self, event: Tree.NodeHighlighted) -> None:
        event.stop()
        # track the current node in the tree
        self.cur_node = event.node
        # reset edit field before any changes
        self.edit_box.border_subtitle = ''
        self.edit_box.placeholder = self.edit_node_help
        self.edit_box.tooltip = self.edit_node_help
        self.edit_box.disabled = True
        # preview value in the edit box
        if self.cur_node.data.get('editable'):
            self.edit_box.value = str(self.cur_node.data.get('value'))
        else:
            self.edit_box.value = ''

    @on(Input.Submitted)
    def edit_field_handler(self, event: Input.Submitted) -> None:
        event.stop()
        # check for input type: edit or add
        if self.edit_box.placeholder == self.edit_node_help:
            status = self.edit_value()
        elif self.edit_box.placeholder == self.add_node_help:
            status = self.add_new_node()

        if status:
            # reset edit field
            self.edit_box.border_subtitle = ''
            self.edit_box.disabled = True
            # once input submitted change focus to tree for viewing
            self.json_tree.focus()

    def action_insert_node(self) -> None:
        """Add new nodes under the selected node"""
        # set edit field properties for insertion
        self.edit_box.placeholder = self.add_node_help
        self.edit_box.tooltip = self.add_node_help
        self.edit_box.value = ''
        self.edit_box.disabled = False
        # change focus to input box for editing
        self.edit_box.focus()

    def action_delete_node(self) -> None:
        """Remove the selected node."""
        # do not delete root node
        if not self.cur_node.data.get('abs_key'):
            return
        
        def get_return_status(status: bool) -> None:
            """Called when AlertScreen is dismissed."""
            if status:
                # delete the node on confirmation
                try:
                    self._update_yaml_(None, action='delete')
                    self.cur_node.remove()
                except TreeNode.RemoveRootError as rre:
                    pass

                parent = self.cur_node.parent
                # repaint if parent is a list to refresh numbering inside the list only for in-memory yaml
                if parent.data['type'] == 'list' and self.config_type == 'yaml':
                    parent.remove_children()
                    self.update_tree(parent.data['key'], parent, self._traverse_yaml_data_(parent.data['abs_key']), self.default_highlight)

                # highlight parent node to indicate change
                parent.set_label(self._text_highlighter_(self.delete_highlight, parent.label))

                # reset cursor to parent & generate a node event for updates
                self.json_tree.select_node(parent)
                self.toggle_edit_field(self.json_tree.NodeHighlighted(parent))

        confirm_screen = AlertScreen(message=f"Delete node \[{' > '.join(str(k) for k in self.cur_node.data['abs_key'])}] ?")
        self.push_screen(confirm_screen, get_return_status)

    def action_save(self) -> None:
        """Save the configuration changes."""

        if self.config_type == 'yaml':              # load in-memory yaml data
            new_data = self.json_data
        elif self.config_type == 'json':            # lazy load the updated data from tree if config type is json
            new_data = self._export_tree_to_json_(self.json_tree.root)

        # send user to Save As popup
        self.push_screen(SaveScreen(input_file=self.config_file, config_type=self.config_type, data=new_data, yml_obj=self.yaml))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ConfigTUI to view/edit yaml files using a TUI')
    parser.add_argument('-v', '--version', action='version', version=f'{os.path.basename(__file__)} v{__version__}')
    parser.add_argument('-i', '--input', required=True, type=str, help='yaml configuration file to be loaded')
    parser.add_argument('-edk', '--edit-dict-keys', action='store_true', default=False, help='enable editing keys with nested data [default: disabled]')
    parser.add_argument('-sdt', '--enable-strict-data-types', action='store_false', default=True, help='enforce strict data type while editing [default: disabled]')

    args = parser.parse_args()
    input_file = args.input
    edit_dict_keys = args.edit_dict_keys
    allow_value_data_type_changes = args.enable_strict_data_types

    if not os.path.isfile(input_file):
        print(f'Config file [{input_file}] not found')
        exit(1)

    ce_tui = ConfigurationEditor(config_file=input_file)
    ce_tui.run()