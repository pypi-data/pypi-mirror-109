/**********************************************************************************
 * Copyright (c) 2019 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 **********************************************************************************/

#pragma once

#define LIBALE_MAX_DIM 3
#define LIBALE_MAX_SET_DIM 1

#if (LIBALE_MAX_DIM < 1)
    #error LIBALE_MAX_DIM must be between 1 and 10
#endif
#if (LIBALE_MAX_SET_DIM < 1)
    #error LIBALE_MAX_SET_DIM must be between 1 and 10
#endif
