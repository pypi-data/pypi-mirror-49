// Copyright (C) 2018, 2019 Columbia University Irving Medical Center,
//     New York, USA

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

#include <time.h>
#include "methods/methods.h"

/*
 *----------------------------------------------
 * Functions for processing objects from Python.
 *----------------------------------------------
 */

/*
 * SWIGwrapper for glp_prob * (see https://wiki.python.org/moin/boost.python/HowTo#SWIG_exposed_C.2B-.2B-_object_from_Python ).
 */

struct PySwigprobObject{
    PyObject_HEAD
    glp_prob *ptr;
    const char *desc;
};

/*
 * LP problem extraction from SWIG glp_prob * wrapper.
 */

glp_prob* extract_swigprob(PyObject* model)
{
    char method[] = "lp_problem"; //name of lp_problem method
    if(!PyObject_HasAttrString(model,method)){ //if object does not have method
        return NULL; //return NULL
    }
    PyObject *swig_prob = PyObject_CallMethod(model,method,NULL); //get pointer to LP problem in Python
    if(swig_prob == NULL){ //if method returns NULL
        return NULL; //return NULL
    }
    glp_prob *lp = ((PySwigprobObject*)swig_prob)->ptr; //extract glp_prob * pointer
    Py_DECREF(swig_prob); //decrement reference
    return lp; //return glp_prob * pointer
}

/*
 *-----------------------------------
 * Functions to be exposed to Python.
 *-----------------------------------
 */

/*
 * Simulate individual dfba model.
 */

int simulate_dfba_model(PyObject *dfba_model)
{
    ///PYTHON INTERFACE TO GET MODEL
    ////////////////////////////////

    ///Here we get SWIGLPK wrapped glp_prob * using Python/C API
    glp_prob *lp = extract_swigprob(dfba_model); //assign new pointer to LP problem in Python
    glp_smcp parm; //TODO: obtain copy of LP configuration from Python

    ///Here we convert remainer to bp::object and extract copy of wrapped UserData attribute
    bp::handle<> handle(dfba_model); //create handle to PyObject *
    bp::object bp_dfba_model = bp::object(handle); //create bp object from PyObject *
    UserData user_data = bp::extract<UserData>(bp_dfba_model.attr("user_data")); //extract UserData attribute
    SolverData solver_data = bp::extract<SolverData>(bp_dfba_model.attr("solver_data")); //extract SolverData attribute

    ///Here we confim sunmatrix and sunlinearsolve combination supported
    if(solver_data.sunlinsolver != "dense"){
        std::cout << "SUNMatrix and SUNLinearSolver combination not supported! See SUNDIALS documentation for details." << std::endl;
        return 0;
    }

    ///Here hide glpk display if requested
    glp_init_smcp(&parm);
    if(!(solver_data.display == "full" || solver_data.display == "glpk_only")){
        parm.msg_lev = GLP_MSG_OFF;
    }

    ///CREATE MODEL AND RUN SIMULATION
    //////////////////////////////////
    std::ofstream outputfile; //create output file
    outputfile.open("results.txt"); //open output file
    clock_t t1, t2; //time tracking
    t1 = clock(); //set start time
    if(solver_data.algorithm == "Harwood"){
        EMBLP_HARWOOD model(lp,parm,user_data); //init emblp Harwood model from pointer to LP problem in Python and user data
        PrintOutput(model,outputfile); //store initial conditions to file
        integrateHarwood(model,outputfile,solver_data); //run simulation on model
        model.clear(); //clear model memory
    }
    else if(solver_data.algorithm == "direct"){
        EMBLP_DIRECT model(lp,parm,user_data); //init emblp direct model from pointer to LP problem in Python and user data
        PrintOutput(model,outputfile); //store initial conditions to file
        integrateDirect(model,outputfile,solver_data); //run simulation on model
        model.clear(); //clear model memory
    }
    else{
        std::cout << "Algorithm currently not supported!" << std::endl;
        return 0;
    }
    t2 = clock(); //set end time
    std::cout << std::endl << "Total simulation time was " << ((float)t2-(float)t1)/CLOCKS_PER_SEC << " seconds" << std::endl << std::endl;
    outputfile.close(); //close output file
    return 0;
}

/*
 *----------------
 * Python wrapper.
 *----------------
 */

BOOST_PYTHON_MODULE(dfba_utils)
{
    ///Here we expose simulate dfba model method
    bp::def("simulate_dfba_model", simulate_dfba_model);

    ///Here we expose UserData
    bp::class_<UserData>("UserData")
    .def("set_name", &UserData::set_name)
    .def("set_kinetic_dimensions", &UserData::set_kinetic_dimensions)
    .def("set_output_times", &UserData::set_output_times)
    .def("set_initial_conditions", &UserData::set_initial_conditions)
    .def("set_exchange_indices", &UserData::set_exchange_indices)
    .def("set_required_indices", &UserData::set_required_indices)
    .def("set_current_indices", &UserData::set_current_indices)
    .def("add_objective", &UserData::add_objective)
    .def("set_directions", &UserData::set_directions)
    .def("set_change_points", &UserData::set_change_points)
    ;

    ///Here we expose SolverData
    bp::class_<SolverData>("SolverData")
    .def("set_rel_tolerance", &SolverData::set_rel_tolerance)
    .def("set_abs_tolerance", &SolverData::set_abs_tolerance)
    .def("set_sunmatrix", &SolverData::set_sunmatrix)
    .def("set_sunlinsolver", &SolverData::set_sunlinsolver)
    .def("set_ode_method", &SolverData::set_ode_method)
    .def("set_algorithm", &SolverData::set_algorithm)
    .def("set_display", &SolverData::set_display)
    ;
}

