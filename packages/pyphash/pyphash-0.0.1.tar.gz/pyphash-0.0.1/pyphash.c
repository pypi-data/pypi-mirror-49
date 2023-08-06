/* pyphash - extremely simple wrapper around crypt(3).
   Copyright 2019 Zack Weinberg <zackw@panix.com>.
   Distributed under the terms of the Apache Software License, version 2.0;
   see the file LICENSE in the source distribution for details.  */

#define _GNU_SOURCE 1
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <crypt.h>
#include <errno.h>
#include <string.h>

static PyObject *
pyphash_crypt(PyObject *self, PyObject *args)
{
  const char *phrase;
  const char *setting;
  if (!PyArg_ParseTuple(args, "ss", &phrase, &setting))
    return 0;

  struct crypt_data data;
  memset(&data, 0, sizeof data);

  /* Some versions of crypt() don't set errno meaningfully on failure.  */
  int save_errno = errno;
  errno = 0;
  char *hash = crypt_r(phrase, setting, &data);
  if (!hash || hash[0] == '*') {
    if (!errno)
      errno = EINVAL;
    return PyErr_SetFromErrno(PyExc_OSError);
  }

  /* successful if we get here; restore errno */
  errno = save_errno;

  return Py_BuildValue("s", hash);
}

static PyMethodDef pyphash_methods[] = {
  { "crypt", pyphash_crypt, METH_VARARGS,
    "One-way hash a passphrase." },
  { 0, 0, 0, 0 }
};

static const char pyphash_doc[] =
  "Extremely simple wrapper around crypt(3).";

#if PY_VERSION_HEX >= 0x03000000

static struct PyModuleDef pyphash_module = {
  PyModuleDef_HEAD_INIT,
  "pyphash",
  pyphash_doc,
  0,
  pyphash_methods
};

PyMODINIT_FUNC
PyInit_pyphash(void)
{
  return PyModule_Create(&pyphash_module);
}

#else /* 2.x */

PyMODINIT_FUNC
initpyphash(void)
{
  Py_InitModule3("pyphash", pyphash_methods, pyphash_doc);
}

#endif
