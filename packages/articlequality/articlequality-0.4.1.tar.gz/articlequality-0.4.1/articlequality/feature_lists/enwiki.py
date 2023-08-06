"""
English Wikipedia
+++++++++++++++++
"""

from revscoring.datasources.meta import filters, mappers
from revscoring.features import wikitext
from revscoring.features.meta import aggregators
from revscoring.features.modifiers import log, max, sub
from revscoring.features.wikitext.datasources import Revision
from revscoring.languages import english

from . import wikipedia

# Templates
infobox_templates = wikitext.revision.template_names_matching(
    r"infobox", name="enwiki.revision.infobox_templates")
CN_TEMPLATES = [
    r"Citation[_ ]needed",
    r"Cn",
    r"Fact"
]
cn_templates = wikitext.revision.template_names_matching(
    "|".join(CN_TEMPLATES), name="enwiki.revision.cn_templates")
who_templates = wikitext.revision.template_names_matching(
    "Who", name="enwiki.revision.who_templates")
main_article_templates = wikitext.revision.template_names_matching(
    "Main", name="enwiki.main_article_templates")
CITE_TEMPLATES = [
    r"Cite",
    r"Harvard[_ ]citation[_ ]no[_ ]brackets", r"harvnb",
    r"Harvard citation", r"harv",
    r"Harvard citation text", r"harvtxt",
    r"Harvcoltxt",
    r"Harvcol",
    r"Harvcolnb",
    r"Harvard citations", r"harvs",
    r"Harvp"
]
cite_templates = wikitext.revision.template_names_matching(
    "|".join(CITE_TEMPLATES), name="enwiki.revision.cite_templates")
SFN_TEMPLATES = [
    r"Shortened footnote template", r"sfn",
    r"Sfnp",
    r"Sfnm",
    r"Sfnmp"
]
shortened_footnote_templates = wikitext.revision.template_names_matching(
    "|".join(SFN_TEMPLATES),
    name="enwiki.revision.shortened_footnote_templates")
all_ref_tags = shortened_footnote_templates + wikitext.revision.ref_tags
all_cite_templates = cite_templates + shortened_footnote_templates
proportion_of_templated_references = \
    all_cite_templates / max(all_ref_tags, 1)
non_templated_references = max(all_ref_tags - all_cite_templates, 0)
non_cite_templates = sub(
    wikitext.revision.templates, all_cite_templates,
    name="enwiki.revision.non_cite_templates"
)

# Links
category_links = wikitext.revision.wikilink_titles_matching(
    r"Category\:", name="enwiki.revision.category_links")
image_links = wikitext.revision.wikilink_titles_matching(
    r"File|Image\:", name="enwiki.revision.image_links")

# References
revision = Revision(
    "enwiki.revision.revision",
    wikitext.revision.datasources,
)
paragraphs = mappers.map(
    str, revision.paragraphs_sentences_and_whitespace,
    name="enwiki.revision.paragraphs"
)
paragraphs_without_refs = filters.regex_matching(
    r"^(?!\s*$)((?!<ref>)(.|\n))*$",
    paragraphs,
    name="enwiki.revision.paragraphs_without_refs"
)
paragraphs_without_refs_total_length = aggregators.sum(
    mappers.map(len, paragraphs_without_refs),
    name="enwiki.revision.paragraphs_without_refs_total_length"
)

# Wikipedia:Manual of Style/Words to watch
words_to_watch_count = english.words_to_watch.revision.matches

local_wiki = [
    image_links,
    image_links / max(wikitext.revision.content_chars, 1),
    category_links,
    category_links / max(wikitext.revision.content_chars, 1),
    all_ref_tags,
    all_ref_tags / max(wikitext.revision.content_chars, 1),
    all_cite_templates,
    all_cite_templates / max(wikitext.revision.content_chars, 1),
    proportion_of_templated_references,
    non_templated_references,
    non_templated_references / max(wikitext.revision.content_chars, 1),
    non_cite_templates,
    non_cite_templates / max(wikitext.revision.content_chars, 1),
    infobox_templates,
    cn_templates + 1,
    cn_templates / max(wikitext.revision.content_chars, 1),
    who_templates + 1,
    who_templates / max(wikitext.revision.content_chars, 1),
    main_article_templates,
    main_article_templates / max(wikitext.revision.content_chars, 1),
    (english.stemmed.revision.stem_chars /
     max(wikitext.revision.content_chars, 1)),
    log(paragraphs_without_refs_total_length + 1),
    words_to_watch_count,
    words_to_watch_count / max(wikitext.revision.words, 1),
]

wp10 = wikipedia.article + local_wiki
"""
Based largely on work by Morten Warncke-Wang et al.[1] and with a few
improvements and extensions that Morten identified after publication.

1. Warncke-Wang, M., Cosley, D., & Riedl, J. (2013, August). Tell me more: An
   actionable quality model for wikipedia. In Proceedings of the 9th
   International Symposium on Open Collaboration (p. 8). ACM.
   http://opensym.org/wsos2013/proceedings/p0202-warncke.pdf
"""
