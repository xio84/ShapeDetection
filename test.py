from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
Window.size = (500, 200)


def populate_tree_view(tree_view, parent, node):
    if parent is None:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True))
    else:
        tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                     is_open=True), parent)

    for child_node in node['children']:
        populate_tree_view(tree_view, tree_node, child_node)


tree = []
rows = [(1, 'test1', 11), (2, 'test2', 2), (3, 'test3', 3)]
for r in rows:
    tree.append({'node_id': r[1], 'children': []})



class TreeViewLabel(Label, TreeViewNode):
    pass


class TreeviewGroup(Popup):
    treeview = ObjectProperty(None)
    tv = ObjectProperty(None)
    #ti = ObjectProperty()

    def __init__(self, **kwargs):
        super(TreeviewGroup, self).__init__(**kwargs)
        self.tv = TreeView(root_options=dict(text=""),
                       hide_root=False,
                       indent_level=4)
        for branch in tree:
            populate_tree_view(self.tv, None, branch)
        self.remove_widgets()
        self.treeview.add_widget(self.tv)

    def remove_widgets(self):
        for child in [child for child in self.treeview.children]:
            self.treeview.remove_widget(child)

    def select_node(self, node):
        '''Select a node in the tree.
                '''
        if node.no_selection:
            return
        if self._selected_node:
            self._selected_node.is_selected = False
        node.is_selected = True
        self._selected_node = node
        print(node)

class GroupScreen(Screen):
    name = ObjectProperty(None)
    popup = ObjectProperty(None)

    def display_groups(self, instance):
        if len(instance.text) > 0:
            if self.popup is None:
                self.popup = TreeviewGroup()
            #self.popup.filter(instance.text)
            self.popup.open()


    def select_node(self, node):
        '''Select a node in the tree.
                '''
        if node.no_selection:
            return
        if self._selected_node:
            self._selected_node.is_selected = False
        node.is_selected = True
        self._selected_node = node
        print(node)


class Group(App):
    def build(self):
        self.root = Builder.load_file('test.kv')
        return self.root


if __name__ == '__main__':
    Group().run()