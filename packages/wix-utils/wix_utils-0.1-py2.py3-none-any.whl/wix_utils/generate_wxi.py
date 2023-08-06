# Copyright (C) 2011-2019 Vanderbilt University
# Copyright (C) 2013-2019 MetaMorph Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this data, including any software or models in source or binary
# form, as well as any drawings, specifications, and documentation
# (collectively "the Data"), to deal in the Data without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Data, and to
# permit persons to whom the Data is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Data.
#
# THE DATA IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS, SPONSORS, DEVELOPERS, CONTRIBUTORS, OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE DATA OR THE USE OR OTHER DEALINGS IN THE DATA.


import sys
import os
import os.path
import hashlib
import re
import errno
import itertools
import tempfile
import hashlib
import subprocess

import xml.etree.ElementTree
import xml.sax
from xml.sax.handler import ContentHandler
ElementTree = xml.etree.ElementTree

prefs = { 'verbose': True }

def system(args, dirname=None):
    """
    Executes a system command (throws an exception on error)
    params
        args : [command, arg1, arg2, ...]
        dirname : if set, execute the command within this directory
    """
    #print args
    with open(os.devnull, "w") as nulfp:
        # n.b. stderr=subprocess.STDOUT fails mysteriously
        import sys
        subprocess.check_call(args, stdout=(sys.stdout if prefs['verbose'] else nulfp), stderr=subprocess.STDOUT, shell=False, cwd=dirname)

# http://bugs.python.org/issue8277
class CommentedTreeBuilder(ElementTree.TreeBuilder):
    def __init__(self, html=0, target=None):
        ElementTree.TreeBuilder.__init__(self, html)
        self._parser.CommentHandler = self.handle_comment

    def handle_comment(self, data):
        self._target.start(ElementTree.Comment, {})
        self._target.data(data)
        self._target.end(ElementTree.Comment)

#http://effbot.org/zone/element-lib.htm#prettyprint
def _indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def gen_dir_from_vc(src, output_filename=None, id=None, diskId=None, file_map={}):
    while src[-1] in ('/', '\\'):
        src = src[:-1]
    name = os.path.basename(src)
    id = id or name.replace('-', '_').replace(' ', '_')
    output_filename = output_filename or (id + ".wxi")

    ElementTree.register_namespace("", "http://schemas.microsoft.com/wix/2006/wi")
    wix = ElementTree.Element("{http://schemas.microsoft.com/wix/2006/wi}Wix")
    SubElement = ElementTree.SubElement
    fragment = SubElement(wix, "Fragment")
    root_dir = SubElement(fragment, "DirectoryRef")
    root_dir.set("Id", id)
    component_group = SubElement(fragment, "ComponentGroup")
    component_group.set("Id", id)
    dirs = {}
    def get_dir(dirname):
        if dirname == src:
            return root_dir
        dir_ = dirs.get(dirname)
        if dir_ is None:
            parent = get_dir(os.path.dirname(dirname))
            dir_ = SubElement(parent, 'Directory')
            dir_.set('Name', os.path.basename(dirname))
            # "Identifiers may contain ASCII characters A-Z, a-z, digits, underscores (_), or periods (.)"
            dir_.set('Id', 'dir_' + re.sub('[^A-Za-z0-9_]', '_', os.path.relpath(dirname, '..').replace('\\', '_').replace('.', '_').replace('-', '_')))
            # "Standard identifiers are 72 characters long or less."
            if len(dir_.attrib['Id']) > 72:
                dir_.set('Id', 'dir_' + hashlib.md5(dirname).hexdigest())
            dirs[dirname] = dir_
        return dir_

    import subprocess
    # git ls-files should show files to-be-added too
    svn_status = subprocess.Popen('git ls-files'.split() + [src], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = svn_status.communicate()
    exit_code = svn_status.poll()
    if exit_code != 0:
        raise Exception('svn status failed: ' + err)
    for filename in (line.replace("/", "\\") for line in out.splitlines()):
        # print filename
        if filename == src or os.path.isdir(filename):
            continue
        dir_ = get_dir(os.path.dirname(filename))
        mapped_filename = file_map.get(os.path.normpath(filename), -1)
        if mapped_filename is None:
            continue
        elif mapped_filename != -1:
            filename = mapped_filename

        component = SubElement(component_group, 'Component')
        component.set('Directory', dir_.attrib['Id'])
        component.set('Id', 'cmp_' + hashlib.md5(filename).hexdigest())
        file_ = SubElement(component, 'File')
        file_.set('Source', filename)
        file_.set('Id', get_file_id(filename))
        if diskId:
            component.attrib['DiskId'] = diskId

    _indent(wix)
    ElementTree.ElementTree(wix).write(output_filename, xml_declaration=True, encoding='utf-8')


def get_file_id(filename):
    return 'fil_' + hashlib.md5(filename).hexdigest()

def download_file(url, filename):
    import requests
    if os.path.isfile(filename):
        return
    print('Downloading {} => {}'.format(url, filename))
    if os.path.dirname(filename):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    r = requests.get(url, stream=True)
    r.raise_for_status()
    fd, tmp_path = tempfile.mkstemp()
    # wix bootstrapper uses SHA1
    hash = hashlib.sha1()
    with os.fdopen(fd, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                hash.update(chunk)
                f.write(chunk)
        # n.b. don't use f.tell(), since it will be wrong for Content-Encoding: gzip
        downloaded_octets = r.raw._fp_bytes_read
    if int(r.headers.get('content-length', downloaded_octets)) != downloaded_octets:
        os.unlink(tmp_path)
        raise ValueError('Download of {} was truncated: {}/{} bytes'.format(url, downloaded_octets, r.headers['content-length']))
    else:
        os.rename(tmp_path, filename)
        print('  => {} {}'.format(filename, hash.hexdigest()))


class WixProcessingInstructionHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.defines = {}

    def processingInstruction(self, target, data):
        if target == 'define':
            eval(compile(data, '<string>', 'exec'), globals(), self.defines)
        elif target == 'include':
            pass  # TODO


def download_bundle_deps(bundle_wxs):
    defines = WixProcessingInstructionHandler()
    xml.sax.parse("bundle_defines.xml", defines)
    xml.sax.parse("META_bundle_x64.wxs", defines)

    def eval_vars(attr):
        for name, val in defines.defines.iteritems():
            attr = attr.replace('$(var.{})'.format(name), str(val))
        return attr

    # , parser=CommentedTreeBuilder()
    tree = ElementTree.parse(bundle_wxs).getroot()
    ElementTree.register_namespace("", "http://schemas.microsoft.com/wix/2006/wi")

    for package in itertools.chain(tree.findall(".//{http://schemas.microsoft.com/wix/2006/wi}ExePackage"),
            tree.findall(".//{http://schemas.microsoft.com/wix/2006/wi}MsuPackage"),
            tree.findall(".//{http://schemas.microsoft.com/wix/2006/wi}MsiPackage")):
        url = eval_vars(package.get('DownloadUrl', ''))
        if not url:
            continue
        filename = eval_vars(package.get('SourceFile', '') or package.get('Name', ''))
        download_file(url, filename)
    # from https://github.com/wixtoolset/wix3/blob/develop/src/ext/NetFxExtension/wixlib/NetFx4.5.wxs
    download_file('http://go.microsoft.com/fwlink/?LinkId=225704', 'redist\\dotNetFx45_Full_setup.exe')


def generate_dir(src, output_filename=None, id=None, diskId=None, mod_function=None):
    while src[-1] in ('/', '\\'):
        src = src[:-1]
    name = os.path.basename(src)
    id = id or name.replace('-', '_').replace(' ', '_')
    output_filename = output_filename or (id + ".wxi")

    args = ['heat', 'dir', src, '-template', 'fragment', '-sreg', '-scom',
      '-o', output_filename, '-ag', '-cg', id, '-srd', '-var', 'var.' + id, '-dr', id, '-nologo']
    print(" ".join(args))
    subprocess.check_call(args)

    ElementTree.register_namespace("", "http://schemas.microsoft.com/wix/2006/wi")
    tree = ElementTree.parse(output_filename).getroot()
    tree.insert(0, ElementTree.Comment('generated with gen_dir_wxi.py %s\n' % src))
    tree.insert(0, ElementTree.ProcessingInstruction('define', '%s=%s' % (id, os.path.normpath(src))))
    parent_map = dict((c, p) for p in tree.getiterator() for c in p)
    for file in tree.findall(".//{http://schemas.microsoft.com/wix/2006/wi}Component/{http://schemas.microsoft.com/wix/2006/wi}File"):
        file_Source = file.get('Source', '')
        if file_Source.find('.svn') != -1 or os.path.basename(file_Source) in ('Thumbs.db', 'desktop.ini', '.DS_Store') or file_Source.endswith('.pyc'):
            comp = parent_map[file]
            parent_map[comp].remove(comp)
    for dir in tree.findall(".//{http://schemas.microsoft.com/wix/2006/wi}Directory"):
        if dir.get('Name', '') in ('.svn', '__pycache__'):
            for dirref in tree.findall(".//{http://schemas.microsoft.com/wix/2006/wi}DirectoryRef"):
                if dirref.get('Id', '') == dir.get('Id', ''):
                    frag = parent_map[dirref]
                    parent_map[frag].remove(frag)
            parent_map[parent_map[dir]].remove(parent_map[dir])
    if diskId:
        for component in tree.findall(".//{http://schemas.microsoft.com/wix/2006/wi}Component"):
            component.attrib['DiskId'] = diskId
    if mod_function:
        mod_function(tree, parent_map)

    ElementTree.ElementTree(tree).write(output_filename, xml_declaration=True, encoding='utf-8')


if __name__ == '__main__':
    main(sys.argv[1])
