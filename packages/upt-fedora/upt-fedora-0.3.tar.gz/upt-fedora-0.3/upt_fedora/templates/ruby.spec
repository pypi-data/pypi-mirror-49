{% extends 'base.spec' %}
{% block globals %}
%global gem_name {{ pkg.sourcename }}
{% endblock %}

{% block requirements %}
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
  {% for build_dep in pkg.build_depends %}
BuildRequires: {{ build_dep | reqformat }}
  {% endfor %}
  {% for test_dep in pkg.test_depends %}
BuildRequires: {{ test_dep | reqformat }}
  {% endfor %}
{% endblock %}

{% block prep %}
%prep
%if 0%{?fedora} <= 26
gem unpack %{SOURCE0}
gem spec %{SOURCE0} -l --ruby > %{gem_name}-%{version}.gemspec

%setup -q -D -T -n  %{gem_name}-%{version}
%else
%setup -q -n  %{gem_name}-%{version}
%endif
{% endblock %}

{% block build %}
gem build ../%{gem_name}-%{version}.gemspec
{% endblock %}

{% block install %}
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

# TODO: Uncomment if there were programs installed:
# mkdir -p %{buildroot}%{_bindir}
# cp -a ./%{_bindir}/* %{buildroot}%{_bindir}

# TODO: Uncomment if there are C extensions:
# mkdir -p %{buildroot}%{gem_extdir_mri}
# cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} %{buildroot}%{gem_extdir_mri}/
{% endblock %}

{% block check %}
%check
TODO
{% endblock %}
