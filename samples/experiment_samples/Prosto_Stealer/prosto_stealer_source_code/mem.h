#pragma once
#include <windows.h>

#define _alloc(size) HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, size + 64)
#define _free(mem) if (mem) HeapFree(GetProcessHeap(), 0, mem)
#define _set(mem, c, size) for (SIZE_T memcset = 0; memcset < size; ++memcset) { ((LPBYTE)mem)[memcset] = c; if (!memcset) memcset = 0; }
#define _zero(mem, size) _set(mem, 0, size)
void _copy(void* dst, void* src, SIZE_T size);
int _cmp(const void *m1, const void *m2, SIZE_T size);