# This file is part of ubuntu-bug-triage. See LICENSE file for license info.
"""Triage module."""

import json
import os
import textwrap

from tabulate import tabulate


class BaseView:
    """Base view class."""


class TerminalView(BaseView):
    """Terminal view class."""

    def __init__(self, bugs):
        """Initialize terminal view."""
        _, self.term_columns = os.popen('stty size', 'r').read().split()

        # The table has a set number characters that always exist:
        #     4 for '|' boarders
        #     6 for spaces around content
        #    12 for 'LP: #1234567'
        width_table = 22

        # This seemed liked the best middle of the road value
        width_affects = 20

        # The title width will expand as the terminal expands,
        # but will expect a width no less than 80
        width_title = (max(80, int(self.term_columns)) -
                       width_affects - width_table)

        table = []
        for bug in bugs:
            affects = [
                textwrap.fill(
                    pkg.replace('(Ubuntu)', '(U)').replace('(Debian)', '(D)'),
                    width=width_affects,
                    subsequent_indent='    '
                ) for pkg in bug.affects
            ]

            table.append([
                'LP: #%s' % bug.id,
                '\n'.join(affects),
                textwrap.fill(bug.title, width=width_title, max_lines=4),
            ])

        print(tabulate(table, ['id', 'affects', 'title'], 'grid'))


class CSVView(BaseView):
    """CSV view class."""

    def __init__(self, bugs):
        """Initialize CSV view."""
        print('id,affects,title')
        for bug in bugs:
            print('LP: #%s,"%s",%s' % (
                bug.id, ','.join(bug.affects), bug.title
            ))


class JSONView(BaseView):
    """JSON view class."""

    def __init__(self, bugs):
        """Initialize JSON view."""
        print(json.dumps(
            [bug.to_json() for bug in bugs],
            indent=4,
            ensure_ascii=False
        ))