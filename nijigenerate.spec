%define nijigenerate_ver 0.7.1
%define nijigenerate_semver 0.7.1+build.994.ge77ca8a
%define nijigenerate_dist 994
%define nijigenerate_commit e77ca8ab25a31b54b0b3e6747e98a5d9b7eea993
%define nijigenerate_short e77ca8a

# Project maintained deps
%define nijilive_semver 0.0.0+build.652.bd00329
%define nijilive_commit bd003295f2bae1c67127d4f5c051a9e91099078a
%define nijilive_short bd00329

%if 0%{nijigenerate_dist} > 0
%define nijigenerate_suffix ^%{nijigenerate_dist}.git%{nijigenerate_short}
%endif

Name:           nijigenerate
Version:        %{nijigenerate_ver}%{?nijigenerate_suffix:}
Release:        %autorelease
Summary:        Tool to create and edit nijilive puppets

# Bundled lib licenses
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
##   i2d-imgui licenses: BSL-1.0 and MIT
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
Source1:        https://github.com/nijigenerate/nijilive/archive/%{nijilive_commit}/nijilive-%{nijilive_short}.tar.gz

Patch0:         nijigenerate_0_icon-path.patch
Patch1:         nijigenerate_1_deps.patch

# dlang
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  git

BuildRequires:  zdub-dub-settings-hack

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
BuildRequires:  zdub-i2d-imgui-static
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

# static i2d-imgui reqs
BuildRequires:  gcc-c++
BuildRequires:  freetype-devel
BuildRequires:  SDL2-devel

Requires:       hicolor-icon-theme

#dportals deps
Requires:       dbus

#i2d-imgui deps
Requires:       libstdc++
Requires:       freetype
Requires:       SDL2


%description
nijilive is a framework for realtime 2D puppet animation which can be used for VTubing, 
game development and digital animation. 
nijigenerate is a tool that lets you create and edit nijilive puppets.


%prep
%setup -n %{name}-%{nijigenerate_commit}

# FIX: Nijigenerate version dependent on git
cat > source/nijigenerate/ver.d <<EOF
module nijigenerate.ver;

enum INC_VERSION = "%{nijigenerate_semver}";
EOF

# FIX: Add fake dependency
mkdir -p deps/vibe-d
cat > deps/vibe-d/dub.sdl <<EOF
name "vibe-d"
subpackage "http"
EOF
dub add-local deps/vibe-d "0.9.5"

%patch -P 0 -p1 -b .nijigenerate-icon-path
%patch -P 1 -p1 -b .nijigenerate-deps
mkdir -p deps

# Project maintained deps
tar -xzf %{SOURCE1}
mv nijilive-%{nijilive_commit} deps/nijilive
dub add-local deps/nijilive/ "%{nijilive_semver}"

pushd deps; pushd nijilive

# FIX: nijilive version dependent on git
cat > source/nijilive/ver.d <<EOF
module nijilive.ver;

enum IN_VERSION = "%{nijilive_semver}";
EOF

[ -f dub.sdl ] && dub convert -f json
mv -f dub.json dub.json.base
jq 'walk(if type == "object" then with_entries(select(.key | test("preBuildCommands*") | not)) else . end)' dub.json.base > dub.json

popd; popd


%build
export DFLAGS="%{_d_optflags}"
dub build \
    --cache=local \
    --config=linux-full \
    --skip-registry=all \
    --non-interactive \
    --temp-build \
    --compiler=ldc2
mkdir ./out/
cp /tmp/.dub/build/nijigenerate*/linux-full*/* ./out/


%install
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -p ./out/nijigenerate ${RPM_BUILD_ROOT}%{_bindir}/nijigenerate

install -d ${RPM_BUILD_ROOT}%{_datadir}/applications/
install -p -m 644 ./build-aux/linux/nijigenerate.desktop ${RPM_BUILD_ROOT}%{_datadir}/applications/nijigenerate.desktop
desktop-file-validate \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/nijigenerate.desktop

install -d ${RPM_BUILD_ROOT}%{_metainfodir}/
install -p -m 644 ./build-aux/linux/nijigenerate.appdata.xml ${RPM_BUILD_ROOT}%{_metainfodir}/nijigenerate.appdata.xml
appstream-util validate-relax --nonet \
    ${RPM_BUILD_ROOT}%{_metainfodir}/nijigenerate.appdata.xml

install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/
install -p -m 644 ./res/logo_256.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/nijigenerate.png

# Dependency licenses
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