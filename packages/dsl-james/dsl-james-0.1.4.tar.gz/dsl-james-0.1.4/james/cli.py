"""Console script for james."""
import sys
from pathlib import Path

from loguru import logger
import click
from termcolor import colored

from james import __version__
from james.utils import check_path, cmd, timeit, PythonVersionType
from james.config import IgniteConfig, IgniteInvalidStateError
from james.azure import AzureSetup
from james.james import Ignition
from james.review import CodeInspection


logger.remove(0)
logger.add(sys.stderr, level='INFO')


INTRO_TEXT = r"""

     ██╗ █████╗ ███╗   ███╗███████╗███████╗
     ██║██╔══██╗████╗ ████║██╔════╝██╔════╝
     ██║███████║██╔████╔██║█████╗  ███████╗
██   ██║██╔══██║██║╚██╔╝██║██╔══╝  ╚════██║
╚█████╔╝██║  ██║██║ ╚═╝ ██║███████╗███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝                                          
                                           
█████████████████████████████████████████████████████████████████████████████████
██▀▄─██─▄─▄─███▄─█─▄█─▄▄─█▄─██─▄█▄─▄▄▀███─▄▄▄▄█▄─▄▄─█▄─▄▄▀█▄─█─▄█▄─▄█─▄▄▄─█▄─▄▄─█
██─▀─████─██████▄─▄██─██─██─██─███─▄─▄███▄▄▄▄─██─▄█▀██─▄─▄██▄▀▄███─██─███▀██─▄█▀█
▀▄▄▀▄▄▀▀▄▄▄▀▀▀▀▀▄▄▄▀▀▄▄▄▄▀▀▄▄▄▄▀▀▄▄▀▄▄▀▀▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▀▄▄▀▀▀▄▀▀▀▄▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀

************************************************ powered by Data Science Lab ////                                                                                                   

Fast & easy project startup 
"""


"""
- Main: 
- setup: only set variables
- show: show variables / status
- go: execute (if vars are set)

Typical workflow

$ [~/projects/] james setup
    -> reads / creates file in ~
$ [~/projects/] james go
    -> reads file in ~, copies file to ~/projects/my-project/  
$ [~/projects/my-project] james show
    -> reads file in ~/projects/my-project/ 
"""


def msg_error(msg: str) -> None:
    click.secho(f'\n\n{msg}\n', bg='red', fg='white', bold=True)


def msg_success(msg: str) -> None:
    click.secho(f'\n\n{msg}\n', bg='green', fg='white', bold=True)


def bold(txt: str) -> str:
    return colored(txt, attrs=['bold'])


def pprompt(text, default, options=None):
    text = colored(f'✣ {text}', 'blue', attrs=['bold'])
    if isinstance(options, list):
        ptype = click.Choice(options, case_sensitive=True)
    else:
        ptype = str
    #default = colored(default, attrs=['underline'])
    return click.prompt(text=text, type=ptype, default=default)


@click.group()
@click.version_option(message='You are using %(prog)s version %(version)s')
@click.pass_context
@timeit()
def main(ctx: click.Context) -> None:
    """
    Console script for james.
    The main function only reads the config
    """
    click.secho(INTRO_TEXT, fg='cyan')

    logger.info('Creating config object')
    ctx.obj = IgniteConfig()


@main.command()
@click.pass_context
@click.confirmation_option(prompt="""
This will prompt for generic settings that apply to all projects.
If you change this it may invalidate existing projects.

Are you sure you want to continue?
""")
def setup(ctx: click.Context) -> None:
    """
    One-time setup for generic settings like
    - Azure & Azure DevOps defaults
    - Projects dir

    Args:
        ctx (click.Context): ctx.obj contains the IgniteConfig object
    """
    # handle git provider
    git_provider = pprompt(
        text='Choose a git provider',
        #type=click.Choice(['Azure DevOps Repos', 'Github'], case_sensitive=True),
        options=['Azure DevOps Repos', 'Github'],
        default='Azure DevOps Repos'
    )
    ctx.obj.set('META', 'git_provider', git_provider)
    if git_provider == 'Azure DevOps Repos':
        devops_organization = click.prompt(
            text='✣ Enter Azure DevOps organization name (https://dev.azure.com/<organization>)',
            type=str,
            default='data-science-lab'
        )
        ctx.obj.set('AZUREDEVOPS', 'devops_organization', devops_organization)
    elif git_provider == 'Github':
        github_username = click.prompt(
            text='Enter Github username',
            type=str,
            default=''
        )
        ctx.obj.set('GITHUB', 'github_username', github_username)
    else:
        raise ValueError(f'Unsupported git provider "{git_provider}"')

    # handle cloud resource provider
    cloud_provider = click.prompt(
        text='Choose a cloud provider (currently only Azure is supported!)',
        type=click.Choice(['Azure'], case_sensitive=True),
        default='Azure'
    )
    ctx.obj.set('META', 'cloud_provider', cloud_provider)
    if cloud_provider == 'Azure':
        # ask subscription
        pass  # subscription can be project specific

    # set user project directory
    projects_dir = click.prompt(
        text='Choose a directory containing your projects (use "~" for your home dir)',
        type=click.Path(),
        default='~/projects'
    )
    projects_dir = Path(projects_dir.replace('~', Path.home().as_posix())).resolve()
    if not projects_dir.exists():
        raise FileExistsError(f'Directory {projects_dir} does not exist. Please check if it\'s correct.')
    ctx.obj.set('META', 'projects_dir', projects_dir.as_posix())

    msg_success('All set!\nYou can now use james init from your projects dir to start a new project.')


@main.command()
@click.pass_context
def init(ctx: click.Context) -> None:
    """
    Start a new project
    Set project settings via prompts

    Args:
        ctx (click.Context): ctx.obj contains the IgniteConfig object
    """
    if Path.cwd() == Path.home():
        msg_error('Cannot init a new project here.\nChange to projects dir first')
        return
    if ctx.obj.is_existing_project:
        #raise IgniteInvalidStateError(f'Current config defines an existing project. Cannot call james init here.')
        msg_error('Current config defines an existing project. Cannot call james init here.')
        return

    # new project: clear existing values in config file
    ctx.obj.clear()

    if ctx.obj.get('META', 'cloud_provider') == 'Azure':
        # set Azure config
        azsetup = AzureSetup()

        # azure subscription
        subscriptions = azsetup.get_subscriptions()
        options = [
            sub['name']
            for sub in subscriptions
            if sub['isDefault']
        ] + [
            sub['name']
            for sub in subscriptions
            if not sub['isDefault']
        ]
        subscription_name = click.prompt(
            text='Choose Azure subscription',
            type=click.Choice(options, case_sensitive=True),
            default=options[0]
        )
        subscription_id = [
            sub['id']
            for sub in subscriptions
            if sub['name'] == subscription_name
        ][0]
        ctx.obj.set('AZURE', 'subscription_name', subscription_name)
        ctx.obj.set('AZURE', 'subscription_id', subscription_id)
        azsetup.set_subscription(subscription_id)

    if ctx.obj.get('META', 'git_provider') == 'Azure DevOps Repos':
        # Azure DevOps settings
        devops_projects = azsetup.get_devops_projects()
        project = click.prompt(
            text='Choose Azure DevOps project',
            type=click.Choice(devops_projects, case_sensitive=True),
            default=azsetup.DEFAULT_PROJECT
        )
        ctx.obj.set('AZUREDEVOPS', 'devops_organization', azsetup.DEFAULT_ORG)
        ctx.obj.set('AZUREDEVOPS', 'devops_project', project)
        azsetup.set_devops_project(project)

    # prompt for project setting values
    for section, var in ctx.obj.iter_settings(project_only=True):
        value = click.prompt(
            text=var['description'],
            type=var['type'],
            default=var['default']()
        )
        ctx.obj.set(section, var['name'], value)

    ctx.obj.cleanup()


@main.command()
@click.pass_context
@click.argument('section')
@click.argument('key')
@click.argument('value')
def set(ctx: click.Context, section: str, key: str, value: str) -> None:
    """
    Set a single value
    """
    logger.info(f'Setting {section}.{key} = {value}')
    ctx.obj.set(section, key, value)


@main.command()
@click.pass_context
def show(ctx: click.Context) -> None:
    """
    Display settings
    """
    try:
        #ctx.obj.show(method=click.echo)
        file, contents = ctx.obj.list()
        prefix = colored('\n\n❯ Settings read from ', 'white', 'on_blue')
        file = colored(file.resolve(), 'white', 'on_blue', ['bold'])
        postfix = colored(':\n', 'white', 'on_blue')
        click.echo(f'{prefix}{file}{postfix}')
        click.echo(contents)
    except FileExistsError:
        #click.secho('There is no project defined in this directory. Run "james init" first', bg='red', bold=True)
        msg_error('There is no project defined in this directory. Run "james init" first')


@main.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """
    Check status of stages for ignition
    """
    try:
        plan = Ignition(config=ctx.obj)
        click.echo(plan.stage_report())
    except ValueError as e:
        logger.error(e)
        msg_error('There is no project defined in this directory. Run "james init" first')


@main.command()
@click.pass_context
@click.argument('directory')
def review(ctx: click.Context, directory: str = None) -> None:
    """
    Linting / code review
    """
    # if directory is None:
    #     path = Path.cwd()
    # else:
    #     path = Path(directory)
    #     if not path.is_dir():
    #         raise ValueError(f'Path {directory} is not a valid directory')
    path = check_path(directory or Path.cwd(), check_dir=True)

    inspection = CodeInspection(path=path)
    report = inspection()
    click.echo(report)


@main.command()
@click.pass_context
@click.confirmation_option(prompt="""
This will execute the actual project setup work:
- create a git repository
- create a new local project dir from a cookiecutter template
- create a python environment

Are you sure you want to continue?
""")
def go(ctx: click.Context) -> None:
    """
    Execute actions for project start
    """
    Ignition(config=ctx.obj).execute(callback_fn=click.echo)


if __name__ == "__main__":
    main()
