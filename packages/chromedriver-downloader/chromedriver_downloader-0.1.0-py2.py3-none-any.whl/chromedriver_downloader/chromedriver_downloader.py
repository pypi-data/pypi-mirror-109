import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

import wget

DEFAULT_DOWNLOAD_ROOT = 'https://chromedriver.storage.googleapis.com'


def version_map(version):
    versions = {
        '80': '80.0.3987.16',
        '79': '79.0.3945.36',
        '78': '78.0.3904.105',
        '77': '77.0.3865.40',
        '76': '76.0.3809.126',
        '75': '75.0.3770.140',
        '74': '74.0.3729.6',
        '73': '73.0.3683.68',
    }
    result = versions.get(version)
    if result is None:
        raise ValueError(f'Versão do chrome não esperada: {version}')

    return result


def platform_map(platform):
    name = {
        'linux': '_linux64',
        'darwin': '_mac64'
    }
    result = name.get(platform)

    if result is None:
        raise ValueError(f'Plataforma não esperada: {platform}')

    return result


def platform_name():
    return sys.platform


def get_chromedriver_name():
    chromedriver_name_map = {
        "linux": "chromedrive_linux",
        "darwin": "chromedriver_darwin"
    }
    platform = platform_name()
    if platform not in chromedriver_name_map:
        raise ValueError("Platform {} não esperada.".format(platform))

    return chromedriver_name_map[platform]


def ensure_chromedriver(assets_path):
    driver_name = 'chromedriver'
    driver_path = Path(assets_path) / driver_name
    if driver_path.exists():
        return driver_path

    _make_target_dir(driver_path)

    version = get_chrome_version()

    download_driver(version, sys.platform, driver_path)

    _chmod(driver_path)

    return driver_path


def _chmod(driver_path):
    driver_path.chmod(driver_path.stat().st_mode |
                      stat.S_IXGRP |
                      stat.S_IXUSR |
                      stat.S_IXOTH)


def _make_target_dir(driver_path):
    driver_path.parent.mkdir(parents=True, exist_ok=True)


def download_driver(version,
                    platform,
                    output_path,
                    download_root=DEFAULT_DOWNLOAD_ROOT):

    platform_part = platform_map(platform)
    full_version = version_map(version)
    driver_url = _make_driver_url(download_root, full_version, platform_part)

    _download_driver(driver_url, output_path)


def _make_driver_url(download_root, full_version, platform_part):
    file_name = f'chromedriver{platform_part}.zip'
    driver_url = f'{download_root}/{full_version}/{file_name}'
    return driver_url


def _download_driver(driver_url, output_path):
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_driver_zip = _make_target_path(tmpdirname)
        wget.download(driver_url, str(temp_driver_zip))

        _extract_zip(output_path, temp_driver_zip)


def _extract_zip(output_path, temp_driver_zip):
    with ZipFile(temp_driver_zip) as zipfile:
        zipfile.extract('chromedriver', output_path.parent)


def _make_target_path(tmpdirname):
    temp_driver_zip = Path(tmpdirname) / 'chromedriver.zip'
    return temp_driver_zip


def get_chrome_version():
    chrome_path = find_chrome()
    version_info = subprocess.check_output([chrome_path, '--version'])
    version = _extract_version(version_info)

    return version


def _extract_version(version_info):
    res = re.search(r'[^\d]*(\d+)\..*', version_info.decode('utf-8'))
    if not res:
        raise ValueError('Não consegui obter a versão do chrome neste '
                         'sistema.')

    return res.groups()[0]


def find_chrome():
    """
    Busca o executável do chrome na máquina.
    Inicialmente vamos fazer a busca em lugares conhecidos.
    Com o tempo essa função pode ir sendo aprimorada por plataforma e
    considerando possíveis variações entre máquinas.
    :return: Caminho completo (absoluto) do executável do chrome (se houver)
    """
    finder_map = {
        'linux': find_chrome_linux,
        'darwin': find_chrome_darwin
    }
    if sys.platform not in finder_map:
        raise ValueError('Platform não esperado: {}'.format(sys.platform))

    return finder_map[sys.platform]()


def find_chrome_linux():
    known_locals = [
        '/usr/bin/google-chrome-stable',
        '/usr/bin/google-chrome'
    ]

    for current_local in known_locals:
        chrome_path = Path(current_local)
        if chrome_path.exists():
            return current_local

    return None


def find_chrome_darwin():
    """To be defined"""
    raise NotImplementedError
