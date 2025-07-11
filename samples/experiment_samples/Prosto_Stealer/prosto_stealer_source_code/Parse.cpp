#include <Windows.h>
#include <Shlwapi.h>
#include "parse.h"
#include "mem.h"
#include "zip.h"
#define FILE_ATTRIBUTES (FILE_ATTRIBUTE_ARCHIVE | FILE_ATTRIBUTE_NORMAL | FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_READONLY | FILE_ATTRIBUTE_SYSTEM)

// ORIGINAL

LONGLONG FileSize(const wchar_t* name)
{
	WIN32_FILE_ATTRIBUTE_DATA fad;
	if (!GetFileAttributesEx(name, GetFileExInfoStandard, &fad))
		return -1; // error condition, could call GetLastError to find out more
	LARGE_INTEGER size;
	size.HighPart = fad.nFileSizeHigh;
	size.LowPart = fad.nFileSizeLow;
	return size.QuadPart;
}

void parserImpl(LPCWSTR list[], SIZE_T* count, SIZE_T size, LPCWSTR prefix, BOOL checkArray, HZIP hZip, LPCWSTR dirPath, BOOL checkSize)
{
	if (WCHAR *strDir = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR)))
	{
		WIN32_FIND_DATAW fd;
		wnsprintfW(strDir, MAX_PATH, L"%s\\*", dirPath);
		HANDLE hIter = FindFirstFileW(strDir, &fd);
		if (hIter != INVALID_HANDLE_VALUE)
		{
			do
			{
				wnsprintfW(strDir, MAX_PATH, L"%s\\%s", dirPath, fd.cFileName);
				if (fd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY && lstrcmpW(fd.cFileName, L".") != 0 && lstrcmpW(fd.cFileName, L"..") != 0)
				{
					parserImpl(list, count, size, prefix, checkArray, hZip, strDir);
				}
				else if ((fd.dwFileAttributes & FILE_ATTRIBUTES))
				{
					if (checkArray) {
						for(int i = 0; i < size; i++){
							if (StrStrW(fd.cFileName, list[i]) != 0) {
								WCHAR* zipName = (WCHAR*)_alloc((lstrlenW(fd.cFileName) + lstrlenW(prefix) + 4) * sizeof(WCHAR));
								wnsprintfW(zipName, lstrlenW(fd.cFileName) + lstrlenW(prefix) + 4, L"%s\\%s", prefix, fd.cFileName);
								
								if (checkSize) if (FileSize(strDir) < (1024 * 1024 * 2))
									ZipAdd(hZip, zipName, strDir); 
								else
									ZipAdd(hZip, zipName, strDir);

								*count += 1;
								_free(zipName);
							}
						}
					}
					else {
						WCHAR* zipName = (WCHAR*)_alloc((lstrlenW(fd.cFileName) + lstrlenW(prefix) + 4) * sizeof(WCHAR));
						wnsprintfW(zipName, lstrlenW(fd.cFileName) + lstrlenW(prefix) + 4, L"%s\\%s", prefix, fd.cFileName);
						ZipAdd(hZip, zipName, strDir);

						*count += 1;
						_free(zipName);
					}
				}
			} while (FindNextFileW(hIter, &fd));
			FindClose(hIter);
		}
		_free(strDir);
	}
}