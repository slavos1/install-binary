# How the stuff works

## Resolving artifact names

[Restic](https://github.com/restic/restic/releases) uses release names in artifact names without `v` prefix.
That is, Linux 64bit binary is `restic_0.16.4_linux_amd64.bz2` for the tag `v0.16.4`.
To download such artifact:
1. we resolve the `latest` release to the actual tag, say, `v0.16.4`
2. we download the artifact using the tag with stripped `v` prefix, like `https://github.com/restic/restic/releases/latest/download/restic_0.16.4_linux_amd64.bz2`
3. Last, we try unpacking the artifact:
* as a binary from `tar.gz` archive
* as a sole binary from `bz2`
4. we install (copy) it to `~/.local/bin`

Note: there is an [issue raised](issues/1) to support installing of Debian packages (.deb).
