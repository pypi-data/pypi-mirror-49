{% extends 'base.spec' %}
{% block globals %}
%global srcname {{ pkg.sourcename }}
{% endblock %}

{% block requirements %}
  {% for pythonversion in [2, 3] %}
    {% if not loop.first %}

    {% endif %}
%package -n python{{ pythonversion }}-%{srcname}
Summary:	{{ pkg.summary }}
BuildRequires:  python{{ "2" if pythonversion == 2 else "%{python3_pkgversion}"}}-devel
    {% for build_dep in pkg.build_depends %}
BuildRequires:	{{ build_dep | reqformat(pythonversion) }}
    {% endfor %}
    {% for test_dep in pkg.test_depends %}
# Tests
BuildRequires:	{{ test_dep | reqformat(pythonversion) }}
    {% endfor %}

    {% for run_dep in pkg.run_depends %}
Requires:	{{ run_dep | reqformat(pythonversion)}}
    {% endfor %}

%description -n python{{ pythonversion }}-%{srcname}
TODO
  {% endfor %}
{% endblock requirements%}

{% block prep %}
%prep
%autosetup -n %{srcname}-%{version}
{% endblock %}

{% block build %}
%build
%py2_build
%py3_build
{% endblock %}

{% block install %}
%install
%py2_install
%py3_install
{% endblock %}

{% block files %}
%files -n python2-%{srcname}
%{python2_sitelib}/*.egg-info
%{python2_sitelib}/requests/

%files -n python%{python3_pkgversion}-%{srcname}
%{python3_sitelib}/-*.egg-info/
%{python3_sitelib}/%{srcname}/
{% endblock %}
