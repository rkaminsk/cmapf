#ifndef CMAPF_H
#define CMAPF_H

//! Major version number.
#define CMAPF_VERSION_MAJOR 1
//! Minor version number.
#define CMAPF_VERSION_MINOR 0
//! Revision number.
#define CMAPF_VERSION_REVISION 0
//! String representation of version.
#define CMAPF_VERSION "1.0.0"

#ifdef __cplusplus
extern "C" {
#endif

#if defined _WIN32 || defined __CYGWIN__
#   define CMAPF_WIN
#endif
#ifdef CMAPF_NO_VISIBILITY
#   define CMAPF_VISIBILITY_DEFAULT
#   define CMAPF_VISIBILITY_PRIVATE
#else
#   ifdef CMAPF_WIN
#       ifdef CMAPF_BUILD_LIBRARY
#           define CMAPF_VISIBILITY_DEFAULT __declspec (dllexport)
#       else
#           define CMAPF_VISIBILITY_DEFAULT __declspec (dllimport)
#       endif
#       define CMAPF_VISIBILITY_PRIVATE
#   else
#       if __GNUC__ >= 4
#           define CMAPF_VISIBILITY_DEFAULT  __attribute__ ((visibility ("default")))
#           define CMAPF_VISIBILITY_PRIVATE __attribute__ ((visibility ("hidden")))
#       else
#           define CMAPF_VISIBILITY_DEFAULT
#           define CMAPF_VISIBILITY_PRIVATE
#       endif
#   endif
#endif

#include <clingo.h>

//! Obtain the version of the library.
CMAPF_VISIBILITY_DEFAULT void cmapf_version(int *major, int *minor, int *patch);

//! Compute an approximation of reachable nodes assuming limited moves of the
//! agents.
//!
//! An agent can only move for the first n time points, where n is the
//! length of its shortest path from start to goal plus the given delta.
//!
//! The function assumes that the control object already holds a MAPF problem
//! in standard form.
//!
//! Atoms over the predicates reach/3 and shortest_path/2 are added to the
//! control object. Atoms reach(A,U,T) indicate that an agent A can reach a
//! node U at time point T. Atom shortest_path(A,L) indicate that agent A can
//! reach its goal within L time steps from its start ignoring any collisions
//! with other agents.
CMAPF_VISIBILITY_DEFAULT bool cmapf_compute_reachable(clingo_control_t *c_ctl, int delta);

#ifdef __cplusplus
}
#endif

#endif
