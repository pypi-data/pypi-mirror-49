from __future__ import absolute_import

import collections
import logging
import os
import re

from ins._vendor import six
from ins._vendor.packaging.utils import canonicalize_name
from ins._vendor.pkg_resources import RequirementParseError

from ins._internal.exceptions import BadCommand, InstallationError
from ins._internal.req.constructors import (
    install_req_from_editable, install_req_from_line,
)
from ins._internal.req.req_file import COMMENT_RE
from ins._internal.utils.misc import (
    dist_is_editable, get_installed_distributions,
)
from ins._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from typing import (
        Iterator, Optional, List, Container, Set, Dict, Tuple, Iterable, Union
    )
    from ins._internal.cache import WheelCache
    from ins._vendor.pkg_resources import (
        Distribution, Requirement
    )

    RequirementInfo = Tuple[Optional[Union[str, Requirement]], bool, List[str]]


logger = logging.getLogger(__name__)


def freeze(
    requirement=None,  # type: Optional[List[str]]
    find_links=None,  # type: Optional[List[str]]
    local_only=None,  # type: Optional[bool]
    user_only=None,  # type: Optional[bool]
    skip_regex=None,  # type: Optional[str]
    isolated=False,  # type: bool
    wheel_cache=None,  # type: Optional[WheelCache]
    exclude_editable=False,  # type: bool
    skip=()  # type: Container[str]
):
    # type: (...) -> Iterator[str]
    find_links = find_links or []
    skip_match = None

    if skip_regex:
        skip_match = re.compile(skip_regex).search

    for link in find_links:
        yield '-f %s' % link
    installations = {}  # type: Dict[str, FrozenRequirement]
    for dist in get_installed_distributions(local_only=local_only,
                                            skip=(),
                                            user_only=user_only):
        try:
            req = FrozenRequirement.from_dist(dist)
        except RequirementParseError:
            logger.warning(
                "Could not parse requirement: %s",
                dist.project_name
            )
            continue
        if exclude_editable and req.editable:
            continue
        installations[req.name] = req

    if requirement:
        # the options that don't get turned into an InstallRequirement
        # should only be emitted once, even if the same option is in multiple
        # requirements files, so we need to keep track of what has been emitted
        # so that we don't emit it again if it's seen again
        emitted_options = set()  # type: Set[str]
        # keep track of which files a requirement is in so that we can
        # give an accurate warning if a requirement appears multiple times.
        req_files = collections.defaultdict(list)  # type: Dict[str, List[str]]
        for req_file_path in requirement:
            with open(req_file_path) as req_file:
                for line in req_file:
                    if (not line.strip() or
                            line.strip().startswith('#') or
                            (skip_match and skip_match(line)) or
                            line.startswith((
                                '-r', '--requirement',
                                '-Z', '--always-unzip',
                                '-f', '--find-links',
                                '-i', '--index-url',
                                '--pre',
                                '--trusted-host',
                                '--process-dependency-links',
                                '--extra-index-url'))):
                        line = line.rstrip()
                        if line not in emitted_options:
                            emitted_options.add(line)
                            yield line
                        continue

                    if line.startswith('-e') or line.startswith('--editable'):
                        if line.startswith('-e'):
                            line = line[2:].strip()
                        else:
                            line = line[len('--editable'):].strip().lstrip('=')
                        line_req = install_req_from_editable(
                            line,
                            isolated=isolated,
                            wheel_cache=wheel_cache,
                        )
                    else:
                        line_req = install_req_from_line(
                            COMMENT_RE.sub('', line).strip(),
                            isolated=isolated,
                            wheel_cache=wheel_cache,
                        )

                    if not line_req.name:
                        logger.info(
                            "Skipping line in requirement file [%s] because "
                            "it's not clear what it would install: %s",
                            req_file_path, line.strip(),
                        )
                        logger.info(
                            "  (add #egg=PackageName to the URL to avoid"
                            " this warning)"
                        )
                    elif line_req.name not in installations:
                        # either it's not installed, or it is installed
                        # but has been processed already
                        if not req_files[line_req.name]:
                            logger.warning(
                                "Requirement file [%s] contains %s, but "
                                "package %r is not installed",
                                req_file_path,
                                COMMENT_RE.sub('', line).strip(), line_req.name
                            )
                        else:
                            req_files[line_req.name].append(req_file_path)
                    else:
                        yield str(installations[line_req.name]).rstrip()
                        del installations[line_req.name]
                        req_files[line_req.name].append(req_file_path)

        # Warn about requirements that were included multiple times (in a
        # single requirements file or in different requirements files).
        for name, files in six.iteritems(req_files):
            if len(files) > 1:
                logger.warning("Requirement %s included multiple times [%s]",
                               name, ', '.join(sorted(set(files))))

        yield(
            '## The following requirements were added by '
            'ins freeze:'
        )
    for installation in sorted(
            installations.values(), key=lambda x: x.name.lower()):
        if canonicalize_name(installation.name) not in skip:
            yield str(installation).rstrip()


def get_requirement_info(dist):
    # type: (Distribution) -> RequirementInfo
    """
    Compute and return values (req, editable, comments) for use in
    FrozenRequirement.from_dist().
    """
    if not dist_is_editable(dist):
        return (None, False, [])

    location = os.path.normcase(os.path.abspath(dist.location))

    from ins._internal.vcs import vcs, RemoteNotFoundError
    vc_type = vcs.get_backend_type(location)

    if not vc_type:
        req = dist.as_requirement()
        logger.debug(
            'No VCS found for editable requirement {!r} in: {!r}', req,
            location,
        )
        comments = [
            '# Editable install with no version control ({})'.format(req)
        ]
        return (location, True, comments)

    try:
        req = vc_type.get_src_requirement(location, dist.project_name)
    except RemoteNotFoundError:
        req = dist.as_requirement()
        comments = [
            '# Editable {} install with no remote ({})'.format(
                vc_type.__name__, req,
            )
        ]
        return (location, True, comments)

    except BadCommand:
        logger.warning(
            'cannot determine version of editable source in %s '
            '(%s command not found in path)',
            location,
            vc_type.name,
        )
        return (None, True, [])

    except InstallationError as exc:
        logger.warning(
            "Error when trying to get requirement for VCS system %s, "
            "falling back to uneditable format", exc
        )
    else:
        if req is not None:
            return (req, True, [])

    logger.warning(
        'Could not determine repository location of %s', location
    )
    comments = ['## !! Could not determine repository location']

    return (None, False, comments)


class FrozenRequirement(object):
    def __init__(self, name, req, editable, comments=()):
        # type: (str, Union[str, Requirement], bool, Iterable[str]) -> None
        self.name = name
        self.req = req
        self.editable = editable
        self.comments = comments

    @classmethod
    def from_dist(cls, dist):
        # type: (Distribution) -> FrozenRequirement
        req, editable, comments = get_requirement_info(dist)
        if req is None:
            req = dist.as_requirement()

        return cls(dist.project_name, req, editable, comments=comments)

    def __str__(self):
        req = self.req
        if self.editable:
            req = '-e %s' % req
        return '\n'.join(list(self.comments) + [str(req)]) + '\n'
