{% block globals %}{% endblock %}

Name:		{{ pkg.name }}	
Version:	{{ pkg.version }}
Release:	1%{?dist}
Summary:	{{ pkg.summary | truncate(60)}}

License:	{{ pkg.licenses }}
URL:		{{ pkg.homepage }}
Source0:	{{ pkg.source0 }}
BuildArch:	noarch

{% block description %}
%description
TODO
{% endblock %}

{% block requirements %}{% endblock %}

{% block prep %}
%prep
TODO
{% endblock %}

{% block build %}{% endblock %}

{% block install %}{% endblock %}

{% block check %}{% endblock %}

{% block files %}{% endblock %}

%changelog
* {{ pkg.today() }} TODO <TODO> - {{ pkg.version }}-1
- Initial package
