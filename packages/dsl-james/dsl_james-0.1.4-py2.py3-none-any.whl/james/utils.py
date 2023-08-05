"""
Utilities
"""
from typing import Dict, Union, Callable
from pathlib import Path
import subprocess
import re
import time
from functools import wraps

import click
from loguru import logger


def cmd(command: str, return_success: bool = False, no_error: bool = False) -> Union[str, bool]:
    logger.debug(f'Executing system command: [{command}]')
    if return_success:
        # only check if a command runs successfully
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    else:
        res = subprocess.run(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0 and not no_error:
            logger.error(res.stdout.strip())
            raise SystemError(res.stderr)
        return res.stdout.strip()


def az_cmd(command: str, params: Dict, **kwargs) -> Union[str, bool]:
    """
    Wrapper for slightly easing az cli commands

    Args:
        command (str): base az cli command, e.g. 'az login' or 'az container create' (az part may be omitted)
        params (Dict): dict with parameter key values

    Returns:
        str: result of the command
    """
    prefix = '' if command[:3] == 'az ' else 'az '
    param_str = ' '.join([
        f'--{key.replace("_", "-")} "{value}"'
        for key, value in params.items()
    ])
    full_command = f'{prefix}{command} {param_str}'
    return cmd(full_command, **kwargs)


def check_path(
    path: Union[str, Path], 
    resolve: bool = True, 
    check_exists: bool = False, 
    check_file: bool = False, 
    check_dir: bool = False
) -> Path:
    if isinstance(path, str) and '~' in path:
        path = path.replace('~', Path.home())
    
    if resolve:
        path = Path(path).resolve()
    
    if check_dir:
        assert path.is_dir()
    elif check_file:
        assert path.is_file()
    elif check_exists:
        assert path.exists()

    return path
    

class ProjectNameType(click.ParamType):
    """
    Custom CLI parameter type for Python version specification
    """
    name = 'project-name'

    def convert(self, value, param, ctx):
        found = re.match(r'[a-z0-9]+(-[a-z0-9]+)*', value)
        if not found:
            self.fail(f'{value} is not a valid project name. Use lowercase-with-dashes', param, ctx, )
        return value


class PythonVersionType(click.ParamType):
    """
    Custom CLI parameter type for Python version specification
    """
    name = 'python-version'

    def convert(self, value, param, ctx):
        found = re.match(r'3\.[56789](\.\d)?', value)
        if not found:
            self.fail(f'{value} is not a valid Python version', param, ctx, )
        return value


def timeit(units='s', method=logger.info):
    """
    Decorator for timing functions (that run for a significant while)

    Args:
        units: (string) [s, ms]
        method: (callable) [print, logging.info, logging.debug]

    Returns:
        decorated function that prints or logs execution time
    """
    def timeit_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            t0 = time.time()
            res = func(*args, **kwargs)
            t1 = time.time()
            if units == 'ms':
                diff = f'{(t1 - t0) * 1000:.0f} ms'
            else:
                diff = f'{(t1 - t0):.1f} seconds'
            msg = f'Call to {func.__name__} took {diff}'
            method(msg)
            return res
        return wrapper
    return timeit_decorator


class Timer:

    def __init__(self):
        self.time = time.time()

    def __call__(self, msg: str = None, update: bool = True, method: Callable = logger.info) -> None:
        new_time = time.time()
        diff = new_time - self.time

        # update last timestamp
        if update:
            self.time = new_time

        if diff < 1.:
            duration = f'{diff * 1000:.0f} ms'
        else:
            duration = f'{diff:.1f} seconds'

        method(f'Time elapsed: {duration} at checkpoint {msg}')
