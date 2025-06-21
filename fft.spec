# RPM spec file for FFT (File Type Tester)
# Copyright (c) 2025 Brandon Perkins <bdperkin@gmail.com>
# SPDX-License-Identifier: MIT

%global srcname fft
%global desc FFT (File Type Tester) is a Python tool that determines the file type of files \
using three different test categories performed in sequence: filesystem tests, magic tests, \
and language tests. The first test that successfully identifies the file type will be reported.

Name:           python3-%{srcname}
Version:        1.3.0
Release:        1%{?dist}
Summary:        File Type Tester - determine file types using filesystem, magic, and language tests

License:        MIT
URL:            https://github.com/bdperkin/fft
Source0:        https://github.com/bdperkin/fft/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

# Build dependencies
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  texinfo
BuildRequires:  groff-base

# Runtime dependencies
Requires:       python3
Requires:       python3-magic >= 0.4.24
Requires:       file-libs

# Development dependencies (for -dev subpackage)
%if 0%{?with_tests}
BuildRequires:  python3-pytest >= 7.0.0
BuildRequires:  python3-pytest-cov >= 4.0.0
BuildRequires:  python3-black >= 23.0.0
BuildRequires:  python3-flake8 >= 6.0.0
BuildRequires:  python3-isort >= 5.12.0
BuildRequires:  python3-mypy >= 1.5.0
%endif

%description
%{desc}

Key Features:
* Three-tier detection system for comprehensive file type identification
* Support for over 30 common file extensions
* Magic number detection using libmagic
* Programming language detection through content analysis
* Special file type detection (directories, symlinks, devices)
* Verbose mode showing which test detected the file type
* Brief mode for script-friendly output
* Cross-platform compatibility

%package doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}

%description doc
This package contains comprehensive documentation for FFT including:
* Manual pages (man fft)
* GNU Info documentation (info fft)
* HTML documentation
* Contributing guidelines and development documentation

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       python3-pytest >= 7.0.0
Requires:       python3-pytest-cov >= 4.0.0
Requires:       python3-black >= 23.0.0
Requires:       python3-flake8 >= 6.0.0
Requires:       python3-isort >= 5.12.0
Requires:       python3-mypy >= 1.5.0

%description devel
This package contains development files for FFT including:
* Test suite with pytest framework
* Pre-commit hooks configuration
* Code quality tools configuration
* Build system (Makefile)
* Source Texinfo documentation

%prep
%autosetup -n %{srcname}-%{version}

%build
# Build Python package
%py3_build

# Build documentation
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
makeinfo %{srcname}.texi
makeinfo --html --no-split %{srcname}.texi
%endif

%install
# Install Python package
%py3_install

# Install manual page
install -Dpm 644 %{srcname}.1 %{buildroot}%{_mandir}/man1/%{srcname}.1

# Install info documentation
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
install -Dpm 644 %{srcname}.info %{buildroot}%{_infodir}/%{srcname}.info
%endif

# Install HTML documentation
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
install -Dpm 644 %{srcname}.html %{buildroot}%{_docdir}/%{name}/%{srcname}.html
%endif

# Install additional documentation
install -Dpm 644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -Dpm 644 CHANGELOG.md %{buildroot}%{_docdir}/%{name}/CHANGELOG.md
install -Dpm 644 CONTRIBUTING.md %{buildroot}%{_docdir}/%{name}/CONTRIBUTING.md
install -Dpm 644 LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE
install -Dpm 644 COPYING %{buildroot}%{_docdir}/%{name}/COPYING

# Install development files
install -Dpm 644 Makefile %{buildroot}%{_docdir}/%{name}/Makefile
install -Dpm 644 %{srcname}.texi %{buildroot}%{_docdir}/%{name}/%{srcname}.texi
install -Dpm 644 pyproject.toml %{buildroot}%{_docdir}/%{name}/pyproject.toml
install -Dpm 644 .pre-commit-config.yaml %{buildroot}%{_docdir}/%{name}/.pre-commit-config.yaml

# Install test suite
mkdir -p %{buildroot}%{_docdir}/%{name}/tests
cp -r tests/* %{buildroot}%{_docdir}/%{name}/tests/

%check
%if 0%{?with_tests}
# Run test suite
export PYTHONPATH=%{buildroot}%{python3_sitelib}
python3 -m pytest tests/ -v
%endif

%post doc
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
if [ -f %{_infodir}/%{srcname}.info ]; then
    /sbin/install-info %{_infodir}/%{srcname}.info %{_infodir}/dir || :
fi
%endif

%preun doc
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
if [ $1 = 0 ] && [ -f %{_infodir}/%{srcname}.info ]; then
    /sbin/install-info --delete %{_infodir}/%{srcname}.info %{_infodir}/dir || :
fi
%endif

%files
%license LICENSE COPYING
%doc README.md
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{_bindir}/%{srcname}

%files doc
%{_mandir}/man1/%{srcname}.1*
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
%{_infodir}/%{srcname}.info*
%{_docdir}/%{name}/%{srcname}.html
%endif
%{_docdir}/%{name}/README.md
%{_docdir}/%{name}/CHANGELOG.md
%{_docdir}/%{name}/CONTRIBUTING.md
%{_docdir}/%{name}/LICENSE
%{_docdir}/%{name}/COPYING

%files devel
%{_docdir}/%{name}/Makefile
%{_docdir}/%{name}/%{srcname}.texi
%{_docdir}/%{name}/pyproject.toml
%{_docdir}/%{name}/.pre-commit-config.yaml
%{_docdir}/%{name}/tests/

%changelog
* Thu Dec 19 2024 Brandon Perkins <bdperkin@gmail.com> - 1.3.0-1
- Add comprehensive info format documentation with build system
- Create enterprise-grade documentation system alongside man pages
- Add 12 structured chapters with hierarchical navigation
- Include cross-referenced sections with searchable index
- Add Makefile with automated build targets
- Configure pytest framework with comprehensive test suite
- Add -b/--brief command line option for script-friendly output
- Create COPYING file with MIT license text

* Wed Dec 18 2024 Brandon Perkins <bdperkin@gmail.com> - 1.2.0-1
- Configure cSpell for comprehensive spell checking
- Add project author information and GitHub repository URLs
- Implement dynamic versioning system
- Add Python 3.13 to supported versions (3.6-3.13)
- Add MIT license headers to source files
- Update project metadata and documentation

* Tue Dec 17 2024 Brandon Perkins <bdperkin@gmail.com> - 1.1.0-1
- Enhanced CLI output with filename prepending
- Add verbose mode showing detection test categories
- Update project to modern pyproject.toml build system
- Add comprehensive pre-commit hooks for code quality
- Implement code quality tools (Black, Flake8, isort, MyPy)
- Add comprehensive documentation (CHANGELOG.md, CONTRIBUTING.md)

* Mon Dec 16 2024 Brandon Perkins <bdperkin@gmail.com> - 1.0.0-1
- Initial RPM package release
- Implement three-tier file type detection system
- Add filesystem tests for extensions and permissions
- Add magic tests using libmagic for file signatures
- Add language tests for programming language detection
- Support for 30+ file extensions and special file types
- Command-line interface with multiple file support
- Cross-platform compatibility (Linux, macOS, Windows)
