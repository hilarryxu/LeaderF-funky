# coding: utf-8

import os
import os.path
import re

import vim

from leaderf.utils import (
    lfEncode, lfCmd, lfEval, lfPrintError,
    escQuote
)
from leaderf.explorer import Explorer
from leaderf.manager import Manager

MODE_FULLPATH = 0
MODE_NAMEONLY = 1
MODE_DESC = 2

default_ft_filters = {
    'python': [
        {
            'pattern': r'^\s*(def|class)\s+([a-zA-Z0-9_]+)\s*[:\(]'
        }
    ]
}


class FunkyExplorer(Explorer):
    def getContent(self, *args, **kwargs):
        ft = lfEval('&filetype') or ''
        filters = default_ft_filters.get(ft, [])
        if not filters:
            return

        lst = []
        buffer = vim.current.buffer
        for line_nr, line in enumerate(buffer, 1):
            for filter_ in filters:
                if '_regex' not in filter_:
                    filter_['_regex'] = re.compile(filter_['pattern'])
                regex = filter_['_regex']
                if regex.match(line):
                    s = "%s\t[%d %d]" % (line, line_nr, buffer.number)
                    lst.append(s)
                    break
        return lst

    def getStlCategory(self):
        return 'Funky'

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def isFilePath(self):
        return False


class FunkyManager(Manager):
    def __init__(self):
        super(FunkyManager, self).__init__()
        self._match_ids = []

    def _getExplClass(self):
        return FunkyExplorer

    def _defineMaps(self):
        lfCmd('call leaderf#funky#define_maps()')

    def _acceptSelection(self, *args, **kwargs):
        if not args:
            return

        line = args[0]
        # line_no buf_num
        location = line.rsplit("\t", 1)[1][1:-1]
        line_nr, buf_num = location.split()
        lfCmd('hide buffer +%s %s' % (line_nr, buf_num))
        lfCmd('normal! ^')
        lfCmd('normal! zz')
        lfCmd('setlocal cursorline! | redraw | sleep 100m | setlocal cursorline!')

    def _getDigest(self, line, mode):
        return line.rsplit("\t", 1)[0]

    def _getDigestStartPos(self, line, mode):
        return 0

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : goto to funky under cursor')
        help.append('" x : open file under cursor in a horizontally split window')
        help.append('" v : open file under cursor in a vertically split window')
        help.append('" t : open file under cursor in a new tabpage')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" ---------------------------------------------------------')
        return help

    def _afterEnter(self):
        super(FunkyManager, self)._afterEnter()
        mid = int(lfEval('''matchadd('Lf_hl_funkyLocation', '\t\zs\[\d\+ \d\+]$')'''))
        self._match_ids.append(mid)

    def _beforeExit(self):
        super(FunkyManager, self)._beforeExit()
        for mid in self._match_ids:
            lfCmd('silent! call matchdelete(%d)' % mid)
        self._match_ids = []


leader_funky_man = FunkyManager()
