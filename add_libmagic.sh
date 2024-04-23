#!/usr/bin/env bash

set -euxo pipefail

install_source() {
    version="file-5.45"
    (
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
    ) || (cd .. && rm -r "${version}" && false)
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
    elif [ -n "$(which yum)" ]; then
        yum install file-libs
    else
        python -c 'import platform, sysconfig, io, zipfile, urllib.request; assert platform.system() == "Windows"; machine = "x86" if sysconfig.get_platform() == "win32" else "x64"; print(machine); zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f"https://github.com/julian-r/file-windows/releases/download/v5.44/file_5.44-build104-vs2022-{machine}.zip").read())).extractall(".")' &&
        ls -ltra
    fi
}

copy_libmagic() {
    # on cibuildwheel, the lib needs to exist in the project before running setup.py
    # copy lib into the magic dir, regardless of platform
    libmagic_path="$(python -c 'from magic.loader import load_lib; print(load_lib()._name)')" &&
    cp "${libmagic_path}" "magic" &&
    # only on linux: additionally copy compiled db into magic dir
    ( ( cp "/usr/local/share/misc/magic.mgc" "magic" || cp "/usr/share/misc/magic.mgc" "magic" ) || true ) &&
    # check what was copied
    ls -ltra magic
}

install_source || install_precompiled
copy_libmagic
