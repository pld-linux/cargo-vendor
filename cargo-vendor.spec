Summary:	Cargo subcommand to vendor all crates.io dependencies into a local directory
Summary(pl.UTF-8):	Podpolecenie Cargo do wystawiania wszystkich zależności crates.io w lokalnym katalogu
Name:		cargo-vendor
Version:	0.1.23
Release:	1
License:	Apache v2.0 or MIT
Group:		Development/Tools
#Source0Download: https://github.com/alexcrichton/cargo-vendor/releases
Source0:	https://github.com/alexcrichton/cargo-vendor/releases/download/%{version}/%{name}-src-%{version}.tar.gz
# Source0-md5:	4c35b8f917b42c6fc600292d9779a84c
URL:		https://github.com/alexcrichton/cargo-vendor
BuildRequires:	cargo >= 0.33.0
BuildRequires:	curl-devel
BuildRequires:	rust
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Cargo subcommand which vendors all crates.io dependencies
into a local directory using Cargo's support for source replacement.

%description -l pl.UTF-8
Ten pakiet zawiera podpolecenie Cargo, które wystawia wszystkie
zależności crates.io w lokalnym katalogu przy użyciu obsługi
zamienników źródeł w Cargo.

%prep
%setup -q -n %{name}-src-%{version}

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

cargo -v build --release --frozen --features vendored-openssl

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

cargo -v install --frozen --root $RPM_BUILD_ROOT%{_prefix}
%{__rm} $RPM_BUILD_ROOT%{_prefix}/.crates.toml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE-MIT README.md
%attr(755,root,root) %{_bindir}/cargo-vendor
