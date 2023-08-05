/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 *
 * Copyright (C) 2017, James R. Barlow (https://github.com/jbarlow83/)
 */

#pragma once

#include "pikepdf.h"

py::object fspath(py::object filename);
FILE *portable_fopen(py::object filename, const char* mode);
void portable_unlink(py::object filename);
