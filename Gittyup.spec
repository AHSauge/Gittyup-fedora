%global gittag      gittyup_v2.0.0
%global commit      68bfd9cebe5ad7b81e724d25c1355cdbd4a3a351
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate  20260515

%global lexilla_commit      82b21cd1348366a7dc25d57c6de532968da40541
%global lexilla_shortcommit %(c=%{lexilla_commit}; echo ${c:0:7})

%global scintillua_commit      33d0e3433a2046c1077f6b33fc801caf6bfac7a9
%global scintillua_shortcommit %(c=%{scintillua_commit}; echo ${c:0:7})

Name:     Gittyup
Version:  2.0.0^%{commitdate}git%{shortcommit}
Release:  %autorelease
Summary:  Graphical Git client designed to help you understand your source code history
License:  MIT
URL:      https://github.com/Murmele/Gittyup
Source0:  https://github.com/Murmele/Gittyup/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:  https://github.com/ScintillaOrg/lexilla/archive/%{lexilla_commit}/lexilla-%{lexilla_shortcommit}.tar.gz
Source2:  https://github.com/orbitalquark/scintillua/archive/%{scintillua_commit}/scintillua-%{scintillua_shortcommit}.tar.gz
#Fix CMAKE_EXE_LINKER_FLAGS being overwritten, breaking PIE
# https://github.com/Murmele/Gittyup/pull/963
Patch0:   0001-Append-CMAKE_EXE_LINKER_FLAGS-instead-of-overwriting.patch
#Fix crash during rapid scrolling
# https://github.com/Murmele/Gittyup/pull/952
Patch1:   0002-Fix-a-re-entrancy-issue-in-the.DiffView-code.patch
#Fix crash when using Filter by Path search
# https://github.com/Murmele/Gittyup/pull/962
Patch2:   0003-Fix-crash-in-Filter-by-Path-due-to-out-of-bound-acce.patch
#Fix performance regression in settings code
# https://github.com/Murmele/Gittyup/pull/958
Patch3:   0004-Add-a-cache-for-settings-to-avoid-reading-the-settin.patch
BuildRequires:   git g++ cmake ninja-build
BuildRequires:   cmark-devel hunspell-devel libgit2-devel libssh2-devel lua-devel openssl-devel pcre-devel
BuildRequires:   qt6-qtbase-devel qt6-linguist qt6-qttools-devel
Requires:   cmark hunspell lua openssl pcre qt6-qtbase

%description
Gittyup is a graphical Git client designed to help you understand and manage
 your source code history. Gittyup is a continuation of the GitAhead client.

%prep
%autosetup -n %{name}-%{commit} -p1

# Replace the placeholders for submodules with the downloaded source
rmdir dep/scintilla/lexilla
rmdir dep/scintilla/scintillua

tar -xf %{SOURCE1} -C dep/scintilla/
mv dep/scintilla/lexilla-%{lexilla_commit} dep/scintilla/lexilla

tar -xf %{SOURCE2} -C dep/scintilla/
mv dep/scintilla/scintillua-%{scintillua_commit} dep/scintilla/scintillua

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
    -DENABLE_TESTS=OFF \
    -DCMAKE_SKIP_RPATH=ON
%cmake_build

%check
#TBD check

%install
%cmake_install

%files
%{_bindir}/gittyup
%{_bindir}/gittyup-indexer
%{_datadir}/Gittyup/*
%{_datadir}/applications/gittyup.desktop
%{_datadir}/icons/hicolor/*
%{_datadir}/locale/Gittyup/*
%license %{_datadir}/licenses/Gittyup/LICENSE
%doc README.md

%exclude
%{_bindir}/gittyup-relauncher

%changelog
%autochangelog
