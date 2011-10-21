%define		origname libxml
%include	/usr/lib/rpm/macros.java
Summary:	Namespace aware SAX-Parser utility library
Name:		java-pentaho-%{origname}
Version:	1.1.3
Release:	0.1
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/jfreereport/%{origname}-%{version}.zip
# Source0-md5:	8008caa6819ed7a03eb908cc989a65b9
Patch0:		libxml-1.1.2-build.patch
URL:		http://reporting.pentaho.org/
BuildRequires:	ant
#BuildRequires:	ant-contrib
BuildRequires:	ant-nodeps
BuildRequires:	jdk
BuildRequires:	jpackage-utils
#BuildRequires:	libbase
#BuildRequires:	libloader
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	jpackage-utils
#Requires:	libbase >= 1.1.2
#Requires:	libloader >= 1.1.2
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
%patch0 -p1

%undos README.txt licence-LGPL.txt ChangeLog.txt

find . -name "*.jar" | xargs rm -v

ln -s %{_javadir}/ant lib/ant-contrib

%build
mkdir -p lib
build-jar-repository -s -p lib commons-logging-api libbase libloader
%ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{origname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}
ln -s %{origname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{origname}.jar # ghost symlink

install -d $RPM_BUILD_ROOT%{_javadocdir}/%{origname}
cp -a bin/javadoc/docs/api $RPM_BUILD_ROOT%{_javadocdir}/%{origname}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{origname}-%{version} %{_javadocdir}/%{origname}

%files
%defattr(644,root,root,755)
%doc licence-LGPL.txt README.txt ChangeLog.txt
%{_javadir}/%{origname}-%{version}.jar
%{_javadir}/%{origname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{origname}-%{version}
%ghost %{_javadocdir}/%{origname}
%endif
