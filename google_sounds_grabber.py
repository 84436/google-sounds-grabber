from bs4 import BeautifulSoup
import os
import re
from sys import argv

################################################################################
# Check if we got arguments

if len(argv) != 3:
    print('Please specify exactly 2 arguments: <input dump folder> <output folder>\nThank you.')
    exit(-1)

_, in_dir, out_dir = argv

################################################################################
# Constants

ROOT_XMLS = f'{in_dir}/res/xml'
ROOT_VALUES = f'{in_dir}/res/values/strings.xml'
OUT_FILE = f'{out_dir}.aria2.txt'

KEY_BLACKLIST = [
    'abc_',
    'app_',
    'add_new_sounds',
    'appbar_scrolling_view_behavior',
    'bottomsheet_action_expand_halfway',
    'common_google_play_services_',
    'content_desc_',
    'currently_set',
    'default_ringtone',
    'deletion_warning_',
    'firebase_database_url',
    'gcm_defaultSenderId',
    'gm3_sys_',
    'gm_sys_',
    'google_',
    'licenses',
    'material_',
    'network_',
    'no_items',
    'not_set',
    'password_toggle_content_description',
    'path_password_',
    'preferences_license_title',
    'privacy_policy',
    'project_id',
    'select_',
    'silent',
    'terms_of_service',
    'track_counts',
    'unable_to_add_ringtone',
    'volume_muted_',
]

GROUP_NAME_MAP = {
    'classical': 'Classical Harmonies',
    'loud': 'Play It Loud',
    'material-adventures': 'Material Adventures',
    'minimal': 'Minimal Melodies',
    'pixel-gen1': 'Pixel (1st Gen)',
    'pixel-gen2': 'Pixel (2nd Gen)',
    'real-world': 'Reality Bytes',
    'retro': 'Retro Riffs',
    'seasonal': 'Seasonal Celebrations',
}

################################################################################
# Helper classes & functions

class LinkSuperGroup:
    def __init__(self, name, groups):
        self.name = name
        self.groups = groups

class LinkGroup:
    def __init__(self, name, links):
        self.name = name
        self.links = links

class Link:
    def __init__(self, name, id, url):
        self.name = name
        self.id = id
        self.url = url

def convert_track_def_to_link(track):
    return Link(
        name = track['sounds:title'],
        id = track['sounds:trackId'],
        url = track['sounds:url']
    )

def convert_file_to_subgroup(filename):
    links = []
    with open(f'{ROOT_XMLS}/{filename}', 'r') as f:
        soup = BeautifulSoup(f, 'xml')
        for track in soup.select('track'):
            links.append(convert_track_def_to_link(track))
    return LinkGroup(
        name = get_formal_name_from_filename(filename),
        links = links
    )

def get_formal_name_from_filename(filename):
    key = '-'.join(re.split('[_.]', filename)[1:-1])
    name = GROUP_NAME_MAP.get(key)
    return filename if name is None else name

################################################################################
# Main: Find list of files from the APK dump

alarm_raw = []
ring_raw = []
notif_raw = []

for _, _, files in os.walk('test/res/xml'):
    for file in files:
        name, ext = os.path.splitext(file)
        if ext.endswith('.xml') and name.startswith('alarm_'):
            alarm_raw.append(file)
        if ext.endswith('.xml') and name.startswith('ring_'):
            ring_raw.append(file)
        if ext.endswith('.xml') and name.startswith('notif_'):
            notif_raw.append(file)

print(f'\
Found {len(alarm_raw) + len(ring_raw) + len(notif_raw)} lists \
({len(alarm_raw)} alarm, {len(ring_raw)} ringtone, {len(notif_raw)} notification)\
')

################################################################################
# Main: Generate keymap (for turning @strings to something more human-readable)

keymap = {}

with open(ROOT_VALUES, 'r') as f:
    soup = BeautifulSoup(f, 'xml')
    keymap = {
        f'{e["name"]}': e.text.replace('"', '')
        for e in soup.select('string')
        if not any(map(
            lambda prefix, name = e["name"]: name.startswith(prefix),
            KEY_BLACKLIST
        ))
    }

################################################################################
# Main: Generate a hella lot of links in a nice aria2 job file

supergroups = [
    LinkSuperGroup(
        name = 'Alarms',
        groups = map(convert_file_to_subgroup, alarm_raw)
    ),
    LinkSuperGroup(
        name = 'Ringtones',
        groups = map(convert_file_to_subgroup, ring_raw)
    ),
    LinkSuperGroup(
        name = 'Notifications',
        groups = map(convert_file_to_subgroup, notif_raw)
    ),
]

byte_counter = 0

with open(OUT_FILE, 'w') as f:
    for supergroup in supergroups:
        for group in supergroup.groups:
            for link in group.links:
                filename = f'{keymap.get(link.name.split("/")[1])}'
                final_path = f'{out_dir}/{supergroup.name}/{group.name}/{filename}.ogg'
                final_aria2_str = f'{link.url}\n    out={final_path}\n'
                byte_counter += f.write(final_aria2_str)

print(f'{byte_counter} bytes written to {OUT_FILE}')
