from ins._vendor.packaging.utils import canonicalize_name

from ins._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from typing import Optional, Set, FrozenSet


class FormatControl(object):
    """Helper for managing formats from which a package can be installed.
    """

    def __init__(self, no_binary=None, only_binary=None):
        # type: (Optional[Set], Optional[Set]) -> None
        if no_binary is None:
            no_binary = set()
        if only_binary is None:
            only_binary = set()

        self.no_binary = no_binary
        self.only_binary = only_binary

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "{}({}, {})".format(
            self.__class__.__name__,
            self.no_binary,
            self.only_binary
        )

    @staticmethod
    def handle_mutual_excludes(value, target, other):
        # type: (str, Optional[Set], Optional[Set]) -> None
        new = value.split(',')
        while ':all:' in new:
            other.clear()
            target.clear()
            target.add(':all:')
            del new[:new.index(':all:') + 1]
            # Without a none, we want to discard everything as :all: covers it
            if ':none:' not in new:
                return
        for name in new:
            if name == ':none:':
                target.clear()
                continue
            name = canonicalize_name(name)
            other.discard(name)
            target.add(name)

    def get_allowed_formats(self, canonical_name):
        # type: (str) -> FrozenSet
        result = {"binary", "source"}
        if canonical_name in self.only_binary:
            result.discard('source')
        elif canonical_name in self.no_binary:
            result.discard('binary')
        elif ':all:' in self.only_binary:
            result.discard('source')
        elif ':all:' in self.no_binary:
            result.discard('binary')
        return frozenset(result)

    def disallow_binaries(self):
        # type: () -> None
        self.handle_mutual_excludes(
            ':all:', self.no_binary, self.only_binary,
        )
