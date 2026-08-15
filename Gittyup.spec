%global gittag      gittyup_v2.0.0
%global commit      a52b17a626fcebd815efcb75c98495039853dd57
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260721

%global lexilla_commit      82b21cd1348366a7dc25d57c6de532968da40541
%global lexilla_shortcommit %(c=%{lexilla_commit}; echo ${c:0:7})

%global scintillua_commit      33d0e3433a2046c1077f6b33fc801caf6bfac7a9
%global scintillua_shortcommit %(c=%{scintillua_commit}; echo ${c:0:7})

%global kuba_zip_commit      d7a2252a537926cbdef8512741a322a183fcfd09
%global kuba_zip_shortcommit %(c=%{kuba_zip_commit}; echo ${c:0:7})

Name:     Gittyup
Version:  2.0.0^git%{commitdate}.%{shortcommit}
Release:  2%{?dist}
Summary:  Graphical Git client designed to help you understand your source code history
License:  MIT
URL:      https://github.com/Murmele/Gittyup
Source0:  https://github.com/Murmele/Gittyup/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:  https://github.com/ScintillaOrg/lexilla/archive/%{lexilla_commit}/lexilla-%{lexilla_shortcommit}.tar.gz
Source2:  https://github.com/orbitalquark/scintillua/archive/%{scintillua_commit}/scintillua-%{scintillua_shortcommit}.tar.gz
Source3:  https://github.com/kuba--/zip/archive/%{kuba_zip_commit}/zip-%{kuba_zip_shortcommit}.tar.gz
Patch0:   0001-shell_injection_fix.patch
Patch1:   0002-fix_zip_test_dep_werror.patch
BuildRequires:   gcc-c++
BuildRequires:   cmake
BuildRequires:   ninja-build
BuildRequires:   pkgconfig(libcmark)
BuildRequires:   pkgconfig(hunspell)
BuildRequires:   pkgconfig(libgit2)
BuildRequires:   pkgconfig(lua)
BuildRequires:   pkgconfig(openssl)
BuildRequires:   cmake(Qt6Concurrent)
BuildRequires:   cmake(Qt6Core)
BuildRequires:   cmake(Qt6DBus)
BuildRequires:   cmake(Qt6Gui)
BuildRequires:   cmake(Qt6LinguistTools)
BuildRequires:   cmake(Qt6Network)
BuildRequires:   cmake(Qt6Widgets)
BuildRequires:   cmake(Qt6Test)

%description
Gittyup is a graphical Git client designed to help you understand and manage
 your source code history. Gittyup is a continuation of the GitAhead client.

%prep
%autosetup -n %{name}-%{commit} -p1 -N
%patch -P0 -p1

# Replace the placeholders for submodules with the downloaded source
rmdir dep/scintilla/lexilla
rmdir dep/scintilla/scintillua
rmdir test/dep/zip

tar -xf %{SOURCE1} -C dep/scintilla/
mv dep/scintilla/lexilla-%{lexilla_commit} dep/scintilla/lexilla

tar -xf %{SOURCE2} -C dep/scintilla/
mv dep/scintilla/scintillua-%{scintillua_commit} dep/scintilla/scintillua

tar -xf %{SOURCE3} -C test/dep
mv test/dep/zip-%{kuba_zip_commit} test/dep/zip
%patch -P1 -p1

%build
%cmake -G Ninja \
    -D CMAKE_BUILD_TYPE=RelWithDebInfo \
    -DUSE_SYSTEM_CMARK=ON \
    -DUSE_SYSTEM_GIT=ON \
    -DUSE_SYSTEM_HUNSPELL=ON \
    -DUSE_SYSTEM_LIBGIT2=ON \
    -DUSE_SYSTEM_LIBSSH2=ON  \
    -DUSE_SYSTEM_LUA=ON  \
    -DUSE_SYSTEM_OPENSSL=ON \
    -DUSE_SYSTEM_QT=ON \
    -DENABLE_UPDATE_OVER_GUI=OFF \
    -DENABLE_TESTS=ON \
    -DCMAKE_SKIP_RPATH=ON
%cmake_build

%check
export QT_QPA_PLATFORM=offscreen
ctest --test-dir redhat-linux-build --output-on-failure -j1 \
  --exclude-regex 'branches_panel|referencelist'

%install
%cmake_install

%files
%{_bindir}/gittyup
%{_bindir}/gittyup-indexer
%{_bindir}/gittyup-relauncher
%{_datadir}/Gittyup/*
%{_datadir}/applications/gittyup.desktop
%{_datadir}/icons/hicolor/*
%{_datadir}/locale/Gittyup/*
%exclude %{_includedir}/zip/*
%exclude %{_exec_prefix}/lib/cmake/zip/*
%exclude %{_exec_prefix}/lib/libzip*
%license %{_datadir}/licenses/Gittyup/LICENSE
%doc README.md

%changelog
%autochangelog
