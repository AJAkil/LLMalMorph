#pragma once
#include "prototypes.h"

ULONG_PTR dyn_call(char* dll, const char* func);

#define MAKESTR(x) # x
#define FNC(func, lib) ((PROTO_##func) dyn_call(lib, MAKESTR(func)))