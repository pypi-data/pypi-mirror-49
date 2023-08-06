# Standard library imports
import json
import sys
import contextlib
import os
import tempfile
import uuid
import datetime

# Imports
import click

# Package imports
from . import client
from . import errors
from . import constants
from . import util
from . import version

HOST = 'GENCOVE_HOST'
HOST_HELP = 'backend host; defaults to ${} if set, otherwise: {}'.format(
    HOST, constants.HOST_DEFAULT)
DEVICE_UUID = 'GENCOVE_DEVICE_UUID'
DEVICE_UUID_HELP = 'unique id for client device; defaults to hardware address'
TOKEN = 'GENCOVE_TOKEN'
TOKEN_HELP = 'backend access token; defaults to ${}'.format(TOKEN)
API_KEY = 'GENCOVE_API_KEY'
API_KEY_HELP = 'backend API key; defaults to ${}'.format(API_KEY)

AWS_CONFIG_FILE = 'AWS_CONFIG_FILE'
AWS_SHARED_CREDENTIALS_FILE = 'AWS_SHARED_CREDENTIALS_FILE'
env_var_save_restore = [
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_SESSION_TOKEN',
    'AWS_SECURITY_TOKEN',
    'AWS_DEFAULT_REGION',
    'AWS_DEFAULT_PROFILE',
    'AWS_CA_BUNDLE',
    AWS_SHARED_CREDENTIALS_FILE,
    AWS_CONFIG_FILE
]

PROFILE_NAME = 'gencove-cli-profile'
COMMAND_BASE = ['aws', '--profile', PROFILE_NAME]

TMP_UPLOADS_WARNING = (
    'The Gencove upload area is temporary storage. Log into the dashboard and '
    'assign uploaded files to a project in order to avoid automatic deletion.'
)

UPLOAD_PREFIX = 'gncv://'


def debug_header(ctx, param, value, *args, **kwargs):
    if value:
        click.echo(
            'Gencove CLI version: {}'.format(version.version()), err=True)
    return value


def output_warning(text):
    return click.style(
        'WARNING: {}'.format(text), bg='red', fg='white', bold=True)


@click.group()
@click.version_option(version=version.version())
def cli():
    pass


@cli.group()
def auth():
    pass


@cli.group()
def study():
    pass


@study.group()
def participant():
    pass


@cli.group()
def app():
    pass


@cli.group()
def project():
    pass


@cli.group()
def upload():
    pass


@cli.group()
def credentials():
    pass


@auth.command()
@click.argument('name')
@click.argument('email')
@click.option(
    '--password', default=None, help='password associated with user acccount')
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
@click.option(
    '--print-token/--no-print-token', default=True,
    help='indicate backend access token should be printed to console')
@click.option(
    '--print-response/--no-print-response', default=False,
    help='indicate server response should be printed to console')
def register(
        name, email, password, host, device_uuid, print_token, print_response):
    '''Register new user on gencove backend'''
    c = client.Client(host, device_uuid)

    try:
        response_dict = c.register(name, email, password, return_response=True)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    if print_response:
        click.echo(util.get_output(response_dict))
    if print_token:
        click.echo(c.get_refresh_token())


@auth.command()
@click.argument('email')
@click.option(
    '--password', default=None, help='password associated with user acccount')
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
@click.option(
    '--print-token/--no-print-token', default=True,
    help='indicate backend access token should be printed to console')
@click.option(
    '--print-response/--no-print-response', default=False,
    help='indicate server response should be printed to console')
def login(email, password, host, device_uuid, print_token, print_response):
    '''Log into gencove backend

    CAUTION: This will log out any sessions (tokens) the user has with
    specified device_uuid
    '''
    c = client.Client(host, device_uuid)

    try:
        response_dict = c.login(email, password, return_response=True)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    if print_response:
        click.echo(util.get_output(response_dict))
    if print_token:
        click.echo(c.get_refresh_token())


@auth.command()
@click.option(
    '--token', required=True, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def logout(token, host, device_uuid):
    '''Log out of gencove backend'''
    c = client.Client(host, device_uuid)
    c.set_refresh_token(token)

    try:
        response_dict = c.logout(return_response=True)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    click.echo(util.get_output(response_dict))


@auth.command()
@click.argument('confirm-id')
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def email_confirm(confirm_id, host, device_uuid):
    '''Confirm email'''
    c = client.Client(host, device_uuid)

    try:
        response_dict = c.email_confirm(confirm_id, return_response=True)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    click.echo(util.get_output(response_dict))


@auth.command()
@click.argument('email')
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def password_forgot_init(email, host, device_uuid):
    '''Trigger sending of forgotten password email

    CAUTION: changing password invalidates all sessions (tokens) for current
    user
    '''
    c = client.Client(host, device_uuid)

    try:
        response_dict = c.email_confirm(confirm_id, return_response=True)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    click.echo(util.get_output(response_dict))


@auth.command()
@click.option(
    '--token', required=True, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--password', default=None,
    help='current password associated with user acccount')
@click.option(
    '--new-password', default=None,
    help='new password to be associated with user acccount')
@click.option(
    '--new-password-confirm', default=None,
    help='confirmation of new password')
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
@click.option(
    '--print-token/--no-print-token', default=True,
    help='indicate new backend access token should be printed to console')
@click.option(
    '--print-response/--no-print-response', default=False,
    help='indicate server response should be printed to console')
def password_change(
        token, password, new_password, new_password_confirm, host, device_uuid,
        print_token, print_response):
    '''Change password

    CAUTION: changing password invalidates all sessions (tokens) for current
    user
    '''
    c = client.Client(host, device_uuid)
    c.set_refresh_token(token)

    try:
        response_dict = c.password_change(
            password, new_password, new_password_confirm, return_response=True)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    if print_response:
        click.echo(util.get_output(response_dict))
    if print_token:
        click.echo(c.get_refresh_token())


@study.command(name='get_all')
@click.option(
    '--token', required=True, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def study_get_all(token, host, device_uuid):
    '''List all studies owned by user'''
    c = client.Client(host, device_uuid)
    c.set_refresh_token(token)

    try:
        studies = c.studies_get()
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    click.echo(util.pretty_json(studies))


@study.command()
@click.argument('study-id')
@click.option(
    '--token', required=True, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
@click.option(
    '--key', default=None, help='output only this key from study info')
def get(study_id, token, host, device_uuid, key):
    '''Get single study owned by user'''
    c = client.Client(host, device_uuid)
    c.set_refresh_token(token)

    try:
        study = c.study_get(study_id)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    if key:
        try:
            click.echo(study[key])
        except KeyError:
            click.echo('Key "{}" not found'.format(key), err=True)
            exit(1)
    else:
        click.echo(util.pretty_json(study))


@study.command()
@click.argument('name')
@click.argument('href')
@click.argument('description')
@click.option(
    '--enabled/--disabled', default=True,
    help='whether the study is enabled upon creation')
@click.option(
    '--discoverable/--private', default=True,
    help='whether the study is discoverable upon creation')
@click.option(
    '--token', required=True, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
@click.option(
    '--key', default=None, help='output only this key from study info')
def create(
        name, href, description, enabled, discoverable, token, host,
        device_uuid, key):
    '''Create a new study'''
    c = client.Client(host, device_uuid)
    c.set_refresh_token(token)

    try:
        study = c.study_create(
            name=name, href=href, description=description,
            study_enabled=enabled, discoverable=discoverable)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    if key:
        try:
            click.echo(study[key])
        except KeyError:
            click.echo('Key "{}" not found'.format(key), err=True)
            exit(1)
    else:
        click.echo(util.pretty_json(study))


@study.command()
@click.argument('study-id')
@click.option(
    '--name', default=None, help='study name')
@click.option(
    '--href', default=None, help='link to study website')
@click.option(
    '--description', default=None, help='study description')
@click.option(
    '--subsidy-enabled/--subsidy-disabled', default=None,
    help='whether study stubsidies are enabled')
@click.option(
    '--enabled/--disabled', default=None, help='whether the study is enabled')
@click.option(
    '--discoverable/--private', default=None,
    help='whether the study is discoverable')
@click.option(
    '--token', required=True, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
@click.option(
    '--key', default=None, help='output only this key from study info')
def update(
        study_id, name, href, description, subsidy_enabled, enabled,
        discoverable, token, host, device_uuid, key):
    '''Update an existing study'''
    c = client.Client(host, device_uuid)
    c.set_refresh_token(token)

    try:
        study = c.study_update(
            study_id=study_id, name=name, href=href, description=description,
            subsidy_enabled=subsidy_enabled, study_enabled=enabled,
            discoverable=discoverable)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    if key:
        try:
            click.echo(study[key])
        except KeyError:
            click.echo('Key "{}" not found'.format(key), err=True)
            exit(1)
    else:
        click.echo(util.pretty_json(study))


@participant.command(name='get_all')
@click.argument('study-id')
@click.option(
    '--token', required=True, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def participant_get_all(study_id, token, host, device_uuid):
    '''Get all participants of a study'''
    c = client.Client(host, device_uuid)
    c.set_refresh_token(token)

    try:
        participants = c.study_participants_get(study_id)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    click.echo(util.pretty_json(participants))


@participant.command()
@click.argument('study-id')
@click.argument('participant-ids', nargs=-1)
@click.option(
    '--token', required=True, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def get_raw_data(study_id, participant_ids, token, host, device_uuid):
    '''Get all participants of a study'''
    c = client.Client(host, device_uuid)
    c.set_refresh_token(token)

    try:
        raw_data = c.study_raw_data_get(study_id, participant_ids)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    click.echo(util.pretty_json(raw_data))


@cli.command()
@click.option(
    '--env', default='default',
    help='backend environment. Available environments are: {}'.format(
        util.get_envs_string()))
def host(env):
    if env in constants.ENVS:
        click.echo(constants.ENVS[env]['host'])
    else:
        click.echo(
            'Unknown environment. Available environments are: {}'.format(
                util.get_envs_string()), err=True)


@cli.command()
@click.argument('study-id', type=int)
@click.argument('external-id')
@click.argument('study-api-key')
@click.option(
    '--subsidy-in-cents', default=None, type=int,
    help='kit subsidy in cents provided by study')
@click.option(
    '--url-template', default=constants.DEEPLINK_URL_DEFAULT,
    help='template for generated URL, must contain \'{jwt}\'')
@click.option(
    '--print-url/--no-print-url', default=True,
    help='print complete deeplink URL or just JWT')
def jwt(
        study_id, external_id, study_api_key, subsidy_in_cents, url_template,
        print_url):
    if not print_url:
        url_template = None

    try:
        output = util.jwt_signed(
            study_id, external_id, study_api_key, subsidy_in_cents,
            url_template)
    except ValueError as e:
        click.echo(e, err=True)
        exit(1)
    except TypeError as e:
        click.echo(e, err=True)
        exit(1)

    click.echo(output)


OUTPUT_FORMAT_DEFAULT = 'csv'
ID_TYPE_DEFAULT = 'external'


@app.command(name='raw_data')
@click.argument('app-id')
@click.argument('input', type=click.File())
@click.argument('output', type=click.File('w'))
@click.option(
    '--id-type', type=click.Choice(['external', 'member']),
    default=ID_TYPE_DEFAULT,
    help=(
        'Whether ids should be interpreted as external ids or member (i.e. '
        'Gencove) ids [default: {}]'.format(ID_TYPE_DEFAULT))
    )
@click.option(
    '--output-format', type=click.Choice(['csv', 'json']),
    default=OUTPUT_FORMAT_DEFAULT,
    help='Output format [default: {}]'.format(OUTPUT_FORMAT_DEFAULT))
@click.option(
    '--csv-header/--no-csv-header', default=True,
    help='Output csv header [default: yes]')
@click.option(
    '--api-key', default=None, help=API_KEY_HELP, envvar=API_KEY)
@click.option(
    '--token', default=None, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def app_raw_data(
        app_id, input, output, id_type, output_format, csv_header,
        api_key, token, host, device_uuid):
    '''Get raw data for members of an app.

    INPUT and OUTPUT can be file paths or "-" for stdin and stdout.

    INPUT is expected to be one id per line.

    If using the "external" id type, multiple entries for the same external
    id may be returned, since it is not guaranteed to be unique. Member (i.e.,
    Gencove) ids are guaranteed to be unique.

    In case data is not available for a given id or the id is not found, it is
    skipped.

    Order of ids from input is not guaranteed to be preserved in output.

    No need to use both API key and login token, one is enough.
    '''
    c = client.Client(host, device_uuid)
    if token:
        c.set_refresh_token(token)
    elif api_key:
        c.set_api_key(api_key)
    else:
        click.echo('Could not locate an API key or login info', err=True)
        exit(1)

    ids = []
    for line in input:
        line_clean = line.strip()
        if len(line_clean) > 0:
            ids.append(line_clean)

    if len(ids) == 0:
        ids = None

    try:
        if id_type == 'member':
            raw_data = c.app_raw_data_get(
                app_id=app_id,
                member_ids=ids)
        elif id_type == 'external':
            raw_data = c.app_raw_data_get(
                app_id=app_id,
                external_ids=ids)
        else:
            click.echo(
                'An unexpected error occurred: unknown id type', err=True)
            exit(1)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    if output_format == 'csv':
        util.app_raw_data_csv(raw_data, output, header=csv_header)
    elif output_format == 'json':
        util.pretty_json(raw_data, output)
    else:
        click.echo(
            'An unexpected error occurred: unknown output format', err=True)
        exit(1)


@project.command(name='raw_data')
@click.argument('project-id')
@click.argument('input', type=click.File())
@click.argument('output', type=click.File('w'))
@click.option(
    '--id-type', type=click.Choice(['external', 'sample']),
    default=ID_TYPE_DEFAULT,
    help=(
        'Whether ids should be interpreted as external ids or sample (i.e. '
        'Gencove) ids [default: {}]'.format(ID_TYPE_DEFAULT))
    )
@click.option(
    '--output-format', type=click.Choice(['csv', 'json']),
    default=OUTPUT_FORMAT_DEFAULT,
    help='Output format [default: {}]'.format(OUTPUT_FORMAT_DEFAULT))
@click.option(
    '--csv-header/--no-csv-header', default=True,
    help='Output csv header [default: yes]')
@click.option(
    '--api-key', default=None, help=API_KEY_HELP, envvar=API_KEY)
@click.option(
    '--token', default=None, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def project_raw_data(
        project_id, input, output, id_type, output_format, csv_header,
        api_key, token, host, device_uuid):
    '''Get raw data for samples of a project.

    INPUT and OUTPUT can be file paths or "-" for stdin and stdout.

    INPUT is expected to be one id per line.

    If using the "external" id type, multiple entries for the same external
    id may be returned, since it is not guaranteed to be unique. Sample (i.e.,
    Gencove) ids are guaranteed to be unique.

    In case data is not available for a given id or the id is not found, it is
    skipped.

    Order of ids from input is not guaranteed to be preserved in output.

    No need to use both API key and login token, one is enough.
    '''
    c = client.Client(host, device_uuid)
    if token:
        c.set_refresh_token(token)
    elif api_key:
        c.set_api_key(api_key)
    else:
        click.echo('Could not locate an API key or login info', err=True)
        exit(1)

    ids = []
    for line in input:
        line_clean = line.strip()
        if len(line_clean) > 0:
            ids.append(line_clean)

    if len(ids) == 0:
        ids = None

    try:
        if id_type == 'sample':
            raw_data = c.project_raw_data_get(
                project_id=project_id,
                sample_ids=ids)
        elif id_type == 'external':
            raw_data = c.project_raw_data_get(
                project_id=project_id,
                external_ids=ids)
        else:
            click.echo(
                'An unexpected error occurred: unknown id type', err=True)
            exit(1)
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    if output_format == 'csv':
        util.project_raw_data_csv(raw_data, output, header=csv_header)
    elif output_format == 'json':
        util.pretty_json(raw_data, output)
    else:
        click.echo(
            'An unexpected error occurred: unknown output format', err=True)
        exit(1)


@credentials.command(name='upload', hidden=True)
@click.option(
    '--api-key', default=None, help=API_KEY_HELP, envvar=API_KEY)
@click.option(
    '--token', default=None, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def credentials_upload(api_key, token, host, device_uuid):
    '''Fetch upload credentials.

    No need to use both API key and login token, one is enough.
    '''
    c = client.Client(host, device_uuid)
    if token:
        c.set_refresh_token(token)
    elif api_key:
        c.set_api_key(api_key)
    else:
        click.echo('Could not locate an API key or login info', err=True)
        exit(1)

    try:
        credentials = c.credentials_upload_get()
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)
    except errors.CredentialsNotReady as e:
        click.echo(e, err=True)
        exit(1)

    click.echo(json.dumps(credentials['aws'], indent=4))


@contextlib.contextmanager
def aws_cli_credentials(api_key, transfer_acceleration=False):
    saved_api_key = os.getenv(API_KEY, default=None)
    os.environ[API_KEY] = api_key
    env_var_saved = {}
    for env_var in env_var_save_restore:
        env_var_saved[env_var] = os.getenv(env_var, default=None)
        if env_var_saved[env_var] is not None:
            del os.environ[env_var]
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b'[profile ' + util.to_bytes(PROFILE_NAME) + b']\n')
        f.write(b'credential_process = gencove credentials upload\n')
        if transfer_acceleration:
            f.write(b's3 =\n')
            f.write(b'  use_accelerate_endpoint = true\n')
        aws_config_file = f.name
        os.environ[AWS_CONFIG_FILE] = aws_config_file
    with tempfile.NamedTemporaryFile(delete=False) as f:
        # AWS CLI uses the default credentials in ~/.aws/credentials,
        # regardless of setting credential_process above ^.
        # This is a workaround to avoid it.
        f.write(b'[profile ' + util.to_bytes(PROFILE_NAME) + b']\n')
        aws_shared_credentials_file = f.name
        os.environ[AWS_SHARED_CREDENTIALS_FILE] = aws_shared_credentials_file
    try:
        yield
    finally:
        if saved_api_key is None:
            del os.environ[API_KEY]
        else:
            os.environ[API_KEY] = saved_api_key
        for env_var in env_var_save_restore:
            if env_var_saved[env_var] is not None:
                os.environ[env_var] = env_var_saved[env_var]
            # else:
            #     del os.environ[env_var]
        os.remove(aws_config_file)
        os.remove(aws_shared_credentials_file)


def callback_destination_path(ctx, param, value):
    if value[:len(UPLOAD_PREFIX)] != UPLOAD_PREFIX:
        raise click.BadParameter(
            'Destination path must start with "{}"'.format(UPLOAD_PREFIX))
    if len(value) > len(UPLOAD_PREFIX) and value[len(UPLOAD_PREFIX)] == '/':
        raise click.BadParameter(
            'Destination path has "/" after "{}"'.format(UPLOAD_PREFIX))
    return '/' + value[len(UPLOAD_PREFIX):]


def autogenerate_destination_path():
    date_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    uuid_string = uuid.uuid4().hex

    destination_path = '{prefix}cli-{date}-{uuid}/'.format(
        prefix=UPLOAD_PREFIX,
        date=date_string,
        uuid=uuid_string
    )
    click.echo(
        'Generating automatic upload destination: {}'.format(destination_path),
        err=True)
    return destination_path


def tmp_warning(ctx, param, value, *args, **kwargs):
    if value:
        click.echo(output_warning(TMP_UPLOADS_WARNING), err=True)
    return value


@upload.command()
@click.argument('source_path')
@click.argument(
    'destination_path', callback=callback_destination_path, required=False,
    default=autogenerate_destination_path)
@click.option(
    '--exclude', 'excludeinclude_values', multiple=True, default=None,
    help='Exclusion filter(s)')
@click.option(
    '--include', 'excludeinclude_values', multiple=True, default=None,
    help='Inclusion filter(s)')
@click.option(
    '--delete', default=None, is_flag=True,
    help=(
        'Files that exist in the destination but not in the source are '
        'deleted during sync.'
    ))
@click.option(
    '--dryrun', default=None, is_flag=True,
    help=(
        'Displays the operations that would be performed using the specified '
        'command without actually running them.'
    ))
@click.option(
    '--transfer-acceleration/--no-transfer-acceleration', default=False,
    help=(
        'Enables data transfer acceleration. Only useful when transferring '
        'data from outside the northeast United States.'
    ))
@click.option(
    '--tmp-warning/--no-tmp-warning', default=True, callback=tmp_warning,
    is_eager=True, help='Turn on/off warning about temporary storage')
@click.option(
    '--debug', default=None, is_flag=True, callback=debug_header,
    is_eager=True, help='Turn on debug logging')
@click.option(
    '--api-key', default=None, help=API_KEY_HELP, envvar=API_KEY)
@click.option(
    '--token', default=None, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def sync(
        source_path, destination_path, excludeinclude_values, delete, dryrun,
        transfer_acceleration, tmp_warning, debug, api_key, token, host, 
        device_uuid):
    '''Sync local directory with sequencing data to Gencove.

    SOURCE_PATH is the local path (or S3 URI) to sync to Gencove.

    DESTINATION_PATH is used for grouping uploaded files under a common
    prefix. If specified, must start with "gncv://".

    --include/--exclude filters work analogous to AWS CLI S3 upload filters.
    See here for details:
    https://docs.aws.amazon.com/cli/latest/reference/s3/index.html#use-of-exclude-and-include-filters

    --delete flag is analogous to AWS CLI S3 sync command:
    https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html

    No need to use both API key and login token, one is enough.
    '''
    # Get upload path
    c = client.Client(host, device_uuid)
    if token:
        c.set_refresh_token(token)
    elif api_key:
        c.set_api_key(api_key)
    else:
        click.echo('Could not locate an API key or login info', err=True)
        exit(1)

    click.echo('Fetching upload path', err=True)
    try:
        paths = c.paths_upload_get()
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    destination_path_full = '{}{}'.format(
        paths['aws']['path_s3'], destination_path)
    command = COMMAND_BASE + ['s3', 'sync', source_path, destination_path_full]
    if dryrun:
        command.append('--dryrun')
    if delete:
        command.append('--delete')
    if debug:
        command.append('--debug')
    if excludeinclude_values:
        excludeinclude_flags = []
        for el in sys.argv:
            if el in {'--exclude', '--include'}:
                excludeinclude_flags.append(el)
        for el_tuple in zip(excludeinclude_flags, excludeinclude_values):
            command.extend(el_tuple)

    click.echo('Fetching credentials and syncing', err=True)
    with aws_cli_credentials(
            api_key=api_key, transfer_acceleration=transfer_acceleration):
        util.run_command(command)


@upload.command()
@click.argument('source_path')
@click.argument(
    'destination_path', callback=callback_destination_path, required=False,
    default=autogenerate_destination_path)
@click.option(
    '--exclude', 'excludeinclude_values', multiple=True, default=None,
    help='Exclusion filter(s)')
@click.option(
    '--include', 'excludeinclude_values', multiple=True, default=None,
    help='Inclusion filter(s)')
@click.option(
    '--recursive', default=None, is_flag=True,
    help=(
        'Command is performed on all files or objects under the specified '
        'directory or prefix.'
    ))
@click.option(
    '--dryrun', default=None, is_flag=True,
    help=(
        'Displays the operations that would be performed using the specified '
        'command without actually running them.'
    ))
@click.option(
    '--transfer-acceleration/--no-transfer-acceleration', default=False,
    help=(
        'Enables data transfer acceleration. Only useful when transferring '
        'data from outside the northeast United States.'
    ))
@click.option(
    '--tmp-warning/--no-tmp-warning', default=True, callback=tmp_warning,
    is_eager=True, help='Turn on/off warning about temporary storage')
@click.option(
    '--debug', default=None, is_flag=True, callback=debug_header,
    is_eager=True, help='Turn on debug logging')
@click.option(
    '--api-key', default=None, help=API_KEY_HELP, envvar=API_KEY)
@click.option(
    '--token', default=None, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def cp(
        source_path, destination_path, excludeinclude_values, recursive,
        dryrun, transfer_acceleration, tmp_warning, debug, api_key, token,
        host, device_uuid):
    '''Copy a local file with sequencing data to Gencove.

    SOURCE_PATH is the local path (or S3 URI) to copy to Gencove.

    DESTINATION_PATH is used for grouping uploaded files under a common
    identifier. If specified, must start with "gncv://".

    --include/--exclude filters work analogous to AWS CLI S3 upload filters.
    See here for details:
    https://docs.aws.amazon.com/cli/latest/reference/s3/index.html#use-of-exclude-and-include-filters

    --recursive flag is analogous to AWS CLI S3 cp command:
    https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html

    No need to use both API key and login token, one is enough.
    '''
    if source_path == '-' and destination_path == '/':
        click.echo(
            'DESTINATION_PATH should be more than "/" when SOURCE_PATH is "-"')
        exit(1)
    # Get upload path
    c = client.Client(host, device_uuid)
    if token:
        c.set_refresh_token(token)
    elif api_key:
        c.set_api_key(api_key)
    else:
        click.echo('Could not locate an API key or login info', err=True)
        exit(1)

    click.echo('Fetching upload path', err=True)
    try:
        paths = c.paths_upload_get()
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    destination_path_full = '{}{}'.format(
        paths['aws']['path_s3'], destination_path)
    command = COMMAND_BASE + ['s3', 'cp', source_path, destination_path_full]
    if dryrun:
        command.append('--dryrun')
    if recursive:
        command.append('--recursive')
    if debug:
        command.append('--debug')
    if excludeinclude_values:
        excludeinclude_flags = []
        for el in sys.argv:
            if el in {'--exclude', '--include'}:
                excludeinclude_flags.append(el)
        for el_tuple in zip(excludeinclude_flags, excludeinclude_values):
            command.extend(el_tuple)

    click.echo('Fetching credentials and copying', err=True)
    with aws_cli_credentials(
            api_key=api_key, transfer_acceleration=transfer_acceleration):
        util.run_command(command)


@upload.command()
@click.argument(
    'destination_path', callback=callback_destination_path, required=False,
    default=UPLOAD_PREFIX)
@click.option(
    '--recursive', default=None, is_flag=True,
    help=(
        'Command is performed on all files or objects under the specified '
        'directory or prefix.'
    ))
@click.option(
    '--human-readable', default=None, is_flag=True,
    help='Displays file sizes in human readable format')
@click.option(
    '--summarize', default=None, is_flag=True,
    help='Displays summary information (number of objects, total size)')
@click.option(
    '--debug', default=None, is_flag=True, callback=debug_header,
    is_eager=True, help='Turn on debug logging')
@click.option(
    '--api-key', default=None, help=API_KEY_HELP, envvar=API_KEY)
@click.option(
    '--token', default=None, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def ls(
        destination_path, recursive, human_readable, summarize, debug,
        api_key, token, host, device_uuid):
    '''List uploaded data on Gencove.

    DESTINATION_PATH is used for grouping uploaded files under a common
    identifier. If specified, must start with "gncv://".

    --recursive flag is analogous to AWS CLI S3 ls command:
    https://docs.aws.amazon.com/cli/latest/reference/s3/ls.html

    No need to use both API key and login token, one is enough.
    '''
    # Get upload path
    c = client.Client(host, device_uuid)
    if token:
        c.set_refresh_token(token)
    elif api_key:
        c.set_api_key(api_key)
    else:
        click.echo('Could not locate an API key or login info', err=True)
        exit(1)

    click.echo('Fetching upload path', err=True)
    try:
        paths = c.paths_upload_get()
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    destination_path_full = '{}{}'.format(
        paths['aws']['path_s3'], destination_path)
    command = COMMAND_BASE + ['s3', 'ls', destination_path_full]
    if recursive:
        command.append('--recursive')
    if human_readable:
        command.append('--human-readable')
    if summarize:
        command.append('--summarize')
    if debug:
        command.append('--debug')

    click.echo('Fetching credentials and listing', err=True)
    with aws_cli_credentials(api_key=api_key):
        util.run_command(command)


@upload.command()
@click.argument(
    'destination_path', callback=callback_destination_path, required=True)
@click.option(
    '--exclude', 'excludeinclude_values', multiple=True, default=None,
    help='Exclusion filter(s)')
@click.option(
    '--include', 'excludeinclude_values', multiple=True, default=None,
    help='Inclusion filter(s)')
@click.option(
    '--recursive', default=None, is_flag=True,
    help=(
        'Command is performed on all files or objects under the specified '
        'directory or prefix.'
    ))
@click.option(
    '--dryrun', default=None, is_flag=True,
    help=(
        'Displays the operations that would be performed using the specified '
        'command without actually running them.'
    ))
@click.option(
    '--debug', default=None, is_flag=True, callback=debug_header,
    is_eager=True, help='Turn on debug logging')
@click.option(
    '--api-key', default=None, help=API_KEY_HELP, envvar=API_KEY)
@click.option(
    '--token', default=None, help=TOKEN_HELP, envvar=TOKEN)
@click.option(
    '--host', default=None, help=HOST_HELP, envvar=HOST)
@click.option(
    '--device-uuid', default=None, help=DEVICE_UUID_HELP, envvar=DEVICE_UUID)
def rm(
        destination_path, excludeinclude_values, recursive, dryrun, debug,
        api_key, token, host, device_uuid):
    '''Delete uploaded data on Gencove.

    DESTINATION_PATH is used for grouping uploaded files under a common
    identifier. Must start with "gncv://".

    --include/--exclude filters work analogous to AWS CLI S3 upload filters.
    See here for details:
    https://docs.aws.amazon.com/cli/latest/reference/s3/index.html#use-of-exclude-and-include-filters

    --recursive flag is analogous to AWS CLI S3 rm command:
    https://docs.aws.amazon.com/cli/latest/reference/s3/rm.html

    No need to use both API key and login token, one is enough.
    '''
    # Get upload path
    c = client.Client(host, device_uuid)
    if token:
        c.set_refresh_token(token)
    elif api_key:
        c.set_api_key(api_key)
    else:
        click.echo('Could not locate an API key or login info', err=True)
        exit(1)

    click.echo('Fetching upload path', err=True)
    try:
        paths = c.paths_upload_get()
    except errors.HTTPError as e:
        text_out = util.extract_backend_message(e.response)
        click.echo(text_out, err=True)
        exit(1)
    except errors.GencoveClientError as e:
        click.echo(e, err=True)
        exit(1)

    destination_path_full = '{}{}'.format(
        paths['aws']['path_s3'], destination_path)
    command = COMMAND_BASE + ['s3', 'rm', destination_path_full]
    if dryrun:
        command.append('--dryrun')
    if recursive:
        command.append('--recursive')
    if debug:
        command.append('--debug')
    if excludeinclude_values:
        excludeinclude_flags = []
        for el in sys.argv:
            if el in {'--exclude', '--include'}:
                excludeinclude_flags.append(el)
        for el_tuple in zip(excludeinclude_flags, excludeinclude_values):
            command.extend(el_tuple)

    click.echo('Fetching credentials and deleting', err=True)
    with aws_cli_credentials(api_key=api_key):
        util.run_command(command)
