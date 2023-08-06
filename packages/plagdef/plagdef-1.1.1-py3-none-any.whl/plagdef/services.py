from __future__ import annotations

from click import UsageError
from dependency_injector.wiring import Provide, inject

from plagdef.model.detection import DocumentMatcher
from plagdef.model.models import DocumentPairMatches, Document
from plagdef.model.preprocessing import UnsupportedLanguageError
from plagdef.repositories import UnsupportedFileFormatError, DocumentPickleRepository


@inject
def find_matches(doc_repo, archive_repo=None, common_doc_repo=None, config=Provide['config.default']) \
    -> list[DocumentPairMatches]:
    try:
        doc_matcher = DocumentMatcher(config)
        archive_docs = None
        if archive_repo:
            archive_docs = _preprocess_docs(doc_matcher, config['lang'], archive_repo, common_doc_repo)
        docs = _preprocess_docs(doc_matcher, config['lang'], doc_repo, common_doc_repo)
        doc_pair_matches = doc_matcher.find_matches(docs, archive_docs)
        return doc_pair_matches
    except (UnsupportedFileFormatError, UnsupportedLanguageError) as e:
        raise UsageError(str(e)) from e


def _preprocess_docs(doc_matcher, lang, doc_repo, common_doc_repo=None) -> set[Document]:
    common_dir_path = common_doc_repo.dir_path if common_doc_repo else None
    common_docs = common_doc_repo.list() if common_doc_repo else None
    doc_ser = DocumentPickleRepository(doc_repo.dir_path, common_dir_path)
    docs = doc_repo.list()
    prep_docs = {d for d in doc_ser.list() if d in docs}
    unprep_docs = docs.difference(prep_docs)
    doc_matcher.preprocess(lang, unprep_docs, common_docs)
    preprocessed_docs = prep_docs.union(unprep_docs)
    doc_ser.save(preprocessed_docs)
    return preprocessed_docs


def write_json_reports(matches: list[DocumentPairMatches], repo):
    [repo.save(m) for m in matches]


@inject
def update_config(d: dict, container=Provide['<container>']):
    for att, val in d.items():
        container.config.set(f'default.{att}', val)
