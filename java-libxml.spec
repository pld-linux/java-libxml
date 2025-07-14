#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname libxml
Summary:	Namespace aware SAX-Parser utility library
Name:		java-%{srcname}
Version:	1.1.3
Release:	1
License:	LGPL v2+
Group:		Libraries/Java
Source0:	http://downloads.sourceforge.net/jfreereport/%{srcname}-%{version}.zip
# Source0-md5:	8008caa6819ed7a03eb908cc989a65b9
Patch0:		build.patch
URL:		http://reporting.pentaho.org/
BuildRequires:	ant
BuildRequires:	ant-contrib
BuildRequires:	ant-nodeps
BuildRequires:	java-libbase
BuildRequires:	java-libloader
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	java-libbase >= 1.1.2
Requires:	java-libloader >= 1.1.2
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pentaho LibXML is a namespace aware SAX-Parser utility library. It
eases the pain of implementing non-trivial SAX input handlers.

%package javadoc
Summary:	Javadoc for libxml
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils

%description javadoc
Javadoc for libxml.

%prep
%setup -qc
%patch -P0 -p1

%undos README.txt licence-LGPL.txt ChangeLog.txt

find -name "*.jar" | xargs rm -v

install -d lib
ln -s %{_javadir}/ant lib/ant-contrib

%build
build-jar-repository -s -p lib commons-logging-api libbase libloader
%ant jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar # ghost symlink

install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}
# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a bin/javadoc/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
