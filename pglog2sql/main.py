#!/usr/bin/env python
# -*- coding: utf_8 -*
# (C) Copyright 2008-2011 Nuxeo SAS <http://nuxeo.com>
# Authors: Benoit Delbosc <ben@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
"""
Generate a prepared statement and and execute query from a PostgreSQL log.
"""
import sys
from optparse import OptionParser, TitledHelpFormatter
from util import get_version

USAGE = """pglog2sql [--version] [--name prepared_statement_name] [log_file|STDIN]


EXAMPLES

   echo "<paste logged query>" | pglog2sql
"""

import fileinput


def get_input(files):
    lines = []
    for line in fileinput.input(files):
        if line and line.strip():
            lines.append(line.strip())
    return '\n'.join(lines)


def split_query(log):
    assert('execute ' in log)
    DP = "DETAIL:  parameters: "
    assert(DP in log)
    s = log.find('execute ')
    s = log.find(': ', s)
    e = log.find(DP, s)
    query = log[s + 2:e]
    params = log[e + len(DP):]
    return query, params


def clean_query(query):
    return query.replace('"', '')


def get_prepare(name, query, types):
    ret = "DEALLOCATE " + name + ";\n"
    ret += "PREPARE " + name + "(" + ', '.join(types) + ') AS\n'
    ret += query.strip()
    if ';' not in query:
        ret += ';'
    ret += "\n"
    return ret


def get_execute(name, values):
    ret = "EXPLAIN ANALYZE EXECUTE " + name + "(" + ', '.join(values) + ');'
    return ret


def guess_type(value):
    if value.startswith("'{"):
        return "text[]"
    if value.startswith("'"):
        return 'text'
    return 'int'


def parse_params(params, verbose=False):
    values = [kv.split('=')[1].strip() for kv in params.split(', ')]
    types = [guess_type(value) for value in values]
    if verbose:
        for i in range(len(types)):
            print "%i %s\t %s" % (i + 1, types[i], values[i])
        print len(types)
    return values, types


def process(name, log, verbose=False):
    query, params = split_query(log)
    query = clean_query(query)
    values, types = parse_params(params, verbose)
    pquery = get_prepare(name, query, types)
    execute = get_execute(name, values)
    return pquery + "\n" + execute


def main(argv=sys.argv):
    """Main test"""
    global USAGE
    parser = OptionParser(USAGE, formatter=TitledHelpFormatter(),
                          version="pglog2sql %s" % get_version())
    parser.add_option("-n", "--name", default="foo",
                      help="Prepared statement name")
    parser.add_option("-v", "--verbose", action="store_true",
                      help="Verbose output")
    options, args = parser.parse_args(argv)
    log = get_input(args[1:])
    ret = process(options.name, log, verbose=options.verbose)
    print ret

if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
