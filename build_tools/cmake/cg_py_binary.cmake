# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Copied from https://github.com/google/iree/blob/main/build_tools/cmake/iree_cc_binary.cmake
# Copyright 2019 The IREE Authors
#
# Licensed under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

include(cg_py_library)

# cg_cc_binary()
#
# CMake function to imitate Bazel's py_binary rule.
#
# Parameters:
# NAME: name of target (see Note)
# SRCS: List of source files for the binary
# GENERATED_SRCS: List of source files for the binary that are generated by other targets
# DATA: List of other targets and files required for this binary
# DEPS: List of other libraries to be linked in to the binary targets
# TESTONLY: When added, this target will only be built if user passes -DCOMPILER_GYM_BUILD_TESTS=ON to CMake.
#
# Note:
# cg_py_binary will create a binary called ${PACKAGE_NAME}_${NAME}, e.g.
# cg_base_foo with two alias (readonly) targets, a qualified
# ${PACKAGE_NS}::${NAME} and an unqualified ${NAME}. Thus NAME must be globally
# unique in the project.
#
function(cg_py_binary)
  cmake_parse_arguments(
    _RULE
    "PUBLIC;TESTONLY"
    "NAME;SRCS;GENERATED_SRCS"
    "DATA;DEPS"
    ${ARGN}
  )

  # Currently the same as adding a library.
  # When install rules are added they will need to split.
  cg_py_library(${ARGV})
endfunction()
