#include <pybind11/pybind11.h>
#include <iostream>
#include "genstr.h"

namespace py = pybind11;

PYBIND11_MODULE(rapidrand, m) {
    m.doc() = R"pbdoc(
        A library for generate rand hex string faster
        -----------------------
    )pbdoc";


    m.def("genstr", [](int len) {
        return py::bytes(genstr_nonzero_impl(len));  // Return the data without transcoding
    }, R"pbdoc(arg0: target hex length in bytes
gen random hex str for specify length(ranging from 1 - 255)
        )pbdoc");

    m.def("entropy", [](int len) {

        return py::bytes(genstr_impl2(len));

    }, R"pbdoc(arg0: target hex length in bytes
gen random hex str for specify length(ranging from 0 - 255)
        )pbdoc");
#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}



