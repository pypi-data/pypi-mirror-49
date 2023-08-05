#include <Python.h>
#include <alloca.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include "LDPC.h"
#include <string>
#include <iostream>
#include "Def_List.h"
// #include "targetver.h"

#include <stdio.h>
// #include "stdafx.h"

#if PY_MAJOR_VERSION >= 3
#define PY_STRING_FORMAT "y#"
#define PY_CONST_STRING_FORMAT "y"
#else
#define PY_STRING_FORMAT "s#"
#define PY_CONST_STRING_FORMAT "s"
#endif

#define MIX_WORDS (ecceth_MIX_BYTES/4)

static PyObject *
eth_ecc(PyObject *self, PyObject *args){

  char *current_header;
  char *previous_header;
  unsigned long block_number;
  unsigned long nonce;
  int previous_header_size, current_header_size, wc, wr, difficulty_level;

  if (!PyArg_ParseTuple(args, PY_STRING_FORMAT PY_STRING_FORMAT "i" "i" "i" , &previous_header, &previous_header_size, &current_header, &current_header_size, &difficulty_level, &wc, &wr))
      return 0;


//   if (current_header_size != 32) {
//         char error_message[1024];
//         sprintf(error_message, "Seed must be 32 bytes long (was %i)", current_header_size);
//         PyErr_SetString(PyExc_ValueError, error_message);
//         return 0;
//   }

    LDPC *ptr = new LDPC;

	ptr->set_difficulty(24, wc, wr); //2 => n = 64, wc = 3, wr = 6,
	if (!ptr->initialization())
	{
		printf("error for calling the initialization function");
		return 0;
	}

	ptr->generate_seed(previous_header);
	ptr->generate_H();
	ptr->generate_Q();

    ptr->print_H("H2.txt");
	ptr->print_Q(NULL, 1);
	ptr->print_Q(NULL, 2);

  std::string current_block_header = current_header;

  while(1)
  {
    std::string current_block_header_with_nonce;
		current_block_header_with_nonce.assign(current_block_header);
		current_block_header_with_nonce += std::to_string(nonce);

		ptr->generate_hv((unsigned char*)current_block_header_with_nonce.c_str());
		bool flag = ptr->decision();
		if (!flag) // If a hash vector is a codeword itself, we dont need to run the decoding function.
		{
			ptr->decoding();
			flag = ptr->decision();
		}
		if (flag)
		{
			printf("codeword is founded with nonce = %lu\n", nonce);
			break;
		}
		nonce++;
  }
    ptr->print_word(NULL, 1);
	ptr->print_word(NULL, 2);
	delete ptr;

	return Py_BuildValue("{" PY_CONST_STRING_FORMAT ":" PY_STRING_FORMAT "}",
                         "result", nonce, 8);
}


static PyMethodDef PyeccethMethods[] =
    {
        {"eth_ecc", eth_ecc, METH_VARARGS,
            "eth_ecc(previous_header, current_header, difficulty_level, wc, wr)\n\n"
                "Runs the eccpow function using LDPC.  By using byte array(previous_header), make the parity check matrix. After that, using byte array (current_header) and int (nonce) make input vector to decode parity check matrix. Returns an object containing hash result."},
        {NULL, NULL, 0, NULL}
    };

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef PyeccethModule = {
    PyModuleDef_HEAD_INIT,
    "pyecceth",
    "...",
    -1,
    PyeccethMethods
};

PyMODINIT_FUNC PyInit_pyecceth(void) {
    PyObject *module =  PyModule_Create(&PyeccethModule);
//    PyModule_AddIntConstant(module, "ROW_SWAP", (long) ROW_SWAP);
//    PyModule_AddIntConstant(module, "COLUMN_SWAP", (long) COLUMN_SWAP);
//    PyModule_AddIntConstant(module, "BLOCK_LENGTH", (long) BLOCK_LENGTH);
//    PyModule_AddIntConstant(module, "MESSAGE_LENGTH", (long) MESSAGE_LENGTH);
//    PyModule_AddIntConstant(module, "REDUNDANCY_LENGTH", (long) REDUNDANCY_LENGTH);
//    PyModule_AddIntConstant(module, "CODE_RATE", (long) CODE_RATE);
//    PyModule_AddIntConstant(module, "COLUMN_DEGREE", (long) COLUMN_DEGREE);
//    PyModule_AddIntConstant(module, "ROW_DEGREE", (long) ROW_DEGREE);
//    PyModule_AddIntConstant(module, "FIELD_SIZE", (long) FIELD_SIZE);
//    PyModule_AddIntConstant(module, "SEED", (long) SEED);
//    PyModule_AddIntConstant(module, "CROSS_OVER_PROB", (long) CROSS_OVER_PROB);
//    PyModule_AddIntConstant(module, "INPUT_WORD", (long) INPUT_WORD);
//    PyModule_AddIntConstant(module, "OUTPUT_WORD", (long) OUTPUT_WORD);
//    PyModule_AddIntConstant(module, "COLUMN_IN_ROW", (long) COLUMN_IN_ROW);
//    PyModule_AddIntConstant(module, "ROW_IN_COLUMN", (long) ROW_IN_COLUMN);
//    PyModule_AddIntConstant(module, "BIG_INFINITY", (long) BIG_INFINITY);
//    PyModule_AddIntConstant(module, "ITERATIONS", (long) ITERATIONS);
//    PyModule_AddIntConstant(module, "Inf", (long) Inf);
//    PyModule_AddIntConstant(module, "MAX_BUFF_SIZE", (long) MAX_BUFF_SIZE);

    return module;
}
#else
PyMODINIT_FUNC
initpyecceth(void) {
    PyObject *module = Py_InitModule("pyecceth", PyeccethMethods);
}
#endif



