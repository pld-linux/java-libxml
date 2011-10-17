# Use rpmbuild --without gcj to disable native bits
%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}
%define origname libxml

Summary:	Namespace aware SAX-Parser utility library
Name:		pentaho-libxml
Version:	1.1.3
Release:	2%{?dist}
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/jfreereport/%{origname}-%{version}.zip
URL:		http://reporting.pentaho.org/
BuildRequires:	jpackage-utils
BuildRequires:	libbase
BuildRequires:	libloader
BuildRequires:	ant
BuildRequires:	ant-contrib
BuildRequires:	ant-nodeps
BuildRequires:	java-devel
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	java
Requires:	jpackage-utils
Requires:	libbase >= 1.1.2
Requires:	libloader >= 1.1.2
%if %{with_gcj}
BuildRequires:	java-gcj-compat-devel >= 1.0.31
Requires(post):	java-gcj-compat >= 1.0.31
Requires(postun):	java-gcj-compat >= 1.0.31
%else
BuildArch:	noarch
%endif
Patch0:		libxml-1.1.2-build.patch

%description
Pentaho LibXML is a namespace aware SAX-Parser utility library. It
eases the pain of implementing non-trivial SAX input handlers.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils
%if %{with_gcj}
BuildArch:	noarch
%endif

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
%patch0 -p1 -b .build
find . -name "*.jar" -exec rm -f {} \;
mkdir -p lib
build-jar-repository -s -p lib commons-logging-api libbase libloader
cd lib
ln -s %{_javadir}/ant ant-contrib

%build
%ant jar javadoc
for file in README.txt licence-LGPL.txt ChangeLog.txt; do
	tr -d '\r' < $file > $file.new
	mv $file.new $file
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_javadir}
cp -p ./dist/%{origname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
pushd $RPM_BUILD_ROOT%{_javadir}
ln -s %{origname}-%{version}.jar %{origname}.jar
popd

install -d $RPM_BUILD_ROOT%{_javadocdir}/%{origname}
cp -rp bin/javadoc/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{origname}
%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(644,root,root,755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/%{origname}-%{version}.jar
%{_javadir}/%{origname}.jar
%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{origname}

BuildRequires:  jpackage-utils
BuildRequires:  rpmbuild(macros) >= 1.300
