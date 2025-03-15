#!/usr/bin/env bash

set -euxo pipefail

install_source() {
    # skip on Windows for now
    python -c 'import platform; assert platform.system() != "Windows"' || exit 1
    # install from source
    # https://www.darwinsys.com/file/
    # https://github.com/file/file/blob/FILE5_46/INSTALL#L51
    (
        version="file-5.46" &&
        tmpfile="$(mktemp)" &&
        curl -sSLo "${tmpfile}" "https://astron.com/pub/file/${version}.tar.gz" &&
        tar xvf "${tmpfile}" &&
        cd "${version}" &&
        ./configure &&
        make &&
        make install &&
        make installcheck &&
        cd .. &&
        rm -r "${version}"
    ) || ( cd .. && false )
}

install_precompiled() {
    # Mac https://formulae.brew.sh/formula/libmagic
    # Debian https://packages.ubuntu.com/libmagic1
    # Alpine https://pkgs.alpinelinux.org/package/libmagic
    # RHEL https://git.almalinux.org/rpms/file
    # Windows https://github.com/julian-r/file-windows
    if [ -n "$(which brew)" ]; then
        brew install libmagic
    elif [ -n "$(which apt-get)" ]; then
        apt-get update
        apt-get install -y libmagic1
    elif [ -n "$(which apk)" ]; then
        apk add --update libmagic
    elif [ -n "$(which dnf)" ]; then
        dnf --setopt install_weak_deps=false -y install file-libs
    else
        # windows (no install, just download into current working directory)
        # could also consider install using `pacman`: https://packages.msys2.org/base/mingw-w64-file
        # which would require an update of copy_libmagic below to account for new magic.mgc paths
        python <<EOF
import platform, sysconfig, io, zipfile, urllib.request
assert platform.system() == "Windows"
machine = "x86" if sysconfig.get_platform() == "win32" else "x64"
url = f"https://github.com/julian-r/file-windows/releases/download/v5.44/file_5.44-build104-vs2022-{machine}.zip"
print("Downloading", url)
zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url).read())).extractall(".")
EOF
        # check what was copied
        ls -ltra
    fi
}

copy_libmagic() {
    # on cibuildwheel, the lib needs to exist in the project before running setup.py
    # copy lib into the magic dir, regardless of platform
    # this python command relies on current working directory containing `./magic/loader.py`
    libmagic_path="$(python -c 'from magic.loader import load_lib; print(load_lib()._name)')" &&
    cp "${libmagic_path}" "magic" &&
    # only on linux/macos: additionally copy compiled db into magic dir (prefer the one installed by install_source)
    ( ( cp "/usr/local/share/misc/magic.mgc" "magic" || cp "/usr/share/misc/magic.mgc" "magic" ) || true ) &&
    # check what was copied
    ls -ltra magic
}

# prefer a recent build from source
install_source || install_precompiled
# files to be copied into the wheel
copy_libmagic
