#! /usr/bin/env python

''' This script sorts MP3 and M4A audio files. It renames the files
based on their titles, and creates a directory structure as follows

- Artist A
    - Album 1
        - Song A
        - Song B
        - ...
    - Album 2
    - ...
- Artist B
- ...

The script should be run inside the folder containing all audio files.
'''

import os
import mutagen

# Create list of audio files


def gen_file_list():

    '''Generate a file listing from the files in the current directory.'''

    global mapping
    global base_dir

    mapping = dict()
    filePaths = []
    base_dir = os.getcwd()
    files = os.listdir(base_dir)

    for file in files:
        if file.endswith('.mp3') or file.endswith('.m4a'):
            filePaths.append(os.path.join(base_dir, file))

    return filePaths

# Define necessary functions


def make_dirs_from_dict(d, current_dir='./'):
    '''Helper function to create directory structure
    from mapping dictionary.'''

    for key in d:
        if not os.path.exists(os.path.join(current_dir, key)):
            os.mkdir(os.path.join(current_dir, key))
        for item in d[key]:
            if not os.path.exists(os.path.join(current_dir, key, item)):
                os.mkdir(os.path.join(current_dir, key, item))


def create_mapping(filename):

    '''Extracts necessary artist and album data and
    appends to the mapping dictionary.'''

    try:

        clean_tags = []

        media = mutagen.File(filename)
        metadata = media.pprint()
        tags = [x.split('=', 1) for x in metadata[0:].split('\n')]
        for i in range(len(tags)):
            if len(tags[i]) == 2:
                clean_tags.append(tags[i])
        tags_dict = dict(clean_tags)

        # Extract artist, album, and title information
        # Reclassify to "unknown" if not available

        if 'TPE1' in tags_dict.keys():
            artist = tags_dict['TPE1'].replace('/', '&')
        elif '©ART' in tags_dict.keys():
            artist = tags_dict['©ART'].replace('/', '&')
        else:
            artist = 'Unknown'

        if 'TALB' in tags_dict.keys():
            album = tags_dict['TALB'].replace('/', '&')
        elif '©alb' in tags_dict.keys():
            album = tags_dict['©alb'].replace('/', '&')
        else:
            album = 'Unknown'

        if 'TIT2' in tags_dict.keys():
            title = tags_dict['TIT2'].split('  ')[0].replace('/', ':')
        elif '©nam' in tags_dict.keys():
            title = tags_dict['©nam'].split('  ')[0].replace('/', ':')
        else:
            title = 'Unknown'

        if artist in mapping:
            if album in mapping[artist]:
                if title in mapping[artist][album]:
                    pass
                else:
                    mapping[artist][album].append([title])
            else:
                mapping[artist][album] = [title]
        else:
            mapping[artist] = dict()
            mapping[artist][album] = [title]

        # Make directories as necessary

        make_dirs_from_dict(mapping)

        # Rename and resort files

        new_dir = os.path.join(base_dir, artist, album)
        os.rename(filename, os.path.join(new_dir, title))

    except KeyError:
        return filename


# Run the function to sort all files

if __name__ == "__main__":
    files = gen_file_list()
    for file in files:
        create_mapping(file)
