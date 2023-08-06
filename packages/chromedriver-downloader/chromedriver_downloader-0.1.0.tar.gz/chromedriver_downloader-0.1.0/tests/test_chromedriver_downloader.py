import stat
import sys
from unittest.mock import patch, MagicMock

# noinspection PyPackageRequirements
import pytest
# noinspection PyPackageRequirements
from pytest import raises

# noinspection PyProtectedMember
from chromedriver_downloader.chromedriver_downloader import platform_name, \
    get_chromedriver_name, ensure_chromedriver, _chmod, _make_target_dir, \
    version_map, platform_map, download_driver, _make_driver_url, \
    _download_driver, _extract_zip, _make_target_path, get_chrome_version, \
    _extract_version, find_chrome, find_chrome_linux, find_chrome_darwin

prefix = 'chromedriver_downloader.chromedriver_downloader'


def test_version_map():
    result = version_map('80')

    assert result == '80.0.3987.16'


def test_version_map_unknown():
    with raises(ValueError) as excinfo:
        version_map('XX')

    assert str(excinfo.value) == 'Versão do chrome não esperada: XX'


def test_platform_map():
    result = platform_map('linux')

    assert result == '_linux64'


def test_platform_map_unknown():
    with raises(ValueError) as excinfo:
        platform_map('xxx')

    assert str(excinfo.value) == 'Plataforma não esperada: xxx'


@patch(f'{prefix}.sys')
def test_platform_name(mock_sys):
    result = platform_name()

    assert (result == mock_sys.platform)


# noinspection PyUnusedLocal
@patch(f'{prefix}.platform_name', return_value='linux')
def test_get_chromedriver_name_linux(mock_platform_name):
    result = get_chromedriver_name()

    assert result == 'chromedrive_linux'


# noinspection PyUnusedLocal
@patch(f'{prefix}.platform_name', return_value='darwin')
def test_get_chromedriver_name_darwin(mock_platform_name):
    result = get_chromedriver_name()

    assert result == 'chromedriver_darwin'


# noinspection PyUnusedLocal
@patch(f'{prefix}.platform_name', return_value='other')
def test_get_chromedriver_name_other(mock_platform_name):
    with(raises(ValueError)) as exc_info:
        get_chromedriver_name()

    assert (str(exc_info.value) == 'Platform other não esperada.')


@patch(f'{prefix}.Path')
def test_ensure_chromedriver_already_exists(mock_path):
    mock_asserts_path = MagicMock()
    result = ensure_chromedriver(mock_asserts_path)

    mock_path.assert_called_with(mock_asserts_path)
    mock_path().__truediv__.assrt_called_with('chromedriver')
    mock_path().__truediv__().exists.assert_called_once()

    assert result == mock_path().__truediv__()


# noinspection PyUnusedLocal
@patch(f'{prefix}.Path')
@patch(f'{prefix}.get_chrome_version')
@patch(f'{prefix}._make_target_dir')
@patch(f'{prefix}.download_driver')
@patch(f'{prefix}._chmod')
def test_ensure_chromedriver_needs_download(mock_chmod,
                                            mock_download_driver,
                                            mock_make_target_dir,
                                            mock_get_chrome_version,
                                            mock_path):
    mock_asserts_path = MagicMock()
    mock_path.return_value = MagicMock(__truediv__=MagicMock(
        return_value=MagicMock(
            exists=MagicMock(return_value=False)
        )
    ))
    result = ensure_chromedriver(mock_asserts_path)

    mock_path.assert_called_with(mock_asserts_path)
    mock_path().__truediv__.assrt_called_with('chromedriver')
    mock_path().__truediv__().exists.assert_called_once()
    mock_driver_path = mock_path().__truediv__()

    mock_get_chrome_version.assert_called_once()
    mock_version = mock_get_chrome_version()
    mock_download_driver.assert_called_with(mock_version,
                                            sys.platform,
                                            mock_driver_path)
    mock_chmod.assert_called_with(mock_driver_path)

    assert result == mock_driver_path


def test_chmod():
    mock_path = MagicMock()

    _chmod(mock_path)

    mock_path.chmod.assert_called_with(
        mock_path.stat().st_mode | stat.S_IXGRP | stat.S_IXUSR | stat.S_IXOTH)


def test_make_target_dir():
    mock_path = MagicMock()
    _make_target_dir(mock_path)

    mock_path.parent.mkdir.assert_called_with(parents=True, exist_ok=True)


@patch(f'{prefix}.platform_map')
@patch(f'{prefix}.version_map')
@patch(f'{prefix}._make_driver_url')
@patch(f'{prefix}._download_driver')
def test_download_driver(mock_download_driver,
                         mock_make_driver_url,
                         mock_version_map,
                         mock_platform_map):
    mock_version = MagicMock()
    mock_platform = MagicMock()
    mock_output_path = MagicMock()
    mock_download_root = MagicMock()
    download_driver(mock_version,
                    mock_platform,
                    mock_output_path,
                    mock_download_root)
    mock_platform_map.assert_called_with(mock_platform)
    mock_version_map.assert_called_with(mock_version)
    mock_make_driver_url.assert_called_with(mock_download_root,
                                            mock_version_map(),
                                            mock_platform_map())
    mock_download_driver.assert_called_with(mock_make_driver_url(),
                                            mock_output_path)


def test_make_driver_url():
    mock_download_root = MagicMock()
    mock_full_version = MagicMock()
    mock_platform_part = MagicMock()
    result = _make_driver_url(mock_download_root,
                              mock_full_version,
                              mock_platform_part)

    file_name = f'chromedriver{mock_platform_part}.zip'
    assert result == f'{mock_download_root}/{mock_full_version}/{file_name}'


@patch(f'{prefix}.tempfile')
@patch(f'{prefix}._make_target_path')
@patch(f'{prefix}.wget')
@patch(f'{prefix}._extract_zip')
def test__download_driver(mock_extract_zip,
                          mock_wget,
                          mock_make_target_path,
                          mock_tempfile):
    mock_driver_url = MagicMock()
    mock_output_path = MagicMock()
    _download_driver(mock_driver_url, mock_output_path)

    mock_tempfile.TemporaryDirectory.assert_called_once()
    mock_tmpdirname = mock_tempfile.TemporaryDirectory().__enter__()
    mock_make_target_path.assert_called_with(mock_tmpdirname)
    mock_wget.download.assert_called_with(mock_driver_url,
                                          str(mock_make_target_path()))
    mock_extract_zip.assert_called_with(mock_output_path,
                                        mock_make_target_path())


@patch(f'{prefix}.ZipFile')
def test_extract_zip(mock_zipfile):
    mock_output_path = MagicMock()
    mock_temp_driver_zip = MagicMock()
    _extract_zip(mock_output_path, mock_temp_driver_zip)

    mock_zipfile.assert_called_with(mock_temp_driver_zip)
    mock_zipfile = mock_zipfile().__enter__()
    mock_zipfile.extract.assert_called_with('chromedriver',
                                            mock_output_path.parent)


@patch(f'{prefix}.Path')
def test_make_target_path(mock_path):
    mock_tempdirname = MagicMock()
    result = _make_target_path(mock_tempdirname)

    mock_path.assert_called_with(mock_tempdirname)
    mock_path().__truediv__.assert_called_with('chromedriver.zip')
    assert result == mock_path().__truediv__()


@patch(f'{prefix}.find_chrome')
@patch(f'{prefix}.subprocess')
@patch(f'{prefix}._extract_version')
def test_get_chrome_version(mock_extract_version,
                            mock_subprocess,
                            mock_find_chrome):
    result = get_chrome_version()

    mock_find_chrome.assert_called_once()
    mock_chrome_path = mock_find_chrome()

    mock_subprocess.check_output.assert_called_with([mock_chrome_path,
                                                     '--version'])
    mock_extract_version.assert_called_with(mock_subprocess.check_output())

    assert result == mock_extract_version()


@pytest.mark.parametrize('test_input, expected',
                         [
                             (b'80.0.3987.16', '80'),
                             (b'79.0.3945.36', '79'),
                             (b'78.0.3904.105', '78'),
                             (b'77.0.3865.40', '77'),
                             (b'76.0.3809.126', '76'),
                             (b'75.0.3770.140', '75'),
                             (b'74.0.3729.6', '74'),
                             (b'73.0.3683.68', '73')
                         ])
def test_extract_version(test_input, expected):
    assert _extract_version(test_input) == expected


def test_extract_version_fail():
    with raises(ValueError) as excinfo:
        _extract_version(b'asf')

    assert str(excinfo.value) == 'Não consegui obter a versão ' \
                                 'do chrome neste sistema.'


@pytest.mark.parametrize('platform, finder',
                         [
                             ('linux', 'find_chrome_linux'),
                             ('darwin', 'find_chrome_darwin'),
                         ])
def test_find_chrome(platform, finder):
    patch_sys = patch(f'{prefix}.sys', platform=platform)
    patch_findr = patch(f'{prefix}.{finder}')
    patch_sys.start()
    mock_finder = patch_findr.start()

    result = find_chrome()

    mock_finder.assert_called_once()

    assert result == mock_finder()

    patch_findr.stop()
    patch_sys.stop()


# noinspection PyUnusedLocal
@patch(f'{prefix}.sys', platform='xxx')
def test_find_chrome_fail(mock_sys):
    with raises(ValueError) as excinfo:
        find_chrome()

    assert str(excinfo.value) == 'Platform não esperado: xxx'


# noinspection PyUnusedLocal
@patch(f'{prefix}.Path')
def test_find_chrome_linux(mock_path):
    result = find_chrome_linux()

    assert result == '/usr/bin/google-chrome-stable'


# noinspection PyUnusedLocal
@patch(f'{prefix}.Path', side_effect=[
    MagicMock(exists=MagicMock(return_value=False)),
    MagicMock(exists=MagicMock(return_value=True))])
def test_find_chrome_linux_second(mock_path):
    result = find_chrome_linux()

    assert result == '/usr/bin/google-chrome'


# noinspection PyUnusedLocal
@patch(f'{prefix}.Path', return_value=MagicMock(
    exists=MagicMock(return_value=False)))
def test_find_chrome_linux_fail(mock_path):
    result = find_chrome_linux()

    assert result is None


def test_find_chrome_darwin():
    with raises(NotImplementedError):
        find_chrome_darwin()
