# Force out of source build
%undefine __cmake_in_source_build

%define major 0
%define libname %mklibname airspy %{major}
%define devname %mklibname -d airspy

Name:           airspyone_host
Version:	1.0.10
Release:	1
Summary:        AirSpy host tools and library
Group:      Communications
License:        GPLv2+
URL:            http://airspy.com/
Source0:	https://github.com/airspy/airspyone_host/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	pkgconfig(libusb)
BuildRequires:	cmake
Requires:       systemd

%description
Software for AirSpy, a project to produce a low cost, open
source software radio platform.

%package -n %{libname}
Summary:	AirSpy library
Group:		System/Libraries

%description -n %{libname}
AirSpy host tools and library

%package -n     %{devname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
License:        MIT and BSD
Summary:        Development files for %{name}
Group:          System/Libraries
Requires:       %{libname} = %{EVRD}

%description -n %{devname}
Files needed to develop software against libairspy.

%prep
%autosetup -p1

# Remove win stuff
rm -rf libairspy/vc

# Fix udev rule
sed -i -e 's/GROUP="plugdev"/ENV{ID_SOFTWARE_RADIO}="1"/g' airspy-tools/52-airspy.rules

%build
%cmake -DINSTALL_UDEV_RULES=on

%make_build

%install
%make_install -C build

# Remove static object
rm -f %{buildroot}%{_libdir}/libairspy.a

# Move udev rule to correct location
mkdir -p %{buildroot}%{_udevrulesdir}
mv %{buildroot}%{_sysconfdir}/udev/rules.d/52-airspy.rules %{buildroot}%{_udevrulesdir}

%files
%license airspy-tools/LICENSE.md
%doc README.md
%{_bindir}/airspy_*
%{_udevrulesdir}/52-airspy.rules

%files -n %{libname}
%{_libdir}/libairspy.so.%{major}*
%{_libdir}/libairspy.so.%{version}*

%files -n %{devname}
%{_includedir}/libairspy
%{_libdir}/pkgconfig/libairspy.pc
%{_libdir}/libairspy.so
