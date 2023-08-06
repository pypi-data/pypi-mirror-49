import sys
from collections import defaultdict

from phyltr.commands.base import PhyltrCommand


class MonophylyFailure(Exception):
    """Raised when asked to collapse a non monophyletic taxon set."""


class Collapse(PhyltrCommand):
    """
    Collapse monophyletic sets of leaf nodes, by turning their MRCA into a leaf,
    and giving the newly formed leaf a specified label.
    """
    __options__ = [
        (
            ('-a', '--attribute'),
            dict(
                dest="attribute", default=None,
                help="Specify an attribute by which to collapse clades instead of a translation "
                     "file.  Clades will only be collapsed for attribute values which are "
                     "monophyletic.")),
        (
            ('-t', '--translate'),
            dict(
                dest="filename", default=None,
                help='The filename of the translate file.  Each line of the translate file should '
                     'be of the format: "label:taxa1,taxa2,taxa3,....". The MRCA of the specified '
                     'taxa will be replaced by a leaf named "label".')),
    ]

    def __init__(self, clades=None, **kw):
        PhyltrCommand.__init__(self, **kw)
        if clades:
            self.trans = clades  # trans = translation
        elif self.opts.filename:
            self.read_clade_file(self.opts.filename)
        elif self.opts.attribute:
            self.trans = {}
        else:
            raise ValueError("Must provide a dictionary of clades, a filename or an attribute.")

    def process_tree(self, t, _):
        return self.collapse_by_dict(t) if self.trans else self.collapse_by_attribute(t)

    def read_clade_file(self, filename):

        """Read a file of names and clade definitions and return a dictionary of
        this data."""

        self.trans = {}
        with open(filename, "r") as fp:
            for line in fp:
                name, clade = line.strip().split(":")
                clade = clade.strip().split(",")
                self.trans[name] = clade

    def collapse_by_dict(self, t):
        cache = t.get_cached_content()
        tree_leaves = cache[t]
        for name, clade in self.trans.items():
            # Get a list of leaves in this tree
            clade_leaves = [l for l in tree_leaves if l.name in clade]
            if not clade_leaves:
                continue
            try:
                self.test_monophyly_and_collapse(t, cache, name, clade_leaves)
            except MonophylyFailure:
                # Clade is not monophyletic.  We can't collapse it.
                sys.stderr.write("Monophyly failure for clade: %s\n" % name)
        return t

    def collapse_by_attribute(self, t):
        cache = t.get_cached_content()
        tree_leaves = cache[t]
        # Build a dictionary mapping attribute values to lists of leaves
        values = defaultdict(list)
        for leaf in tree_leaves:
            if hasattr(leaf, self.opts.attribute):
                values[getattr(leaf, self.opts.attribute)].append(leaf)
        # Do monophyly tests
        for value, clade_leaves in values.items():
            try:
                self.test_monophyly_and_collapse(t, cache, value, clade_leaves)
            except MonophylyFailure:
                # Clade is not monophyletic.  We can't collapse it.
                sys.stderr.write(
                    "Monophyly failure for attribute value: %s=%s\n" % (self.opts.attribute, value))
        return t

    def test_monophyly_and_collapse(self, t, cache, clade, clade_leaves):
        # Check monophyly
        if len(clade_leaves) == 1:
            mrca = clade_leaves[0]  # .get_common_ancestor works oddly for singletons
        else:
            mrca = t.get_common_ancestor(clade_leaves)
        mrca_leaves = cache[mrca]
        if set(mrca_leaves) != set(clade_leaves):
            raise MonophylyFailure

        # Clade is monophyletic, so rename and prune
        # But don't mess up distances
        mrca.name = clade
        leaf, dist = mrca.get_farthest_leaf()
        mrca.dist += dist
        for child in mrca.get_children():
            child.detach()
