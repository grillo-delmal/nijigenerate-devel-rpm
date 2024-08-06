%define nijigenerate_ver 0.7.1
%define nijigenerate_semver 0.7.1+build.993.g1d7e82d
%define nijigenerate_dist 993
%define nijigenerate_commit 1d7e82dc6a4a7d0a9afbb9bb77007a9550a92508
%define nijigenerate_short 1d7e82d

# Project maintained deps
%define i2d_imgui_semver 0.8.0+build.4.ge34f8ba
%define i2d_imgui_commit e34f8ba04c0085be7ee83a8df200cf2ffb30bfd3
%define i2d_imgui_short e34f8ba

%define nijilive_semver 0.0.1+build.0-og.0.0.0.build.649.20567d5
%define nijilive_commit 20567d51f25d629c9378745b88a2c30d0f6216e0
%define nijilive_short 20567d5

# cimgui
%define cimgui_commit 49bb5ce65f7d5eeab7861d8ffd5aa2a58ca8f08c
%define cimgui_short 49bb5ce
%define imgui_commit dd5b7c6847372016f45d5b5abda687bd5cd19224
%define imgui_short dd5b7c6


%if 0%{nijigenerate_dist} > 0
%define nijigenerate_suffix ^%{nijigenerate_dist}.git%{nijigenerate_short}
%endif

Name:           nijigenerate
Version:        %{nijigenerate_ver}%{?nijigenerate_suffix:}
Release:        %autorelease
Summary:        Tool to create and edit nijilive puppets

# Bundled lib licenses
##   i2d-imgui licenses: BSL-1.0 and MIT
##   nijilive licenses: BSD-2-Clause
# Static dependencies licenses
##   bcaa licenses: BSL-1.0
##   bindbc-loader licenses: BSL-1.0
##   bindbc-sdl licenses: BSL-1.0
##   dcv licenses: BSL-1.0
##   ddbus licenses: MIT
##   dportals licenses: BSD-2-Clause
##   dunit licenses: MIT
##   dxml licenses: BSL-1.0
##   fghj licenses: BSL-1.0
##   i18n-d licenses: BSD-2-Clause
##   i2d-opengl licenses: BSL-1.0
##   imagefmt licenses: BSD-2-Clause
##   inmath licenses: BSD-2-Clause
##   kra-d licenses: BSD-2-Clause
##   mir-algorithm licenses: Apache-2.0
##   mir-core licenses: Apache-2.0
##   mir-linux-kernel licenses: BSL-1.0
##   mir-random licenses: Apache-2.0
##   psd-d licenses: BSD-2-Clause
##   silly licenses: ISC
##   tinyfiledialogs licenses: Zlib
License:        BSD-2-Clause and Apache-2.0 and BSL-1.0 and ISC and MIT and Zlib

URL:            https://github.com/grillo-delmal/nijigenerate-rpm

Source0:        https://github.com/nijigenerate/nijigenerate/archive/%{nijigenerate_commit}/%{name}-%{nijigenerate_short}.tar.gz

# Project maintained deps
Source1:        https://github.com/Inochi2D/i2d-imgui/archive/%{i2d_imgui_commit}/i2d-imgui-%{i2d_imgui_short}.tar.gz
Source2:        https://github.com/nijigenerate/nijilive/archive/%{nijilive_commit}/nijilive-%{nijilive_short}.tar.gz

# cimgui
Source3:        https://github.com/Inochi2D/cimgui/archive/%{cimgui_commit}/cimgui-%{cimgui_short}.tar.gz
Source4:        https://github.com/Inochi2D/imgui/archive/%{imgui_commit}/imgui-%{imgui_short}.tar.gz

Patch0:         nijigenerate_0_icon-path.patch
Patch1:         nijilive_0_rm-gitver.patch


# dlang
BuildRequires:  ldc
BuildRequires:  dub

# cimgui
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  freetype-devel
BuildRequires:  SDL2-devel
BuildRequires:  dbus-devel

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  git

BuildRequires:  zdub-bcaa-static
BuildRequires:  zdub-bindbc-loader-static
BuildRequires:  zdub-bindbc-sdl-static
BuildRequires:  zdub-dcv-static
BuildRequires:  zdub-ddbus-static
BuildRequires:  zdub-dportals-static
BuildRequires:  zdub-dunit-static
BuildRequires:  zdub-dxml-static
BuildRequires:  zdub-fghj-static
BuildRequires:  zdub-i18n-d-static
BuildRequires:  zdub-i2d-opengl-static
BuildRequires:  zdub-imagefmt-static
BuildRequires:  zdub-inmath-static
BuildRequires:  zdub-kra-d-static
BuildRequires:  zdub-mir-algorithm-static
BuildRequires:  zdub-mir-core-static
BuildRequires:  zdub-mir-linux-kernel-static
BuildRequires:  zdub-mir-random-static
BuildRequires:  zdub-psd-d-static
BuildRequires:  zdub-silly-static
BuildRequires:  zdub-tinyfiledialogs-static

Requires:       hicolor-icon-theme


%description
nijilive is a framework for realtime 2D puppet animation which can be used for VTubing, 
game development and digital animation. 
nijigenerate is a tool that lets you create and edit nijilive puppets.

%prep
%setup -n %{name}-%{nijigenerate_commit}

# FIX: nijigenerate version dependent on git
cat > source/nijigenerate/ver.d <<EOF
module nijigenerate.ver;

enum INC_VERSION = "%{nijigenerate_semver}";
EOF

%patch0 -p1 -b .nijigenerate-icon-path
mkdir deps

# Project maintained deps
tar -xzf %{SOURCE1}
mv i2d-imgui-%{i2d_imgui_commit} deps/i2d-imgui
dub add-local deps/i2d-imgui/ "%{i2d_imgui_semver}"

tar -xzf %{SOURCE2}
mv nijilive-%{nijilive_commit} deps/nijilive
dub add-local deps/nijilive/ "%{nijilive_semver}"

pushd deps; pushd nijilive

%patch1 -p1 -b .nijilive-rm-gitver

# FIX: nijilive version dependent on git
cat > source/nijilive/ver.d <<EOF
module nijilive.ver;

enum IN_VERSION = "%{nijilive_semver}";
EOF

popd; popd

# cimgui

tar -xzf %{SOURCE3}
rm -r deps/i2d-imgui/deps/cimgui
mv cimgui-%{cimgui_commit} deps/i2d-imgui/deps/cimgui

tar -xzf %{SOURCE4}
rm -r deps/i2d-imgui/deps/cimgui/imgui
mv imgui-%{imgui_commit} deps/i2d-imgui/deps/cimgui/imgui

pushd deps; pushd i2d-imgui

rm -rf deps/freetype
rm -rf deps/glbinding
rm -rf deps/glfw
rm -rf deps/SDL
rm -rf deps/cimgui/imgui/examples/

# FIX: Make i2d-imgui submodule checking only check cimgui
rm .gitmodules
cat > .gitmodules <<EOF
[submodule "deps/cimgui"]
	path = deps/cimgui
	url = https://github.com/Inochi2D/cimgui.git
EOF
mkdir deps/cimgui/.git

popd; popd



%build
export DFLAGS="%{_d_optflags}"
dub build \
    --cache=local \
    --config=linux-full \
    --skip-registry=all \
    --temp-build \
    --compiler=ldc2
mkdir ./out/
cp /tmp/.dub/build/nijigenerate*/linux-full*/* ./out/


%install
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -p ./out/nijigenerate ${RPM_BUILD_ROOT}%{_bindir}/nijigenerate

install -d ${RPM_BUILD_ROOT}%{_datadir}/applications/
install -p -m 644 build-aux/linux/nijigenerate.desktop ${RPM_BUILD_ROOT}%{_datadir}/applications/nijigenerate.desktop
desktop-file-validate \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/nijigenerate.desktop

install -d ${RPM_BUILD_ROOT}%{_metainfodir}/
install -p -m 644 build-aux/linux/nijigenerate.appdata.xml ${RPM_BUILD_ROOT}%{_metainfodir}/nijigenerate.appdata.xml
appstream-util validate-relax --nonet \
    ${RPM_BUILD_ROOT}%{_metainfodir}/nijigenerate.appdata.xml

install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/
install -p -m 644 res/logo_256.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/nijigenerate.png

# Dependency licenses
install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/./deps/i2d-imgui/cimgui/
install -p -m 644 ./deps/i2d-imgui/deps/cimgui/LICENSE \
    ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/./deps/i2d-imgui/cimgui/LICENSE
install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/./deps/i2d-imgui/imgui/
install -p -m 644 ./deps/i2d-imgui/deps/cimgui/imgui/LICENSE.txt \
    ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/./deps/i2d-imgui/imgui/LICENSE.txt

install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/deps/
find ./deps/ -mindepth 1 -maxdepth 1 -exec \
    install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/{} ';'

find ./deps/ -mindepth 2 -maxdepth 2 -iname '*LICENSE*' -exec \
    install -p -m 644 "{}" "${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/{}" ';'

install -d ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/res/
find ./res/ -mindepth 1 -maxdepth 1 -iname '*LICENSE*' -exec \
    install -p -m 644 {} ${RPM_BUILD_ROOT}%{_datadir}/licenses/%{name}/{} ';'


%files
%license LICENSE
%{_datadir}/licenses/%{name}/*
%{_bindir}/nijigenerate
%{_metainfodir}/nijigenerate.appdata.xml
%{_datadir}/applications/nijigenerate.desktop
%{_datadir}/icons/hicolor/256x256/apps/nijigenerate.png


%changelog
%autochangelog