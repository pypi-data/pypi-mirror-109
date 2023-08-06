import os
import os.path as osp

CURRENT_PATH = osp.abspath(osp.dirname(__file__))
import re
from bffacilities import createLogger
logger = createLogger("mulcpack", savefile=False, stream=True)

projectName = "bfqtLibrary"
pat = r"(?P<dstType>-\w+)?_Qt_(?P<qt_ver>(?:\d+_){2}\d+)_(?P<compiler>[\w\d]+)_(?P<bit>\d+)bit-(?P<buildType>\w+)"

QtCreatorPat = re.compile(f"build-{projectName}" + pat)

ContainedLibraries = [
    "BasicLibrary", 
    "Builib", 
    "DisplayCompass",
    "BUpdator",
]

BuildTypeMapping = {
    "Debug": "Debug",
    "MinSizeRel": "Release",
    "RelWithDebInfo": "Debug",
    "Release": "Release",
}
def extractMajorMinor(ver):
    vers = ver.split("_")
    return "_".join([vers[0], vers[1]])

class BuildTypeDao():

    def __init__(self):
        self.qtver = None
        self.compiler = None
        self.types = []
        self._folders = []
        self.root = ""
        self.bit = 32

    def addType(self, t, file):
        if t not in self.types:
            self.types.append(t)
        self._folders.append(file)
    @property 
    def files(self):
        return self._folders

    def equal(self, qtver, compiler, bit):
        if self.bit != bit:
            return False
        if self.qtver != qtver :
            return False
        if self.compiler != compiler:
            return False
        return True

    def abspaths(self):
        p = []
        for f in self._folders:
            path = osp.join(self.root, f)
            path = path.replace("\\", "/")
            p.append(path)
        return p

    def __repr__(self):
        return f"<BTDao: {self.qtver} {self.compiler} {self._folders}>"

def constructBuildType(path, bits = None):
    if bits is None:
        bits = [32, 64]
    buildTypes = []
    for file in os.listdir(path):
        absPath = osp.join(path, file)
        if not osp.isdir(absPath):
            continue
        matched = QtCreatorPat.match(file)
        if matched is None:
            continue
        qtver = matched.group("qt_ver")
        qtver = extractMajorMinor(qtver)
        compiler = matched.group("compiler").lower()
        compBit = matched.group("bit")
        if int(compBit) not in bits:
            logger.warning(f"Path: {file} is not bits compat {compBit}, needed {bits}")
            continue

        buildType = matched.group("buildType")
        if buildType in ["MinSizeRel", "RelWithDebInfo"]:
            logger.warning(f"Found unneed type: {buildType} ")
            continue

        found = False
        for d in buildTypes:
            if d.equal(qtver, compiler, compBit):
                d.addType(buildType, file)
                found = True
        if found: continue

        btDao = BuildTypeDao()
        btDao.bit = compBit
        btDao.root = path
        btDao.qtver = qtver
        btDao.compiler = compiler
        btDao.addType(buildType, file)

        buildTypes.append(btDao)
    return buildTypes


# exit()

from jinja2 import Template

cmakeTemp = Template(
"""
{%- for file in abspaths %}
include( "{{ file }}/CPackConfig.cmake" )
{%- endfor %}

set(CPACK_INSTALL_CMAKE_PROJECTS
    {%- for file in abspaths %}
        {%- for comp in libraries %}
    "{{ file }}/;{{ comp }};ALL;/;"
        {%- endfor %}
    {%- endfor %}
)
""")

import subprocess as sp

from argparse import ArgumentParser
def main(args):
    if len(args) == 0:
        logger.critical(f"Len args: {len(args)}, args not contain program path ")
        return
    curPath = osp.abspath(args[0])
    parser = ArgumentParser(prog="generateMultiCpack")
    parser.add_argument("--cpack", type=str, default="cpack", help="Specified CPack executable")
    parser.add_argument("--bits", type=str, default="32,64", help="Specified Bits that needs to be packed, default is 32,64")
    args = vars(parser.parse_args(args[1:]))
    
    logger.info(f"Using cpack: {args['cpack']}, destinate bits: {args['bits']}")
    ParentPath = osp.abspath(osp.join(curPath, ".."))
    bits = list(map(int, args["bits"].split(",")))
    buildTypes = constructBuildType(ParentPath, bits)
    logger.info(f"Build Directory Found: {buildTypes}")

    libraries = ";".join(ContainedLibraries)
    for bt in buildTypes:
        dirname = f"build-{projectName}-{bt.qtver}-{bt.compiler}"
        os.makedirs(dirname, exist_ok=True)
        output = cmakeTemp.render(abspaths = bt.abspaths(), folders = bt.files, libraries = ContainedLibraries)
        packName = f"MultiCPackConfig-{bt.bit}.cmake"
        with open(osp.join(curPath, dirname, packName), "w") as f:
            f.write(output)
        cwd = osp.abspath(osp.join(curPath, dirname))
        logger.info(f"CPACK DIR: {cwd}")
        p = sp.Popen([args["cpack"], "--config", packName], 
            cwd=cwd, 
            stdout=sp.PIPE, encoding='utf-8')
        print(p.stdout.read())
    # p = mp.Process("")
### cpack --config {path}/MultiCPackConfig.cmake
if __name__ == "__main__":
    CurrentPath = osp.abspath(osp.dirname(__file__))
    main([CurrentPath])