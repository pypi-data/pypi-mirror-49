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

#include <boost/python.hpp>
#include <vector>
#include <iostream>
#include <fstream>

namespace bp = boost::python;

/*
 *-----------------
 * UserData struct.
 *-----------------
 */

struct UserData{

    void set_name(std::string text){
        name = text;
    }

    void set_kinetic_dimensions(int nkin, int nexc, int nreq){
        kinetic_dimensions[0] = nkin;
        kinetic_dimensions[1] = nexc;
        kinetic_dimensions[2] = nreq;
        initial_conditions = std::vector<double>(nkin+1);
        exchange_indices = std::vector<int>(nexc);
        required_indices = std::vector<int>(nreq);
    }

    void set_output_times(double tstop, double tout){
        output_times[0] = tstop;
        output_times[1] = tout;
    }

    void set_initial_conditions(bp::list init_cond){
        if(len(init_cond) != kinetic_dimensions[0]+1){
            std::cout << "Initial conditions of wrong length (" << len(init_cond) << " when expected " << kinetic_dimensions[0]+1 << ")!" << std::endl;
            return;
        }
        for(int i=0; i<(kinetic_dimensions[0]+1); i++){
            initial_conditions[i] = bp::extract<double>(init_cond[i]);
        }
    }

    void set_exchange_indices(bp::list exc_idx){
        if(len(exc_idx) != kinetic_dimensions[1]){
            std::cout << "Exchange indices of wrong length (" << len(exc_idx) << " when expected " << kinetic_dimensions[1] << ")!" << std::endl;
            return;
        }
        for(int i=0; i<kinetic_dimensions[1]; i++){
            exchange_indices[i] = bp::extract<int>(exc_idx[i]);
        }
    }

    void set_required_indices(bp::list req_idx){
        if(len(req_idx) != kinetic_dimensions[2]){
            std::cout << "Required indices of wrong length (" << len(req_idx) << " when expected " << kinetic_dimensions[2] << ")!" << std::endl;
            return;
        }
        for(int i=0; i<kinetic_dimensions[2]; i++){
            required_indices[i] = bp::extract<int>(req_idx[i]);
        }
    }

    void set_current_indices(bp::list cur_idx){
        for(int i=0; i<len(cur_idx); i++){
            current_indices.push_back(bp::extract<int>(cur_idx[i]));
        }
    }

    void add_objective(bp::list obj_inds, bp::list obj_coefs){
        int length = len(obj_inds);
        if(length != len(obj_coefs)){
            std::cout << "Lengths of objective indices and coefficients do not match! (" << length << " vs " << len(obj_coefs) <<  ", respectively)" << std::endl;
            return;
        }
        std::vector<int> indices(length);
        std::vector<double> coefficients(length);
        for(int i=0; i<length; i++){
            indices[i] = bp::extract<int>(obj_inds[i]) + 1;
            coefficients[i] = bp::extract<double>(obj_coefs[i]);
        }
        obj_indices.push_back(indices);
        obj_coefficients.push_back(coefficients);
    }

    void set_directions(bp::list directions){
        int nobj = obj_indices.size();
        if(len(directions) != nobj){
            std::cout << "Objective directions of wrong length (" << len(directions) << " when expected " << nobj << ")!" << std::endl;
            return;
        }
        for(int i=0; i<nobj; i++){
            std::string dir = bp::extract<std::string>(directions[i]);
            if(dir == "max"){
                obj_directions.push_back(2);
            }
            else if(dir == "min"){
                obj_directions.push_back(1);
            }
            else{
                std::cout << "Direction " << dir << " unexpected!" << std::endl;
                return;
            }
        }
    }

    void set_change_points(bp::list change_pnts){
        for(int i=0; i<len(change_pnts); i++){
            change_points.push_back(bp::extract<double>(change_pnts[i]));
        }
    }

    std::string name;
    std::vector<int> kinetic_dimensions = std::vector<int>(3,0);
    std::vector<double> output_times = std::vector<double>(2);
    std::vector<double> initial_conditions;
    std::vector<int> exchange_indices;
    std::vector<int> required_indices;
    std::vector<int> current_indices;
    std::vector< std::vector<int> > obj_indices;
    std::vector< std::vector<double> > obj_coefficients;
    std::vector<int> obj_directions;
    std::vector<double> change_points;
};
