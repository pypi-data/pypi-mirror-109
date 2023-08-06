import logging
import re
from pathlib import Path

from typing import Tuple, Dict
from io import StringIO
from enum import Enum
import yaml

from fluidtopics.connector.model.metadata import SemanticMetadata


class MetadataError(Exception):
    pass


logger = logging.getLogger("antidot.md2ft")

RE_LINEMETA = re.compile(r'\s*\[_metadata_\:(\w*[\:\w*]*)\]\:\s*-\s*["\'](.+)["\']')
RE_YAMLMETA_BEGIN = re.compile(r'^---')
RE_YAMLMETA_END = re.compile(r'^---|^\.\.\.')
RE_H1_MD = re.compile("^# (.*)$")


class MetadataType(Enum):
    NoMeta = 1
    LineMeta = 2
    YamlMeta = 3

# List of meta data that ought to be single-valued
# See: https://doc.antidot.net/r/FT/3.7/empower-metadata/Metadata-in-Fluid-Topics/Semantic-Metadata


# The authorized single value semantic meta are given
# by the official fluidtopics API
# see: https://pypi.org/project/fluidtopics
FT_SEMANTIC_META = SemanticMetadata.ALL
# This one is authorized too for md2ft
FT_SEMANTIC_META.add("ft:originID")
FT_SEMANTIC_META.add("ft:lang")
SINGLE_VALUE_M2FT = {"audience"}

SINGLE_VALUE_META = SINGLE_VALUE_M2FT.union(FT_SEMANTIC_META)


def detect_metadata(f: Path) -> MetadataType:
    """Detects which kind of markdown metadata is present in markdown file (if any)
    Metadata should be present on the very first line. If there is no metadata
    marker on the first line, it is assumed that there is no metadata in the file.
    """
    metatype = MetadataType.NoMeta
    with f.open('r') as mdfile:
        firstline = mdfile.readline()
        if RE_YAMLMETA_BEGIN.match(firstline):
            metatype = MetadataType.YamlMeta
        elif RE_LINEMETA.match(firstline):
            metatype = MetadataType.LineMeta
    return metatype


def get_md_metas(f: Path, implicit_meta: bool = False) -> Tuple[Dict[str, str], str]:
    """Get markdown metadata from a file and verify other MD content is there too"""
    metas = {}
    metatype = detect_metadata(f)
    # at the end the md_content will contain the md data with the metadata stripped-out
    md_content = StringIO()

    logger.debug(f"MD file={f}")
    with f.open('r') as mdfile:
        if metatype == MetadataType.LineMeta:
            for line in mdfile:
                m = RE_LINEMETA.match(line)
                if m:
                    key = m.group(1)
                    value = m.group(2)
                    # case insensitivity title compatibility
                    if key.lower() == "title":
                        metas["title"] = value
                    else:
                        # create a multi-valued meta
                        if key in metas:
                            if type(metas[key]) == list:
                                metas[key].append(value)
                            else:
                                metas[key] = [metas[key], value]
                        else:
                            metas[key] = value
                else:
                    match_h1 = RE_H1_MD.match(line)
                    if match_h1:
                        metas["ft:title"] = match_h1.group(1)
                        continue
                    md_content.write(line)
        elif metatype == MetadataType.YamlMeta:
            # skip first line which should be the YAML data begin marker
            _ = mdfile.readline()
            yamldata = StringIO()
            buffer = yamldata
            for k, line in enumerate(mdfile.readlines()):
                if RE_YAMLMETA_END.match(line):
                    buffer = md_content
                    continue
                match_h1 = RE_H1_MD.match(line)
                if match_h1:
                    metas["ft:title"] = match_h1.group(1)
                    continue
                buffer.write(line)
            metas.update(yaml.safe_load(yamldata.getvalue()))
        elif metatype == MetadataType.NoMeta:
            # when no meta is present in file we should at least
            # handle H1 header as ft:title.
            for line in mdfile:
                match_h1 = RE_H1_MD.match(line)
                if match_h1:
                    metas["ft:title"] = match_h1.group(1)
                    continue
                md_content.write(line)

    logger.debug(f"metatype={metatype}, metas={metas}")
    # Handle implicit meta and compatibility
    if not metas and implicit_meta:
        metas = {"ft:title": f.stem}
    # Handle meta compatibility format
    if "ft:title" not in metas and "title" in metas:
        logger.warning("Using '[_metadata_:title]:-' for title is deprecated")
        logger.warning("Use '[_metadata_:ft:title]:- \"your title\"'")
        metas["ft:title"] = metas["title"]
        del metas["title"]
    if "ft:originID" not in metas and "originID" in metas:
        logger.warning("Using '[_metadata_:originID]:-' for originID is deprecated")
        logger.warning("Use '[_metadata_:ft:originID]:- \"your originID\"'")
        metas["ft:originID"] = metas["originID"]
        del metas["originID"]

    # Check that ft semantic metadata are in the list of authorized meta
    # and that some meta are not multivalued
    for k, v in metas.items():
        logger.debug(f"Check meta {k} with value {v} (type={type(v)})")
        if k.startswith("ft:") and k not in FT_SEMANTIC_META:
            raise MetadataError(f"Fluid Topics Semantic meta {k} cannot be set (value = {v} in file {f})")
        if (k in SINGLE_VALUE_META) and (type(v) == list) and len(v)>1:
            raise MetadataError(f"meta {k} cannot be multi-valued (current = {v} in file {f})")
    return metas, md_content.getvalue()
