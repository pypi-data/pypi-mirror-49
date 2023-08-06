# pyphash: extremely simple wrapper around `crypt(3)`

pyphash is a Python extension module that wraps the C library function
`crypt`, which performs passphrase hashing, in the simplest possible
fashion.  It exposes one function, named `crypt`, which works just
like the C `crypt` except that it is thread safe:


    >>> pyphash.crypt("swordfish", "$5e$z4x3Zlhs")
    '$5$z4x3Zlhs$g7JP4M7HZw5L25Xwklbd2nQ2rfjzVGFB1SJutFnmvK4'

You have to create settings strings yourself.

This module is not intended to be used by programs that actually need
to hash passphrases—if it were, it would at least also provide access
to `crypt_gensalt`.  Rather, its purpose is to be a test case for the
packaging toolchain for C extension modules.  Linux distributions are
changing how they provide the shared library that implements `crypt`,
and Python packaging must adapt.  See [manylinux bug
#305](https://github.com/pypa/manylinux/issues/305) for the gory details.

For thread safety, the module actually uses the reentrant variant of
`crypt` called `crypt_r`, and looks for it in `crypt.h` rather than
`unistd.h`.  It will fail to compile if this function or this header
is not available.
