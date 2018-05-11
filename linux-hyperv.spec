#
# This is a special configuration of the Linux kernel, aimed exclusively
# for running inside a Hyper-V virtual machine
# This specialization allows us to optimize memory footprint and boot time.
#

Name:           linux-hyperv
Version:        4.14.21
Release:        126
License:        GPL-2.0
Summary:        The Linux kernel optimized for running inside Hyper-V
Url:            http://www.kernel.org/
Group:          kernel
Source0:        https://www.kernel.org/pub/linux/kernel/v4.x/linux-4.14.21.tar.xz
Source1:        config
Source2:        cmdline

%define kversion %{version}-%{release}.hyperv

BuildRequires:  bash >= 2.03
BuildRequires:  bc
BuildRequires:  binutils-dev
BuildRequires:  elfutils-dev
BuildRequires:  make >= 3.78
BuildRequires:  openssl-dev
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  kmod

# don't strip .ko files!
%global __os_install_post %{nil}
%define debug_package %{nil}
%define __strip /bin/true

#    000X: cve, bugfixes patches
Patch0001: cve-2017-13693.patch

#    00XY: Mainline patches, upstream backports

# Serie    01XX: Clear Linux patches
Patch0101: 0101-init-don-t-wait-for-PS-2-at-boot.patch
Patch0102: 0102-i8042-decrease-debug-message-level-to-info.patch
Patch0103: 0103-init-do_mounts-recreate-dev-root.patch
Patch0104: 0104-Increase-the-ext4-default-commit-age.patch
Patch0105: 0105-silence-rapl.patch
Patch0106: 0106-pci-pme-wakeups.patch
Patch0107: 0107-ksm-wakeups.patch
Patch0108: 0108-intel_idle-tweak-cpuidle-cstates.patch
Patch0109: 0109-xattr-allow-setting-user.-attributes-on-symlinks-by-.patch
Patch0110: 0110-init_task-faster-timerslack.patch
Patch0111: 0111-fs-ext4-fsync-optimize-double-fsync-a-bunch.patch
Patch0112: 0112-overload-on-wakeup.patch
Patch0113: 0113-bootstats-add-printk-s-to-measure-boot-time-in-more-.patch
Patch0114: 0114-fix-initcall-timestamps.patch
Patch0115: 0115-smpboot-reuse-timer-calibration.patch
Patch0116: 0116-raid6-add-Kconfig-option-to-skip-raid6-benchmarking.patch
Patch0117: 0117-Initialize-ata-before-graphics.patch
Patch0118: 0118-reduce-e1000e-boot-time-by-tightening-sleep-ranges.patch
Patch0119: 0119-Skip-synchronize_rcu-on-single-CPU-systems.patch
Patch0120: 0120-Make-a-few-key-drivers-probe-asynchronous.patch
Patch0121: 0121-use-the-new-async-probing-feature-for-the-hyperv-dri.patch
Patch0122: 0122-sysrq-Skip-synchronize_rcu-if-there-is-no-old-op.patch
Patch0123: 0123-printk-end-of-boot.patch
Patch0124: 0124-Boot-with-rcu-expedite-on.patch
Patch0125: 0125-give-rdrand-some-credit.patch
Patch0126: 0126-print-starve.patch
Patch0127: 0127-increase-readahead-amounts.patch
Patch0128: 0128-free-initmem-asynchronously.patch
Patch0129: 0129-remove-clear-ioapic.patch
Patch0130: 0130-Add-dysk-driver.patch
Patch0131: 0131-dysk-let-compiler-handle-inlining.patch
Patch0132: 0132-Modify-Kconfig-Makefiles-to-support-dysk.patch

# Serie    XYYY: Extra features modules
patch0200: zero-regs.patch

%description
The Linux kernel.

%package extra
License:        GPL-2.0
Summary:        The Linux kernel Hyper-V extra files
Group:          kernel

%description extra
Linux kernel extra files

%prep
%setup -q -n linux-4.14.21

#     000X  cve, bugfixes patches
%patch0001 -p1

#     00XY  Mainline patches, upstream backports

#     01XX  Clear Linux patches
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1
%patch0131 -p1
%patch0132 -p1

%patch0200 -p1

cp %{SOURCE1} .

%build
BuildKernel() {
    MakeTarget=$1

    Arch=x86_64
    ExtraVer="-%{release}.hyperv"

    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = ${ExtraVer}/" Makefile

    make -s mrproper
    cp config .config

    make -s ARCH=$Arch oldconfig > /dev/null
    make -s CONFIG_DEBUG_SECTION_MISMATCH=y %{?_smp_mflags} ARCH=$Arch %{?sparse_mflags}
}

BuildKernel bzImage

%install

InstallKernel() {
    KernelImage=$1

    Arch=x86_64
    KernelVer=%{kversion}
    KernelDir=%{buildroot}/usr/lib/kernel

    mkdir   -p ${KernelDir}
    install -m 644 .config    ${KernelDir}/config-${KernelVer}
    install -m 644 System.map ${KernelDir}/System.map-${KernelVer}
    install -m 644 %{SOURCE2} ${KernelDir}/cmdline-${KernelVer}
    cp  $KernelImage ${KernelDir}/org.clearlinux.hyperv.%{version}-%{release}
    chmod 755 ${KernelDir}/org.clearlinux.hyperv.%{version}-%{release}

    mkdir -p %{buildroot}/usr/lib/modules/$KernelVer
    make -s ARCH=$Arch INSTALL_MOD_PATH=%{buildroot}/usr modules_install KERNELRELEASE=$KernelVer

    rm -f %{buildroot}/usr/lib/modules/$KernelVer/build
    rm -f %{buildroot}/usr/lib/modules/$KernelVer/source

    # Erase some modules index
    for i in alias ccwmap dep ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols usbmap softdep devname
    do
        rm -f %{buildroot}/usr/lib/modules/${KernelVer}/modules.${i}*
    done
    rm -f %{buildroot}/usr/lib/modules/${KernelVer}/modules.*.bin
}

InstallKernel arch/x86/boot/bzImage

rm -rf %{buildroot}/usr/lib/firmware

# Recreate modules indices
depmod -a -b %{buildroot}/usr %{kversion}

ln -s org.clearlinux.hyperv.%{version}-%{release} %{buildroot}/usr/lib/kernel/default-hyperv

%files
%dir /usr/lib/kernel
%dir /usr/lib/modules/%{kversion}
/usr/lib/kernel/config-%{kversion}
/usr/lib/kernel/cmdline-%{kversion}
/usr/lib/kernel/org.clearlinux.hyperv.%{version}-%{release}
/usr/lib/kernel/default-hyperv
/usr/lib/modules/%{kversion}/kernel
/usr/lib/modules/%{kversion}/modules.*

%files extra
%dir /usr/lib/kernel
/usr/lib/kernel/System.map-%{kversion}
