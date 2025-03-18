#!/usr/bin/env bash

set -euxo pipefail

install_source() {
    # install from source
    # https://www.darwinsys.com/file/
    # https://github.com/file/file/blob/FILE5_46/INSTALL#L51
    (
        python -c 'import platform; assert platform.system() != "Windows"' &&
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
    if [ -n "$(which brew)" ]; then
        brew install libmagic
    elif [ -n "$(which apt-get)" ]; then
        apt-get update
        apt-get install -y libmagic1
    elif [ -n "$(which apk)" ]; then
        apk add --update libmagic
    elif [ -n "$(which dnf)" ]; then
        dnf --setopt install_weak_deps=false -y install file-libs
    fi
}

copy_libmagic() {
    # on cibuildwheel, the lib needs to exist in the project before running setup.py
    # copy lib into the magic dir, regardless of platform
    # this python command relies on current working directory containing `./magic/loader.py`
    libmagic_path="$(python -c 'from magic.loader import load_lib; print(load_lib()._name)')" &&
    cp "${libmagic_path}" "magic" &&
    # additionally copy compiled db into magic dir (prefer the one installed by install_source)
    ( ( cp "/usr/local/share/misc/magic.mgc" "magic" || cp "/usr/share/misc/magic.mgc" "magic" ) || true ) &&
    # check what was copied
    ls -ltra magic
}

# skip windows (taken care of separately in wheels.yml)
python -c 'import platform; assert platform.system() != "Windows"' || ( echo "skipping on windows" && exit 0 )
# prefer a recent build from source
install_source || install_precompiled
# files to be copied into the wheel
copy_libmagic
