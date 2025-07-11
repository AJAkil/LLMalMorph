#pragma once
#include <windows.h>
#include "vector.h"

void vec_get_str(vector v, CHAR** c, SIZE_T* s, SIZE_T prefix_len);
vector sqliteProcessFunction(LPCWSTR dbPath, SIZE_T* count_value, LPCSTR query, LPCSTR endstr, int addrn, int count, int encrypted_columns[], char* columns_prefix[], int encrypted_columns_count);