#pragma once

typedef HANDLE(WINAPI *PROTO_FindFirstFileA)(
	__in LPCSTR lpFileName,
	__out LPWIN32_FIND_DATAA lpFindFileData
	);

typedef BOOL(WINAPI *PROTO_FindNextFileA)(
	__in HANDLE hFindFile,
	__out LPWIN32_FIND_DATAA lpFindFileData
	);

typedef BOOL(WINAPI *PROTO_FindClose)(
	_Inout_ HANDLE hFindFile
	);

typedef BOOL (WINAPI *PROTO_SetFileAttributesA)(
	LPCSTR lpFileName,
	DWORD  dwFileAttributes
	);

typedef BOOL(WINAPI *PROTO_CopyFileA)(
	LPCTSTR lpExistingFileName,
	LPCTSTR lpNewFileName,
	BOOL    bFailIfExists
	);

typedef BOOL(WINAPI *PROTO_GetFileAttributesA)(
	LPCSTR lpFileName
	);

typedef BOOL(WINAPI *PROTO_CreateDirectoryA)(
	LPCSTR lpPathName,
	LPSECURITY_ATTRIBUTES lpSecurityAttributes
	);

typedef BOOL(WINAPI *PROTO_DeleteFileA)(
	LPCSTR lpFileName
	);

typedef BOOL(WINAPI *PROTO_RemoveDirectoryA)(
	LPCSTR lpPathName
	);

typedef DWORD(WINAPI *PROTO_GetModuleFileNameA)(
	_In_opt_ HMODULE hModule,
	_Out_    LPTSTR  lpFilename,
	_In_     DWORD   nSize
	);

typedef DPAPI_IMP BOOL(WINAPI *PROTO_CryptUnprotectData)(
	DATA_BLOB                 *pDataIn,
	LPWSTR                    *ppszDataDescr,
	DATA_BLOB                 *pOptionalEntropy,
	PVOID                     pvReserved,
	CRYPTPROTECT_PROMPTSTRUCT *pPromptStruct,
	DWORD                     dwFlags,
	DATA_BLOB                 *pDataOut
	);

typedef LSTATUS(WINAPI *PROTO_RegQueryValueExA)(
	HKEY							  hKey,
	LPCSTR                            lpValueName,
	LPDWORD                           lpReserved,
	LPDWORD                           lpType,
	__out_data_source(REGISTRY)LPBYTE lpData,
	LPDWORD                           lpcbData
	);

typedef int(WINAPI *PROTO_GetObjectA)(
	HANDLE h,
	int    c,
	LPVOID pv
	);

typedef HLOCAL(WINAPI *PROTO_LocalAlloc)(
	UINT   uFlags,
	SIZE_T uBytes
	);

typedef HGLOBAL(WINAPI *PROTO_GlobalAlloc)(
	UINT   uFlags,
	SIZE_T dwBytes
	);

typedef int(WINAPI *PROTO_GetDIBits)(
	HDC          hdc,
	HBITMAP      hbm,
	UINT         start,
	UINT         cLines,
	LPVOID       lpvBits,
	LPBITMAPINFO lpbmi,
	UINT         usage
	);

typedef HANDLE (WINAPI *PROTO_CreateFileA)(
	LPCSTR                lpFileName,
	DWORD                 dwDesiredAccess,
	DWORD                 dwShareMode,
	LPSECURITY_ATTRIBUTES lpSecurityAttributes,
	DWORD                 dwCreationDisposition,
	DWORD                 dwFlagsAndAttributes,
	HANDLE                hTemplateFile
);

typedef BOOL(WINAPI *PROTO_WriteFile)(
	HANDLE       hFile,
	LPCVOID      lpBuffer,
	DWORD        nNumberOfBytesToWrite,
	LPDWORD      lpNumberOfBytesWritten,
	LPOVERLAPPED lpOverlapped
	);

typedef BOOL(WINAPI *PROTO_CloseHandle)(
	_In_ HANDLE hObject
	);

typedef HGLOBAL(WINAPI *PROTO_GlobalFree)(
	_Frees_ptr_opt_ HGLOBAL hMem
	);

typedef LSTATUS(WINAPI *PROTO_RegOpenKeyA)(
	HKEY   hKey,
	LPCSTR lpSubKey,
	PHKEY  phkResult
	);

typedef BOOL(WINAPI *PROTO_EnumDisplayDevicesA)(
	LPCSTR           lpDevice,
	DWORD            iDevNum,
	PDISPLAY_DEVICEA lpDisplayDevice,
	DWORD            dwFlags
	);

typedef int(WINAPI *PROTO_GetSystemMetrics)(
	_In_ int nIndex
	);

typedef HDC(WINAPI *PROTO_GetDC)(
	HWND hWnd
	);

typedef HWND(WINAPI *PROTO_GetDesktopWindow)(
	void
	);

typedef HDC(WINAPI *PROTO_CreateCompatibleDC)(
	HDC hdc
	);

typedef HBITMAP(WINAPI *PROTO_CreateCompatibleBitmap)(
	HDC hdc,
	int cx,
	int cy
);

typedef HGDIOBJ(WINAPI *PROTO_SelectObject)(
	HDC     hdc,
	HGDIOBJ h
	);

typedef HBRUSH(WINAPI *PROTO_CreateBrushIndirect)(
	CONST LOGBRUSH *plbrush
	);

typedef int(WINAPI *PROTO_FillRect)(
	HDC        hDC,
	CONST RECT *lprc,
	HBRUSH     hbr
	);

typedef BOOL(WINAPI *PROTO_BitBlt)(
	HDC   hdc,
	int   x,
	int   y,
	int   cx,
	int   cy,
	HDC   hdcSrc,
	int   x1,
	int   y1,
	DWORD rop
	);

typedef BOOL(WINAPI *PROTO_GetVolumeInformationA)(
	LPCSTR  lpRootPathName,
	LPSTR   lpVolumeNameBuffer,
	DWORD   nVolumeNameSize,
	LPDWORD lpVolumeSerialNumber,
	LPDWORD lpMaximumComponentLength,
	LPDWORD lpFileSystemFlags,
	LPSTR   lpFileSystemNameBuffer,
	DWORD   nFileSystemNameSize
	);

typedef DWORD(WINAPI *PROTO_GetTickCount)(
	void
	);

typedef HANDLE(WINAPI *PROTO_CreateFileMappingA)(
	HANDLE                hFile,
	LPSECURITY_ATTRIBUTES lpFileMappingAttributes,
	DWORD                 flProtect,
	DWORD                 dwMaximumSizeHigh,
	DWORD                 dwMaximumSizeLow,
	LPCSTR                lpName
	);

typedef LPVOID(WINAPI *PROTO_MapViewOfFile)(
	_In_ HANDLE hFileMappingObject,
	_In_ DWORD  dwDesiredAccess,
	_In_ DWORD  dwFileOffsetHigh,
	_In_ DWORD  dwFileOffsetLow,
	_In_ SIZE_T dwNumberOfBytesToMap
	);

typedef BOOL(WINAPI *PROTO_ReadFile)(
	HANDLE                        hFile,
	__out_data_source(FILE)LPVOID lpBuffer,
	DWORD                         nNumberOfBytesToRead,
	LPDWORD                       lpNumberOfBytesRead,
	LPOVERLAPPED                  lpOverlapped
	);

typedef DWORD(WINAPI *PROTO_SetFilePointer)(
	HANDLE hFile,
	LONG   lDistanceToMove,
	PLONG  lpDistanceToMoveHigh,
	DWORD  dwMoveMethod
	);

typedef BOOL(WINAPI *PROTO_GetFileInformationByHandle)(
	HANDLE					     hFile,
	LPBY_HANDLE_FILE_INFORMATION lpFileInformation
	);

typedef HANDLE(WINAPI *PROTO_GetCurrentProcess)(
	void
	);

typedef DWORD(WINAPI *PROTO_GetFileSize)(
	HANDLE  hFile,
	LPDWORD lpFileSizeHigh
	);