from revscoring.datasources.revision_oriented import revision
from revscoring.dependencies import solve

from .. import enwiki

revision_text = revision.text


def test_cite_templates():
    text = """
    This is some text with a citation.<ref>{{cite lol|title=Made up}}</ref>
    This is some more text. {{foo}} {{{cite}}}  {{sfn}}  {{Harvard citation}}

    I am a new paragraph.<ref>{{cite book|title=The stuff}}</ref>
    {{Cite hat|ascii=_n_}}
    """
    assert solve(enwiki.all_ref_tags, cache={revision_text: text}) == 3
    assert solve(enwiki.all_cite_templates, cache={revision_text: text}) == 5


def test_infobox_templates():
    text = """
    {{Infobox pants|hats=2|pajams=23}}
    This is some text with a citation.<ref>{{cite lol|title=Made up}}</ref>
    This is some more text.

    I am a new paragraph.<ref>{{cite book|title=The stuff}}</ref>
    {{Cite hat|ascii=_n_}}
    """
    assert solve(enwiki.infobox_templates, cache={revision_text: text}) == 1


def test_cn_templates():
    text = """
    {{Infobox pants|hats=2|pajams=23}}
    This is some text with a citation.{{cn}}
    This is some more text. {{foo}}

    I am a new paragraph.{{fact|date=never}}

    I am a new paragraph.{{Citation_needed|date=never}}
    """
    assert solve(enwiki.cn_templates, cache={revision_text: text}) == 3


def test_who_templates():
    text = """
    This is some text with a citation.{{cn}}
    This is some more text. {{foo}}

    I am a new paragraph.{{who}}

    I am a new paragraph.{{who|date=today}}
    """
    assert solve(enwiki.who_templates, cache={revision_text: text}) == 2


def test_main_article_templates():
    text = """
    This is some text with a citation.{{cn}}
    This is some more text. {{foo}}

    == Some section ==
    {{Main|section}}

    I am a new paragraph.{{who|date=today}}
    """
    assert solve(enwiki.main_article_templates,
                 cache={revision_text: text}) == 1


def test_paragraphs_without_refs_total_length():
    text = """
    Here is the first paragraph.
    It contains some references <ref>first reference</ref>.

    Here is second paragraph. One line with reference <ref>reference</ref>.

    Here is third paragraph.
    It has two lines, but no references.


    Here is fourth paragraph.
    It has two lines <ref>reference</ref>.
    One of which has a reference.

    Here is fifth paragraph. One line, no references.

    Short line.<ref>last</ref><ref>One more reference</ref>
    """
    assert solve(enwiki.paragraphs_without_refs_total_length,
                 cache={revision_text: text}) == 114
