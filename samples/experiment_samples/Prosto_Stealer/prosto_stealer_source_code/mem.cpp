#include <windows.h>
#include "mem.h"

// ORIGINAL 

int _cmp(const void *m1, const void *m2, SIZE_T size)
{
	BYTE *BM1 = (BYTE*)m1;
	BYTE *BM2 = (BYTE*)m2;
	for (; size--; ++BM1, ++BM2) if (*BM1 != *BM2) return (*BM1 - *BM2);
	return NULL;
}

void _copy(void* dst, void* src, SIZE_T size) {
	for (SIZE_T memccpy = 0; memccpy < size; ++memccpy) ((LPBYTE)(dst))[memccpy] = ((LPBYTE)(src))[memccpy];
}