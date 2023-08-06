import plistlib
import os
import click
import shutil
from time import time_ns
import zipfile

ARCH_ARM64 = 'arm64'
ARCH_ARMV7 = 'armv7'
ARCH_I386 = 'i386'
ARCH_X86_64 = 'x86_64'


@click.command()
# @click.option('--template', default='jspatch', help='Patch termplate. Default to \'jspatch\'.')
@click.option('--patch-file', help='Default arch patch file')
@click.option('--arm64-patch-file', help='arm64 arch patch file')
@click.option('--armv7-patch-file', help='armv7 arch patch file')
@click.option('--i386-patch-file', help='i386 arch patch file')
@click.option('--x86_64-patch-file', help='x86_64 arch patch file')
@click.option('--debug', is_flag=True)
def makePatch(patch_file: str, arm64_patch_file: str, armv7_patch_file: str, i386_patch_file: str, x86_64_patch_file: str, debug):
    """
    A patch template generation tool for BDHotfix. BDHotfix is the iOS hotfix SDK provided by veMARS.
    For description in detail, please visit https://www.volcengine.com/docs/6363/69074.
    """
    # arch -> patch file of arch
    patch_file_list = {
        ARCH_ARM64: arm64_patch_file if arm64_patch_file else patch_file,
        ARCH_ARMV7: armv7_patch_file if armv7_patch_file else patch_file,
        ARCH_I386: i386_patch_file if i386_patch_file else patch_file,
        ARCH_X86_64: x86_64_patch_file if x86_64_patch_file else patch_file
    }

    # plist content
    patch_description = {
        "patches": [
            {"arch": ARCH_ARM64, "name": ARCH_ARM64},
            {"arch": ARCH_ARMV7, "name": ARCH_ARMV7},
            {"arch": ARCH_I386, "name": ARCH_I386},
            {"arch": ARCH_X86_64, "name": ARCH_X86_64},
        ]
    }

    patch_directory = os.path.join(os.curdir, f'patch-{time_ns()}')
    os.mkdir(patch_directory)

    # 生成架构描述Plist
    plist_path = os.path.join(patch_directory, 'patch.plist')
    with open(plist_path, 'wb') as fp:
        plistlib.dump(patch_description, fp)

    # 生成各个架构Patch的文件夹, 将热修包放入其中
    for patch in patch_description["patches"]:
        patch_arch_dir = os.path.join(patch_directory, patch["name"])
        os.mkdir(patch_arch_dir)
        t_patch_file = patch_file_list[patch['arch']]
        shutil.copy(t_patch_file, patch_arch_dir)
        shutil.make_archive(patch_arch_dir, 'zip', patch_arch_dir)
        if not debug:
            shutil.rmtree(patch_arch_dir)

    shutil.make_archive(patch_directory, 'zip', patch_directory)
    print('done')


if __name__ == '__main__':
    makePatch()
