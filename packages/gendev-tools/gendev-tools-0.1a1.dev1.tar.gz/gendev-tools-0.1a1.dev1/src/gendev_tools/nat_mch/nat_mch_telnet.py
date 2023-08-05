# -*- coding: utf-8 -*-

"""
nat_mch_telnet.py
~~~~~~~~~~~~~~~~~

This is a lazy implementation of the GenDev interface. The ultimate purpose
of this module is to be encapsulated within another module that really
implements that interface.
Unfortunately, NAT MCHs don't allow to go for a full implementation of the
GenDev interface based on an only communication interface.
The main operation that is only supported by the command line interface is the
firmware update. So that, this module based on Telnet, as access way, and the
command line interface of the MCH, shall only be used to perform a firmware
update and nothing else. For other operations, better use the module based on
the communication via the MHC web interface.
"""

import re
import time
import socket
import ipaddress
from ..gendev_err import ConnTimeout, NoRouteToDevice
from telnetlib import Telnet
from logging import Logger

__author__ = ["Felipe Torres González", "Ross Elliot"]
__copyright__ = "Copyright 2021, ESS MTCA Tools"
__credits__ = ["Jeong Han Lee"]
__license__ = "GPL-3.0"
__version__ = "0.1"
__maintainer__ = "Felipe Torres González"
__email__ = "felipe.torresgonzalez@ess.eu"
__status__ = "Development"


class NATMCHTelnet:
    """NATMCTelnet access an NAT MCH via Telnet.

    This module implements some operations using the command line interface
    via Telnet. Thus, the MCH has to be accessible in the network.
    The firmware update relies on **the mchconfig-server** to serve the
    firmware image using the FTP protocol.

    Supported operations:
    - Retrieve the general information of the MCH.
    - Firmware update of the MCH.
    - Enable DHCP mode of the MCH.
    """

    def __init__(
        self,
        ip_address: str,
        port: int = 23,
        logger: Logger = None,
        hostname: str = None,
        telnet_ip_address: str = None,
    ):
        """Class constructor.

        Args:
            ip_address: the IP address of the MCH.
            port: port of the Telnet service (usually, 23).
            logger: reference to a logger that is being used.
            hostname: hostname of the MCH.
            telnet_ip_address (optional): the ip address of the telnet
            connection, if not equal to the IP address of the MCH, i.e. when
            connecting via a MOXA.

        Raises:
            gendev_err.ConnTimeout if the device is not reachable.
        """
        self.ip_address = ip_address
        self.hostname = hostname
        self._server_ip = "172.30.4.69"
        self._fw_path = "fw/"
        self._telnet_ip_address = telnet_ip_address

        # If no telnet IP address is provided, use MCH IP address
        if telnet_ip_address is None:
            self._telnet_ip_address = self.ip_address

        try:
            self._session = Telnet(self._telnet_ip_address, port, timeout=10)
        except Exception as e:
            if isinstance(e, socket.timeout):
                raise ConnTimeout(
                    "Timeout while opening the link to the MCH using Telnet"
                )
            elif isinstance(e, OSError):
                if e.errno == 113:
                    raise NoRouteToDevice(
                        "Check the connectivity to the MCH"
                        " using the IP: {}".format(self._telnet_ip_address)
                    )

        # Regular expresions for extracting the infomration relative to the
        # MCH from the version command.
        self._match_fw_ver = re.compile(r"Firmware (V\d{1,2}\.\d{1,2}\.\d{1,2})")
        # Search for the first occurrence of the token FPGA
        self._match_fpga_ver = re.compile(r"FPGA (V\d{1,2}\.\d{1,2})")
        self._match_mcu_ver = re.compile(r"AVR (\d{1,2}\.\d{1,2})")
        self._match_board_sn = re.compile(r"sn: (\d{6}-\d{4})")
        self._match_ip_addr = re.compile(r"ip address +: +((\d{1,3}\.?){4})")
        self._match_mac_addr = re.compile(r"ieee address +: +(([\d\D]{2}:?){6})")
        self._match_subnet_mask = re.compile(r"network mask +: +((\d{1,3}\.?){4})")
        self._match_gateway_addr = re.compile(r"default gateway +: +((\d{1,3}\.?){4})")
        self._match_hostname = re.compile("hostname +: (.+?(?=\r))")
        self._match_dhcp_state = re.compile("dhcp state +: (.+?(?=\r))")

    def _send_backspace(self, sleep: float = 0.25):
        """Internal method to write a backspace character to the MCH console.

        Some fields in the MCH interface are already populated, and must be
        cleared before writing the new value. The only way to do this is to
        issue a backspace character.
        """
        # Backspace is ASCII character 0x08, or special character ''\b'
        self._session.write(b"\b")
        time.sleep(sleep)

    def _send_command(self, command: str, sleep: int = 1, clear_buffer: bool = True):
        """Internal method for sending a low level command to the MCH.

        This command allows forgetting about the particular details of using
        a Telnet session behind the scenes. A regular command from the MCH
        command line interface can be sent through this interface without
        worrying about the underlying communication.

        Args:
            command: command to be sent to the MCH.
            sleep: amount of seconds to wait after sending a command.
            clear_buffer: send a carriage return before the command. This
            helps clearing previous garbage from the buffer, but
            it should be used with caution because there are
            commands that doesn't expect a carriage return after.
        """
        # clean up
        if clear_buffer:
            self._session.write(b"\r")
            self._session.read_until(b"nat> ")
            time.sleep(sleep)
        self._session.write(command.encode("ascii") + b"\r")
        time.sleep(sleep)

    def _reboot(self, sleep: int = 50):
        """Internal command to send a reboot to the MCH.

        Args:
            sleep: indicates how many seconds to wait after returning from the
            method. Write a 0 to avoid it.
        """
        self._send_command("reboot")

    def _read_command(self) -> str:
        """Internal command to read the Telnet Rx buffer.

        This method attempts to read the content from the buffer without I/O
        blocking.

        Returns:
            A string containing the content of the Rx buffer.
        """
        response = self._session.read_very_eager()
        return response.decode("ascii")

    def _set_hostname(self):
        """Sets the hostname of the MCH device.

        Returns:
            True on success.
            False on failure.
        """
        self._send_command("mchcfg")
        # Modify
        self._send_command("11", clear_buffer=False)
        # Clear previous entry
        for num in range(0, 75):
            self._send_backspace()
        self._send_command(self.hostname, clear_buffer=False)
        self._send_command("q", clear_buffer=False)

        # TODO: re-enable this check
        # success = self._check_hostname()
        success = True

        return success

    def _check_hostname(self):
        """Checks that the hostname set on the MCH matches
        the value provided.

        Returns:
            True if the hostname setting matches the expected string.
            False if the hostname setting does not match the expected string.
        """

        self._send_command("ni")
        network_info = self._read_command()

        mch_hostname = self._match_hostname.search(network_info).group(1)

        success = False
        if mch_hostname == self.hostname:
            success = True

        return success

    def _enable_dhcp(self):
        """Enables DHCP mode on the MCH

        Returns:
            True if DHCP was enabled successfully.
            False if DHCP setting failed.
        """

        self._send_command("mchcfg")
        self._send_command("3", clear_buffer=False)
        for i in range(0, 4):
            self._send_command("", clear_buffer=False)
        self._send_command("2", clear_buffer=False)
        for i in range(0, 8):
            self._send_command("", clear_buffer=False)
        self._send_command("q", clear_buffer=False)

        # The MCH needs a reboot for the hostname
        # to update.
        # self._reboot()
        # Wait for the MCH to complete the reboot process
        # time.sleep(50)

        # Finally, verify the change
        success = self._check_dhcp()

        return success

    def _check_dhcp(self):
        """Check wether DHCP is enabled.

        Returns:
            True if DHCP is enabled
            False if DHCP is disabled
        """

        self._send_command("ni")
        network_info = self._read_command()

        dhcp_state = self._match_dhcp_state.search(network_info).group(1)
        enabled = False
        if dhcp_state == " enabled":
            enabled = True

        return enabled

    def _clear_ip_address(self):
        """Helper method to send enough backspace characters
        to clear an IP address
        """

        # Maximum length of an IP address is 15 characters
        for i in range(0, 15):
            self._send_backspace()

    def _set_ip_addr(self):
        """Set the IP address of the MCH device."""
        # Get network information
        self._send_command("ni")
        network_info = self._read_command()

        # Retrieve gateway address and netmask from network info
        gateway_addr = self._match_gateway_addr.search(network_info).group(1)
        netmask = self._match_subnet_mask.search(network_info).group(1)

        # Calculate broadcast ip_address
        ipv4net = ipaddress.IPv4Network(self.ip_address + "/" + netmask, False)
        broadcast_addr = ipv4net.broadcast_address.compressed

        # Trigger IP setting menu
        self._send_command("ip")

        # Clear the existing IP address, and update with new value
        self._clear_ip_address()
        self._send_command(self.ip_address, clear_buffer=False)
        # Clear the existing netmask, and update with new value
        self._clear_ip_address()
        self._send_command(netmask, clear_buffer=False)
        # Clear the existing broadcast address, and update with new value
        self._clear_ip_address()
        self._send_command(broadcast_addr, clear_buffer=False)
        # Clear the existing gateway address, and update with new value
        self._clear_ip_address()
        self._send_command(gateway_addr, clear_buffer=False)

        # Check we are at the confirmation prompt
        response = self._read_command()
        if not response.endswith("Are you really sure ?"):
            return False  # Failure

        # Issue confirmation 'y'
        self._send_command("y", clear_buffer=False)

        # Success
        return True

    def device_info(self) -> dict:
        """Retrieve the main information about the device.

        The information is returned in a dictionary with 2 categories:
        *board* and *network*.

        Returns:
            If success, a dictionary with the device information.
            If failure, an empty dictionary on failure.
        """
        self._send_command("version")
        raw_info_version = self._read_command()
        self._send_command("ni")
        raw_info_network = self._read_command()

        if raw_info_version != "" and raw_info_network != "":
            resp_dict = dict()
            resp_dict["Board"] = dict()

            resp_dict["Board"]["fw_ver"] = self._match_fw_ver.search(
                raw_info_version
            ).group(1)
            resp_dict["Board"]["fpga_ver"] = self._match_fpga_ver.search(
                raw_info_version
            ).group(1)
            resp_dict["Board"]["mcu_ver"] = self._match_mcu_ver.search(
                raw_info_version
            ).group(1)
            resp_dict["Board"]["serial_num"] = self._match_board_sn.search(
                raw_info_version
            ).group(1)

            resp_dict["Network"] = dict()
            resp_dict["Network"]["ip_address"] = self._match_ip_addr.search(
                raw_info_network
            ).group(1)
            resp_dict["Network"]["mac_address"] = self._match_mac_addr.search(
                raw_info_network
            ).group(1)
            resp_dict["Network"]["subnet_address"] = self._match_subnet_mask.search(
                raw_info_network
            ).group(1)
            resp_dict["Network"]["gateway_address"] = self._match_gateway_addr.search(
                raw_info_network
            ).group(1)

        else:
            resp_dict = dict()

        return resp_dict

    def set_dhcp_mode(self):
        """Enables DHCP mode in the network configuration of the device.

        Performs the following steps:
            - Enables DHCP mode on the MCH.
            - Sets the internal IP address value to match the address
              provided by the DHCP server(required to prevent DHCP lease
              issues).
            - Sets the hostname value.

        Returns
            If failure, a tuple containing False, and a message about the
            failure.
            If success, a tuple containing True, and an empty string.

        Raises:
            ConnectionError: If the device is not accessible.
            NoValidConn: If no valid connection types supporting this feature
                         are used by the device.
        """

        total_success = True
        success = [True] * 3
        response = ""

        # Enable DHCP mode
        success[0] = self._enable_dhcp()
        if not success[0]:
            response = "Enabling of DHCP mode failed.\r\n"

        # Set the internal IP address
        success[1] = self._set_ip_addr()
        if not success[1]:
            response = response + "Setting IP address failed.\r\n"

        # Set the hostname
        success[2] = self._set_hostname()
        if not success[2]:
            response = response + "Setting hostname failed.\r\n"

        # If any of the subtasks failed, fail overall
        if False in success:
            total_success = False

        return total_success, response

    def update_fw(self, fw_version: str, part: str = "MCH") -> tuple:
        """Update the firmware of the device.

        This method expects the firmware binary pointed by the value of the
        argument *fw_version* to be available in the TFTP server.
        Mainly, this method injects the command *update_firmware* to an NAT
        MCH.

        Args:
            fw_version: version release number for the new fw.
            part: not used

        Returns:
            If failure, it returns a tuple containing False, and a message
            about the failure.
            If success, it returns True,
        """
        self._send_command("update_firmware")
        # Avoid clearing the buffer bewteen these commands because it would
        # skip the update mode in the MCH.
        self._send_command(
            "{}:{}{}/mch_fw_{}.bin".format(
                self._server_ip, self._fw_path, fw_version, fw_version
            ),
            clear_buffer=False,
        )
        # Erasing the internal memory. If it is attempted to read now from the
        # buffer, it will get the promt.
        time.sleep(30)
        # There's a useless promt which is received first, get rid of it, and
        # wait for the good one that should come when the flashing is finished.
        response = self._session.read_until(b"nat> ")
        # Sometimes, at this point, the buffer has content, sometimes not.
        # It seems reasonable using a length 100 to detect this situation.
        if len(response) < 100:
            response = self._session.read_until(b"nat> ")
        response = response.decode("ascii")

        # Let's see if the update was successful. The MCH prints the word
        # "successful" at the end of the process, just before the prompt.
        if "successful" in response:
            success = (True,)
            self._reboot()
            # Finally, wait for the MCH to complete the reboot process
            time.sleep(50)
        else:
            # Something went wrong, let's check it!
            if "TFTP: could not get file" in response:
                # This error is mainly caused when the target fw_version
                # is not available in the TFTP server.
                success = (
                    False,
                    "The fw version {} couldn't be found in the"
                    " TFTP server".format(fw_version),
                )
            else:
                success = False, "Unknown error. Check the debug log."

        return success
