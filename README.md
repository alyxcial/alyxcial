 ## alyxcial

  Low-level systems and security engineering. Mostly virtualization, firmware,
and the parts of an operating system that are easier to read in a disassembler
than in documentation.

### What I work on

**Virtualization internals.** QEMU/KVM device models, VFIO quirks, OVMF/EDK2,
and the SMBIOS and ACPI tables a guest actually reads. The firmware identity a
virtual machine reports is generated from bytes measured on real hardware
rather than copied by hand.

**Kernel.** Custom Linux trees, KVM on AMD (SVM), scheduling and timing paths.

**Windows internals.** Kernel-mode drivers (WDM/WDF), the display stack, and
offline registry and hive work.

**Reverse engineering.** Binaries and firmware, recovering undocumented
interfaces when there is no datasheet to read.

Most of it is declared in NixOS, so a host, a guest and the firmware between
them can be rebuilt from source and diffed.

### Tools

C · C++ · x86-64 assembly · Go · Python
Linux · NixOS · QEMU · radare2 · Ghidra

### How I work

Measured, not assumed. A fix is not finished until I have broken it on
purpose and watched the test catch it.
