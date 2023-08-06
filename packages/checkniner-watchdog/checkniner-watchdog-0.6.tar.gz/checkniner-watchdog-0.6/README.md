Watchdog
========

Keep things running. Listen and respond in German.

Usage
-----

```shell
# Todo: How to install?
$ watchdog --version
$ watchdog --help
$ watchdog [--witness https://...] init
$ watchdog [--file PATH] patrol
$ watchdog wipe
```

Features
--------

- [x] Generating encryption keys
- [x] Generating signature keys
- [x] Registering as a witness with `Witness`
- [x] Extracting instructions from file contents
- [x] Executing commands
- [x] Sending results to `Witness`
- [ ] Creating an encrypted bundle with a small shim for decrypting
- [ ] Installable as a wheel
- [ ] Installable from pip
- [ ] Installable from a `Witness` instance
