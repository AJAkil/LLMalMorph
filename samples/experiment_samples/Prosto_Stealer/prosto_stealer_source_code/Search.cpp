#include <windows.h>
#include <shlwapi.h>
#include "search.h"
#include "vector.h"
#include "crypt.h"
#include "mem.h"

// ORIGINAL

#define FILE_ATTRIBUTES (FILE_ATTRIBUTE_ARCHIVE | FILE_ATTRIBUTE_NORMAL | FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_READONLY | FILE_ATTRIBUTE_SYSTEM)

void searchImpl(LPCWSTR dirPath, vector* v, uint32_t search_name)
{
	if (WCHAR *strDir = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR)))
	{
		WIN32_FIND_DATAW fd;
		wnsprintfW(strDir, MAX_PATH, L"%s\\*", dirPath);
		HANDLE hIter = FindFirstFileW(strDir, &fd);
		if (hIter != INVALID_HANDLE_VALUE)
		{
			SIZE_T pos = -1;
			do
			{
				wnsprintfW(strDir, MAX_PATH, L"%s\\%s", dirPath, fd.cFileName);
				if (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY && lstrcmpW(fd.cFileName, L".") != 0 && lstrcmpW(fd.cFileName, L"..") != 0)
				{
					searchImpl(strDir, v, search_name);
				}
				else if ((fd.dwFileAttributes & FILE_ATTRIBUTES))
				{
					WCHAR* fn = PathFindFileNameW(strDir);
					if (crc(fn, lstrlenW(fn)) == search_name) {
						WCHAR* mem = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));

						lstrcpyW(mem, strDir);
						vector_add(v, mem);
					}
				}
			} while (FindNextFileW(hIter, &fd));
			FindClose(hIter);
		}

		_free(strDir);
	}
}