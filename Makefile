SHELL := /bin/bash

.PHONY: install_libmagic
## Install libmagic
install_libmagic:
	# Mac https://formulae.brew.sh/formula/libmagic
	# Debian https://packages.ubuntu.com/libmagic1
	# Alpine https://pkgs.alpinelinux.org/package/libmagic
	# RHEL https://git.almalinux.org/rpms/file
	# Windows https://github.com/julian-r/file-windows
	( ( ( \
	    brew install libmagic \
		|| ( apt-get update && apt-get install -y libmagic1 ) ) \
		|| apk add --update libmagic ) \
		|| yum install file-libs ) \
		|| ( python -c 'import platform, sysconfig, io, zipfile, urllib.request; assert platform.system() == "Windows"; machine = "x86" if sysconfig.get_platform() == "win32" else "x64"; print(machine); zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(f"https://github.com/julian-r/file-windows/releases/download/v5.44/file_5.44-build104-vs2022-{machine}.zip").read())).extractall(".")' && ls -ltra )
	# on cibuildwheel, the lib needs to exist in the project before running setup.py
	# copy lib into the magic dir, regardless of platform
	python -c "import subprocess; from magic.loader import load_lib; lib = load_lib()._name; print(f'linking {lib}'); subprocess.check_call(['cp', lib, 'magic'])"
	# only on linux: additionally copy compiled db into magic dir
	cp /usr/share/misc/magic.mgc magic || true
	# check what was copied
	ls -ltra magic

.DEFAULT_GOAL := help
.PHONY: help
## Print Makefile documentation
help:
	@perl -0 -nle 'printf("\033[36m  %-15s\033[0m %s\n", "$$2", "$$1") while m/^##\s*([^\r\n]+)\n^([\w.-]+):[^=]/gm' $(MAKEFILE_LIST) | sort
