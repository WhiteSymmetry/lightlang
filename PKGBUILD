# Contributor : eduard_pustobaev <eduard_pustobaev@mail.ru>

pkgname=lightlang-git
pkgver=20110723
pkgrel=1
pkgdesc="LightLang - system of electronic dictionaries for Linux."
arch=('i686' 'x86_64')
url="http://code.google.com/p/lightlang"
license="GPL"
depends=('qt' 'pyqt' 'python2-pyqt' 'python-xlib' 'sox')
makedepends=('git' 'autoconf')
provides=('lightlang')
replaces=('lightlang-svn')
source=()
md5sums=()

_gitroot="git://github.com/mdevaev/lightlang.git"
_gitname="lightlang"


build() {
	cd $startdir/src
	if [ -d $_gitname ]; then
		msg "Updateing local repository..."
		cd $_gitname
		git pull origin master || return 1
		msg "The local files are updated."
		cd ..
	else
		git clone $_gitroot --depth=1
	fi

	msg "Git clone done or server timeout"
	msg "Starting make..."

	rm -rf $_gitname-build
	cp -r $_gitname $_gitname-build
	cd $_gitname-build

	sed -i -e 's/python -c/python2 -c/g' configure.in
	sed -i -e 's/AC_X_PATH_PROG(PYTHON_PROG, python,/AC_X_PATH_PROG(PYTHON_PROG, python2,/g' configure.in
	sed -i -e 's/"python"/"python2"/g' apps/xsl/src/xsl/StartupLock.py
	autoconf
	./configure || return 1
	make || return 1
	make DESTDIR=$pkgdir install
}

