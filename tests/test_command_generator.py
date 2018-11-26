from tempfile import NamedTemporaryFile

import pytest

from node_launcher.command_generator import CommandGenerator
from node_launcher.configuration import Configuration
from node_launcher.configuration.bitcoin_configuration import \
    BitcoinConfiguration
from node_launcher.constants import OPERATING_SYSTEM, DARWIN, BITCOIN_QT_PATH


@pytest.fixture
def command_generator():
    with NamedTemporaryFile(suffix='-bitcoin-mainnet.conf', delete=False) as f_main:
        with NamedTemporaryFile(suffix='-bitcoin-testnet.conf', delete=False) as f_test:
            bitcoin_mainnet_conf = BitcoinConfiguration(f_main.name)
            bitcoin_testnet_conf = BitcoinConfiguration(f_test.name)
            command_generator = CommandGenerator(
                mainnet_conf=Configuration('mainnet', bitcoin_mainnet_conf),
                testnet_conf=Configuration('testnet', bitcoin_testnet_conf)
            )
    return command_generator


class TestCommandGenerator(object):
    def test_bitcoin_qt(self, command_generator):
        command = command_generator.bitcoin_qt(command_generator.mainnet)
        if OPERATING_SYSTEM == DARWIN:
            assert command[0] == BITCOIN_QT_PATH[OPERATING_SYSTEM]
            assert command[1].startswith('-datadir=/')

    def test_testnet_bitcoin_qt(self, command_generator):
        command = command_generator.testnet_bitcoin_qt()
        assert command[-1] == '-testnet=1'

    def test_mainnet_bitcoin_qt(self, command_generator):
        command = command_generator.mainnet_bitcoin_qt()
        assert command[-1] == '-testnet=0'

    def test_testnet_lnd(self, command_generator):
        assert len(command_generator.testnet_lnd())

    def test_mainnet_lnd(self, command_generator):
        assert len(command_generator.mainnet_lnd())
