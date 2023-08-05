"""
adapted from nbsphinx
"""
import re
import os
try:
    from urllib.parse import unquote  # Python 3.x
except ImportError:
    from urllib2 import unquote  # Python 2.x

import docutils
import nbconvert

from ipypublish.sphinx.utils import import_sphinx


class CreateNotebookSectionAnchors(docutils.transforms.Transform):
    """Create section anchors for Jupyter notebooks.

    Note: Sphinx lower-cases the HTML section IDs, Jupyter doesn't.
    This transform creates anchors in the Jupyter style.

    # TODO do this in pandoc filter?
    """

    default_priority = 200  # Before CreateSectionLabels (250)

    def apply(self):
        for section in self.document.traverse(docutils.nodes.section):
            title = section.children[0].astext()
            link_id = title.replace(' ', '-')
            section['ids'] = [link_id]


def _local_file_from_reference(node, document):
    """Get local file path from reference and split it into components."""
    # NB: Anonymous hyperlinks must be already resolved at this point!
    refuri = node.get('refuri')
    if not refuri:
        refname = node.get('refname')
        if refname:
            refid = document.nameids.get(refname)
        else:
            # NB: This can happen for anonymous hyperlinks
            refid = node.get('refid')
        target = document.ids.get(refid)
        if not target:
            # No corresponding target, Sphinx may warn later
            return '', '', ''
        refuri = target.get('refuri')
        if not refuri:
            # Target doesn't have URI
            return '', '', ''
    if '://' in refuri:
        # Not a local link
        return '', '', ''
    elif refuri.startswith('#') or refuri.startswith('mailto:'):
        # Not a local link
        return '', '', ''

    # NB: We look for "fragment identifier" before unquoting
    match = re.match(r'^([^#]+)(\.[^#]+)(#.+)$', refuri)
    if match:
        base = unquote(match.group(1))
        # NB: The suffix and "fragment identifier" are not unquoted
        suffix = match.group(2)
        fragment = match.group(3)
    else:
        base, suffix = os.path.splitext(refuri)
        base = unquote(base)
        fragment = ''
    return base, suffix, fragment


class RewriteLocalLinks(docutils.transforms.Transform):
    """Turn links to source files into ``:doc:``/``:ref:`` links.

    Links to subsections are possible with ``...#Subsection-Title``.
    These links use the labels created by CreateSectionLabels.

    Links to subsections use ``:ref:``, links to whole source files use
    ``:doc:``.  Latter can be useful if you have an ``index.rst`` but
    also want a distinct ``index.ipynb`` for use with Jupyter.
    In this case you can use such a link in a notebook::

        [Back to main page](index.ipynb)

    In Jupyter, this will create a "normal" link to ``index.ipynb``, but
    in the files generated by Sphinx, this will become a link to the
    main page created from ``index.rst``.

    """

    default_priority = 500  # After AnonymousHyperlinks (440)

    def apply(self):
        sphinx = import_sphinx()
        env = self.document.settings.env
        for node in self.document.traverse(docutils.nodes.reference):
            base, suffix, fragment = _local_file_from_reference(node,
                                                                self.document)
            if not base:
                continue

            for s in env.config.source_suffix:
                if suffix.lower() == s.lower():
                    target = base
                    if fragment:
                        target_ext = suffix + fragment
                        reftype = 'ref'
                    else:
                        target_ext = ''
                        reftype = 'doc'
                    break
            else:
                continue  # Not a link to a potential Sphinx source file

            target_docname = nbconvert.filters.posix_path(os.path.normpath(
                os.path.join(os.path.dirname(env.docname), target)))
            if target_docname in env.found_docs:
                reftarget = '/' + target_docname + target_ext
                if reftype == 'ref':
                    reftarget = reftarget.lower()
                linktext = node.astext()
                xref = sphinx.addnodes.pending_xref(
                    reftype=reftype, reftarget=reftarget, refdomain='std',
                    refwarn=True, refexplicit=True, refdoc=env.docname)
                xref += docutils.nodes.Text(linktext, linktext)
                node.replace_self(xref)


class CreateSectionLabels(docutils.transforms.Transform):
    """Make labels for each document and each section thereof.

    These labels are referenced in RewriteLocalLinks but can also be
    used manually with ``:ref:``.

    """

    default_priority = 250  # Before references.PropagateTargets (260)

    def apply(self):
        env = self.document.settings.env
        file_ext = os.path.splitext(env.doc2path(env.docname))[1]
        i_still_have_to_create_the_document_label = True
        for section in self.document.traverse(docutils.nodes.section):
            assert section.children
            assert isinstance(section.children[0], docutils.nodes.title)
            title = section.children[0].astext()
            link_id = section['ids'][0]
            label = '/' + env.docname + file_ext + '#' + link_id
            label = label.lower()
            env.domaindata['std']['labels'][label] = (
                env.docname, link_id, title)
            env.domaindata['std']['anonlabels'][label] = (
                env.docname, link_id)

            # Create a label for the whole document using the first section:
            if i_still_have_to_create_the_document_label:
                label = '/' + env.docname.lower() + file_ext
                env.domaindata['std']['labels'][label] = (
                    env.docname, '', title)
                env.domaindata['std']['anonlabels'][label] = (
                    env.docname, '')
                i_still_have_to_create_the_document_label = False


class CreateDomainObjectLabels(docutils.transforms.Transform):
    """Create labels for domain-specific object signatures."""

    default_priority = 250  # About the same as CreateSectionLabels

    def apply(self):
        sphinx = import_sphinx()
        env = self.document.settings.env
        file_ext = os.path.splitext(env.doc2path(env.docname))[1]
        for sig in self.document.traverse(sphinx.addnodes.desc_signature):
            try:
                title = sig['ids'][0]
            except IndexError:
                # Object has same name as another, so skip it
                continue
            link_id = title.replace(' ', '-')
            sig['ids'] = [link_id]
            label = '/' + env.docname + file_ext + '#' + link_id
            label = label.lower()
            env.domaindata['std']['labels'][label] = (
                env.docname, link_id, title)
            env.domaindata['std']['anonlabels'][label] = (
                env.docname, link_id)
