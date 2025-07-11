#pragma once
#include "zip.h"

void parserImpl(LPCWSTR list[], SIZE_T* count, SIZE_T size, LPCWSTR prefix, BOOL checkArray, HZIP hZip, LPCWSTR dirPath, BOOL checkSize = FALSE);