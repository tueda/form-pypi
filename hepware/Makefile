CC = cc
CXX = c++
FETCH = wget --no-use-server-timestamps -qO

clean: phony
	rm -rf bin/ build/ include/ lib/ share/ *.done

phony: ;

DIR = ${CURDIR}
DEP_CFLAGS = -I${DIR}/include -O3 -fno-omit-frame-pointer -fdata-sections -ffunction-sections ${CFLAGS}
DEP_FFLAGS = -I${DIR}/include -O3 ${FFLAGS}
DEP_LDFLAGS = -L${DIR}/lib -Wl,--gc-sections ${LDFLAGS}

MAKEOVERRIDES =

build/.dir:
	mkdir -p bin build include lib share
	date >$@

## GMP

VER_gmp = 6.3.0

build/gmp-${VER_gmp}.tar.xz: build/.dir
	rm -f build/gmp*.tar.xz
	${FETCH} $@ \
		"https://gmplib.org/download/gmp/gmp-${VER_gmp}.tar.xz" \
		|| rm -f $@

gmp.done: build/gmp-${VER_gmp}.tar.xz
	rm -rf build/gmp-*/
	cd build && tar xf gmp-${VER_gmp}.tar.xz
	cd build/gmp-*/ && mv configfsf.guess config.guess
	cd build/gmp-*/ && \
		env CC="${CC}" CXX="${CXX}" CFLAGS="-std=c11 ${DEP_CFLAGS}" CXXFLAGS="${DEP_CFLAGS}" LDFLAGS="${DEP_LDFLAGS}" \
		./configure \
		--prefix="${DIR}" --libdir="${DIR}/lib" \
		--includedir="${DIR}/include" --bindir="${DIR}/bin" \
		--enable-static --disable-shared --enable-cxx
	+${MAKE} -C build/gmp-*/
	+${MAKE} -C build/gmp-*/ install
	date >$@

## MPFR

VER_mpfr = 4.2.2

build/mpfr-${VER_mpfr}.tar.xz: build/.dir
	rm -f build/mpfr*.tar.xz
	${FETCH} $@ \
		"https://www.mpfr.org/mpfr-${VER_mpfr}/mpfr-${VER_mpfr}.tar.xz" \
		|| rm -f $@

mpfr.done: build/mpfr-${VER_mpfr}.tar.xz gmp.done
	rm -rf build/mpfr-*/
	cd build && tar xf mpfr-${VER_mpfr}.tar.xz
	cd build/mpfr-*/ && \
		env CC="${CC}" CXX="${CXX}" CFLAGS="${DEP_CFLAGS}" CXXFLAGS="${DEP_CFLAGS}" LDFLAGS="${DEP_LDFLAGS}" \
		./configure \
		--prefix="${DIR}" --libdir="${DIR}/lib" \
		--includedir="${DIR}/include" --bindir="${DIR}/bin" \
		--enable-static --disable-shared --enable-thread-safe \
		--with-gmp="${DIR}"
	+${MAKE} -C build/mpfr-*/
	+${MAKE} -C build/mpfr-*/ install
	date >$@

## Flint

VER_flint = 3.5.0

build/flint-${VER_flint}.tar.gz: build/.dir
	rm -f build/flint*.tar.gz
	${FETCH} $@ \
		"https://flintlib.org/download/flint-${VER_flint}.tar.gz" \
		|| rm -f $@

flint.done: build/flint-${VER_flint}.tar.gz gmp.done mpfr.done
	rm -rf build/flint-*/
	cd build && tar xf flint-${VER_flint}.tar.gz
	cd build/flint-*/ && mv config/configfsf.guess config/config.guess
	cd build/flint-*/ && \
		./configure \
		--prefix="${DIR}" --enable-static --disable-shared \
		CC="${CC}" CXX="${CXX}" CFLAGS="${DEP_CFLAGS} -Wno-deprecated-declarations -Wmissing-prototypes -Wno-stringop-overflow -Wno-stringop-overread -Werror=implicit-function-declaration -Wall -std=c11 -pedantic -O3" \
		--with-gmp="${DIR}" \
		--with-mpfr="${DIR}"
	+${MAKE} -C build/flint-*/ V=1
	+${MAKE} -C build/flint-*/ install
	date >$@

## zlib

VER_zlib = 1.3.2

build/zlib-${VER_zlib}.tar.gz: build/.dir
	rm -f build/zlib*.tar.gz
	${FETCH} $@ \
		"http://zlib.net/fossils/zlib-${VER_zlib}.tar.gz" \
		|| rm -f $@

zlib.done: build/zlib-${VER_zlib}.tar.gz
	rm -rf build/zlib-*/
	cd build && tar xf zlib-${VER_zlib}.tar.gz
	cd build/zlib-*/ && \
		env CC="${CC}" CXX="${CXX}" CFLAGS="${DEP_CFLAGS}" \
		./configure \
		--prefix="${DIR}" --static
	+${MAKE} -C build/zlib-*/
	+${MAKE} -C build/zlib-*/ install
	date >$@

## FORM

VER_form = 5.0.0

build/form-${VER_form}.tar.gz: build/.dir
	rm -f build/form*.tar.gz
	${FETCH} $@ \
		"https://github.com/form-dev/form/releases/download/v${VER_form}/form-${VER_form}.tar.gz" \
		|| rm -f $@

form.done: build/form-${VER_form}.tar.gz flint.done gmp.done mpfr.done zlib.done zstd.done
	rm -rf build/form-*/
	cd build && tar xf form-${VER_form}.tar.gz
	cd build/form-*/ && \
		env CC="${CC}" CXX="${CXX}" CFLAGS="${DEP_CFLAGS} -g" CXXFLAGS="${DEP_CFLAGS} -g" LDFLAGS="${DEP_LDFLAGS}" \
		./configure \
		--prefix="${DIR}" --libdir="${DIR}/lib" \
		--includedir="${DIR}/include" --bindir="${DIR}/bin" \
		--enable-scalar=yes \
		--enable-threaded=yes \
		--enable-debug=yes \
		--enable-parform=no \
		--enable-float=yes \
		--enable-static-link=no \
		--enable-native=no \
		--with-flint="${DIR}" \
		--with-gmp="${DIR}" \
		--with-mpfr="${DIR}" \
		--with-zlib="${DIR}" \
		--with-zstd="${DIR}"
	+${MAKE} -C build/form-*/
	+${MAKE} -C build/form-*/ install
	date >$@

## Zstd

VER_zstd = 1.5.7

build/zstd-${VER_zstd}.tar.gz: build/.dir
	rm -f build/zstd*.tar.gz
	${FETCH} $@ \
		"https://github.com/facebook/zstd/releases/download/v${VER_zstd}/zstd-${VER_zstd}.tar.gz" \
		|| rm -f $@

zstd.done: build/zstd-${VER_zstd}.tar.gz zlib.done
	rm -rf build/zstd-*/
	cd build && tar xf zstd-${VER_zstd}.tar.gz
	@# build libzstd.a, libastd_zlibwrapper.a, and zstd
	+${MAKE} -C build/zstd-*/lib/ CC=${CC} CXX=${CXX} CFLAGS="${DEP_CFLAGS}" LDFLAGS="${DEP_LDFLAGS}" VERBOSE=1 libzstd.a-release-nomt
	+${MAKE} -C build/zstd-*/programs/ CC=${CC} CXX=${CXX} CFLAGS="${DEP_CFLAGS}" LDFLAGS="${DEP_LDFLAGS}" VERBOSE=1 HAVE_ZLIB=no HAVE_LZMA=no HAVE_LZ4=no zstd-nomt
	+${MAKE} -C build/zstd-*/zlibWrapper/ CC=${CC} CXX=${CXX} CFLAGS="${DEP_CFLAGS} -DZWRAP_USE_ZSTD=1" LDFLAGS="${DEP_LDFLAGS}" VERBOSE=1 zstd_zlibwrapper.o gzclose.o gzlib.o gzread.o gzwrite.o
	cd build/zstd-*/zlibWrapper/ && ${AR} rcs libzstd_zlibwrapper.a zstd_zlibwrapper.o gzclose.o gzlib.o gzread.o gzwrite.o
	@# install libzstd.a, libastd_zlibwrapper.a, zstd*.h, and zstd
	+${MAKE} -C build/zstd-*/lib/ PREFIX="${DIR}" VERBOSE=1 install-static install-includes
	+${MAKE} -C build/zstd-*/programs/ PREFIX="${DIR}" VERBOSE=1 install
	cd build/zstd-*/zlibWrapper/ && cp -a libzstd_zlibwrapper.a "${DIR}/lib/"
	cd build/zstd-*/zlibWrapper/ && cp -a zstd_zlibwrapper.h "${DIR}/include/"
	date >$@
