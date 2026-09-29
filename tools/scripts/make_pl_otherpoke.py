#!/usr/bin/env python3

import argparse
import pathlib
import subprocess

argparser = argparse.ArgumentParser(
    prog='pl_poke_icon.narc packer',
    description='Packs the archive containing Pokemon icons'
)
argparser.add_argument('-n', '--nitrogfx',
                       required=True,
                       help='Path to nitrogfx executable')
argparser.add_argument('-k', '--narc',
                       required=True,
                       help='Path to narc executable')
argparser.add_argument('-p', '--private-dir',
                       required=True,
                       help='Path to the private directory (where binaries will be made)')
argparser.add_argument('-o', '--output-dir',
                       required=True,
                       help='Path to the output directory (where the NARC will be made)')
argparser.add_argument('-se', '--sprite-entries',
                       required=True, type=int,
                       help='Number of entries to interpret from the list as NCGR-sources')
argparser.add_argument('-pe', '--palette-entries',
                       required=True, type=int,
                       help='Number of entries to interpret from the list as NCLR-sources')
argparser.add_argument('-a', '--appended',
                       action='append', default=[],
                       help='A sprite (.png) or palette (.pal) added after the last member (Platinum Oxide)')
argparser.add_argument('files',
                       nargs='+',
                       help='List of files to process in-order')
args = argparser.parse_args()

private_dir = pathlib.Path(args.private_dir)
output_dir = pathlib.Path(args.output_dir)

private_dir.mkdir(parents=True, exist_ok=True)

# The first batch of files should all be sprites
for i in range(args.sprite_entries):
    infile = args.files[i]
    target = private_dir / f'pl_otherpoke_{i:04}.NCGR'
    subprocess.run([
        args.nitrogfx,
        infile,
        target,
        '-encodefronttoback',
        '-scan',
    ])

# The next batch of files should all be palettes
for i in range(args.sprite_entries, args.sprite_entries + args.palette_entries):
    infile = args.files[i]
    target = private_dir / f'pl_otherpoke_{i:04}.NCLR'
    subprocess.run([
        args.nitrogfx,
        infile,
        target,
        '-bitdepth', '8',
        '-nopad',
        '-comp', '10'
    ])

# The last five entries are the Substitute sprite and in-battle shadows
sub_back = args.files[-5]
sub_front = args.files[-4]
sub_pal = args.files[-3]
shadows = args.files[-2]
shadows_pal = args.files[-1]
i = args.sprite_entries + args.palette_entries

subprocess.run([
    args.nitrogfx,
    sub_back,
    private_dir / f'pl_otherpoke_{i:04}.NCGR',
    '-encodefronttoback',
    '-scan',
])
subprocess.run([
    args.nitrogfx,
    sub_front,
    private_dir / f'pl_otherpoke_{(i+1):04}.NCGR',
    '-encodefronttoback',
    '-scan',
])
subprocess.run([
    args.nitrogfx,
    sub_pal,
    private_dir / f'pl_otherpoke_{(i+2):04}.NCLR',
    '-bitdepth', '8',
    '-nopad',
    '-comp', '10'
])
subprocess.run([
    args.nitrogfx,
    shadows,
    private_dir / f'pokemon_shadows.NCGR',
    '-encodefronttoback',
    '-scan',
])
subprocess.run([
    args.nitrogfx,
    shadows_pal,
    private_dir / f'pokemon_shadows_pal.NCLR',
    '-bitdepth', '8',
    '-nopad',
    '-comp', '10'
])

# Platinum Oxide: members added after the in-battle shadows. The archive is
# packed in name order, so each takes a name that sorts after
# pokemon_shadows_pal and keeps them in the order given; the naix names them
# from their species, form and file, as pokemon_z_00_arceus_fairy_back_NCGR.
for k, infile in enumerate(args.appended):
    path = pathlib.Path(infile)
    stem = f'pokemon_z_{k:02}_{path.parts[-4]}_{path.parts[-2]}_{path.stem}'
    if path.suffix == '.png':
        subprocess.run([
            args.nitrogfx,
            infile,
            private_dir / f'{stem}.NCGR',
            '-encodefronttoback',
            '-scan',
        ])
    else:
        subprocess.run([
            args.nitrogfx,
            infile,
            private_dir / f'{stem}.NCLR',
            '-bitdepth', '8',
            '-nopad',
            '-comp', '10'
        ])

subprocess.run([
    args.narc,
    '--create',
    '--index',
    '--file', output_dir / 'pl_otherpoke.narc',
    private_dir
])
