Name:		yum-plugin-at-exit
Version:	0.0.1
Release:	1
License:	GPLv3+
Group:		System Environment/Base
Summary:	Yum plugin to run arbitrary commands just before yum terminates
Url:		https://github.com/galaxy4public/yum-plugin-at-exit

Source0:	%name.py
Source1:	%name.conf
Source2:	%name.helper

Requires:	yum >= 3.2.19-15

BuildRequires:	python

BuildArch:	noarch

%description
This yum plugin provides support for running defined actions at the end of the
yum execution.

%install
rm -rf -- '%buildroot'
mkdir -p -m755 '%buildroot%_prefix/lib/yum-plugins'
install -m644 -p '%_sourcedir/%name.py' '%buildroot%_prefix/lib/yum-plugins/at-exit.py'
printf "import py_compile\npy_compile.compile('%buildroot%_prefix/lib/yum-plugins/at-exit.py')\n" | python
install -m755 -p '%_sourcedir/%name.helper' '%buildroot%_prefix/lib/yum-plugins/at-exit.helper'
mkdir -p -m755 '%buildroot%_sysconfdir/yum/pluginconf.d'
install -m644 -p '%_sourcedir/%name.conf' '%buildroot%_sysconfdir/yum/pluginconf.d/at-exit.conf'
mkdir -p -m755 '%buildroot%_sysconfdir/yum/pluginconf.d/at-exit.conf.d'

%files
%defattr(0600,root,root,0700)
%attr(0644,root,root) %_prefix/lib/yum-plugins/at-exit.py*
%attr(0755,root,root) %_prefix/lib/yum-plugins/at-exit.helper
%config(noreplace) %attr(0644,root,root) %_sysconfdir/yum/pluginconf.d/at-exit.conf
%dir %attr(0755,root,root) %_sysconfdir/yum/pluginconf.d/at-exit.conf.d

%changelog
* Sun Apr 03 2016 (GalaxyMaster) <galaxy-at-openwall.com> - 0.0.1-1
- Initial release to the public.
