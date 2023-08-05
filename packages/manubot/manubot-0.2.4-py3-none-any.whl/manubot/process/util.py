import collections
import json
import logging
import os
import pathlib
import re
import textwrap
import warnings

import jinja2
import pandas
import requests
import requests_cache
import yaml

from manubot.process.bibliography import (
    load_manual_references,
)
from manubot.process.manuscript import (
    datetime_now,
    get_citation_ids,
    get_manuscript_stats,
    get_text,
    update_manuscript_citations,
)
from manubot.cite.util import (
    citation_to_citeproc,
    get_citation_short_id,
    is_valid_citation,
    standardize_citation,
)


def check_collisions(citation_df):
    """
    Check for short_id hash collisions
    """
    collision_df = citation_df[['standard_id', 'short_id']].drop_duplicates()
    collision_df = collision_df[collision_df.short_id.duplicated(keep=False)]
    if not collision_df.empty:
        logging.error(f'OMF! Hash collision. Congratulations.\n{collision_df}')
    return collision_df


def check_multiple_citation_strings(citation_df):
    """
    Identify different citation strings referring the the same reference.
    """
    message = textwrap.dedent(f'''\
    {len(citation_df)} unique citations strings extracted from text
    {citation_df.standard_id.nunique()} unique standard citations\
    ''')
    logging.info(message)
    multi_df = citation_df[citation_df.standard_id.duplicated(keep=False)]
    if not multi_df.empty:
        table = multi_df.to_string(index=False, columns=['standard_id', 'manuscript_id'])
        logging.warning(f'Multiple citation strings detected for the same reference:\n{table}')
    return multi_df


def read_json(path):
    """
    Read json from a path or URL.
    """
    if re.match('^(http|ftp)s?://', path):
        response = requests.get(path)
        obj = response.json(object_pairs_hook=collections.OrderedDict)
    else:
        path = pathlib.Path(path)
        with path.open(encoding='utf-8-sig') as read_file:
            obj = json.load(read_file, object_pairs_hook=collections.OrderedDict)
    return obj


def read_jsons(paths):
    """
    Read multiple JSON files into a user_variables dictionary. Provide a list
    of paths (URLs or filepaths). Paths can optionally have a namespace
    prepended. For example:

    ```
    paths = [
        'https://git.io/vbkqm',  # update the dictionary's top-level
        'namespace_1=https://git.io/vbkqm',  # store under 'namespace_1' key
        'namespace_2=some_local_path.json',  # store under 'namespace_2' key
    ]
    ```

    If a namespace is not provided, the JSON must contain a dictionary as its
    top level. Namespaces should consist only of ASCII alphanumeric characters
    (includes underscores, first character cannot be numeric).
    """
    user_variables = collections.OrderedDict()
    for path in paths:
        logging.info(f'Read the following user-provided templating variables for {path}')
        # Match only namespaces that are valid jinja2 variable names
        # http://jinja.pocoo.org/docs/2.10/api/#identifier-naming
        match = re.match(r'([a-zA-Z_][a-zA-Z0-9_]*)=(.+)', path)
        if match:
            namespace, path = match.groups()
            logging.info(f'Using the "{namespace}" namespace for template variables from {path}')
        try:
            obj = read_json(path)
        except Exception:
            logging.exception(f'Error reading template variables from {path}')
            continue
        if match:
            obj = {namespace: obj}
        assert isinstance(obj, dict)
        conflicts = user_variables.keys() & obj.keys()
        if conflicts:
            logging.warning(f'Template variables in {path} overwrite existing '
                            'values for the following keys:\n' +
                            '\n'.join(conflicts))
        user_variables.update(obj)
    logging.info(f'Reading user-provided templating variables complete:\n'
                 f'{json.dumps(user_variables, indent=2, ensure_ascii=False)}')
    return user_variables


def add_author_affiliations(variables):
    """
    Edit variables to contain numbered author affiliations. Specifically,
    add a list of affiliation_numbers for each author and add a list of
    affiliations to the top-level of variables. If no authors have any
    affiliations, variables is left unmodified.
    """
    rows = list()
    for author in variables['authors']:
        if 'affiliations' not in author:
            continue
        if not isinstance(author['affiliations'], list):
            warnings.warn(
                f"Expected list for {author['name']}'s affiliations. "
                f"Assuming multiple affiliations are `; ` separated. "
                f"Please switch affiliations to a list.",
                category=DeprecationWarning
            )
            author['affiliations'] = author['affiliations'].split('; ')
        for affiliation in author['affiliations']:
            rows.append((author['name'], affiliation))
    if not rows:
        return variables
    affil_map_df = pandas.DataFrame(rows, columns=['name', 'affiliation'])
    affiliation_df = affil_map_df[['affiliation']].drop_duplicates()
    affiliation_df['affiliation_number'] = range(1, 1 + len(affiliation_df))
    affil_map_df = affil_map_df.merge(affiliation_df)
    name_to_numbers = {name: sorted(df.affiliation_number) for name, df in
                       affil_map_df.groupby('name')}
    for author in variables['authors']:
        author['affiliation_numbers'] = name_to_numbers.get(author['name'], [])
    variables['affiliations'] = affiliation_df.to_dict(orient='records')
    return variables


def get_metadata_and_variables(args):
    """
    Process metadata.yaml and create variables available for jinja2 templating.
    """
    # Generated manuscript variables
    variables = collections.OrderedDict()

    # Read metadata which contains pandoc_yaml_metadata
    # as well as author_info.
    if args.meta_yaml_path.is_file():
        with args.meta_yaml_path.open(encoding='utf-8-sig') as read_file:
            metadata = yaml.safe_load(read_file)
            assert isinstance(metadata, dict)
    else:
        metadata = {}
        logging.warning(f'missing {args.meta_yaml_path} file with yaml_metadata_block for pandoc')

    # Add date to metadata
    now = datetime_now()
    logging.info(
        f'Using {now:%Z} timezone.\n'
        f'Dating manuscript with the current datetime: {now.isoformat()}')
    metadata['date-meta'] = now.date().isoformat()
    variables['date'] = f'{now:%B} {now.day}, {now.year}'

    # Process authors metadata
    authors = metadata.pop('author_info', [])
    if authors is None:
        authors = []
    metadata['author-meta'] = [author['name'] for author in authors]
    variables['authors'] = authors
    variables = add_author_affiliations(variables)

    # Set repository version metadata for Travis CI builds only
    # https://docs.travis-ci.com/user/environment-variables/
    if os.getenv('TRAVIS', 'false') == 'true':
        repo_slug = os.environ['TRAVIS_REPO_SLUG']
        repo_owner, repo_name = repo_slug.split('/')
        variables['ci_source'] = {
            'repo_slug': repo_slug,
            'repo_owner': repo_owner,
            'repo_name': repo_name,
            'commit': os.environ['TRAVIS_COMMIT'],
        }

    # Update variables with user-provided variables here
    user_variables = read_jsons(args.template_variables_path)
    variables.update(user_variables)

    return metadata, variables


def get_citation_df(args, text):
    """
    Generate citation_df and save it to 'citations.tsv'.
    citation_df is a pandas.DataFrame with the following columns:
    - manuscript_id: citation ids extracted from the manuscript content files.
    - detagged_id: manuscript_id but with tag citations dereferenced
    - standard_id: detagged_id standardized
    - short_id: standard_id hashed to create a short base
    """
    citation_df = pandas.DataFrame(
        {'manuscript_id': get_citation_ids(text)}
    )
    if args.citation_tags_path.is_file():
        tag_df = pandas.read_csv(args.citation_tags_path, sep='\t')
        na_rows_df = tag_df[tag_df.isnull().any(axis='columns')]
        if not na_rows_df.empty:
            logging.error(
                f'{args.citation_tags_path} contains rows with missing values:\n'
                f'{na_rows_df}\n'
                'This error can be caused by using spaces rather than tabs to delimit fields.\n'
                'Proceeding to reread TSV with delim_whitespace=True.'
            )
            tag_df = pandas.read_csv(args.citation_tags_path, delim_whitespace=True)
        tag_df['manuscript_id'] = 'tag:' + tag_df.tag
        tag_df = tag_df.rename(columns={'citation': 'detagged_id'})
        for detagged_id in tag_df.detagged_id:
            is_valid_citation(detagged_id, allow_raw=True)        
        citation_df = citation_df.merge(tag_df[['manuscript_id', 'detagged_id']], how='left')
    else:
        citation_df['detagged_id'] = None
        logging.info(f'missing {args.citation_tags_path} file: no citation tags set')
    citation_df.detagged_id.fillna(citation_df.manuscript_id.astype(str), inplace=True)
    citation_df['standard_id'] = citation_df.detagged_id.map(standardize_citation)
    citation_df['short_id'] = citation_df.standard_id.map(get_citation_short_id)
    citation_df = citation_df.sort_values(['standard_id', 'detagged_id'])
    citation_df.to_csv(args.citations_path, sep='\t', index=False)
    check_collisions(citation_df)
    check_multiple_citation_strings(citation_df)
    return citation_df


def generate_csl_items(args, citation_df):
    """
    General CSL (citeproc) items for standard_ids in citation_df.
    Writes references.json to disk and logs warnings for potential problems.
    """
    # Read manual references (overrides) in JSON CSL
    manual_refs = load_manual_references(args.manual_references_paths)

    requests_cache.install_cache(args.requests_cache_path, include_get_headers=True)
    cache = requests_cache.get_cache()
    if args.clear_requests_cache:
        logging.info('Clearing requests-cache')
        requests_cache.clear()
    logging.info(f'requests-cache starting with {len(cache.responses)} cached responses')

    csl_items = list()
    failures = list()
    for standard_id in citation_df.standard_id.unique():
        if standard_id in manual_refs:
            csl_items.append(manual_refs[standard_id])
            continue
        elif standard_id.startswith('raw:'):
            logging.error(
                f'CSL JSON Data with a standard_id of {standard_id} not found in manual-references.json. '
                'Metadata must be provided for raw citations.'
            )
            failures.append(standard_id)
        try:
            citeproc = citation_to_citeproc(standard_id)
            csl_items.append(citeproc)
        except Exception:
            logging.exception(f'Citeproc retrieval failure for {standard_id}')
            failures.append(standard_id)

    logging.info(f'requests-cache finished with {len(cache.responses)} cached responses')
    requests_cache.uninstall_cache()

    if failures:
        message = 'CSL JSON Data retrieval failed for:\n{}'.format(
            '\n'.join(failures))
        logging.error(message)

    # Write JSON CSL bibliography for Pandoc.
    with args.references_path.open('w', encoding='utf-8') as write_file:
        json.dump(csl_items, write_file, indent=2, ensure_ascii=False)
        write_file.write('\n')
    return csl_items


def template_with_jinja2(text, variables):
    """
    Template using jinja2 with the variables dictionary unpacked as keyword
    arguments.
    """
    jinja_environment = jinja2.Environment(
        loader=jinja2.BaseLoader(),
        undefined=jinja2.make_logging_undefined(logging.getLogger()),
        comment_start_string='{##',
        comment_end_string='##}',
    )
    template = jinja_environment.from_string(text)
    return template.render(**variables)


def prepare_manuscript(args):
    """
    Compile manuscript, creating manuscript.md and references.json as inputs
    for pandoc.
    """
    text = get_text(args.content_directory)
    citation_df = get_citation_df(args, text)

    generate_csl_items(args, citation_df)

    short_citation_mapper = collections.OrderedDict(
        zip(citation_df.manuscript_id, citation_df.short_id))
    text = update_manuscript_citations(text, short_citation_mapper)

    metadata, variables = get_metadata_and_variables(args)
    variables['manuscript_stats'] = get_manuscript_stats(text, citation_df)
    with args.variables_path.open('w', encoding='utf-8') as write_file:
        json.dump(variables, write_file, ensure_ascii=False, indent=2)
        write_file.write('\n')

    text = template_with_jinja2(text, variables)

    # Write manuscript for pandoc
    with args.manuscript_path.open('w', encoding='utf-8') as write_file:
        yaml.dump(metadata, write_file, default_flow_style=False,
                  explicit_start=True, explicit_end=True)
        write_file.write('\n')
        write_file.write(text)
