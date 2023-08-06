import plistlib
import os
import click
import shutil
from time import time_ns
import zipfile

ARCH_ARM64 = 'arm64'
ARCH_ARMV7 = 'armv7'
ARCH_X86_64 = 'x86_64'
# Note: i386 arch is not supported.


def createDictionaryPlist(plist_data: dict, plist_file_path: str):
    with open(plist_file_path, 'wb') as fp:
        plistlib.dump(plist_data, fp)


@click.command()
# @click.option('--template', default='jspatch', help='Patch termplate. Default to \'jspatch\'.')
@click.option('--patch-file', help='Default arch patch file')
@click.option('--arm64-patch-file', help='arm64 arch patch file')
@click.option('--armv7-patch-file', help='armv7 arch patch file')
@click.option('--x86_64-patch-file', help='x86_64 arch patch file')
@click.option('--debug', is_flag=True)
def makePatch(patch_file: str, arm64_patch_file: str, armv7_patch_file: str, i386_patch_file: str, x86_64_patch_file: str, debug):
    """
    A patch template generation tool for BDHotfix. BDHotfix is the iOS hotfix SDK provided by veMARS.
    For description in detail, please visit https://www.volcengine.com/docs/6363/69074.
    """
    def fname(arch: str) -> str:
        return arch + '_patch'

    # arch -> patch file of arch
    patch_file_list = {
        ARCH_ARM64: arm64_patch_file if arm64_patch_file else patch_file,
        ARCH_ARMV7: armv7_patch_file if armv7_patch_file else patch_file,
        ARCH_X86_64: x86_64_patch_file if x86_64_patch_file else patch_file
    }

    # plist content
    patch_description = {
        "patches": [
            {"arch": ARCH_ARM64,  "name": fname(ARCH_ARM64)},
            {"arch": ARCH_ARMV7,  "name": fname(ARCH_ARMV7)},
            {"arch": ARCH_X86_64, "name": fname(ARCH_X86_64)},
        ]
    }

    patch_directory = os.path.join(os.curdir, f'patch-{time_ns()}')
    os.mkdir(patch_directory)

    # 生成架构描述Plist
    createDictionaryPlist(patch_description, os.path.join(patch_directory, 'patch.plist'))

    # 生成各个架构Patch的文件夹, 将热修包放入其中
    for patch in patch_description["patches"]:
        current_patch_arch = patch['arch']
        current_patch_name = patch['name']

        # 创建对应架构热修包的文件夹
        patch_arch_dir = os.path.join(patch_directory, current_patch_name)
        os.mkdir(patch_arch_dir)
        # 放入对应架构的热修文件
        tmp_patch_file = patch_file_list[current_patch_arch]
        shutil.copy(tmp_patch_file, patch_arch_dir)
        # 放入一个空plist (not necessary)
        # createDictionaryPlist({}, os.path.join(patch_arch_dir, 'no_use.plist'))
        # 打包成zip
        shutil.make_archive(patch_arch_dir, 'zip', root_dir=patch_directory, base_dir=current_patch_name)
        if not debug:
            shutil.rmtree(patch_arch_dir)

    shutil.make_archive(patch_directory, 'zip', patch_directory)
    # print('done')


if __name__ == '__main__':
    makePatch()
