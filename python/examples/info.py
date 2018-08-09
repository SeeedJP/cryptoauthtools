"""
Device Info Retrieval Example
"""
# (c) 2015-2018 Microchip Technology Inc. and its subsidiaries.
#
# Subject to your compliance with these terms, you may use Microchip software
# and any derivatives exclusively with Microchip products. It is your
# responsibility to comply with third party license terms applicable to your
# use of third party software (including open source software) that may
# accompany Microchip software.
#
# THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER
# EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY IMPLIED
# WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A
# PARTICULAR PURPOSE. IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT,
# SPECIAL, PUNITIVE, INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE
# OF ANY KIND WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF
# MICROCHIP HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE
# FORESEEABLE. TO THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL
# LIABILITY ON ALL CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED
# THE AMOUNT OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR
# THIS SOFTWARE.

from cryptoauthlib import *
from common import *


def info(iface='hid', device='ecc'):
    ATCA_SUCCESS = 0x00

    # Loading cryptoauthlib(python specific)
    load_cryptoauthlib()

    # Get the target default config
    cfg = eval('cfg_at{}a_{}_default()'.format(atca_names_map.get(device), atca_names_map.get(iface)))

    # Initialize the stack
    assert atcab_init(cfg) == ATCA_SUCCESS
    print('')
    
    # Request the Revision Number
    info = bytearray(4)
    assert atcab_info(info) == ATCA_SUCCESS
    print('\nDevice Part:')
    print('    ' + get_device_name(info))

    # Request the Serial Number
    serial_number = bytearray(9)
    assert atcab_read_serial_number(serial_number) == ATCA_SUCCESS
    print('\nSerial number: ')
    print(pretty_print_hex(serial_number, indent='    '))

    # Read the configuration zone
    config_zone = bytearray(128)
    assert atcab_read_config_zone(config_zone) == ATCA_SUCCESS

    print('\nConfiguration Zone:')
    print(pretty_print_hex(config_zone, indent='    '))

    # Check the device locks
    print('\nCheck Device Locks')
    is_locked = bytearray(1)
    assert atcab_is_locked(0, is_locked) == ATCA_SUCCESS
    print('    Config Zone is %s' % ('locked' if is_locked[0] else 'unlocked'))

    assert atcab_is_locked(1, is_locked) == ATCA_SUCCESS
    print('    Data Zone is %s' % ('locked' if is_locked[0] else 'unlocked'))

    # Free the library
    atcab_release()


if __name__ == '__main__':
    parser = setup_example_runner(__file__)
    args = parser.parse_args()

    info(args.iface, args.device)
    print('\nDone')