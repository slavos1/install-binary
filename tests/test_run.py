from argparse import Namespace

import pytest  # type: ignore

from install_binary.install import install


@pytest.skip("TODO")  # type: ignore
def test_install() -> None:
    install(Namespace(a=1))
